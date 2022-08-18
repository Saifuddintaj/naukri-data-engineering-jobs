from bs4 import BeautifulSoup
import requests
import json

def extract(page):
    url='https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword=data%20engineer&pageNo=1&k=data%20engineer&seoKey=data-engineer-jobs&src=jobsearchDesk&latLong='
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36','appid' : '109','systemid' : '109'}
    r = requests.get(url,headers=headers)
    json_response = json.loads(r.text)
    jobs = []
    for i in range(len(json_response['jobDetails'])):
       title = json_response['jobDetails'][i]['title']
       company =json_response['jobDetails'][i]['companyName']
       posted = json_response['jobDetails'][i]['footerPlaceholderLabel']
       description = json_response['jobDetails'][i]['jobDescription']
       location = json_response['jobDetails'][i]['placeholders'][2]['label']
       salary = json_response['jobDetails'][i]['placeholders'][1]['label']
       experience = json_response['jobDetails'][i]['placeholders'][0]['label']
       job_dict = {"company":company,"title":title,"posted_on":posted,"location":location,"salary":salary,"experience":experience,"description":description}
       jobs.append(job_dict)
    
    return jobs

print(extract(1))
