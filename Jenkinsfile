
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






        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying application to Kubernetes...'

                sh '''
                    set -e

                    IMAGE="prithvimistral/jenkins-kubernetes-cicd:${BUILD_NUMBER}"

                    echo "Deploying image: ${IMAGE}"

                    kubectl apply -f k8s/namespace.yaml

                    TEMP_MANIFEST=$(mktemp)
                    trap 'rm -f "${TEMP_MANIFEST}"' EXIT

                    sed "s|image: prithvimistral/jenkins-kubernetes-cicd:latest|image: ${IMAGE}|" \
                        k8s/deployment.yaml > "${TEMP_MANIFEST}"

                    kubectl apply -n cicd-demo -f "${TEMP_MANIFEST}"
                    kubectl apply -n cicd-demo -f k8s/service.yaml

                    kubectl rollout status deployment/fastapi-app \
                        -n cicd-demo --timeout=180s

                    kubectl get deployment fastapi-app -n cicd-demo -o wide
                    kubectl get pods -n cicd-demo
                    kubectl get service -n cicd-demo

                    echo "Testing application health..."
                    for i in $(seq 1 10); do
                        if curl --fail --silent --show-error \
                            http://192.168.49.2:30080/health; then
                            echo
                            echo "Kubernetes health check passed!"
                            exit 0
                        fi
                        echo "Waiting for application..."
                        sleep 5
                    done

                    echo "Kubernetes health check failed!"
                    exit 1
                '''
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

