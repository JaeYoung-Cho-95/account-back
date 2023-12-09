import sys, os, re, requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from crawling.utility.crawling_main import crawling_news
from bs4 import BeautifulSoup
from crawling.serializers import NewsSerializer
from logging import getLogger

logger = getLogger("A")


class MoneyCrawling(crawling_news):
    def save(self):
        response = requests.get(self.crawling_url)

        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")
            li_tags = bs.select("div.content > ul > li.bundle")
            data = self.make_data(li_tags=li_tags)
            NS = NewsSerializer(data=data, many=True)
            if NS.is_valid():
                NS.save()
            return NS.data
        else:
            logger.info("6")
            return {"message": "해당 홈페이지에 정상적으로 접속하지 못했습니다"}

    def make_data(self, li_tags):
        data = []
        for li_bs in li_tags:
            save_img_path = self.make_file_path(self.news)

            data.append({})
            data[-1]["title"] = li_bs.find("strong", class_="subject").text
            data[-1]["news_url"] = f"{self.news_homepage}{li_bs.find('a').get('href')}"
            data[-1]["content"] = re.sub(
                r"[\n\t]", "", li_bs.find("p", class_="txt").text
            )

            if self.check_models(data[-1]):
                if li_bs.find("a").find("img"):
                    img_path = self.save_image(li_bs.find("a").find("img").get("src"), save_img_path)
                    data[-1]["img_url"] = img_path
                else:
                    data[-1]["img_url"] = None
            else:
                data.pop()
        return data


if __name__ == "__main__":
    money_crawling = MoneyCrawling(
        news="money",
        homepage="",
        crawling_url="https://news.mt.co.kr/newsList.html?pDepth1=bank&pDepth2=Btotal",
    )
    money_crawling.save()