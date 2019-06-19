#!/bin/bash
TAG=$(/Users/wubowen/miniconda3/bin/python setup.py --version)
DATE=$(date "+%Y-%m-%d %H:%M:%S")

git add .
git commit -m "add tag version ${TAG} ${DATE}"
git push origin master:master
git tag -d v${TAG}
git tag -a v${TAG} -m "version ${TAG} ${DATE}"
git push origin v${TAG}