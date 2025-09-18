pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/hatice678/AI-Test-Selector.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                sh '''
                python3 -m venv venv
                venv/bin/pip install --upgrade pip
                venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run AI Test Selector') {
            steps {
                sh '''
                venv/bin/python ai_test_selector.py
                '''
            }
        }

        stage('Publish Reports') {
            steps {
                junit '**/reports/*.xml'
                archiveArtifacts artifacts: 'reports/**', fingerprint: true
            }
        }
    }
}
