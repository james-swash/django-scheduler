import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()


class CronObj(object):

    def __init__(self, action_id, scheduled, job_id):
        split_string = scheduled.split(' ')
        self.year = split_string[0]
        self.month = split_string[1]
        self.day = split_string[2]
        self.week = split_string[3]
        self.day_of_week = split_string[4]
        self.hour = split_string[5]
        self.minute = split_string[6]
        self.second = split_string[7]
        self.action_id = action_id
        self.job_id = str(job_id)
        # self.start = split_string[8]
        # self.end = split_string[9]

    def start_job(self):
        print(self.action_id)
        scheduler.add_job(
            func=scheduler_execution,
            kwargs={'action_id': self.action_id},
            trigger='cron',
            id=self.job_id,
            year=self.year,
            month=self.month,
            day=self.day,
            week=self.week,
            day_of_week=self.day_of_week,
            hour=self.hour,
            minute=self.minute,
            second=self.second
            # start_date=self.start,
            # end_date=self.end
        )


def scheduler_print(action_id):
    print(action_id)


def scheduler_execution(action_id):

    cookies = {
        '_ga': 'GA1.2.995791224.1495549650',
        'JSESSIONID': 'DEC9134EC3F3FFA705E13D49574CA5A3',
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",#"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://beta.tocabot.io/login',#'http://10.68.15.168:8080/login',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
    }

    data = '{"email":"admin@tocabot.io","password": "CheckOUTth!spasschang#"}' #tocabot

    response = requests.post('http://10.68.15.168:8080/rpa-security-rest/v1/user/auth/login', headers=headers, cookies=cookies, data=data)

    jwttoken = response.headers['Authorization']

    # replace the headers var above to satisfy the new request.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",#"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://beta.tocabot.io/dashboard',#''http://10.68.15.168:8080/dashboard',
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer '+jwttoken,
        'X-User-Timezone': 'GMT+0100',
        'Connection': 'keep-alive',
    }

    data = '{"orderBy":{"id":"desc"},"limit":15,"page":1,"order":"id","count":0}'

    response = requests.post('http://10.68.15.168:8080/rpa-core-server-rest/v1/workflow/'+action_id+'/execute', headers=headers, cookies=cookies, data=data)

    print(response.text)


def remove_job(job_id):
    scheduler.remove_job(job_id=job_id)


def get_table():
    cookies = {
        '_ga': 'GA1.2.995791224.1495549650',
        'JSESSIONID': 'DEC9134EC3F3FFA705E13D49574CA5A3',
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",#"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://beta.tocabot.io/login',#'http://10.68.15.168:8080/login',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
    }

    data = '{"email":"admin@tocabot.io","password":"CheckOUTth!spasschang#"}'#tocabot"}'

    response = requests.post('https://beta.tocabot.io/rpa-security-rest/v1/user/auth/login', headers=headers,
                             cookies=cookies, data=data)

    jwttoken = response.headers['Authorization']

    # replace the headers var above to satisfy the new request.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",#"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://beta.tocabot.io/dashboard',#'http://10.68.15.168:8080/dashboard',
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Bearer ' + jwttoken,
        'X-User-Timezone': 'GMT+0100',
        'Connection': 'keep-alive',
    }

    data = '{"orderBy":{"id":"desc"},"limit":15,"page":1,"order":"id","count":0}'

    response = requests.post('http://10.68.15.168:8080/rpa-core-server-rest/v1/workflow/query', headers=headers,
                             cookies=cookies, data=data)

    records = json.loads(response.text)['records']

    return records
