import json, time, requests

from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler


class tstation:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.tstation = requests.get(url='https://news.google.com/search?q=%ED%95%9C%EA%B5%AD%ED%83%80%EC%9D%B4%EC%96%B4+when:1d&hl=ko&gl=KR&ceid=KR%3Ako')

        # self.slack_url = os.environ['SLACK_WEBHOOK']

    def crawler(self):
        html = self.tstation
        soup = BeautifulSoup(html.text, 'html.parser')
        bs = soup.select(
            "#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb"
        )
        answers = bs[0].findAll('h3', class_='ipQwMb ekueJc RD0gLb')

        for answer in answers:
            print('title: ', answer.text)
            print('URL: ', answer.find('a').get('href'))
            # data = {
            #     "attachments": [{
            #         "color": "#36a64f",
            #         "title": answer.text,
            #         "title_link": f"https://www.news.google.com/{answer.find('a').get('href')}"
            #         }]
            #     }
            # requests.post(url=self.slack_url, headers=self.headers, data=json.dumps(data))


if __name__ == '__main__':
    # sched = BackgroundScheduler(timezone="Asia/Seoul")
    # sched.start()

    # while True:
        # 매일 11시에 한국타이어 뉴스 크롤링
        # @sched.scheduled_job('cron', hour='11', id='am')
        # def crawler_tstation_news():
    crawl = tstation()
    crawl.crawler()

        # time.sleep(1)