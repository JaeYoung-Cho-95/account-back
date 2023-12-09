import sys, os, re, requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from crawling.utility.crawling_main import crawling_news
from bs4 import BeautifulSoup


class EconomicCrawling(crawling_news):
    def save(self):
        response = requests.get(self.crawling_url)

        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")
            li_tags = bs.select("ul.type2 > li")

            data = []
            for li_bs in li_tags:
                save_img_path = self.make_file_path(self.news)
                img_path = self.save_image(li_bs.find("img")["src"], save_img_path)

                data.append({})
                data[-1]["title"] = li_bs.find("h4", class_="titles").text
                data[-1][
                    "news_url"
                ] = f"{self.news_homepage}{li_bs.find('a').get('href')}"
                data[-1]["content"] = re.sub(
                    r"[\n\t]", "", li_bs.find("p", class_="lead line-6x2").text
                )
                data[-1]["img_path"] = img_path
            return data
        else:
            return {"message": "해당 홈페이지에 정상적으로 접속하지 못했습니다"}


if __name__ == "__main__":
    eco_crawling = EconomicCrawling(
        news="eco",
        homepage="https://www.econovill.com/",
        crawling_url="https://www.econovill.com/news/articleList.html?sc_section_code=S1N32&view_type=sm",
    )
    eco_crawling.save()
