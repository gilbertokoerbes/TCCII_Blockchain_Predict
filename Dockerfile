FROM jupyter/minimal-notebook
WORKDIR /home/jovyan/work
COPY ./requirements.txt .
RUN pip install -r requirements.txt 
