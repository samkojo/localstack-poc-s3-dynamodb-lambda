# DynamoDB Basics Python Boto3

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

Os arquivos utilizam variáveis contidas no arquivo `.env`

### Criação de tabela

```bash
python3 utils_dynamodb.py createtable
```

- Retorna dados da tabela poc-python-dynamodb (CLI)

```bash
awslocal dynamodb describe-table --table-name poc-python-dynamodb
```

### Deleção de tabela

```bash
python3 utils_dynamodb.py deletetable
```

### Adição de registro em tabela

```bash
python3 utils_dynamodb.py addtableitem
```

### Leitura de registro em tabela

```bash
python3 utils_dynamodb.py readtableitem
```

### Atualização de registro em tabela

```bash
python3 utils_dynamodb.py updatetableitem
```

### Deleção de registro em tabela

```bash
python3 utils_dynamodb.py deletetableitem
```

Referencias:

[https://hands-on.cloud/testing-python-aws-applications-using-localstack/](https://hands-on.cloud/testing-python-aws-applications-using-localstack/)