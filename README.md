## Executar os scripts para execução
Os scripts possui todos os comandos necessários para build e execução simplificada:
</br>
```
./start.sh
./stop.sh
```
</br>
Recomenda-se utilizar o script stop para parada do container e limpeza de arquivos temporários
</br></br>

### ***Anotações - preparação de ambiente EC2:***
Anotações de comandos utilizados para preparar o EC2 com ambiente. Não necessário para o projeto
```PYTHON_V=$(python3 --version | awk '{print $2}' | cut -b '1-4')```
```sudo rm /usr/lib/python$PYTHON_V/EXTERNALLY-MANAGED```

***Save Requirements***
```pip freeze | grep -E 'numpy|pandas|matplotlib' > requirements.txt ```


Ref.:
https://dev.to/lucasreis/executando-jupyter-lab-com-docker-e-docker-compose-35b2
