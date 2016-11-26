import boto3

def create_rule(site,schedule):
    client = boto3.client('events')
    
    rule_name = 'http_check_' + site
    sched_exp = 'cron(%s)' % schedule
    response = client.put_rule(
        Name=rule_name,
        ScheduleExpression=sched_exp,
        State='ENABLED',
        Description='An http health check rule',
        )
    return response

def add_target_to_rule(site,rule_arn):
    ev_client = boto3.client('events')
    rule_name = 'http_check_' + site
    rule_input = '{"site": "%s"}' % site
    add_target = ev_client.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': 'http_check',
                'Arn': 'arn-of-the-http-check-function',
                'Input': rule_input
                },
            ]
        )
    lambda_client = boto3.client('lambda')
    statement_id = 'allow_%s_rule' % site
    add_permission = lambda_client.add_permission(
        FunctionName='http_check',
        StatementId=statement_id,
        Action="lambda:InvokeFunction",
        Principal='events.amazonaws.com',
        SourceArn=rule_arn
    )
    if add_target['ResponseMetadata']['HTTPStatusCode'] == 200 and add_permission['ResponseMetadata']['HTTPStatusCode'] == 200:
        return 200

def lambda_handler(event, context):
    print(event)
    if event['Records'][0]['eventName'] == "INSERT":
        data = event['Records'][0]['dynamodb']['NewImage']
        print(data)
        site = data['site']['S']
        #site = 'test'
        schedule = data['schedule']['S']
        
        rule = create_rule(site,schedule)
        
        if rule['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Cloudwatch rule created")
            rule_arn = rule['RuleArn']
            target = add_target_to_rule(site, rule_arn)
            if target == 200:
                print("Attached lambda function to the rule")
                return 'Site record inserted'

    else:
        return 'Not an insert so ignoring'