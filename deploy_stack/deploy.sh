APILambdaAliasArn=$1
SQSLambdaAliasArn=$2
StageName=$3
TEMPLATE=cf-deploy
STACK_NAME=deploy-stack-${StageName}
S3_BUCKET=cf-templates-onmrt5w123ls-us-east-1

aws cloudformation validate-template --template-body file://${TEMPLATE}.yaml || exit 1

aws cloudformation deploy \
  --template-file ${TEMPLATE}.yaml \
  --stack-name ${STACK_NAME} \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides APILambdaAliasArn=${APILambdaAliasArn} SQSLambdaAliasArn=${SQSLambdaAliasArn} StageName=${StageName} \
  --s3-bucket ${S3_BUCKET}