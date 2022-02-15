import json
import os
import pandas as pd
from datetime import datetime
import time

df = pd.DataFrame([], columns=['URL','SEO','Accessibility','Performance','Best Practices'])

name = "RocketClicks" 
getdate = datetime.now().strftime("%m-%d-%y")

urls = ["https://www.rocketclicks.com","https://www.rocketclicks.com/seo/","https://www.rocketclicks.com/ppc/"]

for url in urls:    
    stream = os.popen('lighthouse --quiet --no-update-notifier --no-enable-error-reporting --output=json --output-path='+ os.getcwd() + name+'_'+getdate+'.report.json --chrome-flags="--headless" ' + url)

time.sleep(120)
print("Report complete for: " + url)
json_filename = os.getcwd() + name + '_' + getdate + '.report.json'

with open(json_filename) as json_data:
        loaded_json = json.load(json_data)

seo = str(round(loaded_json["categories"]["seo"]["score"] * 100))
accessibility = str(round(loaded_json["categories"]["accessibility"]["score"] * 100))
performance = str(round(loaded_json["categories"]["performance"]["score"] * 100))
best_practices = str(round(loaded_json["categories"]["best-practices"]["score"] * 100))

dict = {"URL":url,"SEO":seo,"Accessibility":accessibility,"Performance":performance,"Best Practices":best_practices}
df = df.append(dict, ignore_index=True).sort_values(by='SEO', ascending=False)

df.to_csv(os.getcwd()/'lighthouse_' + name + '_' + getdate + '.csv')
print(df)