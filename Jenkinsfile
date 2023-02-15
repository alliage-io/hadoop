pipeline {
    agent { 
        node {
            label 'docker-tdp-builder'
            }
      }
    triggers {
        pollSCM '0 1 * * *'
      }
    stages {
        stage('clone') {
            steps {
                echo "Cloning..."
                git branch: 'branch-3.1.1-TDP', url: 'https://github.com/TOSIT-IO/hadoop'
                sh '''
                ls
                '''
            }
        }
        stage('Build') {
            steps {
                echo "Building..."
                sh '''
                cd hadoop-build-tools
                mvn clean install -DskipTests
                '''
            }
        }
        stage("Publish to Nexus Repository Manager") {
            steps {
                echo "Publishing..."
                withCredentials([usernamePassword(credentialsId: 'jenkins-user', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh 'echo $user'
                    sh 'echo $pass'
                    sh 'mvn clean deploy -e -X -DskipTests -s hadoop/settings.xml'
                }
            }        
        }
    }
}