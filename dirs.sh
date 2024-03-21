#!/bin/bash

sudo mkdir -p ~/crm/uploads/fast/log
sudo mkdir -p ~/crm/uploads/fast/files
sudo mkdir -p ~/crm/uploads/pytap/log
sudo mkdir -p ~/crm/uploads/sock/log

sudo chmod 777 ~/crm/uploads/fast/log
sudo chmod 777 ~/crm/uploads/fast/files
sudo chmod 777 ~/crm/uploads/pytap/log
sudo chmod 777 ~/crm/uploads/sock/log

sudo chmod +x binsh/PRD/*

