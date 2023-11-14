from dotenv import load_dotenv
import os

load_dotenv()

datapath = os.getenv("DATA_PATH")

def get_jsonpath(filename) :
  return datapath + filename + ".json"

def get_pngpath(filename) :
  return datapath + filename + ".png"
