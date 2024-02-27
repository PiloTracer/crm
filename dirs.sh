#!/bin/bash
sudo mkdir -p /opt/uploads/fast/log
sudo mkdir -p /opt/uploads/fast/files
sudo mkdir -p /opt/uploads/pytap/log
sudo mkdir -p /opt/uploads/sock/log

sudo chmod 777 /opt/uploads/fast/log
sudo chmod 777 /opt/uploads/fast/files
sudo chmod 777 /opt/uploads/pytap/log
sudo chmod 777 /opt/uploads/sock/log

sudo chmod +x binsh/PRD/*

#sudo chmod +x dirs.sh
