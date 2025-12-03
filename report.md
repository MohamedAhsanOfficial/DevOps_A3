# Assignment Report

## Application Summary
The solution is a lightweight Flask Notes Board that persists user notes in a SQLite database (`data/app.db`). The UI relies on Bootstrap for quick layout and includes flash notifications to confirm form submissions. The backend exposes a single route (`/`) that handles both rendering and form submissions, keeping in line with the assignment's "any web app" requirement.

## Environment & Tools
- **Language & runtime:** Python 3.11 (Flask + Flask-SQLAlchemy)
- **Database:** SQLite (bundled file under `data/app.db`)
- **Testing:** `pytest` for unit tests, `selenium` + `webdriver-manager` for UI tests
- **Containers:** Docker for both the web app (`Dockerfile`) and Selenium runner (`Dockerfile.selenium`)
- **CI/CD:** Jenkins pipeline (`Jenkinsfile`) orchestrating lint/build/test/deploy/selenium stages

## Micro-Steps Followed
1. Scaffolded the Flask project structure (`app` package, `templates`, `static`, `data` directory) and added the `Note` model with SQLAlchemy.
2. Implemented `routes.py` to handle GET/POST requests, validation, flash messages, and note listing, then wired everything through `create_app()` in `app/__init__.py`.
3. Built simple Bootstrap layouts (`base.html`, `index.html`) plus a lightweight stylesheet for list grouping.
4. Added `tests/test_app.py` with fixtures for an in-memory SQLite DB covering the landing page and note submission flows.
5. Crafted Selenium smoke tests (`selenium/run_selenium_tests.py`) to ensure the UI loads and the form repeats the submitted note, parameterized via `APP_URL`.
6. Created Docker artifacts: `Dockerfile` (app) and `Dockerfile.selenium` (tests) so Jenkins can spin up containers during its pipeline.
7. Authored the `Jenkinsfile` with the required five stages plus cleanup to demonstrate lint → build → unit test → containerized deployment → Selenium testing.
8. Documented usage steps in `README.md` and captured the workflow, tooling, and placeholders for screenshots in this report.

## Jenkins & AWS Notes
1. Provision an AWS EC2 instance (Linux) with Docker installed, and install Jenkins along with Git, Pipeline, and Docker Pipeline plugins.
2. Point Jenkins to the GitHub repository and create a multibranch pipeline using the provided `Jenkinsfile`.
3. Configure a GitHub Webhook (push or PR event) so Jenkins pulls updates automatically.
4. Ensure the EC2 security group exposes ports `8080` for Jenkins and `5000` if you need to inspect the running app during manual tests.
5. The pipeline's `Containerized Deployment` stage builds the app image and runs it on port `5000`, while `Selenium Testing` uses `Dockerfile.selenium` to run smoke tests against `http://localhost:5000`.

## Selenium Tests Delivered
- `test_homepage`: verifies the landing page title and copy render correctly.
- `test_note_submission`: posts a unique note and confirms the success toast plus note text on the page.

## Docker Artifacts Delivered
- `Dockerfile`: builds the Flask application image and exposes port 5000 via Gunicorn.
- `Dockerfile.selenium`: installs Chromium, ChromeDriver, and Python dependencies to execute Selenium scripts headlessly.

## Jenkins Pipeline Script
Delivered at `Jenkinsfile` with stages:
1. **Code Linting:** ensures `flake8` passes across `app` and `tests`.
2. **Code Build:** runs `python -m compileall app` to verify the package structure.
3. **Unit Testing:** executes `pytest tests`.
4. **Containerized Deployment:** builds and runs the app Docker image so the Selenium container has an endpoint.
5. **Selenium Testing:** builds the Selenium image and runs it via `docker run --network host`.

## Screenshots (attach actual images)
1. Screenshot of the running web UI (`screenshots/ui-home.png`).
2. Screenshot of the Jenkins pipeline stages (`screenshots/jenkins-pipeline.png`).
3. Screenshot of Selenium results or logs (`screenshots/selenium-run.png`).

## Conclusion
The assignment satisfies the requirements by combining a Flask/SQLite web app, pytest/Selenium verification, Docker artifacts, and a Jenkins pipeline covering the prescribed CI/CD stages. The provided documentation and scripts can be extended to the AWS/Jenkins environment once the services are provisioned.
