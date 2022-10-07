#!/bin/bash 

APP_NAME="powermonitor"

pex . -o ${APP_NAME}.pex -e powermonitor.main:main -r requirements.txt 
