pipeline {
    agent {
        label 'slave'   // replace with your actual slave/agent label in Jenkins
    }

    environment {
        IMAGE_NAME = 'flaskpythonapp'
        CONTAINER_NAME = 'flask_app_container'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'cicd-jenkins',
                    credentialsId: 'gitlogin',
                    url: 'git@github.com:pallamrajub/FlaskPythonApp.git'
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
                pytest --junitxml=reports/pytest.xml || echo "No tests found"
                '''
                junit 'reports/pytest.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def commit = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.IMAGE_TAG = "${IMAGE_NAME}:${BUILD_NUMBER}-${commit}"
                    docker.build(env.IMAGE_TAG)
                }
            }
        }

        stage('Deploy (Docker Run)') {
            steps {
                sh '''
                docker stop ${CONTAINER_NAME} || true
                docker rm ${CONTAINER_NAME} || true
                docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_TAG}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                echo "Waiting for Flask app to start..."
                sleep 5
                curl -f http://localhost:5000/ || (echo "App not responding!" && exit 1)
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
            cleanWs()   // cleanup workspace after build
        }
    }
}
