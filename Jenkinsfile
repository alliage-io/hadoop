pipeline {
    agent { 
        node {
            label 'tdp-builder'
        }
    }
    triggers {
        pollSCM '0 1 * * *'
    }
    stages {
        stage('Git Clone') {
            steps {
                echo "Cloning.."
                git branch: 'branch-3.1.1-TDP', url: 'https://github.com/TOSIT-IO/hadoop'
                sh '''
                ls
                '''
            }
        }
        stage ('Build') {
            steps {
                echo "Cloning.."
                sh '''
                mvn clean install -Pdist -Dtar -Pnative -DskipTests -Dmaven.javadoc.skip=true
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                echo "doing testing stuff.."
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                echo "doing delivery stuff.."
                '''
            }
        }
    }
}
