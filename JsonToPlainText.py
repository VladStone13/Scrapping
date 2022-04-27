import codecs
import json
import os.path
import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def main():
    json_path = "C:\\Users\\Vlad\\scrapy2022\\src\\war2022_VMD\\war2022_VMD\\"
    json_file = "comnewsarticles.json"
    json_data = []
    os.mkdir(json_path + "comnews_plain_text")
    with open(json_path+json_file) as json_fileopen:
        json_data = json.load(json_fileopen)

    for article in json_data:
        if len(article['article_title']) >= 1:
            article_text = article['article_title'][0] + "\n\n" + article['article_text'].replace("\xa0", " ")
            article_text = striphtml(article_text)
            article_uuid = article['article_uuid']

            with codecs.open(json_path+"comnews_plain_text/"+article_uuid+".txt", "w", "utf-8-sig") as temp:
                temp.write(article_text)

if __name__== "__main__" :
    main()