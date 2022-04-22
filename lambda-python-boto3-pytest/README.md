# Lambda Python Boto3 PyTest

### Configurando AWS CLI

```bash
#Configure AWS CLI
aws configure --profile localstack

AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]:
```

Criação de um AWS CLI profile chamado `localstack` com os padrões utilizados para uso local.

## Ambiente virtual e instalação de dependências Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install boto3
```

Para testar utilizaremos o Pytest então será necessário instalar

```bash
pip3 install pytest
```

## Lambda

Utilizamos como exemplo para executarmos na lambda o arquivo `lambda-hello.py` que simplesmente retorna `{'message': 'Hello User!'}`

### Criar lambda

Cria lambda com o código contido em `lambda-hello.py` com o nome baseado na variável `LAMBDA_NAME`

```bash
python3 main.py create
```

### Executar lambda

Executa lambda `lambda-hello` e exibe resultado no terminal 

```bash
python3 main.py invoke
# ou 
awslocal lambda invoke --function-name lambda-hello /dev/stdout
```

Executa lambda `lambda-hello` retornando os logs

```bash
awslocal lambda invoke --function-name lambda-hello /dev/stdout --log-type Tail
```

### Deletar lambda

Deleta lambda `lambda-hello`

```bash
python3 main.py delete
```

### Testar lambda

Executa cenário de teste da lambda: criação de lambda, execução e verificação do resultado retornado e deleção da lambda.

```bash
pytest -s .
```

Referencias:

[https://hands-on.cloud/testing-python-aws-applications-using-localstack/](https://hands-on.cloud/testing-python-aws-applications-using-localstack/)