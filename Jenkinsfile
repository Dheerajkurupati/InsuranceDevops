pipeline {
    agent any

    environment {
        IMAGE_NAME = 'insurance-application'
        IMAGE_TAG = 'latest'
        DOCKER_HUB_REPO = 'dheerajk04/insurance-application'
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Cloning the repository...'
                // Jenkins will clone the repo automatically if it's from Git
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Lint Code') {
            steps {
                echo 'Linting the Python code...'
                bat 'pip install flake8 && flake8 app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Run Docker Container (Optional)') {
            steps {
                echo 'Running Docker container locally (optional)...'
                bat "docker run -d -p 10000:10000 ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Push to Docker Hub (Optional)') {
            when {
                expression { return env.DOCKER_HUB_REPO != null }
            }
            steps {
                echo "Pushing to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    bat 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
                    bat "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                    bat "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            bat 'docker container prune -f || true'
            bat 'docker image prune -f || true'
        }
        success {
            echo 'Deployment pipeline executed successfully!'
        }
        failure {
            echo 'Something went wrong. Please check the logs.'
        }
    }
}
