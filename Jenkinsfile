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
                // Jenkins auto-clones from Git
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

        stage('Run Docker Container') {
            steps {
                echo 'Running Docker container...'
                bat "docker run -d -p 10000:10000 --name insurance_app_container ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Test Application') {
            steps {
                echo 'Testing if app is up using curl...'
                bat '''
                echo Waiting for the app to be ready...
                set RETRIES=5
                set WAIT=5
                for /L %%i in (1,1,%RETRIES%) do (
                    echo Attempt %%i: curl http://localhost:10000/health
                    curl http://localhost:10000/health && exit /b 0
                    echo App not ready, waiting %WAIT% seconds...
                    timeout /t %WAIT% >nul
                )
                echo App failed to respond after %RETRIES% attempts.
                exit /b 1
                '''
            }
        }

        stage('Push to Docker Hub (Optional)') {
            when {
                expression { return env.DOCKER_HUB_REPO != null }
            }
            steps {
                echo "Pushing to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    bat 'echo %DOCKERHUB_PASS% | docker login -u %DOCKERHUB_USER% --password-stdin'
                    bat "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                    bat "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            bat 'docker stop insurance_app_container || exit 0'
            bat 'docker rm insurance_app_container || exit 0'
            bat 'docker container prune -f || exit 0'
            bat 'docker image prune -f || exit 0'
        }
        success {
            echo 'Deployment pipeline executed successfully!'
        }
        failure {
            echo 'Something went wrong. Please check the logs.'
        }
    }
}
