aws cloudformation create-stack \
  --stack-name trade-app \
  --template-body file://deploy_app_to_aws.yaml \
  --capabilities CAPABILITY_IAM
