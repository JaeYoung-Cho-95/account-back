import requests, os, re, datetime


class crawling_news:
    def __init__(self, news, homepage, crawling_url):
        self.news = news
        self.news_homepage = homepage
        self.crawling_url = crawling_url

    def save(self):
        pass

    def save_image(self, image_url, save_path):
        response = requests.get(image_url)

        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
            return save_path
        return None

    def make_file_path(self, page):
        par_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        )
        path = f"{par_dir}/images/crawling/"

        path += str(datetime.datetime.today()).split()[0] + "/" + page + "/"

        try:
            path_list = os.listdir(path)
        except:
            os.makedirs(path)
            path_list = os.listdir(path)

        path_list = sorted(path_list, key=lambda x: int(x.split(".")[0]))
        
        if not path_list:
            return path + "1.jpg"
        else:
            return path + str(int(path_list[-1].split(".")[0]) + 1) + ".jpg"
