import time
import requests
import os
import datetime


def save_image(image_url, save_path):
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)

    return save_path


def make_file_path(page):
    par_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    path = f"{par_dir}/images/crawling/"

    # 날짜 및 뉴스 page
    path += str(datetime.datetime.today()).split()[0] + "/" + page + "/"

    try:
        path_list = os.listdir(path)
    except:
        os.makedirs(path)
        path_list = os.listdir(path)

    path_list = sorted(path_list, key=lambda x: x.split(".")[0])

    if not path_list:
        return path + "1.jpg"
    else:
        return path + str(int(path_list[-1].split(".")[0]) + 1) + ".jpg"


if __name__ == "__main__":
    print(make_file_path("news"))
