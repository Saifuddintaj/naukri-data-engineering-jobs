import requests
import json
import pandas as pd

def extract(page):
    url=f'https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword=data%20engineer&pageNo={page}&k=data%20engineer&seoKey=data-engineer-jobs&src=jobsearchDesk&latLong='
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','appid' : '109','systemid' : '109'}
    r = requests.get(url,headers=headers)
    json_response = json.loads(r.text)
    title_list = []
    company_list = []
    posted_list = []
    location_list = []
    salary_list = []
    experience_list = []
    for i in range(len(json_response['jobDetails'])):
       title_list.append(json_response['jobDetails'][i]['title'])
       company_list.append(json_response['jobDetails'][i]['companyName'])
       posted_list.append(json_response['jobDetails'][i]['footerPlaceholderLabel'])
       #description = json_response['jobDetails'][i]['jobDescription']
       location_list.append(json_response['jobDetails'][i]['placeholders'][2]['label'])
       salary_list.append(json_response['jobDetails'][i]['placeholders'][1]['label'])
       experience_list.append(json_response['jobDetails'][i]['placeholders'][0]['label'])
    
    job_dict = {"company":company_list,"title":title_list,"posted_on":posted_list,"location":location_list,"salary":salary_list,"experience":experience_list}
    
    return job_dict


def transform(pages):
    df = pd.DataFrame()
    for i in range(pages):
        jobs_dict = extract(i)
        df_jobs = pd.DataFrame(jobs_dict)
        df = df.append(df_jobs,ignore_index=True)
    return df

def load_data(path,number_of_pages):
    df = transform(number_of_pages)
    df.to_csv(path)


load_data(r'C:\Users\saifuddin\Desktop\jobs.csv',15)
