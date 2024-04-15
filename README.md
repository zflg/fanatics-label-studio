# 1. 部署label-studio
## 1.1. 安装docker
## 1.2. 部署label-studio到docker
创建宿主机的挂载文件目录
```shell
mkdir -p /home/ec2-user/label-studio
```
创建docker image
```shell
docker built -t label-studio .
```
创建docker container
挂载宿主机目录/home/ec2-user/label-studio到容器目录/host_directory
容器内label-studio的web服务端口为8080，映射到宿主机端口8080（可以更换），注意开放宿主机的8080端口到外网能够访问
```shell
docker run -p 8080:8080 -v /home/ec2-user/label-studio:/host_directory --name label-studio label-studio
```
假设宿主机访问ip为3.144.134.13，则访问label-studio的服务可通过http://3.144.134.13:8080登陆主页。

# 2. 使用label-studio
* Sign up to create new account
* Login in
* Create new project
  + project name
  + upload data
  + Labeling Setup
* labeling