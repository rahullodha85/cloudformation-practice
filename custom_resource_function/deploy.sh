TEMPLATE=cf-deploy
STACK_NAME=publish-alias-lambda
S3_BUCKET=cf-templates-onmrt5w123ls-us-east-1

pip install -r ./requirements.txt -t ./external_dependencies/python/lib/python3.8/site-packages

aws cloudformation validate-template --template-body file://${TEMPLATE}.yaml || exit 1

aws cloudformation package \
  --template-file ${TEMPLATE}.yaml \
  --s3-bucket ${S3_BUCKET} \
  --output-template-file ${TEMPLATE}_output.yaml || exit 1

aws cloudformation deploy \
  --template-file ${TEMPLATE}_output.yaml \
  --stack-name ${STACK_NAME} \
  --capabilities CAPABILITY_NAMED_IAM \
  --s3-bucket ${S3_BUCKET}

aws cloudformation list-exports