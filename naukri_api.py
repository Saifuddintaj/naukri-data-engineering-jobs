import requests
import json
import re
import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pyodbc

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
        company = re.sub(',', '.', company)
        posted = json_response['jobDetails'][i]['footerPlaceholderLabel']
        company = re.sub(',', '.', company)
        description = json_response['jobDetails'][i]['jobDescription']
        description = remove_tags(description)
        description = re.sub(',', '.', description)
        location = json_response['jobDetails'][i]['placeholders'][2]['label']
        location = re.sub(',', '.', location)
        salary = json_response['jobDetails'][i]['placeholders'][1]['label']
        salary = re.sub(',', '', salary)
        experience = json_response['jobDetails'][i]['placeholders'][0]['label']
        experience = re.sub(',', '.', experience)
        jd_i = jobDetails(jobid, title, company, posted, description, location, salary, experience)
        jd += (jd_i.get_csv())
    return jd


def load(pages):
    output = ''
    for page in range(pages):
        data = extract(page)
        output += data
    return output


def create_dataframe(pages):
    csv = load(pages)
    columns = ["jobid", "title", "company", "posted", "description", "location", "salary", "experience"]
    df = pd.DataFrame([row.split(',') for row in csv.split('\n')], columns=columns)
    df = df.dropna()
    return df


def write_df_to_table(df):
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};Server=tcp:sqldataengineering.database.windows.net,1433;Database=naukri;Uid=dbadmin;Pwd=0p9o8i7u6yS@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    for index, row in df.iterrows():
        cursor.execute(
            "INSERT INTO dbo.jobtest (jobid,title,company,posted,description,location,salary,experience) values(?,?,?,?,?,?,?,?)",
            row.jobid, row.title, row.company, row.posted, row.description, row.location, row.salary, row.experience)
        cnxn.commit()
    cursor.close()
    return "success"