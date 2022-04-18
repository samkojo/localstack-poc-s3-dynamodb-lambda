# Lambda S3 Python Boto3 PyTest

### Configurando variável de ambiente

Utilizando a porta padrão exposta pelo Localstack.

```bash
#Configure Environment Variables
export LOCALSTACK_ENDPOINT_URL="http://localhost:4566"
```

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

Para verificar se a configuração ficou correta podemos executar o seguinte comando abaixo para listar os buckets

```bash
#Verify LocalStack configuration
aws --profile localstack --endpoint-url=$LOCALSTACK_ENDPOINT_URL s3 ls
```

## Ambiente virtual e instalação de dependências Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install boto3
python3 -m pip install python-dotenv
```

Para testar utilizaremos o Pytest então será necessário instalar

```bash
pip3 install pytest
```

## Lambda

Utilizamos como exemplo para executarmos na lambda o arquivo `lambda.py` que faz upload de um arquivo para o BUCKET confirgurado no `.env` com um nome padrao `hands-on-cloud` e com conteudo `localstack-boto3-python`

### Criar lambda e bucket

```bash
python3 main.py create
python3 main.py createbucket
```

### Executar lambda

```bash
python3 main.py invoke
# ou 
awslocal lambda invoke --function-name lambda /dev/stdout
# ou
aws lambda invoke --endpoint http://localhost:4566 --function-name lambda /dev/stdout
```

### Deletar lambda e bucket

```bash
python3 main.py delete
python3 main.py deletebucket
```

### Testar lambda

```bash
pytest -s .
```

Referencias:

[https://hands-on.cloud/testing-python-aws-applications-using-localstack/](https://hands-on.cloud/testing-python-aws-applications-using-localstack/)