
pipeline {
    agent any

    options {
        timestamps()
    }

    stages {

        stage('Verify Environment') {
            steps {
                echo 'Checking Jenkins build environment...'

                sh '''
                    python3 --version
                    git --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'

                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install --upgrade pip
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running application unit tests...'

                sh '''
                    .venv/bin/python -m pytest -v
                '''
            }
        }


        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'

                sh '''
                    docker build \
                      -t prithvimistral/jenkins-kubernetes-cicd:${BUILD_NUMBER} \
                      -t prithvimistral/jenkins-kubernetes-cicd:latest .
                '''
            }
        }



        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                credentialsId: 'dockerhub-credentials',
                usernameVariable: 'DOCKERHUB_USERNAME',
                passwordVariable: 'DOCKERHUB_TOKEN'
            )]) {
                    echo 'Pushing Docker image to Docker Hub...'    
            sh '''
                set +x
                export DOCKER_CONFIG=$(mktemp -d)
                trap 'docker logout >/dev/null 2>&1 || true; rm -rf "$DOCKER_CONFIG"' EXIT

                printf '%s' "$DOCKERHUB_TOKEN" | docker login \
                    -u "$DOCKERHUB_USERNAME" \
                    --password-stdin

                docker push prithvimistral/jenkins-kubernetes-cicd:${BUILD_NUMBER}
                docker push prithvimistral/jenkins-kubernetes-cicd:latest
            '''
                }
            }
        }


    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }

        failure {
            echo 'CI Pipeline failed. Check the console output.'
        }
    }
}

o
