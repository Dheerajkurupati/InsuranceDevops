pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Dheerajkurupati/InsuranceDevops.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t house-price-predictor .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker-compose down || exit 0' // Stop any running container first
                bat 'docker-compose up -d'
            }
        }

        stage('Wait for App to Start') {
            steps {
                bat '''
                    echo Waiting for app to be ready...
                    ping 127.0.0.1 -n 20 > nul
                '''
            }
        }

        stage('Test App') {
            steps {
                bat 'curl --retry 5 --retry-delay 10 http://localhost:10000 || exit /b 1'
            }
        }
    }
}
