# ocr-doc

### Iniciar o Servidor

para Iniciar o Servidor é necessário abrir o CMD e navegar até o diretório /venv/Scripts
```cmd
> cd venv\Scripts
```
e então digitar "Activate" sem as aspas
```cmd
> activate
```

Antes de executar o servidor é necessário dizer ao flask onde iniciar o servidor;
```
> cd ..\.. && set FLASK_APP=back.py
```
para executar o Servidor o comando é:
```cmd
> flask run --host=127.0.0.1
```
dessa forma o Servidor vai executar endereço localhost na porta 5000 por padrão
Caso haja a necessidade de rodar em outro endereço apenas é preciso trocar o --host
para mudar a porta padrão utiliza-se o parâmetro --port="porta desejada" sem aspas
