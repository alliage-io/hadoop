podTemplate(containers: [
    containerTemplate(
        name: 'tdp-builder', 
        image: 'stbaum/jenkins-mysql:latest',
        resourceLimitCpu: "3000m",
        resourceLimitMemory: "9000Mi", 
        command: 'sleep', 
        args: '30d'
        )
  ]) {

    node(POD_LABEL) {
        container('tdp-builder') {
            environment {
                number="${currentBuild.number}"
            }
            stage('Git Clone') {
                echo "Cloning.."
                git branch: 'branch-3.1.1-TDP-alliage-k8s', url: 'https://github.com/Yanis77240/hadoop'
            }   
            stage ('Build') {
                echo "Building.."
                sh '''
                mvn clean install -Pdist -Dtar -Pnative -DskipTests -Dmaven.javadoc.skip=true
                '''
            }
            stage('Test') {
                echo "Testing.."
                sh '''
                mvn -Ptest-patch -Pparallel-tests -Pshelltest -Pnative -Drequire.fuse -Drequire.openssl -Drequire.snappy -Drequire.valgrind -Drequire.zstd -Drequire.test.libhadoop -Dsurefire.rerunFailingTestsCount=3 --fail-never clean test | grep -E '(Errors:|Failures:|Skipped:)' > tee output-tests.csv
                '''
            }
            stage('Send CSV to Database') {
                echo "send tests to database"
                withEnv(["number=${currentBuild.number}"]) {
                    sh'''
                    mysql -h 10.100.99.143 -u root -padmin tests -e "CREATE TABLE hadoop_${number} (Runs VARCHAR(255), Failures VARCHAR(255), Errors VARCHAR(255), Skipped VARCHAR(255), Test_Name VARCHAR(255));"
                    mysql -h 10.100.99.143 -u root -padmin tests -e "LOAD DATA LOCAL INFILE 'output-tests.csv' INTO TABLE hadoop_${number} FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' (Runs, Failures, Errors, Skipped, @var_Test_name) SET Test_name = IFNULL(NULLIF(@var_Test_name, ''), 'not_precised');"
                    '''
                }
            }
            stage('Deliver') {
                echo "Deploy..."
                withCredentials([usernamePassword(credentialsId: '4b87bd68-ad4c-11ed-afa1-0242ac120002', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh 'mvn clean deploy -Pnative -Pdist -Dtar -Dmaven.javadoc.skip=true -DskipTests -s settings.xml'
                }
            }
            stage("Publish tar.gz to Nexus") {
                echo "Publish tar.gz..."
                withEnv(["number=${currentBuild.number}"]) {
                    withCredentials([usernamePassword(credentialsId: '4b87bd68-ad4c-11ed-afa1-0242ac120002', passwordVariable: 'pass', usernameVariable: 'user')]) {
                        sh '''
                        curl -v -u $user:$pass --upload-file hadoop-dist/target/hadoop-3.1.1-TDP-0.1.0-SNAPSHOT.tar.gz http://10.110.4.212:8081/repository/maven-tar-files/hadoop/hadoop-3.1.1-TDP-0.1.0-SNAPSHOT-${number}.tar.gz
                        '''
                    }
                }
            }       
        }
    }
}