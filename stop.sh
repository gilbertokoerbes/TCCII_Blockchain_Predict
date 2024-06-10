#!/bin/bash
docker stop jupyter_lab
docker rm jupyter_lab
rm -rf ./runtime