import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.start()
SWITCH = {
    'tocabot@ri-team.com': 't0caTRIAL4r3tailinsights',
    'rich.s@blocknine.net': 't0caTRIAL4bl0ckN1NE$',
    'oliver.clinch@bizdevpros.co.uk': 't0caTRIAL4B1ZD3Vpros'
}


class CronObj(object):

    def __init__(self, action_id, scheduled, job_id, username):
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
        self.username = username
        # self.start = split_string[8]
        # self.end = split_string[9]

    def start_job(self):
        print(self.action_id)
        scheduler.add_job(
            func=scheduler_execution,
            kwargs={
                'action_id': self.action_id,
                'username': self.username
            },
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


def scheduler_execution(action_id, username):
    cookies = {
        '_ga': 'GA1.2.995791224.1495549650',
        'JSESSIONID': '7E1994BFCD899BD70BD7FC07B83DD440',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://trial.one.tocabot.io/login',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
    }

    data = '{"email": '+username+', "password": '+SWITCH.get(username)+'}'

    response = requests.post('https://trial.one.tocabot.io/rpa-security-rest/v1/user/auth/login', headers=headers,
                             cookies=cookies, data=data)

    jwttoken = response.headers['Authorization']

    # replace the headers var above to satisfy the new request.
    headers = {
        'Origin': 'https://trial.one.tocabot.io',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Authorization': 'Bearer ' + jwttoken,
        'X-User-Timezone': 'GMT+0100',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://trial.one.tocabot.io/dashboard',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Connection': 'keep-alive',
    }

    data = '{"orderBy":{"id":"desc"},"limit":15,"page":1,"order":"id","count":0}'

    response = requests.post('http://10.87.181.67:8080/rpa-core-server-rest/v1/workflow/'+action_id+'/execute', headers=headers, cookies=cookies, data=data)

    print(response.text)


def remove_job(job_id):
    scheduler.remove_job(job_id=job_id)


def get_table(username):
    cookies = {
        '_ga': 'GA1.2.995791224.1495549650',
        'JSESSIONID': '7E1994BFCD899BD70BD7FC07B83DD440',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Referer': 'https://trial.one.tocabot.io/login',
        'Content-Type': 'application/json;charset=utf-8',
        'Connection': 'keep-alive',
    }

    data = '{"email": '+username+', "password": '+SWITCH.get(username)+'}'

    response = requests.post('https://trial.one.tocabot.io/rpa-security-rest/v1/user/auth/login', headers=headers,
                             cookies=cookies, data=data)

    jwttoken = response.headers['Authorization']

    headers = {
        'Origin': 'https://trial.one.tocabot.io',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Authorization': 'Bearer ' + jwttoken,
        'X-User-Timezone': 'GMT+0100',
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://trial.one.tocabot.io/dashboard',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Connection': 'keep-alive',
    }

    data = '{"orderBy":{"id":"desc"},"limit":15,"page":1,"order":"id","count":0}'

    response = requests.post('https://trial.one.tocabot.io/rpa-core-server-rest/v1/workflow/query', headers=headers,
                             cookies=cookies, data=data)

    records = json.loads(response.text)['records']

    return records
