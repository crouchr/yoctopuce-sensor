#!/bin/bash
VERSION=dev

cd ..
docker build --no-cache -t cicd:meteod .
docker tag cicd:meteod registry:5000/meteod:$VERSION
docker push registry:5000/meteod:$VERSION
docker rmi cicd:meteod
