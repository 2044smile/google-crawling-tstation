import json, time, requests, os

from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler


class Crawlers:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.slack_url = os.environ['SLACK_WEBHOOK']

        self.tstation = requests.get(url='https://news.google.com/search?q=%ED%95%9C%EA%B5%AD%ED%83%80%EC%9D%B4%EC%96%B4+when:1d&hl=ko&gl=KR&ceid=KR%3Ako')
        self.samsung = requests.get(url='https://news.google.com/search?q=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90%20when%3A1d&hl=ko&gl=KR&ceid=KR%3Ako')

    def crawler(self, target):
        if target == 'tstation':
            html = self.tstation
        elif target == 'samsung':
            html = self.samsung

        soup = BeautifulSoup(html.text, 'html.parser')
        bs = soup.select(
            "#yDmH0d > c-wiz > div > div.FVeGwb.CVnAc.Haq2Hf.bWfURe > div.ajwQHc.BL5WZb.RELBvb"
        )
        answers = bs[0].findAll('h3', class_='ipQwMb ekueJc RD0gLb')

        if not answers:
            no_data = {
                "attachments": [{
                    "color": "#36a64f",
                    "title": f":warning: {target} 뉴스 데이터가 존재 하지 않습니다. :warning:",
                }]}
            requests.post(url=self.slack_url, headers=self.headers, data=json.dumps(no_data))
        else:
            for answer in answers:
                data = {
                    "attachments": [{
                        "color": "#36a64f",
                        "title": answer.text,
                        "title_link": f"https://www.news.google.com/{answer.find('a').get('href')}"
                        }]
                    }
                requests.post(url=self.slack_url, headers=self.headers, data=json.dumps(data))


if __name__ == '__main__':
    sched = BackgroundScheduler(timezone="Asia/Seoul")
    sched.start()

    while True:
        # 매일 09시, 11시, 13시 0분 30분 한국타이어 뉴스 크롤링
        @sched.scheduled_job('cron', hour='9,11,13', minute='0,30', id='am')
        def crawler_tstation_news():
            crawlers = Crawlers()

            slack_url = os.environ['SLACK_WEBHOOK']
            headers = {"Content-Type": "application/json"}
            data = {
                "attachments": [{
                    "color": "#36a64f",
                    "title": "🔔 한국타이어, 삼성전자 크롤링 🔔",
                    }]}

            requests.post(url=slack_url, headers=headers, data=json.dumps(data))

            crawlers.crawler('samsung')
            crawlers.crawler('tstation')

        time.sleep(1)