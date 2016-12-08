# README

This is a simple tool for unsecure docker registry 

1. clone the project

        git clone https://github.com/wangc31/docker-registry-viewer.git ~/registry-viewer

2. change to the project folder

        cd ~/registry-viewer

3. build the image

        docker build -t registry-viewer .

4. run the registry viewer

        docker run --rm -p 5000:5000 --env REGISTRY_HOST=http://[REGISTRY_HOST]:[REGISTRY_PORT] registry-viewer

5. view the registry `http://localhost:5000`
