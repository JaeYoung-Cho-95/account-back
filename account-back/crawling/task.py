from background_task import background
from crawling.utility import economic_review, money_today


@background(schedule=86400)
def save_economic_news():
    eco_crawling = economic_review.EconomicCrawling(
        news="eco",
        homepage="https://www.econovill.com/",
        crawling_url="https://www.econovill.com/news/articleList.html?sc_section_code=S1N32&view_type=sm",
    )
    eco_crawling.save()


@background(schedule=86400)
def save_money_news():
    money_crawling = money_today.MoneyCrawling(
        news="money",
        homepage="",
        crawling_url="https://news.mt.co.kr/newsList.html?pDepth1=bank&pDepth2=Btotal",
    )
    money_crawling.save()
