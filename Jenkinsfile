pipeline {
 agent any
 stages {
 stage('Checkout') {
 steps { checkout scm }
 }
 stage('Build and Lint') {
 steps {
 sh 'python3 -m compileall -q app.py storage.py tests'
 sh 'python3 -m pip install -r requirements.txt'
 sh 'python3 -m ruff check app.py storage.py tests'
 }
 }
 stage('Docker Image Assembly') {
 steps { sh 'docker build -t aceest-fitness:jenkins .' }
 }
 stage('Containerized Tests') {
 steps {
 sh 'docker run --rm aceest-fitness:jenkins python -m pytest -v'
 }
 }
 }
 post {
 success { echo 'ACEest BUILD and tests completed successfully.' }
 failure { echo 'ACEest BUILD failed. Review the stage logs.' }
 }
}
