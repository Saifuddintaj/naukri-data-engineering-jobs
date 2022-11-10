import requests
import json
import re

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


class jobDetails():
    def __init__(self, jobid, title, company, posted, location, salary, experience, description):
        self.jobid = jobid
        self.title = title
        self.company = company
        self.posted = posted
        self.location = location
        self.salary = salary
        self.experience = experience
        self.description = description

    def get_csv(self):
        csv = self.jobid + ',' + self.title + ',' + self.company + ',' + self.posted + ',' + self.location + ',' + self.salary + ',' + self.experience + ',' + self.description + '\n'
        return csv


def extract(page):
    url = f'https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword=data%engineer&pageNo={page}&k=data%engineer&seoKey=data-engineer-jobs&src=jobsearchDesk&latLong='
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'appid': '109', 'systemid': '109'}
    r = requests.get(url, headers=headers)
    json_response = json.loads(r.text)
    jd = ''
    for i in range(len(json_response['jobDetails'])):
        jobid = json_response['jobDetails'][i]['jobId']
        title = json_response['jobDetails'][i]['title']
        company = json_response['jobDetails'][i]['companyName']
        posted = json_response['jobDetails'][i]['footerPlaceholderLabel']
        description = json_response['jobDetails'][i]['jobDescription']
        description = remove_tags(description)
        description = re.sub(',', '.', description)
        location = json_response['jobDetails'][i]['placeholders'][2]['label']
        salary = json_response['jobDetails'][i]['placeholders'][1]['label']
        experience = json_response['jobDetails'][i]['placeholders'][0]['label']
        jd_i = jobDetails(jobid, title, company, posted, description, location, salary, experience)
        jd += (jd_i.get_csv())
    return jd


def load(pages):
    output = 'jobid,title,company,posted,description,location,salary,experience \n'
    for page in range(pages):
        data = extract(page)
        output += data
    return output
