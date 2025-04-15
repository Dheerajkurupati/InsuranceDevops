pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Dheerajkurupati/InsuranceDevops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t house-price-predictor .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker-compose up -d'
            }
        }

        stage('Test App') {
            steps {
                bat 'curl http://localhost:10000'
            }
        }
    }
}
