pipeline {
    agent {
        label 'slave'   // This is your slave/agent label
    }

    environment {
        VENV_DIR = 'venv'
        IMAGE_NAME = 'flaskpythonapp'
        CONTAINER_NAME = 'flask_app_container'
    }

    stages {
        stage('Clone') {
            steps {
                git 'https://your.git.repo/url.git'
            }
        }

        stage('Set Up Python Env') {
            steps {
                sh '''
                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . ${VENV_DIR}/bin/activate
                pytest tests/
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("my_python_app:latest")
                }
            }
        }

        stage('Deploy (Docker Run)') {
            steps {
                sh '''
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
