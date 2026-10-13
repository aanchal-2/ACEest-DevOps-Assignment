# ACEest Fitness & Gym — DevOps Assignment 1
 
A fitness management web application developed using Flask and Python as part of the Introduction to DevOps assignment at BITS Pilani.
 
The project demonstrates the application development and DevOps lifecycle, including version control with Git and GitHub, automated testing with Pytest, containerization with Docker, and Continuous Integration (CI) using Jenkins and GitHub Actions.
 
---
 
## Table of Contents
 
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing and Code Quality](#testing-and-code-quality)
- [Docker Setup](#docker-setup)
- [Jenkins Pipeline](#jenkins-pipeline)
- [GitHub Actions](#github-actions)
- [Version Control Workflow](#version-control-workflow)
- [Limitations and Scope](#limitations-and-scope)
- [Author](#author)
 
---
 
## Project Overview
 
ACEest Fitness & Gym is a web-based fitness management application with a black-and-gold dashboard.
 
It allows users to view fitness programs, register clients, manage membership status through the API, and record workout sessions.
 
The project uses a modular Flask backend and an SQLite database. It also demonstrates how an application can be tested, packaged into a Docker image, and validated through automated CI pipelines.
 
## Features
 
### Fitness Programs
- View available fitness programs:
  - Fat Loss
  - Muscle Gain
  - Beginner
- Display sample workout schedules and nutrition recommendations.
 
### Client Management
- Register new clients.
- View registered clients.
- Prevent duplicate client names, ignoring case.
- Track membership status as Active or Inactive through the API.
 
### Workout Management
- Record workouts for registered clients.
- Store workout type and duration.
- Validate workout information.
- Retrieve saved workout records.
 
### DevOps and Automation
- Git-based version control and GitHub repository hosting.
- Automated application tests using Pytest.
- Python syntax validation and linting using Ruff.
- Docker image creation and containerized testing.
- Jenkins pipeline for build and test automation.
- GitHub Actions workflow for push and pull-request validation.
 
---
 
## Technology Stack
 
| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web framework and REST API |
| SQLite | Persistent relational database |
| HTML, CSS, JavaScript | Web interface |
| Pytest | Automated testing |
| Ruff | Python linting |
| Git and GitHub | Version control and source-code hosting |
| Docker | Application containerization |
| Jenkins | CI pipeline automation |
| GitHub Actions | Cloud-based CI automation |
| Rocky Linux | Development environment |
 
---
 
## Project Structure
 
```text
ACEest-DevOps-Assignment/
├── app.py
├── storage.py
├── requirements.txt
├── README.md
├── .gitignore
├── Dockerfile
├── .dockerignore
├── Jenkinsfile
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
└── .github/
    └── workflows/
        └── main.yml
```
 
### Important Files
 
- `app.py` — Flask application, routes, fitness program data, and request validation.
- `storage.py` — SQLite database initialization and database operations.
- `templates/index.html` — Dashboard interface and JavaScript API interactions.
- `tests/test_app.py` — Automated tests for application routes and validation.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — Instructions for building the application image.
- `Jenkinsfile` — Jenkins pipeline definition.
- `.github/workflows/main.yml` — GitHub Actions CI workflow.
- `.gitignore` — Files and directories excluded from Git.
- `.dockerignore` — Files excluded from the Docker build context.
 
---
 
## Prerequisites
 
Ensure the following tools are available on your Rocky Linux system:
 
- Python 3
- pip
- Git
- Docker, for containerization
- Jenkins, for Jenkins-based CI
- A GitHub account, for repository hosting and GitHub Actions
 
Python dependencies are installed through `requirements.txt`.
 
---
 
## Installation and Setup
 
### 1. Clone the repository
 
Replace the URL below with your repository URL if necessary.
 
```bash
git clone https://github.com/aanchal-2/ACEest-DevOps-Assignment.git
cd ACEest-DevOps-Assignment
```
 
### 2. Create a virtual environment
 
```bash
python3 -m venv .venv
source .venv/bin/activate
```
 
### 3. Install dependencies
 
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
 
---
 
## Running the Application
 
Start the Flask application:
 
```bash
python app.py
```
 
Open the following address in your browser:
 
http://127.0.0.1:5000
 
The application listens on port `5000`.
 
To check the application health, visit:
 
http://127.0.0.1:5000/health
 
A successful health check returns a JSON response indicating that the application is running.
 
Press `Ctrl+C` in the terminal to stop the local server.
 
---
 
## API Endpoints
 
The application exposes the following HTTP endpoints.
 
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Displays the fitness dashboard |
| GET | `/health` | Returns application health information |
| GET | `/program/<program_name>` | Retrieves a fitness program |
| GET | `/clients` | Lists registered clients |
| POST | `/clients` | Registers a new client |
| PATCH | `/clients/<client_id>/membership` | Updates membership status |
| GET | `/workouts` | Lists recorded workouts |
| POST | `/workouts` | Records a workout |
 
### Example: Register a Client
 
Send a POST request to `/clients` with a JSON body:
 
```json
{
  "name": "Alex"
}
```
 
Example using curl:
 
```bash
curl -X POST http://127.0.0.1:5000/clients \
  -H "Content-Type: application/json" \
  -d '{"name":"Alex"}'
```
 
### Example: Record a Workout
 
Send a POST request to `/workouts`:
 
```json
{
  "client_id": 1,
  "workout_type": "Cardio",
  "duration_min": 30
}
```
 
Example using curl:
 
```bash
curl -X POST http://127.0.0.1:5000/workouts \
  -H "Content-Type: application/json" \
  -d '{"client_id":1,"workout_type":"Cardio","duration_min":30}'
```
 
The client must already exist before a workout can be recorded.
 
---
 
## Testing and Code Quality
 
### Run automated tests
 
```bash
python -m pytest -v
```
 
The tests cover the dashboard, health endpoint, fitness programs, client registration, duplicate clients, membership updates, workout recording, and input validation.
 
### Check Python syntax
 
```bash
python -m compileall -q app.py storage.py tests
```
 
### Run Ruff
 
```bash
python -m ruff check app.py storage.py tests
```
 
Run these checks before committing changes or pushing them to GitHub.
 
---
 
## Docker Setup
 
Build the Docker image from the project root:
 
```bash
docker build -t aceest-fitness:1.0 .
```
 
Run the application with persistent SQLite storage:
 
```bash
docker run --rm -p 5000:5000 \
  -v aceest-data:/app/instance \
  aceest-fitness:1.0
```
 
Open http://127.0.0.1:5000 in your browser.
 
The named Docker volume `aceest-data` preserves the SQLite database between container runs.
 
### Run tests inside Docker
 
```bash
docker run --rm aceest-fitness:1.0 python -m pytest -v
```
 
On Rocky Linux, use `sudo` for Docker commands if your account has not been configured for Docker access.
 
---
 
## Jenkins Pipeline
 
The `Jenkinsfile` defines a pipeline with the following stages:
 
1. **Checkout** — Retrieves the source code from the configured Git repository.
2. **Build and Lint** — Checks Python syntax, installs dependencies, and runs Ruff.
3. **Docker Image Assembly** — Builds the application Docker image.
4. **Containerized Tests** — Executes Pytest inside the built image.
 
### Jenkins configuration
 
- Create a Jenkins Pipeline job.
- Configure the GitHub repository as the source.
- Select `Pipeline script from SCM`.
- Set the branch to `*/main`.
- Set the script path to `Jenkinsfile`.
- Ensure the Jenkins agent has the required Python and Docker tools and appropriate Docker permissions.
 
A successful pipeline should complete all stages without errors.
 
---
 
## GitHub Actions
 
The workflow file is located at:
 
`.github/workflows/main.yml`
 
The workflow is configured to run on pushes and pull requests.
 
Its steps include:
 
1. Checking out the repository.
2. Setting up Python.
3. Installing project dependencies.
4. Checking syntax and running Ruff.
5. Building the Docker image.
6. Running Pytest inside the Docker image.
 
Workflow results can be reviewed in the **Actions** tab of the GitHub repository.
 
---
 
## Version Control Workflow
 
The project uses Git for source-code management and GitHub for repository hosting.
 
Typical commands:
 
```bash
git status
git add .
git commit -m "Describe your changes"
git push origin main
```
 
A development branch can be created with:
 
```bash
git switch -c develop
```
 
After testing and reviewing changes, merge the development branch into `main` and push the updated branch.
 
Do not commit virtual environments, database files, credentials, access tokens, or other sensitive information.
 
---
 
## Limitations and Scope
 
This project is a new Flask implementation inspired by selected features of the supplied ACEest fitness application.
 
- Fitness schedules and nutrition recommendations are sample data.
- The SQLite database stores client and workout information locally.
- The dashboard displays sample gym metrics.
- Authentication, role-based access control, and production deployment hardening are not implemented in this version.
- The project does not claim to reproduce every feature of the original application.
 
Before production deployment, configure a strong secret key, implement appropriate authentication and authorization, and review security and operational requirements.
 
---
 
## Author
 
**Student:** Aanchal  
**Institution:** BITS Pilani  
**Assignment:** Introduction to DevOps — Assignment 1  
**Project:** ACEest Fitness & Gym
 
---
 
## Project Status
 
This repository is intended for academic demonstration of application development and DevOps practices.
 
Record test results, Docker validation, Jenkins build results, and GitHub Actions status based on actual executions in your environment.
