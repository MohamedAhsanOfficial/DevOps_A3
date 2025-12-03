pipeline {
  agent any
  environment {
    DOCKER_IMAGE = "ssdd-webapp:${env.BUILD_NUMBER}"
    SELENIUM_IMAGE = "ssdd-selenium:${env.BUILD_NUMBER}"
    APP_CONTAINER = "ssdd-app-${env.BUILD_ID}"
  }

  stages {
    stage('Code Linting') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
          flake8 app tests
        '''
      }
    }

    stage('Code Build') {
      steps {
        sh '''
          . .venv/bin/activate
          python -m compileall app
        '''
      }
    }

    stage('Unit Testing') {
      steps {
        sh '''
          . .venv/bin/activate
          pytest tests
        '''
      }
    }

    stage('Containerized Deployment') {
      steps {
        sh '''
          docker build -t ${DOCKER_IMAGE} .
          docker run -d --name ${APP_CONTAINER} -p 5000:5000 ${DOCKER_IMAGE}
          sleep 5
        '''
      }
    }

    stage('Selenium Testing') {
      steps {
        sh '''
          docker build -t ${SELENIUM_IMAGE} -f Dockerfile.selenium .
          docker run --rm --network host -e APP_URL=http://localhost:5000 ${SELENIUM_IMAGE}
        '''
      }
    }
  }

  post {
    always {
      sh 'docker rm -f ${APP_CONTAINER} || true'
    }
  }
}
