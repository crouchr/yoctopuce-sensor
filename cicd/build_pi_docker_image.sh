#!/bin/bash
# Run this on the yoctopi node itself

VERSION=1.0.0

cd ..
#docker build --no-cache -t cicd:meteod .
#docker tag cicd:meteod registry:5000/meteod:$VERSION
#docker push registry:5000/meteod:$VERSION
#docker rmi cicd:meteod

docker build --no-cache -t meteod .
docker tag meteod meteod:$VERSION
#docker push registry:5000/meteod:$VERSION
#docker rmi cicd:meteod