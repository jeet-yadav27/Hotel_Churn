C:\Users\jeety\Desktop\2. MLOPS_DEVOPS\hote_churn\learned-cosine-468917-e9-4cc62a2186e8.json

pip install -e .
python -m src.data_preprocessing


### steps for CI/CD DEPLOYMENT
1. Setup Jenkins Container 
NOTE (DID) Docker in Docker 
    first Docker is for the Jenkins and Second docker is for the project running

2. Github Integration
we have to intergrate the github code to the jenkins pipeline

3. Dockerization of project

4. Create a Virtual Env in your jenkins Pipeline

5. Build Docker Image of the Project-->>>> then push this image to GCR (Google Cloud Registry)

6. Extract image from GCR and push to Google Cloud Run--->>> then App is Deployed


NOTE: open the Docker Desktop and keep the Running the app in background and see if the Engine is running 


prcatical
1. Create the Directory name  --->>> custom_jenkins, insdie this create a ---->>> Dockerfile

2. After paste the Docker code form stepmd. login Docker >>> docker login
3. build the image of jenkins Docker >> docker Build -t jenkins-dind . ### here jenkins-dind . is the Docker name
4. now check if the image is successfully build or not, for this ---->>> docker images
5. Go to setupmd.-->> 4. **Run Jenkins Docker Container:** copy and paste this code

    docker run -d --name jenkins-dind ^
    --privileged ^
    -p 8080:8080 -p 50000:50000 ^
    -v //var/run/docker.sock:/var/run/docker.sock ^
    -v jenkins_home:/var/jenkins_home ^
    jenkins-dind

    After running the code, will get alpha numeric key value>> check same on  docker or you can run-->>> docker ps

6. now> ------ docker logs jenkins-dind

copy the password >>> goto browser search localhost: 8080>>>> Enter the password>>> install the Plugin
user_name>> mlops92
password>> jenkins

7. Download some dependencies for the jenkins
go to steps.md code ### **Step 4: Install Python and Required Packages in Jenkins Container**

### till jenkins done