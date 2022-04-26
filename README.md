## **Requisitos**

- `python` (Suportado versão Python 3.6 até 3.9)

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

**Variação de comandos:**

O comando `python3` pode ser utilizado também como `python` dependendo da instalação ou OS, contanto que a versão seja compatível com os requisitos, assim como o comando `pip3` pode ser utilizado também como `pip`.

## Ambiente Testado

- Mac OS Mojave
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
SERVICES=s3,lambda,dynamodb,logs,iam localstack start
```

Para iniciar com o debug ativo (maior quantidade de logs e logs mais detalhados)

```bash
SERVICES=s3,lambda,dynamodb,logs,iam DEBUG=1 localstack start
```

Para executar em modo background sem manter o terminal ocupado exibindo os logs

```bash
SERVICES=s3,lambda,dynamodb,logs,iam localstack start -d
```

Para finalizar o ambiente localstack quando rodando em backgroud

```json
localstack stop
```

### Status

Para verificar o status do Localstack, ou via url [http://localhost:4566/](http://localhost:4566/)

```bash
localstack status
# retorno quando esta ativo
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Runtime version ┃ 0.14.2                                                ┃
│ Docker image    │ tag: latest, id: 3f87059df553, 📆 2022-04-13T14:51:49 │
│ Runtime status  │ ✔ running (name: "localstack_main", IP: 172.17.0.2)   │
└─────────────────┴───────────────────────────────────────────────────────┘
```

Para verificar o status dos serviços, ou via url [http://localhost:4566/health](http://localhost:4566/health)

```bash
localstack status services
# retorno quando esta ativo
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Service                  ┃ Status      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ acm                      │ ✔ available │
│ apigateway               │ ✔ available │
│ cloudformation           │ ✔ available │
│ cloudwatch               │ ✔ available │
│ config                   │ ✔ available │
│ dynamodb                 │ ✔ available │
│ dynamodbstreams          │ ✔ available │
│ ec2                      │ ✔ available │
│ es                       │ ✔ available │
│ events                   │ ✔ available │
│ firehose                 │ ✔ available │
│ iam                      │ ✔ available │
│ kinesis                  │ ✔ available │
│ kms                      │ ✔ available │
│ lambda                   │ ✔ available │
│ logs                     │ ✔ available │
│ opensearch               │ ✔ available │
│ redshift                 │ ✔ available │
│ resource-groups          │ ✔ available │
│ resourcegroupstaggingapi │ ✔ available │
│ route53                  │ ✔ available │
│ route53resolver          │ ✔ available │
│ s3                       │ ✔ running   │
│ s3control                │ ✔ available │
│ secretsmanager           │ ✔ available │
│ ses                      │ ✔ available │
│ sns                      │ ✔ available │
│ sqs                      │ ✔ available │
│ ssm                      │ ✔ available │
│ stepfunctions            │ ✔ available │
│ sts                      │ ✔ available │
│ support                  │ ✔ available │
│ swf                      │ ✔ available │
└──────────────────────────┴─────────────┘
```

### Logs

Iniciando no modo background é possível acessar os logs de execução com o comando:

```bash
localstack logs -f
# -f : para acompanhar os logs continuamente
```

Caso de algum erro do em relação a dependencia cryptography `ModuleNotFoundError: No module named 'cryptography'`, basta instalar:

```bash
pip install cryptography
```

Links:

[https://docs.localstack.cloud/localstack/configuration/](https://docs.localstack.cloud/localstack/configuration/)

[https://docs.aws.amazon.com/cli/latest/reference/#available-services](https://docs.aws.amazon.com/cli/latest/reference/#available-services)

[https://docs.localstack.cloud/aws/feature-coverage/](https://docs.localstack.cloud/aws/feature-coverage/)

## Utilizando LocalStack via Docker

### Docker

```bash
docker run --rm -it -p "4510-4559:4510-4559" -p "4566:4566" localstack/localstack -e "LOCALSTACK_SERVICES=s3,lambda,dynamodb,logs,iam" -e "DEBUG=1"
```

### Docker Compose

```yaml
version: "3.8"

services:
  localstack:
    container_name: "${LOCALSTACK_DOCKER_NAME-localstack_main}"
    image: localstack/localstack
    network_mode: bridge
    ports:
      - "4510-4559:4510-4559"
      - "4566:4566"
    environment:
      - DEBUG=${DEBUG-1} # ativa modo debug por padrao
      - DATA_DIR=${DATA_DIR-}
      - LAMBDA_EXECUTOR=${LAMBDA_EXECUTOR-}
      - HOST_TMP_FOLDER={$TMPDIR:-/tmp/}localstack
      - DOCKER_HOST=unix:///var/run/docker.sock
      - LOCALSTACK_SERVICES=s3,lambda,dynamodb,logs,iam
    volumes:
      - "${TMPDIR:-/tmp}/localstack:/tmp/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
```

Com o arquivo `docker-compose.yml` com o conteudo acima, basta executar:

```yaml
docker-compose up
```

## Acessando serviços AWS no LocalStack via terminal

Podemos fazer uso dos serviços AWS no Localstack a partir de duas ferramentas AWS CLI e awscli-local. *Recomendo a instalação de ambos.*

### AWS CLI

Ferramenta oficial da AWS para gerenciar serviços, utilizando o comando `aws`.

Para instalação escolher de acordo com o SO [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)

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
#List all buckets
aws --profile localstack --endpoint-url=$LOCALSTACK_ENDPOINT_URL s3 ls
```

### AWSCLI-LOCAL

Ferramenta adaptada a partir do AWS CLI para uso local apenas que facilita utilização dos comandos via terminal, utilizando o comando `awslocal`.

Para instalação:

```bash
pip3 install awscli-local
```

Para verificar se esta funcionando corretamente

```bash
#List all buckets
awslocal s3 ls
```

Links:

[https://docs.localstack.cloud/integrations/aws-cli/](https://docs.localstack.cloud/integrations/aws-cli/)

[https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)