#!/bin/bash

mkdir Minerva
cd Minerva
git init
git config http.sslVerify false
git remote add origin https://djb231-desktop.lsc.phy.private.cam.ac.uk/minerva.git
git config branch.master.remote origin
git config branch.master.merge refs/heads/master
git pull origin master
