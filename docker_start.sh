#!/bin/sh
docker run -p 8080:8080 -v /home/ec2-user/label-studio:/host_directory --name label-studio label-studio