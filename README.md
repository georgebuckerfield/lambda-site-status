# lambda-site-status

An HTTP health checker running in Lambda, storing state in DynamoDB.

## Building a deployment package

These instructions assume you're using a virtual environment:

```
pip install -r requirements.txt
make zip
```

You should now find a Lambda ready deployment package in `deploys/`.