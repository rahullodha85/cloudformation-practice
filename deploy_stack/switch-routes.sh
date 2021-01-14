StageToDelete=$1
TEMPLATE=switch-routes
STACK_NAME=switch-routes
S3_BUCKET=cf-templates-onmrt5w123ls-us-east-1

aws cloudformation validate-template --template-body file://${TEMPLATE}.yaml || exit 1

aws cloudformation deploy \
  --template-file ${TEMPLATE}.yaml \
  --stack-name ${STACK_NAME} \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides StageToDelete=${StageToDelete} \
  --s3-bucket ${S3_BUCKET}