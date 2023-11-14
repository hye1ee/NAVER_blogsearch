from dotenv import load_dotenv
from api import main
import argparse
import json
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_jsonpath, get_pngpath
from konlpy.tag import Komoran
import os

load_dotenv()

jvmpath = os.getenv("JVM_PATH")


def get_textdata(filename) :
  with open(get_jsonpath(filename), 'r', encoding='utf-8') as file:
    data = json.load(file)

  data_text = [x["title"] for x in data]
  data_text.extend([x["description"] for x in data])

  data_text = pd.DataFrame({"text": data_text})
  data_text['text'] = data_text['text'].str.replace('[^가-힣]', ' ', regex = True)
  return data_text

def get_nouns(textdata, count) :
  komoran = Komoran(jvmpath)

  nouns = textdata['text'].apply(komoran.nouns)
  nouns = nouns.explode()
  df_word = pd.DataFrame({'word' : nouns})
  df_word['count'] = df_word['word'].str.len()
  df_word = df_word.groupby('word', as_index = False).count().sort_values('count', ascending = False)
  dic_word = df_word.set_index('word').to_dict()['count']

  dic_word = {key: value for key, value in dic_word.items() if value > count}
  return dic_word

def draw_wordcloud (query, filename, count) : 
  if not os.path.exists(get_jsonpath(filename)):
    print("Request API and store as json file : ", get_jsonpath(filename))
    main(query, filename)

  cloud = WordCloud(random_state = 20200529, font_path = 'AppleGothic', width = 500,
               height = 500, background_color = 'white')
  cloud_img = cloud.generate_from_frequencies(get_nouns(get_textdata(filename), count))
  plt.figure(figsize = (5, 5))
  plt.axis('off')
  plt.imshow(cloud_img)
  plt.savefig(get_pngpath(filename))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="api")

  parser.add_argument("--query", type=str, required=True)
  parser.add_argument("--filename", type=str, required=True)
  parser.add_argument("--count", type=int, required=True)

  args = parser.parse_args()
  draw_wordcloud(args.query, args.filename, args.count)
