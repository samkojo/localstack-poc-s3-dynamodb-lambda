# LocalStack
## **Requisitos**

- `python` (Python 3.6 up to 3.9 supported)

```bash
python3 --version
```

- `pip` (Python package manager)

```bash
pip3 --version
```

- `Docker`

```bash
docker --version
```

## Ambiente Testado

- Python 3.9.4
- pip 20.2.3 (python 3.9)
- Docker version 20.10.10, build b485636

## Instalação LocalStack CLI

```bash
python3 -m pip install localstack
```

Ao finalizar a instalação deve ser possivel executar `localstack --help`

Links:

[https://docs.localstack.cloud/get-started/#localstack-cli](https://docs.localstack.cloud/get-started/#localstack-cli)

## Iniciando serviços com LocalStack

Inciando localstack ([serviços disponiveis](https://docs.localstack.cloud/aws/feature-coverage/)) com os seguintes serviços respectivamente ([baseado em serviços aws](https://docs.aws.amazon.com/cli/latest/reference/#available-services)):

- S3
- Lambda
- CloudWatch Logs
- DynamoDB

```bash
SERVICES=s3,lambda,logs,dynamodb localstack start
```

Para iniciar com o debug ativo (maior quantidade de logs e logs mais detalhados)

```bash
SERVICES=s3,lambda,dynamodb,logs DEBUG=1 localstack start
```

Links:

[https://docs.localstack.cloud/localstack/configuration/](https://docs.localstack.cloud/localstack/configuration/)

[https://docs.aws.amazon.com/cli/latest/reference/#available-services](https://docs.aws.amazon.com/cli/latest/reference/#available-services)

[https://docs.localstack.cloud/aws/feature-coverage/](https://docs.localstack.cloud/aws/feature-coverage/)

## Acessando serviços AWS

- Versão padrão [AWS CLI](https://aws.amazon.com/cli/)
- Versão adaptada local que facilita utilização dos comandos via terminal

```bash
pip3 install awscli-local
```

*Recomendo a instalação de ambos*

### Para utilização do AWS CLI:

- **Configurando AWS CLI**

```bash
#Configure AWS CLI
aws configure --profile localstack

AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]:
```

- **Configurando variável de ambiente**

Utilizando a porta padrão exposta pelo Localstack

```bash
#Configure Environment Variables
export LOCALSTACK_ENDPOINT_URL="http://localhost:4566"
```

Para verificar se a configuração ficou correta podemos executar o seguinte comando abaixo para listar os buckets

```bash
#Verify LocalStack configuration
aws --profile localstack --endpoint-url=$LOCALSTACK_ENDPOINT_URL s3 ls
```

Links:

[https://docs.localstack.cloud/integrations/aws-cli/](https://docs.localstack.cloud/integrations/aws-cli/)

[https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)

## Testando uso dos serviços (via terminal)

### S3

- Criando novo bucket “poc-s3”

```bash
awslocal s3api create-bucket --bucket poc-s3
# ou
awslocal s3 mb s3://poc-s3
# ou
aws --profile localstack --endpoint $LOCALSTACK_ENDPOINT_URL s3api create-bucket --bucket poc-s3
```

- Listando todos buckets

```bash
awslocal s3api list-buckets
# ou
aws --profile localstack --endpoint $LOCALSTACK_ENDPOINT_URL s3api list-buckets
```

- Adicionando um arquivo texto “poc.txt” localizado na pasta local ao bucket “poc-s3”

```bash
awslocal s3api put-object --bucket poc-s3 --key poc.txt --body poc.txt
# ou 
awslocal s3 cp poc.txt s3://poc-s3
# ou 
aws --profile localstack --endpoint $LOCALSTACK_ENDPOINT_URL cp poc.txt s3://poc-s3
```

- Listar arquivos no bucket “poc-s3”

```bash
awslocal s3 ls s3://poc-s3
```

- Download do arquivo do bucket “poc.txt” para pasta local com nome “downloadPOC.txt”

```bash
awslocal s3 cp s3://poc-s3/poc.txt downloadPOC.txt
```

- Deletar objeto no S3

```bash
awslocal s3api delete-object --bucket poc-s3 --key poc.txt
# ou
awslocal s3 rm s3://poc-s3/poc.txt
```

Links:

[https://www.thegeekstuff.com/2019/04/aws-s3-cli-examples/](https://www.thegeekstuff.com/2019/04/aws-s3-cli-examples/)

[https://docs.aws.amazon.com/cli/latest/reference/s3/](https://docs.aws.amazon.com/cli/latest/reference/s3/)

[https://docs.aws.amazon.com/cli/latest/reference/s3api/index.html](https://docs.aws.amazon.com/cli/latest/reference/s3api/index.html)

### DynamoDB

- Criação de tabela Music

```bash
awslocal dynamodb create-table \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema \
        AttributeName=Artist,KeyType=HASH \
        AttributeName=SongTitle,KeyType=RANGE \
--provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5
```

- Verificar tabela

```bash
awslocal dynamodb describe-table --table-name Music
```

- Deleta tabela

```bash
awslocal dynamodb delete-table --table-name Music
```

- Insere registro na tabela

```bash
awslocal dynamodb put-item \
    --table-name Music  \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}, "Awards": {"N": "1"}}'
```

- Le registros tabela

```bash
awslocal dynamodb scan --table-name Music
```

**DynamoDB GUI**

Baixar e instalar conforme a versão do SO: [AWS NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html)

![https://miro.medium.com/max/700/1*8byp3ux_Z6oP0Ro6Jds3EA.png](https://miro.medium.com/max/700/1*8byp3ux_Z6oP0Ro6Jds3EA.png)

![https://miro.medium.com/max/700/1*aiN5bsgXu3qt2Lk3IgZjjA.png](https://miro.medium.com/max/700/1*aiN5bsgXu3qt2Lk3IgZjjA.png)

![https://miro.medium.com/max/700/1*WhXH8bHOotWr9cItkw5aOg.png](https://miro.medium.com/max/700/1*WhXH8bHOotWr9cItkw5aOg.png)

![https://miro.medium.com/max/700/1*_Gz8OL35lME0jYiyfNc3GA.png](https://miro.medium.com/max/700/1*_Gz8OL35lME0jYiyfNc3GA.png)

![https://miro.medium.com/max/700/1*w-9LRgzFcGRVmXRqZbjmCw.png](https://miro.medium.com/max/700/1*w-9LRgzFcGRVmXRqZbjmCw.png)

Alternativa simples: [https://www.npmjs.com/package/dynamodb-admin](https://www.npmjs.com/package/dynamodb-admin)

Links:

[https://onexlab-io.medium.com/localstack-dynamodb-8befdaac802b](https://onexlab-io.medium.com/localstack-dynamodb-8befdaac802b)