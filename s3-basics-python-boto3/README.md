# S3 Basics Python

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
python3 -m pip install python-dotenv
```

Os arquivos utilizam variáveis contidas no arquivo `.env`

### Criação de bucket

```bash
python3 create_bucket.py
```

- Listar todos os buckets (CLI)

```bash
awslocal s3 ls
```

### Listar buckets

```bash
python3 list_bucket.py
```

### Upload de arquivo no bucket

```bash
python3 upload_file.py 
```

- Verificar arquivos no bucket “poc-python-s3”

```bash
awslocal s3api list-objects --bucket poc-python-s3
# ou 
awslocal s3 ls s3://poc-python-s3
```

### Download de arquivo do bucket

```bash
python3 download_file.py
```

### Deletar bucket

```bash
python3 delete_bucket.py
```

Links:

[https://hands-on.cloud/testing-python-aws-applications-using-localstack/](https://hands-on.cloud/testing-python-aws-applications-using-localstack/)