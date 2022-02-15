import json
import os
import time
from numpy.lib.function_base import extract
from datetime import datetime
from os.path import join
from openpyxl import Workbook
wb1 = Workbook()
wb2 = Workbook()

name = "Report"
getdate = datetime.now().strftime("%m-%d-%y")

relative_path = 'C:\\Users\\pedri\\Documents\\tcc\\test-script\\'


csv_file_mob = join(relative_path, 'lighthouse_mobile_' + getdate + '.csv')
csv_file_des = join(relative_path, 'lighthouse_desktop_' + getdate + '.csv')

ws_mob = wb1.active
ws_des = wb2.active
def last_row_mob(): 
    return len(ws_mob['A'])
def last_row_des(): 
    return len(ws_des['A'])

print('----ok----')


urls = [
    "https://www.enfluencive.com/collections/tricouri-topuri-barbati/products/tricou-urban-white",
    "https://www.enfluencive.com/collections/barbati/products/trening-urban-negru-barbati",
    "https://www.enfluencive.com/collections/barbati/products/hanorac-gri-barbati",
    "https://www.enfluencive.com/collections/barbati/products/sc",
    "https://www.enfluencive.com/collections/barbati/products/bcn?variant=39289170165921",
    "https://www.enfluencive.com/collections/barbati/products/cc",
]

base = { 1: 'First Run', 2: 'Second Run', 3: 'Third Run', 4: 'Fourth Run', 5: 'Fifth Run', 6: 'Sixth Run'}

def extract_info(run, preset):
    header = [run, 'Product_Name', 'URL', 'First_Contentful_Paint', 'Speed_Index', 'Largest_Contentful_Paint', 'SEO', 'Performance', 'Best_Practices']
 
    if preset == 'desktop':     ### preset -> 2 values: 'desktop' & 'perf'(for mobile)
        last = last_row_des()+1
        working = ws_des
    else:
        last = last_row_mob()+1
        working = ws_mob

    if 'first' not in run.lower():
        last += 1

    for i, r in enumerate('ABCDEFGHI'):
        working[r+str(last)].value = header[i]

    for url in urls:
        stream = os.popen('lighthouse --chrome-flags="--headless"--disable-storage-reset="true" --preset=' + preset + ' --output=json --output-path='+relative_path + name+'_'+getdate+'.report.json ' + url)

print(extract_info(base[1], preset='perf'))
#https://medium.com/@olimpiuseulean/use-python-to-automate-google-lighthouse-reports-and-keep-a-historical-record-of-these-65f378325d64