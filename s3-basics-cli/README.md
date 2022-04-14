- Criando novo bucket “poc-s3”

```bash
awslocal s3api create-bucket --bucket poc-s3
# ou
awslocal s3 mb s3://poc-s3
```

- Adicionando um arquivo texto “poc.txt” ao bucket “poc-s3”

```bash
awslocal s3api put-object --bucket poc-s3 --key poc.txt --body ../assets/poc.txt
# ou 
awslocal s3 cp ../assets/poc.txt s3://poc-s3
```

- Listar arquivos no bucket “poc-s3”

```bash
awslocal s3 ls s3://poc-s3 
```

- Download do arquivo do bucket “poc.txt” para pasta local com nome “downloadPOC.txt”

```bash
awslocal s3 cp s3://poc-s3/poc.txt ./downloadPOC.txt
```

- Deletar objeto no S3

```bash
awslocal s3api delete-object --bucket poc-s3 --key poc.txt
```

[https://www.thegeekstuff.com/2019/04/aws-s3-cli-examples/](https://www.thegeekstuff.com/2019/04/aws-s3-cli-examples/)