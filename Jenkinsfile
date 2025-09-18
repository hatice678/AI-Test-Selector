pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {
        stage('Checkout') {
            steps {
                // Git repo'yu çek
                git branch: 'main', url: 'https://github.com/hatice678/AI-Test-Selector.git'
            }
        }

        stage('Setup Python Env') {
            steps {
                sh '''
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run AI Test Selector') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                python ai_test_selector.py
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

    post {
        always {
            echo "Pipeline tamamlandı ✅"
        }
        failure {
            echo "Pipeline hata verdi ❌"
        }
    }
}
