pipeline {
    agent any

    environment {
        VENV_DIR    = 'venv'
        GCP_PROJECT = "learned-cosine-468917-e9"
        PATH        = "/var/jenkins_home/google-cloud-sdk/bin:${env.PATH}"
        BUCKET_NAME = "jeet_yadav27"
        DATA_FILE   = "Hotel_Reservations.csv"
    }

    stages {

        stage('Clone GitHub repo') {
            steps {
                script {
                    echo '📥 Cloning GitHub repo into Jenkins workspace...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/jeet-yadav27/Hotel_Churn.git'
                        ]]
                    )
                }
            }
        }

        stage('Set up Python virtual environment') {
            steps {
                script {
                    echo '🐍 Creating virtual environment & installing dependencies...'
                    sh """
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    """
                }
            }
        }

        stage('Download Data from GCS') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "☁️ Downloading dataset from GCS bucket: ${BUCKET_NAME}"
                        sh '''
                            gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
                            gcloud config set project "$GCP_PROJECT"
                            mkdir -p artifacts/raw
                            gsutil cp gs://$BUCKET_NAME/$DATA_FILE artifacts/raw/raw.csv
                        '''
                    }
                }
            }
        }

        stage('Run Data Ingestion (Split Train/Test)') {
            steps {
                script {
                    echo '✂️ Splitting dataset into train.csv and test.csv...'
                    sh """
                        . ${VENV_DIR}/bin/activate
                        python pipeline/data_ingestion.py
                    """
                }
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo '🐳 Building Docker image and pushing to Google Container Registry...'
                        sh '''
                            gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
                            gcloud config set project "$GCP_PROJECT"
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/$GCP_PROJECT/ml-project:latest .
                            docker push gcr.io/$GCP_PROJECT/ml-project:latest
                        '''
                    }
                }
            }
        }

        stage('Run Training Pipeline in Container') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo '🏋️ Running training pipeline inside container...'
                        sh '''
                            gcloud auth activate-service-account --key-file="$GOOGLE_APPLICATION_CREDENTIALS"
                            gcloud config set project "$GCP_PROJECT"

                            docker run --rm \
                                -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/key.json \
                                -v "$GOOGLE_APPLICATION_CREDENTIALS":/tmp/key.json:ro \
                                -v "$PWD/artifacts":/app/artifacts \
                                gcr.io/$GCP_PROJECT/ml-project:latest \
                                python pipeline/training_pipeline.py
                        '''
                    }
                }
            }
        }
    }
}
