# SSDD Assignment 5 Web Application

This repository hosts a simple Flask-powered note board that stores entries in SQLite. It is designed to fulfil the CI/CD workflow requirements for the assignment: lint, build, unit test, containerize, deploy, and exercise Selenium smoke tests inside Docker.

## Features
- Flask application with SQLite persistence and easy form-based input
- Bootstrap-powered UI plus Flash notifications to surface form feedback
- `pytest` unit tests that verify the main page and form behavior
- Selenium scripts that cover navigation and form submission
- Dockerized application and Selenium test runner
- Jenkins pipeline (`Jenkinsfile`) implementing lint → build → unit test → containerized deployment → Selenium testing

## Getting Started
1. Create and activate a Python venv: `python -m venv .venv; .\.venv\Scripts\Activate.ps1` (PowerShell) or `source .venv/bin/activate` (bash).
2. Install dependencies: `pip install -r requirements.txt`.
3. Start the app: `python run.py` (defaults to `http://localhost:5000`).
4. Visit the page and add a note.

## Testing
- **Unit tests:** `pytest tests`
- **Selenium tests:**
  1. Ensure the Flask app is running (`python run.py`).
  2. Execute `cd selenium && python run_selenium_tests.py`.
  3. Set `APP_URL` if the app runs on a different host/port.

## Docker
- **App container:** `docker build -t ssdd-app . && docker run -p 5000:5000 ssdd-app`
- **Selenium runner:** `docker build -t ssdd-selenium -f Dockerfile.selenium . && docker run --rm --network host -e APP_URL=http://localhost:5000 ssdd-selenium`

## Jenkins Pipeline
The provided `Jenkinsfile` assumes a Linux/Jenkins host with Docker access. Key stages:
1. **Code Linting** – installs requirements and runs `flake8 app tests`
2. **Code Build** – compiles the Flask package using `python -m compileall`
3. **Unit Testing** – runs `pytest tests`
4. **Containerized Deployment** – builds the app image and runs it on port 5000
5. **Selenium Testing** – builds `Dockerfile.selenium` and runs the tests with `APP_URL=http://localhost:5000`

Make sure GitHub Webhooks target Jenkins and that Jenkins has the Git, Pipeline, Docker Pipeline (and Docker) plugins enabled. Use a post-build cleanup step (already in the `post { always { ... } }` block) to stop the app container.
