import requests, os, datetime
from crawling.models import NewsModel
from A.settings_detail.set_aws_s3 import AWS_STORAGE_BUCKET_NAME
from logging import getLogger
import os
logger = getLogger("A")
import boto3

class crawling_news:
    def __init__(self, news, homepage, crawling_url):
        self.news = news
        self.news_homepage = homepage
        self.crawling_url = crawling_url

    def save(self):
        pass

    def make_file_path(self, page):
        path = f"/usr/src/account-back/images/crawling/"
        path += str(datetime.datetime.today()).split()[0] + "/" + page + "/"
        try:
            os.makedirs(path)
        except:
            pass
        
        files = os.listdir(path)
        if len(files) >= 1:
            files = sorted(files, key=lambda x: int(x.split(".")[0]))
        else:
            return path + "1.jpg"
        return path + str(int(files[-1].split(".")[0]) + 1) + ".jpg"

    def save_image(self, image_url, save_path):
        response = requests.get(image_url)

        if response.status_code == 200:
            # directory = os.path.dirname(save_path)
            # try:
            #     os.makedirs(directory)
            # except:
            #     pass
            
            with open(save_path, "wb") as file:    
                file.write(response.content)
            return save_path
        return None

    def check_models(self, data):
        try:
            NewsModel.objects.get(title=data["title"])
            return False
        except:
            return True
    
    @staticmethod
    def list_files_in_s3_folder(path):
        bucket_name = AWS_STORAGE_BUCKET_NAME
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=path)

        files = []
        if 'Contents' in response:
            for item in response['Contents']:
                files.append(item['Key'])
        
        return files