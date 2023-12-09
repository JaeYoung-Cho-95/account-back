import sys, os, re, requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from crawling.utility.crawling_main import crawling_news
from bs4 import BeautifulSoup


class MoneyCrawling(crawling_news):
    def save(self):
        response = requests.get(self.crawling_url)

        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")
            li_tags = bs.select("div.content > ul > li.bundle")
            data = []
            for li_bs in li_tags:
                save_img_path = self.make_file_path(self.news)

                if not li_bs.find("a").find("img"):
                    img_path = None
                else:
                    img_path = self.save_image(
                        li_bs.find("a").find("img").get("src"), save_img_path
                    )

                data.append({})
                data[-1]["title"] = li_bs.find("strong", class_="subject").text
                data[-1][
                    "news_url"
                ] = f"{self.news_homepage}{li_bs.find('a').get('href')}"
                data[-1]["content"] = re.sub(
                    r"[\n\t]", "", li_bs.find("p", class_="txt").text
                )
                data[-1]["img_path"] = img_path
            return data
        else:
            return {"message": "해당 홈페이지에 정상적으로 접속하지 못했습니다"}


if __name__ == "__main__":
    eco_crawling = MoneyCrawling(
        news="money",
        homepage="",
        crawling_url="https://news.mt.co.kr/newsList.html?pDepth1=bank&pDepth2=Btotal",
    )
    eco_crawling.save()
