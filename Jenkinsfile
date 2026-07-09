pipeline {
    agent any

    stages {
        stage("run frontend") {
            steps {
                echo "Executing yarn"
                nodejs("26.5."){
                    sh 'yarn install'
                }
            }
        }

        stage("run backend") {
            steps {
                echo "executing gradle"
                withGradle{
                    sh './gradlew -v'
                }
            }
        }

        stage("deployment") {
            steps {
                echo "We are deploying"
            }
        }
    }
}
