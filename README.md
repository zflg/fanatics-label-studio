# 1. Deploying Label Studio
## 1.1. Install Docker
## 1.2. Deploying Label Studio in Docker
Create the mount file directory on the host machine
```shell
mkdir -p /home/ec2-user/label-studio
```
Build the Docker Image for Label Studio
```shell
docker built -t label-studio .
```
* Run a Docker container
* Mount the host machine directory /home/ec2-user/label-studio to the container directory /host_directory
* The web service port for the label-studio container is 8080, map it to the host machine port 8080 (can be changed). Make sure to open the host machine's 8080 port to the internet for external access.
```shell
docker run -p 8080:8080 -v /home/ec2-user/label-studio:/host_directory --name label-studio label-studio
```
Assuming the host machine's access IP is 3.144.134.13, the label-studio service can be accessed through the URL http://3.144.134.13:8080 to reach the home page.

# 2. Using label-studio
* Sign up to create new account
* Login in
* Create new project
  + project name
  + upload data
  + Labeling Setup
* labeling