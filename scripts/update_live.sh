#!/bin/sh

sudo rm -rf /usr/local/dialang-tomcat/webapps/dialang/content/*
sudo cp -r website/dialang/content/* /usr/local/dialang-tomcat/webapps/dialang/content
