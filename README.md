# ACEest Fitness & Gym — DevOps Assignments 1 & 2

A Flask and Python fitness management application developed for the **Introduction to DevOps** course at **BITS Pilani**. Assignment 1 established the application, automated tests, Git workflow, Docker containerization, Jenkins CI and GitHub Actions. Assignment 2 extends the same codebase with SonarQube quality checks, versioned Docker Hub images, Kubernetes on Minikube, and five deployment strategies with rollback demonstrations.

> **Academic demonstration:** This project is designed for a Rocky Linux development environment and local Minikube cluster. It is not a production-hardened deployment. The two published image tags (`v1` and `v2`) were used to demonstrate deployment mechanics; they have the same application behavior, so image tags and Kubernetes state, rather than HTTP response bodies, identify the deployed version.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation and Local Run](#installation-and-local-run)
- [API Endpoints](#api-endpoints)
- [Testing and Code Quality](#testing-and-code-quality)
- [Docker Images](#docker-images)
- [Jenkins CI/CD and SonarQube](#jenkins-cicd-and-sonarqube)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Deployment Strategies](#deployment-strategies)
- [Deployment Verification](#deployment-verification)
- [Version Control](#version-control)
- [Evidence and Submission](#evidence-and-submission)
- [Limitations](#limitations)
- [Author](#author)

## Project Overview

ACEest Fitness & Gym is a web-based fitness management application with a black-and-gold dashboard. The Flask backend uses SQLite for local persistence. The project demonstrates development, testing, packaging, CI/CD and progressive deployment of a containerized application.

## Features

- View sample fitness programs: Fat Loss, Muscle Gain and Beginner.
- View sample workout schedules and nutrition recommendations.
- Register and list clients; reject duplicate names ignoring case.
- Update client membership status through the API.
- Record, validate and retrieve workout sessions.
- Expose a `/health` endpoint for application and deployment checks.
- Run automated tests, linting, container builds and CI checks.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python, Flask | Application and REST API |
| SQLite | Local application database |
| HTML, CSS, JavaScript | Web dashboard |
| Pytest | Automated application tests |
| Ruff | Python linting |
| Git and GitHub | Source control and collaboration |
| Jenkins | CI/CD pipeline and GitHub-triggered builds |
| GitHub Actions | Additional CI workflow |
| SonarQube | Static analysis and quality gate |
| Docker, Docker Hub | Containerization and image registry |
| Minikube, Kubernetes | Local container orchestration |
| Nginx | Shadow traffic mirroring and A/B routing |
| Rocky Linux | Development and demonstration environment |

## Repository Structure

```text
ACEest-DevOps-Assignment/
├── app.py
├── storage.py
├── requirements.txt
├── README.md
├── Dockerfile
├── .dockerignore
├── .gitignore
├── Jenkinsfile
├── sonar-project.properties
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── .github/
│   └── workflows/
│       └── main.yml
└── kubernetes/
    ├── deployment.yaml
    ├── service.yaml
    ├── blue-green/
    │   ├── blue-deployment.yaml
    │   ├── green-deployment.yaml
    │   └── blue-green-service.yaml
    ├── canary/
    │   ├── stable-deployment.yaml
    │   ├── canary-deployment.yaml
    │   └── canary-service.yaml
    ├── shadow/
    │   ├── shadow-deployment.yaml
    │   ├── shadow-service.yaml
    │   ├── nginx.conf
    │   ├── nginx-proxy-deployment.yaml
    │   └── nginx-proxy-service.yaml
    └── ab-deployment/
        ├── variant-a-deployment.yaml
        ├── variant-a-service.yaml
        ├── variant-b-deployment.yaml
        ├── variant-b-service.yaml
        ├── nginx.conf
        ├── nginx-proxy-deployment.yaml
        └── nginx-proxy-service.yaml
```

> Some Nginx configuration is loaded through Kubernetes ConfigMaps created from `nginx.conf`. Recreate the ConfigMap when setting up a new cluster; the proxy Deployment YAML alone does not create it.

## Prerequisites

- Python 3, `pip`, Git and a Rocky Linux terminal.
- Docker Engine and access to Docker Hub.
- Jenkins with appropriate plugins and build-agent permissions.
- SonarQube and SonarScanner for the quality analysis stage.
- Minikube with a functioning Kubernetes cluster (`minikube kubectl -- ...` works without a separately installed `kubectl`).

## Installation and Local Run

Clone the repository and select the Assignment 2 branch:

```bash
git clone https://github.com/aanchal-2/ACEest-DevOps-Assignment.git
cd ACEest-DevOps-Assignment
git switch assignment-2-cicd
```

Set up Python dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the Flask application:

```bash
python app.py
```

Open `http://127.0.0.1:5000` for the dashboard or `http://127.0.0.1:5000/health` for the health endpoint. Stop the local server with `Ctrl+C`.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Fitness dashboard |
| GET | `/health` | Application health |
| GET | `/program/<program_name>` | Fitness program details |
| GET | `/clients` | Registered clients |
| POST | `/clients` | Register client |
| PATCH | `/clients/<client_id>/membership` | Update membership |
| GET | `/workouts` | List workouts |
| POST | `/workouts` | Record workout |

Register a client:

```bash
curl -X POST http://127.0.0.1:5000/clients \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alex"}'
```

Record a workout after creating a client:

```bash
curl -X POST http://127.0.0.1:5000/workouts \
  -H 'Content-Type: application/json' \
  -d '{"client_id":1,"workout_type":"Cardio","duration_min":30}'
```

## Testing and Code Quality

Run the application tests and development checks:

```bash
python -m pytest -v
python -m compileall -q app.py storage.py tests
python -m ruff check app.py storage.py tests
```

**Recorded demonstration:** 21 automated Pytest tests passed. A SonarQube Quality Gate PASS was also captured. Screenshots of the successful results are retained as assignment evidence; these results describe the demonstrated run, not a guarantee that all future runs will pass.

## Docker Images

Build and test a local image:

```bash
docker build -t aceest-fitness:1.0 .
docker run --rm aceest-fitness:1.0 python -m pytest -v
```

Run the application with persistent SQLite storage:

```bash
docker run --rm -p 5000:5000 \
  -v aceest-data:/app/instance \
  aceest-fitness:1.0
```

Docker Hub repository: **`aanchal22/aceest-fitness`**.

Published image tags used in Assignment 2:

```text
aanchal22/aceest-fitness:v1
aanchal22/aceest-fitness:v2
```

Pull an image:

```bash
docker pull aanchal22/aceest-fitness:v1
docker pull aanchal22/aceest-fitness:v2
```

Both tags were used in Kubernetes strategy demonstrations. They do not have distinct HTTP response content; check the image field to verify which version is deployed.

## Jenkins CI/CD and SonarQube

The pipeline is defined in the root-level `Jenkinsfile`. Jenkins job: **`ACEest-Fitness-CICD`**.

- **Source repository:** `https://github.com/aanchal-2/ACEest-DevOps-Assignment.git`
- **Branch specifier:** `*/assignment-2-cicd`
- **Pipeline script path:** `Jenkinsfile`
- **Trigger:** GitHub webhook on source changes (demonstrated with an automatically triggered successful build).
- **Validation:** Source checkout, build/lint, SonarQube analysis/quality checks, Docker image assembly and containerized Pytest, as configured in the pipeline.

Jenkins requires configured tools and a reachable SonarQube server. The SonarQube server name used by the pipeline must match the name configured under **Manage Jenkins → System → SonarQube installations**. Configure SonarScanner under Jenkins tools as required by the `Jenkinsfile`. Store authentication tokens in Jenkins credentials; **do not commit secrets or webhook tokens**.

**Recorded evidence:** successful Jenkins pipeline build, SonarQube Quality Gate PASS and 21 passing Pytest tests. A subsequent local attempt encountered a SonarQube connectivity/configuration issue, so use the recorded successful execution as evidence rather than claiming every later rerun succeeded.

The GitHub Actions workflow is defined in `.github/workflows/main.yml` and supports source checks on configured push/pull-request events.

## Kubernetes Deployment

Start and inspect Minikube:

```bash
minikube start
minikube status
minikube kubectl -- get nodes
```

Deploy the baseline application:

```bash
minikube kubectl -- apply -f kubernetes/deployment.yaml
minikube kubectl -- apply -f kubernetes/service.yaml
minikube kubectl -- rollout status deployment/aceest-fitness
minikube kubectl -- get deployments
minikube kubectl -- get services
```

Baseline service: `aceest-fitness-service`, NodePort **31925** (as configured in this demonstration). Check the running application:

```bash
curl -i "http://$(minikube ip):31925/health"
```

The expected successful result is `HTTP/1.1 200 OK` with a JSON body indicating the application is running. Minikube IPs and NodePorts are local environment details; a private `192.168.x.x` address is **not** a publicly reachable submission endpoint.

## Deployment Strategies

### 1. Rolling Update and Rollback

The baseline Deployment `aceest-fitness` was upgraded from Docker image `v1` to `v2`, verified, then rolled back to `v1`.

```bash
minikube kubectl -- set image deployment/aceest-fitness \
  aceest-fitness=aanchal22/aceest-fitness:v2
minikube kubectl -- rollout status deployment/aceest-fitness
minikube kubectl -- get deployment aceest-fitness \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
```

Rollback:

```bash
minikube kubectl -- rollout undo deployment/aceest-fitness
minikube kubectl -- rollout status deployment/aceest-fitness
minikube kubectl -- get deployment aceest-fitness \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'
curl -i "http://$(minikube ip):31925/health"
```

**Observed result:** successful rollout to `v2`, rollback to `v1`, pod Ready/Running and health endpoint HTTP 200. Preserve screenshots showing both image tags and rollout output.

### 2. Blue-Green Deployment

Manifests: `kubernetes/blue-green/`.

- **Blue:** stable `v1` deployment.
- **Green:** candidate `v2` deployment.
- **Service:** switches its selector between the blue and green deployments, enabling a traffic cutover without rebuilding the app.

```bash
minikube kubectl -- apply -f kubernetes/blue-green/blue-deployment.yaml
minikube kubectl -- apply -f kubernetes/blue-green/green-deployment.yaml
minikube kubectl -- apply -f kubernetes/blue-green/blue-green-service.yaml
```

Switch the Service to green, then back to blue for rollback:

```bash
minikube kubectl -- patch service aceest-blue-green-service \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"green"}}}'

minikube kubectl -- patch service aceest-blue-green-service \
  -p '{"spec":{"selector":{"app":"aceest-fitness","version":"blue"}}}'
```

> Check the exact Service name and selectors in the YAML before running the example patch commands. The blue and green Deployments were subsequently removed from the demonstration cluster to free resources; reapply their manifests to repeat this test.

### 3. Canary Release and Rollback

Manifests: `kubernetes/canary/`.

- Stable: **4 replicas** running `v1`.
- Canary: **1 replica** running `v2`.
- Both versions are selected by the canary Service, giving an approximate **80% stable / 20% canary pod mix**. Actual request distribution is not guaranteed to match this percentage exactly.

```bash
minikube kubectl -- apply -f kubernetes/canary/stable-deployment.yaml
minikube kubectl -- apply -f kubernetes/canary/canary-deployment.yaml
minikube kubectl -- apply -f kubernetes/canary/canary-service.yaml
minikube kubectl -- get deployments
```

Rollback by removing the candidate from service:

```bash
minikube kubectl -- scale deployment aceest-canary --replicas=0
minikube kubectl -- get deployments
```

**Observed result:** stable replicas remained available after the canary was scaled down. The demonstration canary service used NodePort **31927**.

### 4. Shadow Deployment

Manifests and Nginx config: `kubernetes/shadow/`.

- Stable traffic is handled by the stable application service.
- Nginx mirrors selected **GET `/health`** requests to a separate `v2` shadow application.
- The client receives the stable response; shadow responses are not returned to the client.
- Mirroring is limited to safe health-check requests in this demonstration, not user-modifying API operations.

The shadow Nginx configuration is stored in `kubernetes/shadow/nginx.conf`. Create its ConfigMap before deploying the proxy:

```bash
minikube kubectl -- create configmap aceest-shadow-nginx-config \
  --from-file=nginx.conf=kubernetes/shadow/nginx.conf \
  --dry-run=client -o yaml | minikube kubectl -- apply -f -
```

Apply the shadow application and proxy manifests:

```bash
minikube kubectl -- apply -f kubernetes/shadow/shadow-deployment.yaml
minikube kubectl -- apply -f kubernetes/shadow/shadow-service.yaml
minikube kubectl -- apply -f kubernetes/shadow/nginx-proxy-deployment.yaml
minikube kubectl -- apply -f kubernetes/shadow/nginx-proxy-service.yaml
```

Verify proxy responses and compare application logs to demonstrate mirrored requests. Note that readiness probes can independently generate `/health` logs, so correlate test requests with their timestamps rather than treating any single log line as proof of mirroring.

**Observed result:** screenshots of shadow deployment and mirrored-request evidence were captured during the demonstration.

### 5. A/B Testing with Nginx Routing

Manifests and Nginx config: `kubernetes/ab-deployment/`.

- Variant A and Variant B are deployed separately.
- Nginx selects the backend using request-routing rules.
- Requests with the matching A/B header are routed to their intended variant; application access logs confirm the selected backend.

Create the Nginx ConfigMap (check the proxy Deployment's referenced ConfigMap name in its YAML) and apply the manifests in `kubernetes/ab-deployment/`.

**Recorded test:** Nginx proxy NodePort **31931**. A request with `X-AB-Variant: A` and query marker `ab_test=variant_a_123` returned HTTP 200 and appeared in Variant A's logs, not Variant B's logs. An analogous request for Variant B appeared in Variant B's logs, not Variant A's logs.

Example request:

```bash
curl -i \
  -H 'X-AB-Variant: A' \
  "http://$(minikube ip):31931/health?ab_test=variant_a_123"
```

Verify routing using application logs:

```bash
minikube kubectl -- logs deployment/aceest-variant-a --tail=50 | grep 'variant_a_123'
minikube kubectl -- logs deployment/aceest-variant-b --tail=50 | grep 'variant_a_123'
```

## Deployment Verification

The following services returned HTTP 200 during the recorded demonstration:

| Service | NodePort | Purpose |
|---|---:|---|
| `aceest-fitness-service` | 31925 | Baseline / rolling update |
| `aceest-variant-a-service` | 31929 | Variant A |
| `aceest-variant-b-service` | 31930 | Variant B |
| `aceest-ab-proxy-service` | 31931 | Nginx A/B router |

Verify current resources:

```bash
minikube kubectl -- get deployments
minikube kubectl -- get pods
minikube kubectl -- get services
```

Verify the documented HTTP endpoints:

```bash
for port in 31925 31929 31930 31931; do
  echo "Testing NodePort $port"
  curl -s -o /dev/null -w 'HTTP %{http_code}\n' \
    "http://$(minikube ip):$port/health"
done
```

These checks reflect the **demonstrated** cluster configuration. A new cluster may require reapplying manifests, ConfigMaps and image-pull settings before the endpoints work.

## Version Control

Repository: [ACEest-DevOps-Assignment](https://github.com/aanchal-2/ACEest-DevOps-Assignment)

Assignment 2 branch: **`assignment-2-cicd`**.

```bash
git status
git log -5 --oneline
git add README.md
git commit -m "Document Assignment 2 CI/CD and Kubernetes strategies"
git push origin assignment-2-cicd
```

Do not commit `.venv`, database files, credentials, tokens, downloaded Minikube binaries, or screenshots containing secrets. The demonstration includes a structured Git history and a commit covering the A/B deployment manifests.

## Evidence and Submission

The following screenshots were captured during the assignment work:

| Evidence | Recorded status |
|---|---|
| Successful Jenkins CI/CD pipeline | Available |
| SonarQube Quality Gate PASS | Available |
| Pytest (21 passing tests) | Available |
| Docker Hub image tags `v1` and `v2` | Available |
| Rolling update `v1 → v2` and rollback `v2 → v1` | Available after re-running and capturing evidence |
| Blue-Green switching | Available |
| Canary rollout and rollback | Available |
| Shadow mirroring | Available |
| A/B routing with Nginx | Available |
| Kubernetes resources and HTTP 200 health checks | Available |

**Assignment 2 submission requirements:** include the application source, `Jenkinsfile`, `Dockerfile`, Kubernetes YAMLs, Pytest tests, SonarQube evidence, GitHub repository link, and a separate **2–3 page report** summarizing CI/CD architecture, challenges/mitigations, and automation outcomes. Also provide Docker Hub image information and a reachable cluster endpoint if required by the submission portal.

> **Endpoint note:** `http://$(minikube ip):31925/health` is a command to resolve a local Minikube endpoint, not a public URL. If the evaluator needs remote access, arrange an approved reachable endpoint; do not submit a private Minikube IP as though it were public.

## Limitations

- This is an academic demonstration, not a production-ready deployment.
- Fitness schedules and nutrition recommendations are sample data.
- SQLite stores client and workout information locally; Kubernetes persistence and multi-replica database coordination require additional design.
- Authentication, role-based access control and production security hardening are not implemented.
- The `v1` and `v2` images have equivalent application behavior; deployment version evidence relies on image tags and Kubernetes state.
- Blue-Green, Canary, Shadow and A/B were demonstrated at different stages; all strategy deployments need not remain running simultaneously.
- Successful past Jenkins and SonarQube screenshots do not establish that those services are currently reachable.
- Production deployment would require secure secrets management, TLS, access controls, monitoring, resilient persistence and an externally reachable service.

## Author

**Student:** Aanchal  
**Institution:** BITS Pilani  
**Course:** Introduction to DevOps  
**Assignments:** 1 and 2  
**Project:** ACEest Fitness & Gym

---

**Project status:** Application, testing, containerization, CI/CD, and Kubernetes deployment-strategy demonstrations completed; final submission should include the separate report and supporting screenshots.
