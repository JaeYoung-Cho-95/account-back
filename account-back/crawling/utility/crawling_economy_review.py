from bs4 import BeautifulSoup
import sys, os, re, requests

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from crawling.utility.save_image import save_image, make_file_path


news_index_url = "https://www.econovill.com/"
crawling_url = (
    "https://www.econovill.com/news/articleList.html?sc_section_code=S1N32&view_type=sm"
)
response = requests.get(crawling_url)

if response.status_code == 200:
    bs = BeautifulSoup(response.text, "html.parser")
    li_tags = bs.select("ul.type2 > li")

    data = []
    for li_bs in li_tags:
        save_img_path = make_file_path("eco")
        img_path = save_image(li_bs.find("img")["src"], save_img_path)

        data.append({})
        data[-1]["title"] = li_bs.find("h4", class_="titles").text
        data[-1]["news_url"] = f"{news_index_url}{li_bs.find('a').get('href')}"
        data[-1]["content"] = re.sub(
            r"[\n\t]", "", li_bs.find("p", class_="lead line-6x2").text
        )
        data[-1]["img_path"] = img_path
    
    print(data)
