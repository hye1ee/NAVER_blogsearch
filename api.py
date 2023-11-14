from dotenv import load_dotenv
import os
import urllib.request
import json
import plotly.express as px
from datetime import datetime
import argparse
from utils import get_jsonpath

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_pw = os.getenv("CLIENT_PW")

def set_display(url, display_num) :
  # default 10, maximum 100
  display_num = min(100, max(display_num, 10))
  return url + "&display=" + str(display_num)

def set_start(url, start_num) :
  # default 1, maximum 1000 
  start_num = min(1000, max(start_num, 1))
  return url + "&start=" + str(start_num)

def set_sort(url, sort) :
  # sim or date
  return url + "&sort=" + sort

def send_response(request) :
  response = urllib.request.urlopen(request)
  rescode = response.getcode()
  if(rescode==200):
      response_body = response.read()
      return json.loads(response_body.decode('utf-8'))
  else:
      return "error" + rescode

def get_response(query, display=10, start=1, sort="sim") :
  encText = urllib.parse.quote(query)
  url = "https://openapi.naver.com/v1/search/blog?query=" + encText
  url = set_display(url, display)
  url = set_start(url, start)
  url = set_sort(url, sort)

  print(url)
  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_pw)
  return process_response(send_response(request))

def process_response(res) :
  if "error" in res :
    return None
  else :
    return res

def main(query, file_name):
  data = []
  for i in range(11) :
    res = get_response(query, 100, 1 + 100*i)
    if res != None :
      data.extend(res["items"])
  with open(get_jsonpath(file_name), 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="api")

  parser.add_argument("--query", type=str, required=True)
  parser.add_argument("--filename", type=str, required=True)

  args = parser.parse_args()

  main(args.query, args.filename)