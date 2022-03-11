import requests
import json
import urllib3
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urls = ["https://docs.microsoft.com/api/contentbrowser/search/certifications?locale=fr-fr&facet=roles&facet=products&facet=levels&facet=resource_type&facet=type&%24filter=((products%2Fany(t%3A%20t%20eq%20%27azure%27)))%20and%20((resource_type%20eq%20%27examination%27))&%24orderBy=last_modified%20desc&%24top=30",
"https://docs.microsoft.com/api/contentbrowser/search/certifications?locale=fr-fr&branch=live&$skip=30&$top=30&$filter=((products%2Fany(t%3A%20t%20eq%20%27azure%27)))%20and%20((resource_type%20eq%20%27examination%27))&$orderby=last_modified%20desc"]
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "7eb64f13-6076-4c96-a5c3-d0de174b5df9"
    }
exam_info = ()
certs_list= list()
cert_lp = defaultdict(list)

for url in urls:
    response = requests.request("GET", url, headers=headers)

    results = json.loads(response.text)

    for item in results["results"]:
        for key, value in item.items():
            if key == "exams":
                exam_info = key, value
                exam_info = exam_info[1][0]
                certs_list.append(exam_info["display_name"])
            if key == "exam_display_name":
                certs_list.append(value)
print(len(certs_list))
i = 0
count_url = 0
for cert in certs_list:
    url = "https://docs.microsoft.com/fr-fr/learn/certifications/exams/" + cert
    
    response = requests.get(url)

    html = BeautifulSoup(response.text, 'html.parser')

    for tag in html.find_all("meta"):
        if tag.get("name") == "learn_item":
            i = i + 1
            cert_lp[str(i)].append(cert)
            cert_lp[str(i)].append(tag.get("content"))

df = pd.DataFrame.from_dict(cert_lp,orient='index')  

# Example of the line I used to write the result to a CSV file localy
# df.to_csv (r'C:\Users\afourdraine\HierarchyCertificationLearningPath.csv', index = True, header=False)

# Line to fill with the definitive location of the file
df.to_csv (r'<replace_here_with_storage_location>\HierarchyCertificationLearningPath.csv', index = True, header=False)