FROM jupyter/base-notebook

# Instalar dependências necessárias
USER root
RUN apt-get update && apt-get install -yq --no-install-recommends \
    build-essential \
    python3-dev \
    npm \
    nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar jupyter_contrib_nbextensions
RUN pip install jupyter_contrib_nbextensions && \
    jupyter contrib nbextension install --user

# Ativar a extensão hide_input
RUN jupyter nbextension enable hide_input/main

# Voltar ao usuário padrão
USER ${NB_UID}

CMD ["start-notebook.sh"]
