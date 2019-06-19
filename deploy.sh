#!/bin/bash
TAG=$(cat luabish/__init__.py|grep '__version__'|sed "s/^__version__ = '\(.*\)'/\1/")
DATE=$(date "+%Y-%m-%d %H:%M:%S")

git add luabish/__init__.py
git commit -m "add tag version ${TAG} ${DATE}"
git push origin master:master
git tag -d v${TAG}
git tag -a v${TAG} -m "version ${TAG} ${DATE}"
git push origin v${TAG}