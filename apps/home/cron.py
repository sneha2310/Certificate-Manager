import logging
import os
from pathoffile import BASE_DIR      
from datetime import datetime,timedelta
from slack_sdk import WebClient
import pandas as pd
import logging
from dotenv import load_dotenv
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# BASE_DIR = '/home/snehavishwakarma/Documents/Backup@server-21March2022/argon-dashboard-django-master'
logger.info('BASE_DIR:   ',BASE_DIR)
load_dotenv(BASE_DIR+'/.env')
client = WebClient(token=os.getenv('token'))
channel_id = "D043GTBAVEV"
    
def print_hello():
    logger.info('Cron')
    
def message_scheduler(result1,fqdn,dt):
    dt = (dt.replace(hour=23, minute=59, second=59, microsecond=0))
    result = client.chat_scheduleMessage(
                    channel=channel_id,
                    text="The certificate of "+fqdn+" is expired on "+str(dt),
                    post_at=result1
                )
    id_ = result.get('scheduled_message_id')
    print('id_   ',id_)
    ids.append(id_)
            
def schedule_thirtydays(fqdn,d,dt):
    result = d + timedelta(hours=19, minutes=19, seconds=00)
    message_scheduler(result.strftime('%s'),fqdn,dt)
    
# scheduled the messages
def schedule_messages(fqdn,d,dt):
    for i in range(30):
        schedule_thirtydays(fqdn,d,dt)
        d= d+timedelta(days=1)
    df_header_index_col = pd.read_csv(BASE_DIR+'/schedule.csv', sep=',',names=('nameoffile','schedulers'))
    df_header_index_col.loc[len(df_header_index_col.index)] = [fqdn, ids ]
    df_header_index_col.to_csv(BASE_DIR+'/schedule.csv',header=False,index=False)

    
# for reading the data from which we get the dates.
with open(BASE_DIR+'/certrecord.txt') as f:
    dates_expire = []
    fqdn,out =[], []
    for i in f.readlines():
         if len(i) != 1:
            data = i.split('date:')
            data_fqdn = data[0].split(":")[0]
            fqdn.append(data_fqdn)
            print(data[-1])
            out.append(data[-1].split())
    print('out_fqdn_values: ', fqdn)
    print('OUT: ', out)
    for k in out:
        if len(k) != 0:
            dates_expire.append(datetime.strptime(k[3]+" "+k[0]+" "+k[1], '%Y %b %d').strftime('%Y-%m-%d') )
    print(dates_expire)

fqdn_dict={}
if len(fqdn) == len(dates_expire):
    for i in range(len(fqdn)):     
        fqdn_dict[fqdn[i]] = dates_expire[i]


cpr_currentdate=[]
for i in dates_expire:
    date_time_str = i
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    cpr_currentdate.append(date_time_obj- timedelta(days=30))
print('cpr_currentdate: ',cpr_currentdate)
count = 0
ids = []
for i in cpr_currentdate:
    dt = (datetime.now())  
    print(str(i)==str(dt.replace(hour=0, minute=0, second=0, microsecond=0)))
    print(i,(dt.replace(hour=0, minute=0, second=0, microsecond=0)))
    if i==(dt.replace(hour=0, minute=0, second=0, microsecond=0)):
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        print('fqdn[count]: ',fqdn,count, i,dt)
        print('fqdn: ',fqdn)
        schedule_messages(fqdn[count], i,dt)
    count+=1
    