from scrap import ScrapBlogs
import re
import requests
from bs4 import BeautifulSoup
from deta import Deta, app
from dotenv import load_dotenv, find_dotenv
import io
import os
import datetime

load_dotenv(find_dotenv())


urls = os.environ.get("URL")
project_key = os.environ.get("PROJECTKEY")
current_date = datetime.datetime.now()
folder_date=current_date.strftime("%x")
new_folder_date=folder_date.replace("/", "_")


deta = Deta(project_key)
urls = ScrapBlogs(urls)

folder_name = f"mediumblogs{new_folder_date}"
drive = deta.Drive(folder_name)



@app.lib.run(action="blogs")
@app.lib.cron()
def blogs_scrap(event):

    try:

        for url in urls:

            scrap_url = f"https://medium.com{url}"
            find_name=re.findall('\w+', url)
            name_list=[]
            for x in find_name:
                if x.isalpha():
                    name_list.append(x)

            file_name="_".join(name_list)

            response = requests.get(scrap_url).text.encode('utf8').decode('ascii', 'ignore')
            soup = BeautifulSoup(response, 'html.parser')
            find_section = soup.find("section")
            if find_section is None:
                continue
            else:
                with io.StringIO() as f:
                    f.write(f"{scrap_url}")
                    f.write("\n")
                    f.write(str(find_section))

                    drive.put(f"{file_name}.md", f.getvalue())

        return "Scrapped Successfully"


    except Exception as e:
        print(e)