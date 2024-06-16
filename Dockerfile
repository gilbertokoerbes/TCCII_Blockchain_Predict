FROM jupyter/minimal-notebook

# Usuário root para instalar dependências
USER root

# Instalar dependências necessárias
RUN apt-get update && apt-get install -yq --no-install-recommends \
    build-essential \
    python3-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#Voltar ao usuário padrão
USER ${NB_UID}

# #Verificar e garantir uma versão compatível do Jupyter Notebook
# RUN pip install --upgrade notebook==7.2
 
# #Instalar jupyter_contrib_nbextensions
# RUN pip install jupyter_contrib_nbextensions && \
#     jupyter contrib nbextension install --user

# # Ativar a extensão hide_input
# RUN jupyter nbextension enable hide_input/main




WORKDIR /home/jovyan/work
COPY ./requirements.txt .
RUN pip install -r requirements.txt 
