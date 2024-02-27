#!/bin/bash
#this actually does nothing,
#remember the dirs are at ~/crm/uploads/...

sudo mkdir -p /crmdir/uploads/fast/log
sudo mkdir -p /crmdir/uploads/fast/files
sudo mkdir -p /crmdir/uploads/pytap/log
sudo mkdir -p /crmdir/uploads/sock/log

sudo chmod 777 /crmdir/uploads/fast/log
sudo chmod 777 /crmdir/uploads/fast/files
sudo chmod 777 /crmdir/uploads/pytap/log
sudo chmod 777 /crmdir/uploads/sock/log

sudo chmod +x binsh/PRD/*

