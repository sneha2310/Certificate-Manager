from pathoffile import BASE_DIR
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import mimetypes
import shutil
import regex as re
from zipfile import ZipFile
import subprocess as sp
import pandas as pd
from slack_sdk import WebClient
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from pretty_html_table import build_table
import regex as re
import os
from dotenv import load_dotenv
from datetime import timedelta,datetime
import json
# import numpy as np
# ----------------------------- loading credentials -----------------------------------------------------
load_dotenv('.env')
email_mine = os.getenv('email_mine')
password_mine = os.getenv('password_mine')
client = WebClient(token=os.getenv('token'))
channel_id = "D043GTBAVEV"
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print('email',email_mine.strip(), type(email_mine))
# print('password_mine',password_mine.strip(), type(password_mine))
# ------------------------------------------------------------------------------------------------------

def ids_func(i):
        result=client.chat_deleteScheduledMessage(
                channel=channel_id, scheduled_message_id=i)
        print(result)
    
# delete the scheduled messages 
def delete_scheduled_messages(ids):
        x = lambda b : ids.replace(b,'')
        ids=x('[')
        ids=x(']')
        ids=x("'")
        ids = (ids.split(','))
        for i in ids:
            try:
                print("..................")
                print(i.strip())
                print("----------------------------------------------------------------------")
                print(ids_func(i.strip()))
                print("----------------------------------------------------------------------")
        
            except Exception as e:
                    print(e)
        return True
    
# ---------------------------------------------------       csrgeneration      ---------------------------------------------------

# generating the required csr.
def generatefile(das_fqdn_val):
    try:
        os.chdir('./'+'das_folders/'+das_fqdn_val)
        bash_csr_value = os.system('bash csrgenerate')
        try:
            if bash_csr_value is not None:
                out = sp.getoutput('bash verify '+ das_fqdn_val+'.csr')
                try:
                    if out is not None:
                        os.system('chmod +x '+das_fqdn_val+'.csr')
                        with open('csrfile.txt','w') as file:
                            file.write(out)
                        os.chdir('../../')
                        return out
                except:
                    pass
        except:
            pass
    except:
        return False

# replace context from the csrgenerate, openssl.cnf, verify.
def replace_files(das_fqdn_val,txt):
    try:
        files=['csrgenerate','openssl.cnf']
        replace_values_x=['<<DAS FQDN>>',"""DNS.1 = das.address-palace.digivalet.in\n\nDNS.2 = dvs.address-palace.digivalet.in\n\nDNS.3 = his.address-palace.digivalet.in"""]
        replace_values_y=[das_fqdn_val, txt]
        for i in range(2):
            with open( os.path.join(os.getcwd(),'das_folders',das_fqdn_val,files[i]), 'r') as file:
                x = replace_values_x[i]
                y = replace_values_y[i]
                data = file.read()
                data = data.replace(x, y)
            with open(os.path.join(os.getcwd(),'das_folders',das_fqdn_val,files[i]), 'w') as file:
                file.write(data)
    except:
        pass

# copy the required files
def copy_files(das_fqdn_val):
    try:
        l=['csrgenerate','openssl.cnf','verify']
        for i in range(3):
            src_path = os.path.join(os.getcwd(),'files',l[i])
            dst_path = os.path.join(os.getcwd(),'das_folders',das_fqdn_val,l[i])
            shutil.copy(src_path, dst_path)
            os.system('chmod +x '+os.path.join(os.getcwd(),'das_folders',das_fqdn_val,l[i]))
    except:
        pass

def csrgenerate(csrname,txt):
    try:
        os.mkdir('das_folders/'+csrname.strip())
        copy_files(csrname) 
        replace_files(csrname,txt)
        text_of_csr = generatefile(csrname)
        return text_of_csr
    except:
        return None

# CSR generation page.
@login_required(login_url="/login/")
def index(request):
    if request.method == 'POST':
        context = dict()
        try: 
            dns1 = (request.POST.get('dns1')).strip()
            dns2 = (request.POST.get('dns2')).strip()
            dns3 = (request.POST.get('dns3')).strip()
            dns4 = (request.POST.get('dns4')).strip()
            dns5 = (request.POST.get('dns5')).strip()
            dns6 = (request.POST.get('dns6')).strip()
            dns7 = (request.POST.get('dns7')).strip()
            dns8 = (request.POST.get('dns8')).strip()                   
            dns_name = [ i for i in [dns1,dns2,dns3,dns4,dns5,dns6,dns7,dns8] if i != '' and i != None ]                                        
            flag = False
            for i in dns_name:
                if 'das' in i:                  
                    dns_name_data = i
                    flag = True
            if not flag:
                dns_name_data =dns_name[0]
            dns_openssl = [] 
            count=1
            for i in dns_name:
                dns_openssl.append(('DNS.'+str(count)+'='+i))
                count+=1            
            txt = '\n'.join(dns_openssl)
            try:
                if not os.path.isdir(os.path.join(os.getcwd(),'das_folders',dns_name_data)):                       
                        text = csrgenerate(dns_name_data,txt)  
                        print(text)                        
                        if text:                             
                            context['text'] =text                                
                            with open('temp.txt','w') as f:
                                f.write(dns_name_data)                                                             
                            data_unique = []                      
                            for i in dns_name:
                                if 'das' in i:
                                    dns_name.remove(i)
                                    data_unique.append(i)
                            for i in dns_name:
                                if i not in data_unique:
                                    data_unique.append(i)
                            data = ','.join(data_unique)                                
                            with open(os.path.join(os.getcwd() ,'das_folders' ,dns_name_data, 'all_fqdns.txt'), 'w') as f:
                                f.write(str(data))                                   
                else:                  
                    url = reverse('fileapp:indexname')
                    return HttpResponseRedirect(url)  
            except:
                pass
        except:
            print("Exception")
        context['segment'] = 'load_template'
        print(context)
        html_template = loader.get_template('home/index.html')
        return HttpResponse(html_template.render(context, request))
    return render(request,'home/index.html')  

@login_required(login_url="/login/")
def download_file(request):
    try:
        if 'temp.txt' in os.listdir():       
            with open('temp.txt') as f:
                data = (f.read()).strip()                    
            filename = data+'.csr'            
            filepath = BASE_DIR + '/das_folders/'+data+'/'+data+'.csr' 
            path = open(filepath, 'r')            
            mime_type, _ = mimetypes.guess_type(filepath)
            context = HttpResponse(path, content_type=mime_type)
            context['Content-Disposition'] = "attachment; filename=%s" % filename
            os.remove(BASE_DIR+'/temp.txt')            
            return context
        url = reverse('fileapp:indexname')
        return HttpResponseRedirect(url)   
    except FileNotFoundError as e:
        return HttpResponse('''<h1>FILE NOT FOUND.</h1>''')                          

# ---------------------------------------------------       crtgeneration      ---------------------------------------------------

@login_required(login_url="/login/")   
def error(request):
    context = {}
    msg = f'''There are some files missing in the folder.'''
    context['msg'] = msg
    html_template = loader.get_template('home/page-404.html')
    return HttpResponse(html_template.render(context, request))


# compare the server.crt and the server.key.
def checkfile(name_of_file):
    sp.call(['chmod', '-R','755', os.path.join(os.getcwd(),'das_folders',name_of_file)])
    out1 = sp.getoutput("openssl x509 -noout -modulus -in "+os.path.join(os.getcwd(),'das_folders',name_of_file,'server.crt')+ "| openssl md5")
    value1 = out1.split('=')[-1]
    out2 = sp.getoutput("openssl rsa -noout -modulus -in "+os.path.join(os.getcwd(),'das_folders',name_of_file,'server.key')+ "| openssl md5")
    value2 = out2.split('=')[-1]
    if value1 == value2:
        return value1, value2, True
    else:
        return value1, value2, False

# unzip the uploaded file.
def unzipfile(name_of_file,uploaded_file):
    try:
        sp.call(['chmod', '-R','755', os.path.join(os.getcwd(),'das_folders',name_of_file)])
        with ZipFile(os.path.join(os.getcwd(),'das_folders',name_of_file,uploaded_file.name), 'r') as f:
            f.extractall(os.path.join(os.getcwd(),'das_folders',name_of_file))                    
        crt = (uploaded_file.name.split('.')[0])                    
        if '' in crt:
            crt = crt.split()[0]
        os.rename(os.path.join(os.getcwd(),'das_folders',name_of_file,crt)+'.ca-bundle',os.path.join(os.getcwd(),'das_folders',name_of_file)+'/CA.crt')
        os.rename(os.path.join(os.getcwd(),'das_folders',name_of_file,crt)+'.crt',os.path.join(os.getcwd(),'das_folders',name_of_file)+'/server.crt')
        mod1,mod2,condition = checkfile(name_of_file)
        if condition:
            os.mkdir(os.path.join(os.getcwd(),'das_folders',name_of_file)+'/dv')
            os.system('mv '+os.path.join(os.getcwd(),'das_folders',name_of_file,'CA.crt')+' '+os.path.join(os.getcwd(),'das_folders',name_of_file,'server.crt')+' '+os.path.join(os.getcwd(),'das_folders',name_of_file,'dv'))
            os.system('cp '+os.path.join(os.getcwd(),'das_folders',name_of_file,'server.key')+' '+os.path.join(os.getcwd(),'das_folders',name_of_file,'dv'))
            os.system('cat '+os.path.join(os.getcwd(),'das_folders',name_of_file,'dv','server.crt') +' > ' +os.path.join(os.getcwd(),'das_folders',name_of_file,'dv','server.pem'))
            os.system('cat '+os.path.join(os.getcwd(),'das_folders',name_of_file,'dv','CA.crt') +' >> ' +os.path.join(os.getcwd(),'das_folders',name_of_file,'dv','server.pem'))
            os.chdir(os.path.join(os.getcwd(),'das_folders',name_of_file))
            # print("------------------------making zip file-----------------------")
            os.system(f'zip -r {name_of_file}.zip dv')
            os.chdir('../../')
            # os.system('mv '+'das_folders/'+name_of_file+'.zip '+os.path.join('das_folders',name_of_file))
            sp.call(['chmod', '-R','755', os.path.join(os.getcwd(),'das_folders',name_of_file)])
            # print("---------------------------------------------------------------")
            return mod1,mod2,True 
        else:
            return mod1,mod2,False       
    except:
        return mod1,mod2,False
    
# crtgeneration 
@login_required(login_url="/login/")
def crtgeneration(request):
    context = dict()
    context['data'] = os.listdir('das_folders')
    if request.method == 'POST':    
        folder = request.POST.get('folder',False)
        try:
            if 'deleteFolder' in request.POST:                     
                    folder = request.POST.get('folder',False)                               
                    if (os.path.isdir(BASE_DIR+'/das_folders/'+folder)):             
                        shutil.rmtree(BASE_DIR+'/das_folders/'+folder)                   
                        context['data'] = os.listdir('das_folders')                          
            if 'UploadfileSubmit' in request.POST and 'zipfileUploaded' not in  request.POST:                
                    name_of_file = request.POST['folder']      
                    try: 
                        data = os.listdir("das_folders/"+name_of_file)  
                        print(data)
                        for i in ["csrgenerate","server.key","openssl.cnf","verify",name_of_file+'.csr','all_fqdns.txt']:
                            print('Hey', i not in data,i)
                            if i not in data:                       
                                url = reverse('fileapp:error')
                                return  HttpResponseRedirect(url)                            
                        myfile = request.FILES['zipfileUploaded']
                        fs = FileSystemStorage(location='das_folders/'+name_of_file)
                        filename = myfile.name                        
                        flag = ([False for i in os.listdir("das_folders/"+name_of_file) if i==filename])                     
                        try:
                            if len(flag) == 0:          
                                fs.save(myfile.name,myfile)  
                                mod1,mod2,condition=unzipfile(name_of_file,myfile) 
                                try:                       
                                    if condition == False and mod1 != mod2:                                    
                                        req = ["csrfile","csrgenerate","server.key","openssl.cnf","verify",name_of_file+'.csr',name_of_file+'.zip','all_fqdns.txt']
                                        res = [path for path in os.listdir('das_folders/'+name_of_file) if os.path.isfile(os.path.join('das_folders',name_of_file, path))]          
                                        for i in res:
                                            if i not in req:                        
                                                os.remove(os.path.join('das_folders',name_of_file,i))
                                        msg = f'''The modulus i.e. mod1: {mod1} and mod2: {mod2} are different.'''                            
                                        context['msg'] = msg                           
                                        html_template = loader.get_template('home/page-404.html')
                                        return  HttpResponse(html_template.render(context, request))                               
                                    elif condition:                   
                                        df_header_index_col = pd.read_csv('schedule.csv', sep=',' ,names=('nameoffile','schedulers'))
                                        try:
                                            with open(os.path.join(os.getcwd(),'das_folders',name_of_file,'all_fqdns.txt'), 'r') as f:
                                                data_of_allfqdn = ((f.read().split(',')))
                                        except FileNotFoundError:
                                            print("FileNotFoundError")             
                                        for i in data_of_allfqdn:
                                            if (df_header_index_col['nameoffile'].isin([i])).any():
                                                for index, row in df_header_index_col.iterrows():                                              
                                                    if row['nameoffile'] == i:
                                                        delete_scheduled_messages(row['schedulers'])
                                                        df_header_index_col = df_header_index_col.drop(index)
                                                df_header_index_col.to_csv('schedule.csv',header=False,index=False)
                                        with open('/usr/bin/cert-url', 'r') as f:
                                                fqdn_cert = f.read().splitlines()
                                        for i in data_of_allfqdn:                                           
                                            if name_of_file not in fqdn_cert:
                                                with open('/usr/bin/cert-url','a') as f:
                                                    f.write(i+"\n")                    
                                    #    -----------------------------------------------------------------------------------------------------------------------------
                                        df = pd.read_csv(os.path.join(os.getcwd() , 'all_fqdns.txt'), sep="delimeter", header=None, names=["index"],on_bad_lines='skip', engine='python')                            
                                        with open(os.path.join(os.getcwd() ,'das_folders' ,name_of_file, 'all_fqdns.txt')) as f:
                                            df_inside_folder  = f.read()
                                        df_inside_folder = (df_inside_folder.replace('\n',''))
                                        df_inside_folder_mp = df_inside_folder.split(',')
                                        count=0
                                        for index,row in df.iterrows():
                                            df.loc[index, 'index'] =(row['index'].replace('"',""))                               
                                        for i in  df_inside_folder_mp:
                                            if not df[(df['index'].str.contains(i))].empty:                                            
                                                data =df[(df['index'].str.contains(i))].values
                                                count+=1                                  
                                        flag_for_outer_fqdns_txt = False
                                        if  count < len(df_inside_folder_mp) and count !=0:                        
                                            for index, row in df.iterrows():                                          
                                                if row['index'] == data[0][0]:
                                                    df.loc[index, 'index'] = df_inside_folder                                      
                                                    df.to_csv(os.path.join(os.getcwd() , 'all_fqdns.txt'), header=False, index=False) 
                                                    flag_for_outer_fqdns_txt = True     
                                        elif count == 0:                                        
                                                file_object = open(os.path.join(os.getcwd() , 'all_fqdns.txt'), 'a')                                          
                                                file_object.write('\n'+str(df_inside_folder))
                                                flag_for_outer_fqdns_txt = True                                  
                                                file_object.close()                             
                                        if flag_for_outer_fqdns_txt:                                                                            
                                            with open(os.path.join(os.getcwd(),'das_folders',name_of_file,'all_fqdns.txt'), 'r') as f:
                                                data_of_allfqdn = ((f.read().split(',')))
                                            with open('/usr/bin/cert-url', 'r') as f:
                                                    fqdn_cert_data = f.read().splitlines()
                                            fqdn_cert = [i.strip() for i in fqdn_cert_data]                                                                                                                               
                                            for i in data_of_allfqdn:
                                                for line in fqdn_cert:
                                                    if i.strip()in line:
                                                            fqdn_cert.remove(line)
                                            fqdn_cert.append(name_of_file)
                                            with open('/usr/bin/cert-url', 'w') as f:
                                                for i in fqdn_cert:
                                                    f.write(str(i)+'\n')
                                    #    -----------------------------------------------------------------------------------------------------------------------------                        
                                        name_fqdn = (name_of_file+'_'+(":".join([str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[0]), str((str(str('_'.join(str(datetime.now()).split())).split('.')[0]).split(':'))[1])]))+'.zip')                                 
                                        if name_fqdn in os.listdir(os.path.join(os.getcwd() , 'das_folders', name_of_file)):
                                            os.rmdir(os.path.join(os.getcwd() , 'das_folders', name_of_file))                                            
                                        os.system('zip -r '+ name_fqdn +' ./das_folders/'+name_of_file)
                                        os.system('chmod 755 '+ os.getcwd()+'/'+name_fqdn)                                                                          
                                        with open( BASE_DIR+'/tempcrt.txt','w+') as f:
                                            f.write(name_of_file)
                                        shutil.move( BASE_DIR+'/'+name_fqdn, '/tmp/') 
                                        url = reverse('fileapp:crtgeneration')
                                        return HttpResponseRedirect(url)
                                except:
                                    pass                                                                    
                            elif flag[0] == False:  
                                try:         
                                    data_of_folder = (os.listdir(os.path.join(os.getcwd(),'das_folders',name_of_file)))
                                    data = ' ,'.join(data_of_folder)                             
                                    msg = f'''The file user selected is already present. Folder contains following files:{data}.'''
                                    context['msg'] = msg
                                    html_template = loader.get_template('home/page-404.html')
                                    return  HttpResponse(html_template.render(context, request))
                                except:
                                    pass
                        except:
                            data_of_folder = (os.listdir(os.path.join(os.getcwd(),'das_folders',name_of_file)))
                            data = ' ,'.join(data_of_folder)                        
                            msg = f'''Folder contains following files:{data}.'''
                            context['msg'] = msg
                            html_template = loader.get_template('home/page-404.html')
                            return  HttpResponse(html_template.render(context, request))
                    except:
                        pass
        except FileNotFoundError:
            url = reverse('fileapp:error')
            return  HttpResponseRedirect(url)
        html_template = loader.get_template('home/crt.html')
        return  HttpResponse(html_template.render(context, request))
    if request.method == 'GET':     
        html_template = loader.get_template('home/crt.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def zipfiledown(request):
    context = dict()
    print(request.method)
    try:
        if 'tempcrt.txt' in os.listdir():        
            with open('tempcrt.txt','r') as f:
                data = f.read()        
            filename = data+'.zip'
            filepath = BASE_DIR + '/das_folders/'+data+'/'+data+'.zip'
            path = open(filepath, 'rb')
            # mime_type, _ = mimetypes.guess_type(filepath)
            context = HttpResponse(path, content_type='application/octet-stream')
            context['Content-Disposition'] = "attachment; filename=%s" % filename
            os.remove(BASE_DIR+'/tempcrt.txt')
            shutil.rmtree(BASE_DIR+'/das_folders/'+data)
            return context
        else:
            url = reverse('fileapp:crtgeneration')
            return HttpResponseRedirect(url)
    except:
        context['msg'] = 'File Not Found!!!'
        html_template = loader.get_template('home/page-404.html')
        return  HttpResponse(html_template.render(context, request))

# ---------------------------------------------------   domainentry    ---------------------------------------------------

# removing duplicate values from /etc/hosts
def removing_host(t): 
    file1 = open("/etc/hosts", "a")  # append mode
    file1.write(t+" \n")
    file1.close()
        
# domainentry
@login_required(login_url="/login/")
def domainEntry(request):
    try:
        context={}
        # -------------------------------------- /etc/hosts ---------------------------------------------------------------------------------------------
        df1 = pd.read_csv("/etc/hosts", sep="delimeter", header=None, names=["index"],on_bad_lines='skip', engine='python')
        df1['index'] = df1[df1['index'].str.contains(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', regex=True)]
        df1 = df1.dropna(subset=['index'])
        df1 = (df1['index'].str.split(n=1,expand=True))
        df1.rename(columns = {0:'IP',1:'FQDN'}, inplace = True)  # ip,fqdn
        # -------------------------------------- /usr/bin/cert-url ------------------------------------------------------------------------------------------
        df = pd.read_csv("/usr/bin/cert-url", sep="delimeter", header=None, names=["index"],on_bad_lines='skip',engine='python')  # cert-url
        df.rename(columns = {'index':'FQDN'}, inplace = True)
        # ---------------------------------------------------------------------------------------------------------------------------------------------------
        if request.method =='POST':
            IP = request.POST.get('IP')
            FQDN = request.POST.get('FQDN')    
            OldIP = request.POST.get('OldIP')
            OldFQDN = request.POST.get('OldFQDN')
            NewIP = request.POST.get('NewIP')
            NewFQDN = request.POST.get('NewFQDN')
            try:
                if IP is not None and FQDN is not None:
                    if re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',IP) and len(IP.split("."))==4 and len(FQDN)!=0:
                        if len(df1[df1["IP"].isin([IP])]) >=1:
                            data = IP.split('.')               
                            os.system(f'sed -i "/^{int(data[0])}\.{int(data[1])}\.{int(data[2])}\.{int(data[3])}/d" /etc/hosts')
                            removing_host(" ".join([IP,FQDN]))
                        else:
                            removing_host(" ".join([IP,FQDN]))         
                if OldIP is not None and OldFQDN is not None and NewIP is not None and NewFQDN is not None:     
                    if len(df1[df1["IP"].isin([OldIP])]) >=1:
                            data = OldIP.split('.')
                            os.system(f'sed -i "/^{int(data[0])}\.{int(data[1])}\.{int(data[2])}\.{int(data[3])}/d" /etc/hosts')
                            removing_host(" ".join([NewIP,NewFQDN]))            
                url = reverse('fileapp:domainentry')               
                return HttpResponseRedirect(url)
            except:
                print('Error')
                url = reverse('fileapp:domainentry')               
                return HttpResponseRedirect(url)
        data = get_data_for_entry()
        # fqdn, ip=[], []
        total_data = {}              
        for i,j in data.items():
            get_data = {}
            if len(j) != 0:
                for k in j:
                    list_of_data = []
                    for l in (df1[(df1['FQDN'].str.contains(str(k)))]['IP'].to_list()):                   
                        if l not in list_of_data:
                            list_of_data.append(l)      
                    for m in range(len(list_of_data)): 
                        if len(list_of_data) > 1:                                                         
                            list_of_data.pop(m)                
                    if len(list_of_data) !=0:
                        get_data[k] = list_of_data[0]              
                if len(get_data) != 0:
                    total_data[i] = get_data           
        context['data'] = total_data
    except:
        print('except')
    html_template = loader.get_template('home/domainentry.html')
    return HttpResponse(html_template.render(context, request))
    

# ---------------------------------------------------  entry  ---------------------------------------------------

def get_data_for_entry():
    values, file_data, data = [], [], {}
    with open('/usr/bin/cert-url','r') as f:
                values_cert = (f.readlines())    
    for i in values_cert:
        values.append(i.strip('\n'))
    with open(os.path.join(os.getcwd() , 'all_fqdns.txt'), 'r') as f: 
        file = f.readlines()
    for i in file:
        i  = (i.replace('"','').replace('\n',''))
        file_data.append(i)
    for i in values:
        flag = False
        for j in file_data:
            if i.strip() in j.strip() and i != '':    
                data[i] = j.split(',')     
                flag = True
            if flag:             
                break   
        if flag == False:
            if i !='':
               data[i] = [i]       
    return data

def entry(request):
    context = dict()
    try:        
        context['data'] = get_data_for_entry()  
    except:
        print('error')
    html_template = loader.get_template('home/entry.html')
    return HttpResponse(html_template.render(context, request))

# ---------------------------------------------------  certexpirystatus  ---------------------------------------------------

def expire_data(data):
    with open(os.path.join(os.getcwd(),'certrecord.txt'),'r') as f:
        value = f.readlines()
    fqdns, expire_data=[], []
    new_data = datetime.date(datetime.now() + timedelta(days=int(data)))
    for i in value:
            i = i.strip('\n')            
            expire_data_for_append = i.split(" ", 1)[1]            
            expire_data_for_append_split = expire_data_for_append.split()            
            next_thirty_days = datetime.strptime(expire_data_for_append_split[5]+" "+expire_data_for_append_split[2]+" "+expire_data_for_append_split[3], '%Y %b %d') 
            print(datetime.date(next_thirty_days), next_thirty_days, new_data, datetime.date(next_thirty_days) <= new_data)                       
            if datetime.date(next_thirty_days) <= new_data:
                expire_data.append(i.split(" ", 1)[1])
                fqdns.append(re.sub(':','',i.split(" ", 1)[0]))
    if len(fqdns)==0 and len(expire_data)==0:
        data = pd.DataFrame()
    else:
        gdp_dict = {'fqdns': fqdns,
                            'expire_date':expire_data}
        data = pd.DataFrame(gdp_dict)
    return data


def reportgenration(mail_id, days):
            msg = MIMEMultipart()    
             # -------------------------------------------- Mail Subject ---------------------------------------------------------- 
            msg['Subject'] = 'DIGIVALET-CERTIFICATE-MANAGER'
            value = expire_data(days)
            body_content = False
            print(value)
            if not value.empty:
                start = (f"""<html>
                            <body>
                                <strong>The report of DIGIVALET-CERTIFICATE-MANAGER within <strong>{days} days.</strong><br />
                        </body>
                        </html>""")
                output = build_table(value, 'blue_light')
                body_content = output
            else:              
                start = (f"""<html>
                            <body>
                                <strong> There are no certificates expire within <strong>{days} days.</strong><br />
                        </body>
                        </html>""")     
            msg.attach(MIMEText(start, 'html'))
            if body_content:
                msg.attach(MIMEText(body_content, "html"))
            msg_body = msg.as_string()

            # --------------------------------------------- Connection to mail-----------------------------------------------------
            smtp_port = SMTP("smtp.gmail.com", 587)
            smtp_port.ehlo()
            smtp_port.starttls()       
            smtp_port.login(email_mine , password_mine)
            address_list = mail_id
            smtp_port.sendmail(email_mine, address_list, msg_body)  
            smtp_port.quit()
            

@login_required(login_url="/login/")
def certexpirydetails(request):
    context, expander_dict  = dict(), dict()  
    if request.method =='POST':
        try:
            updateButton = request.POST.get('updateButton',False)
            if not updateButton:  
                days=[]
                mail_id = (request.POST.get('Reciever Email Address'))
                days.extend([request.POST.get('15days'),request.POST.get('30days')])
                # days.append(request.POST.get('30days'))
                if ',' in mail_id:
                    data = mail_id.split(',')
                else:
                    data = [mail_id]
                pattern = re.compile("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$")    
                try:    
                    for i in data:
                        i= i.strip()
                        if not pattern.match(i):
                            data.remove(i)
                    if len(data) != 0:
                            if None in days:
                                days.remove(None)
                            if len(days) > 1 :
                                days = '30'                    
                            else:
                                days = days[0]
                            try:
                                if days and len(data) != 0:
                                    reportgenration(data, days)
                            except:
                                print('Unmathced email id')
                    return HttpResponseRedirect('certexpirydetails')
                except:
                    print('Wrong pattern')
            elif updateButton=='Refresh':
                    print('Hey')
                    with open('/usr/bin/cert-url','r') as f:
                        values_cert = (f.readlines())
                    values_cert_url = []
                    for i in values_cert:
                        values_cert_url.append(i.strip('\n'))
                    values = []
                    for i in values_cert_url:
                        if i.strip():
                                values.append(i.strip('\n'))
                    with open(os.path.join(os.getcwd() , 'all_fqdns.txt'), 'r') as f: 
                        file = f.readlines()
                    file_data = []
                    for i in file:
                        i  = (i.replace('"','').replace('\n',''))
                        if i.strip():
                                file_data.append(i)
                    data = {}
                    for i in values:
                        flag = False
                        for j in file_data:
                            if i.strip() in j.strip() and i != '':    
                                data[i] = j.split(',')     
                                flag = True
                            if flag:             
                                break   
                        if flag == False:
                            if i !='':
                                data[i] = [i]   
                    expand = []
                    for i,j in data.items():
                        expander={}        
                        for k in j:
                            if k.endswith('in') or k.endswith('com'):                   
                                data = sp.getoutput(f'curl -vvI https://{k} 2>&1 |grep -ae "expire date:"')                       
                                if len(data) != 0:
                                    expander[k] = data.replace('*','')
                                else:
                                    expand.append(k)
                        if len(expander) != 0:
                            expander_dict[i] = expander                
                    try:
                        fqdn_file = open('fqdnfile.txt', 'w')
                        fqdn_file.write(str(expander_dict))
                        fqdn_file.close()

                    except:
                        print("Unable to write to file")

                    with open("certrecord.txt", 'w') as f: 
                        for key, value in expander_dict.items(): 
                            if type(value) == str:
                                f.write('%s:%s\n' % (key, value))
                            else:
                                for i,j in value.items():
                                    f.write('%s:%s\n' % (i, j))
                    print(expand)
                    with open("unping.txt", 'w') as f: 
                        for i in expand:
                            f.write(i+'\n')                     
                    return HttpResponseRedirect('certexpirydetails')
        except:
            print('exception')
            return HttpResponseRedirect('certexpirydetails')
    # reading the data from the file
    try:
        with open('fqdnfile.txt', 'r') as f:
            data = f.read()     
        with open('unping.txt', 'r') as f:
            data_items = f.readlines()    
        print(data)
        data = str(data).replace("'",'"')  
        expander_dict = json.loads(data)
        print(expander_dict)
        context['data_items'] = data_items
        context['expander'] = expander_dict
        html_template = loader.get_template('home/certstatus.html')
        return HttpResponse(html_template.render(context, request))
    except:
        return HttpResponseRedirect('certexpirydetails')
        

