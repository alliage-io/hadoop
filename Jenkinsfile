pipeline {
    agent { 
        node {
            label 'docker-tdp-builder'
            }
      }
    environment {
        number="${currentBuild.number}"
      }
    triggers {
        pollSCM '0 1 * * *'
      }
    stages {
        stage('clone') {
            steps {
                echo "Cloning..."
                git branch: 'branch-3.1.1-TDP-alliage', url: 'https://github.com/Yanis77240/hadoop'
            }
        }
        stage('Build') {
            steps {
                echo "Building..."
                sh '''
                mvn clean install -Pdist -Dtar -Pnative -DskipTests -Dmaven.javadoc.skip=true
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing..."
                sh '''
                mvn test -Pnative -DskipTests -Dmaven.javadoc.skip=true --fail-never
                '''
            }
        }
        stage("Publish to Nexus Repository Manager") {
            steps {
                echo "Deploy..."
                withCredentials([usernamePassword(credentialsId: '4b87bd68-ad4c-11ed-afa1-0242ac120002', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh 'mvn clean deploy -DskipTests -s settings.xml'
                }
            }        
        }
        stage("Publish tar.gz to Nexus") {
            steps {
                echo "Deploy..."
                withCredentials([usernamePassword(credentialsId: '4b87bd68-ad4c-11ed-afa1-0242ac120002', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh 'curl -v -u $user:$pass --upload-file hadoop-dist/target/hadoop-3.1.1-TDP-0.1.0-SNAPSHOT.tar.gz http://172.19.0.2:8081/repository/maven-tar-files/hadoop/hadoop-3.1.1-TDP-0.1.0-SNAPSHOT-${number}.tar.gz'
                }
            }        
        }
    }
}