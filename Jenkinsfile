pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'learned-cosine-468917-e9'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
        IMAGE_NAME = 'ml-project'
        IMAGE_TAG = 'latest'
        REGION = 'us-central1'          // ✅ set your region
        SERVICE_NAME = 'hotel-churn'    // ✅ Cloud Run service name
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                echo '🔄 Cloning GitHub repository...'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/jeet-yadav27/Hotel_Churn.git',
                        credentialsId: 'github-token'
                    ]]
                )
            }
        }

        stage('Set Up Python Environment') {
            steps {
                echo '🐍 Setting up virtual environment and installing dependencies...'
                sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                '''
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo '🐳 Building and pushing Docker image to GCR...'
                    sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker push gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo '🚀 Deploying to Google Cloud Run...'
                    sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ${SERVICE_NAME} \
                            --image gcr.io/${GCP_PROJECT}/${IMAGE_NAME}:${IMAGE_TAG} \
                            --platform managed \
                            --region ${REGION} \
                            --allow-unauthenticated
                            --port 8080
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed and deployed successfully to Cloud Run!'
        }
        failure {
            echo '❌ Pipeline failed. Check logs for details.'
        }
    }
}
