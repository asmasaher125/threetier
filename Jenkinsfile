pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Test') {
            steps {
                sh '''
                docker run --rm -v $PWD/backend:/app -w /app python:3.11-slim \
                  sh -c "pip install -q flask pymongo && python -m unittest test_app.py"
                '''
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                docker build -t backend-img:${BUILD_NUMBER} -t backend-img:latest ./backend
                docker build -t frontend-img:${BUILD_NUMBER} -t frontend-img:latest ./frontend
                '''
            }
        }

        stage('Remove Old Containers') {
            steps {
                sh 'docker rm -f frontend_c backend_c db_c || true'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker network inspect app-net >/dev/null 2>&1 || docker network create app-net
                docker run -d --name db_c --network app-net -v mongo-data:/data/db mongo:6.0
                sleep 10
                docker run -d --name backend_c --network app-net -e MONGO_HOST=db_c -e APP_VERSION=build-${BUILD_NUMBER} backend-img:latest
                sleep 5
                docker run -d --name frontend_c --network app-net -p 80:80 frontend-img:latest
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                sleep 5
                docker ps
                curl -f http://localhost/api/health
                curl -f http://localhost/api/visit
                '''
            }
        }
    }

    post {
        success { echo 'Deployed successfully' }
        failure { echo 'Pipeline failed - check the stage logs' }
    }
}
