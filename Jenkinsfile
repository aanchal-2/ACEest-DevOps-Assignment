
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Lint') {
            steps {
                sh '''
                    python3 -m venv .jenkins-venv

                    .jenkins-venv/bin/python -m pip install -r requirements.txt

                    .jenkins-venv/bin/python -m compileall -q app.py storage.py tests

                    .jenkins-venv/bin/python -m ruff check app.py storage.py tests
                '''
            }
        }

        stage('Test Coverage') {
            steps {
                sh '''
                    .jenkins-venv/bin/python -m pytest \
                        --cov=app \
                        --cov=storage \
                        --cov-report=xml:coverage.xml \
                        --cov-report=term-missing \
                        tests/
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Docker Image Assembly') {
            steps {
                sh 'docker build -t aceest-fitness:jenkins .'
            }
        }

        stage('Containerized Tests') {
            steps {
                sh 'docker run --rm aceest-fitness:jenkins python -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'ACEest BUILD, SonarQube analysis and tests completed successfully.'
        }

        failure {
            echo 'ACEest BUILD failed. Review the stage logs.'
        }

        always {
            echo 'ACEest Fitness Gym CI/CD Pipeline execution completed.'
        }
    }
}
