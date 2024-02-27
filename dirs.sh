#!/bin/bash
sudo mkdir -p /crmdir/uploads/fast/log
sudo mkdir -p /crmdir/uploads/fast/files
sudo mkdir -p /crmdir/uploads/pytap/log
sudo mkdir -p /crmdir/uploads/sock/log

sudo chmod 777 /crmdir/uploads/fast/log
sudo chmod 777 /crmdir/uploads/fast/files
sudo chmod 777 /crmdir/uploads/pytap/log
sudo chmod 777 /crmdir/uploads/sock/log

sudo chmod +x binsh/PRD/*

