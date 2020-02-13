#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/y &&
cd ~/travis2/tukulsa-linebot
git pull
mkdir storage && cd storage && mkdir log

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop tukulsaBOT
docker rm tukulsaBOT
docker rmi daffa99/containerd:BOT
docker run -d --name tukulsaBOT -p 5001:5001 daffa99/containerd:BOT
