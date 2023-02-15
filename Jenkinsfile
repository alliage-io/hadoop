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
                git branch: 'branch-3.1.1-TDP-alliage', url: 'https://github.com/Yanis77240/hadoop'
                sh '''
                ls
                '''
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
        stage("Publish to Nexus Repository Manager") {
            steps {
                echo "Publishing..."
                withCredentials([usernamePassword(credentialsId: 'jenkins-user', passwordVariable: 'pass', usernameVariable: 'user')]) {
                    sh 'echo $user'
                    sh 'echo $pass'
                    sh 'cat settings.xml'
                    sh 'mvn clean deploy -e -X -DskipTests -s settings.xml'
                }
            }        
        }
    }
}