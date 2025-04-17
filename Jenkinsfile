pipeline {
    agent any

    environment {
        IMAGE_NAME = "house-price-predictor"
        APP_URL = "http://localhost:10000"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Dheerajkurupati/InsuranceDevops.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Run Docker Container') {
            steps {
                bat "docker-compose up -d"
            }
        }

        stage('Wait for App to Start') {
            steps {
                bat '''
                    echo Waiting for app to be ready...
                    timeout /T 15 /NOBREAK
                '''
            }
        }

        stage('Test App') {
            steps {
                bat "curl %APP_URL%"
            }
        }
    }

    post {
        always {
            echo 'Cleaning up containers...'
            bat "docker-compose down"
        }
    }
}
