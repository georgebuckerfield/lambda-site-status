from __future__ import print_function
import requests
import datetime

def http_check(url):

  check = requests.get(url)
  
  resp_time = check.elapsed.total_seconds()
  resp_code = check.status_code

  return resp_code, resp_time

def db_get_url(site):
  print("Get the site URL from DynamoDB")
  return site_url

def db_update(site, check_time, check_resp_code, check_resp_time):
  print("Update DynamoDB here")
  print(check_time, check_resp_code, check_resp_time)

def lambda_handler(event, context):
  check_site = event['site']
  check_url = db_get_url(check_site)
  check_time = datetime.datetime.now()
  
  resp_code, resp_time = http_check(check_url)
  db_update(check_site, check_time, resp_code, resp_time)
