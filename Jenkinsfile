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
            stage('Git Clone') {
                echo "Cloning.."
                git branch: 'branch-3.1.1-TDP-alliage-k8s', url: 'https://github.com/Yanis77240/hadoop'
            }
            stage('Chose comparison') {
                withEnv(["file=${input message: 'Select file in http://10.10.10.11:30000/repository/java-test-reports/', parameters: [string('number of results file')]}"]) {
                    withEnv(["number=${currentBuild.number}"]) {
                        sh '''
                        cd test_comparison
                        curl -v http://10.10.10.11:30000/repository/java-test-reports/hadoop/${file} > ${file}
                        python3 comparison-file-check.py ${file}
                        echo "python3 main.py ${number} ${file}" > transformation.sh
                        chmod 777 transformation.sh
                        '''
                    }
                }
            }
            stage ('Build') {
                echo "Building.."
                sh '''
                mvn clean install -Pdist -Dtar -Pnative -DskipTests -Dmaven.javadoc.skip=true
                '''
            }
            stage('Test') {
                echo "Testing..."
                withCredentials([usernamePassword(credentialsId: '4b87bd68-ad4c-11ed-afa1-0242ac120002', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    withEnv(["number=${currentBuild.number}"]) {
                        /* Perform the tests and the surefire reporting*/
                        sh '''
                        mvn -Ptest-patch -Pparallel-tests -Pshelltest -Pnative -Drequire.fuse -Drequire.openssl -Drequire.snappy -Drequire.valgrind -Drequire.zstd -Drequire.test.libhadoop -Dstyle.color=never --fail-never clean test | tee output.txt
                        '''
                        sh 'mvn surefire-report:report-only  -Daggregate=true'
                        sh 'curl -v -u $user:$pass --upload-file target/site/surefire-report.html http://10.110.4.212:8081/repository/test-reports/hadoop-3.1.1/surefire-report-${number}.html'
                        /* extract the scalatest-plugin data and java-test data output and remove all color signs */
                        sh script: $/
                        # Create CVS file with following titles as header
                        echo "Tests_run, Failures, Errors, Skipped, Test_group" > test_comparison/output-tests.csv
                        # Grep all Java test staistics in CSV file
                        grep -E --color=never 'Failures:| Errors:| Skipped:' output.txt | awk '/Failures:/ && /Errors:/ && /Skipped:/' >> test_comparison/output-tests.csv
                        # Generate text file with all failed Java tests without any colors
                        grep -E --color=never '[Error].*org.*<<< ERROR!|[Error].*org.*<<< FAILURE!' output.txt | sed -r "s|\x1B\[[0-9;]*[mK]||g" > test_comparison/java-test-failures.txt
                        /$
                        /* Perform the data transformation and the comparison*/
                        sh '''
                        cd test_comparison
                        ./transformation.sh
                        ./decision.sh ${number}
                        curl -v -u $user:$pass --upload-file results-${number}.json http://10.110.4.212:8081/repository/java-test-reports/hadoop/results-${number}.json
                        '''
                    }
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