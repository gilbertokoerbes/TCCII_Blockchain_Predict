#!/bin/bash
#DNS='blockchain-predict-67a6f0f5b7872efa.elb.us-east-1.amazonaws.com' # LoadBalancer
DNS='localhost'

docker compose up --build -d --wait	

docker cp jupyter_lab:/home/jovyan/.local/share/jupyter/runtime/ ./runtime

token=$(jq --raw-output '.token' ./runtime/jpserver-*.json)

echo 'Link de acesso:'
echo http://$DNS:8888/notebooks/predict.ipynb?token=$token