from __future__ import print_function
from decimal import Decimal, getcontext
import requests
import datetime
import boto3
import uuid

def http_check(url):
  check = requests.get(url)
  getcontext().prec = 6
  resp_time = Decimal(check.elapsed.total_seconds())
  resp_code = check.status_code
  return resp_code, resp_time


def db_get_url(site):
  print("Get the site URL from DynamoDB")
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('site-status-config')
    
  site_config = table.get_item(
    Key={
      'site': site
    }
  )
  site_url = site_config['Item']['site_url']
  return site_url


def db_update(site, check_time, check_resp_code, check_resp_time):
  print("Updating DynamoDB")
  dynamodb = boto3.resource('dynamodb')
  table = dynamodb.Table('site-status-history')

  check_id = str(uuid.uuid4())
  check_record = table.put_item(
    Item={
      'check_id': check_id,
      'check_site': site,
      'check_time': check_time,
      'check_resp_code': check_resp_code,
      'check_resp_time': check_resp_time
    }
  )


def lambda_handler(event, context):
  check_site = event['site']
  check_url = db_get_url(check_site)
  check_time = str(datetime.datetime.now())
  
  resp_code, resp_time = http_check(check_url)
  db_update(check_site, check_time, resp_code, resp_time)
