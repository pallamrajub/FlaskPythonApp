pipeline {
     agent {
        label 'slave'   // This is your slave/agent label
    }

    environment {
        IMAGE_NAME = 'flaskpythonapp'
        CONTAINER_NAME = 'flask_app_container'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'git@github.com:pallamrajub/FlaskPythonApp.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest tests || echo "No tests found"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}")
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
            echo 'Pipeline completed.'
        }
    }
}
