import pandas as pd
import re
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import json
import time
import pickle
import glob
from shutil import copyfile


class FastReports():

    filepath_tasks=r"C:\Users\016434613\Downloads\progress_dt_tasks_details_report.xlsx"
    filepath_master=r"C:\Users\016434613\Downloads\progress_dt_tasks_master_report.xlsx"
    filepath_ideas=r"C:\Users\016434613\Downloads\progress_sd_tasks_master_report.xlsx"
    filepath_spec=r"C:\Users\016434613\Desktop\Specification.xlsx"
    download_master_box=r"C:\Users\016434613\Box\MASTER REPORT\Master Report 2022 4Q"
    spec_completed=False
    quarter='3Q22'

    def download_tasks(self):
        checkfilepath = self.filepath_tasks
        exists = False

        # This sentence takes care of deleting old tasks report on downloads folder
        if os.path.exists(checkfilepath):
            subprocess.run("del /f C:\\Users\\016434613\\Downloads\\progress_dt_tasks_details_report.xlsx", shell=True, capture_output=True)

        try:
        # Creating the driver conection to handle automatic session with Selenium
            mydriver = webdriver.Chrome(r"C:\Users\016434613\Dev\Reports\chromedriver.exe")
        except:
            print("Update chrome driver version")

        try:
        # automatically opening the above created session with the link in between parenthesis
            mydriver.get("https://progress.us1a.cirrus.ibm.com/api/rpt/dt/1600277460000/ms/jas8n38daai/1/1600431650693")
        except:
            print("Timeout, network issues, try again later.")

        # check if the path of file exists in the directory to make sure file was actually downloaded
        while not exists:
            time.sleep(1)
            exists = os.path.exists(checkfilepath)

        # Close the session driver when the file was downloaded 
        mydriver.close()

    def backlogsub(self):
        '''This function creates the backlog report on a spreadsheet. It uses pandas functions to rename columns, 
        subtract not needed data/columns and filter the information. Also it modifies the date on certified field keeping only Month Year.
        Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
        filepath_ = self.filepath_tasks
        df_Back = pd.read_excel(filepath_,sheet_name="Tasks")
        df_Back = df_Back.rename(columns={'DSL/SUPERVISOR (NAME)':'DSL','ROBOT NUMBER':'ROBOT_NUMBER','AUTOMATION TYPE':'AUTOMATION_TYPE','MANUAL EXECUTION DURATION (hours per year)':'SAVING HS'})
        df_Back = df_Back.loc[:,['TASK ID','CERTIFIED','DSL','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION_TYPE','REGIONS','SAVING HS']]
        df_Back = df_Back.loc[df_Back['STATUS']=="Ready for development"]
        df_Back['CERTIFIED'] = df_Back['CERTIFIED'].apply(lambda x: str(x))
        df_Back['CERTIFIED'] = df_Back['CERTIFIED'].apply(lambda x: x[4:7]+" "+x[11:15])
        df_Back = df_Back.loc[df_Back['ROBOT_NUMBER'].isnull()==True]
        df_Back.drop(columns=['ROBOT_NUMBER','STATUS'],inplace=True)
        df_Back['Count']=1
        df_Back.to_excel(r"C:\Users\016434613\Desktop\Backlog.xlsx", index=False)

    #df_Back

    def specsub(self):
        '''This function creates the specification report on a spreadsheet. It uses pandas functions to rename columns, 
        subtract not needed data/columns and filter the information. Also it modifies the date on certified field keeping only Month Year.
        Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
        filepath_ = self.filepath_tasks
        df_Spec  = pd.read_excel(filepath_,sheet_name="Tasks")
        df_Spec = df_Spec.rename(columns={'DSL/SUPERVISOR (NAME)':'DSL','DSL/SUPERVISOR (EMAIL)':'DSL EMAIL','ROBOT NUMBER':'ROBOT_NUMBER','AUTOMATION TYPE':'AUTOMATION_TYPE',
                'MANUAL EXECUTION DURATION (hours per year)':'SAVING HS','LOCATIONS OF MANUAL EXECUTION':'LOCATIONS'})
        df_Spec = df_Spec.loc[:,['TASK ID','CERTIFIED','DSL','DSL EMAIL','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION_TYPE','LOCATIONS','SAVING HS']]
        df_Spec = df_Spec.loc[df_Spec['STATUS']=="Specification"]
        df_Spec['CERTIFIED'] = df_Spec['CERTIFIED'].apply(lambda x: str(x))
        df_Spec['CERTIFIED'] = df_Spec['CERTIFIED'].apply(lambda x: x[4:7]+" "+x[11:15])
        df_Spec.loc[df_Spec['CERTIFIED']=='fin ','CERTIFIED']=""
        df_Spec = df_Spec.loc[df_Spec['ROBOT_NUMBER'].isnull()==True]
        df_Spec.drop(columns=['ROBOT_NUMBER','STATUS'],inplace=True)
        df_Spec['Count']=1
        df_Spec.to_excel(r"C:\Users\016434613\Desktop\Specification.xlsx", index=False)



    def validsub(self):
        '''This function creates the validation report on a spreadsheet. It uses pandas functions to rename columns, 
        subtract not needed data/columns and filter the information. Also it modifies the date on certified field keeping only Month Year.
        Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
        filepath_age= self.filepath_master
        df_Val = pd.read_excel(filepath_age,sheet_name="Versions")
        df_Val = df_Val.rename(columns={'CREATED BY (NAME)':'DSL','CREATED BY (EMAIL)':'DSL EMAIL','ROBOT NUMBER':'ROBOT_NUMBER','AUTOMATION TYPE':'AUTOMATION_TYPE',
                        'MANUAL EXECUTION DURATION (hours per year)':'SAVING HS','LOCATIONS OF MANUAL EXECUTION':'LOCATIONS'})
        df_Val = df_Val.loc[:,['VERSION ID','DSL','DSL EMAIL','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION_TYPE','LOCATIONS','SAVING HS']]
        df_Val = df_Val.loc[df_Val['STATUS']=="Validation"]
        df_Val = df_Val.loc[df_Val['ROBOT_NUMBER'].isnull()==True]
        df_Val.drop(columns=['ROBOT_NUMBER','STATUS'],inplace=True)
        df_appr = pd.read_excel(filepath_age,sheet_name="Approvals")
        df_appr = df_appr.loc[:,['VERSION ID','STATUS','REQUESTED']]
        df_Val = df_Val.merge(df_appr, on="VERSION ID", how="left")
        df_Val = df_Val.sort_values(by="REQUESTED",ascending=False)
        df_Val.drop_duplicates('VERSION ID', inplace=True)
        df_Val.reset_index(inplace=True, drop=True)
        df_Val['REQUESTED'] = df_Val['REQUESTED'].apply(lambda x: str(x))
        df_Val['REQUESTED'] = df_Val['REQUESTED'].apply(lambda x: x[8:10]+"/"+x[5:7]+"/"+x[0:4])

#        months = {"Dec":"12","Nov":"11","Oct":"10",
#        "Sep":"09","Aug":"08","Jul":"07","Jun":"06","May":"05",
#        "Apr":"04","Mar":"03","Feb":"02","Jan":"01"}

#        for i in range(df_Val['REQUESTED'].size):
#            fecha=df_Val['REQUESTED'][i]
#            m = fecha[3:6]
#            new_mes = fecha[0:3]+months[m]+fecha[6:12]
#            df_Val['REQUESTED'][i]=new_mes

        df_Val['Count']=1
        df_Val.to_excel(r"C:\Users\016434613\Desktop\Validation.xlsx", index=False)


    def changesub(self):
        '''This function creates the changes report and the changes_ report on different spreadsheets. It uses pandas functions to rename columns, 
        subtract not needed data/columns and filter the information and customize some fields.
        This function is also using the regular expresion library to find out if a 
        value from a certain list of keywords is found on the changes summary field on the report, if that is the case it highlights it by
        changing the actual value of the field and additionaly adding a 1 to a new column called prob_poor_desing if there is no keyword find it adds a 0
        instead.
        Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
        filepath_ = self.filepath_tasks
        df_chg = pd.read_excel(filepath_,sheet_name="Tasks")
        df_chg = df_chg.rename(columns={'DSL/SUPERVISOR (NAME)':'DSL','DSL/SUPERVISOR (EMAIL)':'DSL EMAIL','ROBOT NUMBER':'ROBOT_NUMBER',
                                        'AUTOMATION TYPE':'AUTOMATION_TYPE','MANUAL EXECUTION DURATION (hours per year)':'SAVING HS',
                                       'LOCATIONS OF MANUAL EXECUTION':'LOCATIONS'})
        df_chg = df_chg.loc[:,['TASK ID','ROBOT VERSION','CHANGE SUMMARY','DSL','DSL EMAIL','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION_TYPE','REGIONS','LOCATIONS','SAVING HS']]
        df_chg = df_chg.loc[df_chg['STATUS']=="In Production"]
        df_chg = df_chg.loc[df_chg['ROBOT VERSION']>1]
        df_chg.drop(columns=['STATUS','ROBOT VERSION'],inplace=True)
        df_chg.to_excel(r"C:\Users\016434613\Desktop\Reports\Changes.xlsx", index=False)

        df_chg2 = pd.read_excel(r"C:\Users\016434613\Desktop\Reports\Changes.xlsx",sheet_name="Sheet1")
        key_words = ['SQL','sql','countries','minor','country codes','company','query','queries','Query','Maj',
                     'condition','CTY',' LC ','combination','maj','Minor','smin','cty','lc','query','Country','entity','entities',
                    'DIV','Div']
        df_chg2['PROB_POOR_DESIGN']=""
        for i in range(df_chg2['CHANGE SUMMARY'].size):
            for w in key_words:
                x=re.search(w,df_chg2['CHANGE SUMMARY'][i])
                replacement= " -| " + w + " |- "
                valor = df_chg2['CHANGE SUMMARY'][i]
                text = re.sub(w,replacement,valor,flags=re.I)
                if x is not None:
                    df_chg2.loc[df_chg2['CHANGE SUMMARY']==valor,'PROB_POOR_DESIGN']=1
                    df_chg2['CHANGE SUMMARY'][i]=text
                    break
                else:
                    df_chg2.loc[df_chg2['CHANGE SUMMARY']==valor,'PROB_POOR_DESIGN']=0
        df_chg2['CHANGE SUMMARY'] = df_chg2['CHANGE SUMMARY'].apply(lambda x: x[:100]+"...")
        df_chg2['Count']=1
        df_chg2.to_excel(r"C:\Users\016434613\Desktop\Changes_.xlsx", index=False)

    def mgr_report(self):
        mgrserials = ['016434613','A01130693','A51733693','900688897']
        mgrname = {'016434613':'Martin Campos','A01130693':'Marek Tarkos','A51733693':'Andrej Csiaki','900688897':'Melissa Bledsoe'}
        devnames = {}
        for mgr in mgrserials:
            req = requests.get("https://unified-profile-api.us-south-k8s.intranet.ibm.com/v3/profiles/" + mgr + "/teamResolved")
            dictdatos = req.json()
            devlist = dictdatos['content']['functional']['reports']
            for dev in devlist:
                devnames.setdefault(mgrname[mgr], []).append(dev['nameDisplay'])
                
        ### Create Lists ###
        devlistmc = devnames['Martin Campos']
        devlistmt = devnames['Marek Tarkos']
        devlistac = devnames['Andrej Csiaki']
        devlistmb = devnames['Melissa Bledsoe']

        ### Create 2 dimension df, 1 column with the list, second column value fixed de Mgr ###
        df6 = pd.DataFrame(devlistmc, columns=['DEVELOPERS'])
        df6.loc[df6['DEVELOPERS']=="Pablo (Paul) Iacovone",'DEVELOPERS']="Pablo Ariel Iacovone"
        df6.loc[df6['DEVELOPERS']=="Santiago Akira Kitashima",'DEVELOPERS']="Santiago Kitashima"
        df6.loc[df6['DEVELOPERS']=="Ezequiel Ricardo Ferlauto",'DEVELOPERS']="Ezequiel Ferlauto"
        df6['Manager'] = "Martin Campos"

        df7 = pd.DataFrame(devlistmt, columns=['DEVELOPERS'])
        df7.loc[df7['DEVELOPERS']=="Lubomir Cmiko (Lubo)",'DEVELOPERS']="Lubo Čmiko"
        df7['Manager'] = "Marek Tarkos"

        df8 = pd.DataFrame(devlistac, columns=['DEVELOPERS'])
        df8.loc[df8['DEVELOPERS']=="Andre Daniel Rodrigues",'DEVELOPERS']="Andre Rodrigues"
        df8['Manager'] = "Andrej Csiaki"

        df9 = pd.DataFrame(devlistmb, columns=['DEVELOPERS'])
        df9.loc[df9['DEVELOPERS']=="Nuno Macedo Gomes",'DEVELOPERS']="Nuno Filipe Macedo Gomes"
        df9['Manager'] = "Melissa Bledsoe"


        ### Append results into one df - df10 ####
        df10 = df6
        df10 = df10.append(df7)
        df10 = df10.append(df8)
        df10 = df10.append(df9)

        return df10


    def download_master(self):
        checkfilepath = self.filepath_master
        exists = False

        # This sentence takes care of deleting old mater report on downloads folder
        if os.path.exists(checkfilepath):
            subprocess.run("del /f C:\\Users\\016434613\\Downloads\\progress_dt_tasks_master_report.xlsx", shell=True, capture_output=True)
        try:
            mydriver = webdriver.Chrome("chromedriver.exe")
        except:
            print("Update chrome dirver version")
        try:
            mydriver.get("https://progress.us1a.cirrus.ibm.com/api/rpt/mst/1588760663192/lf/bd3hd8xaj/0/1588760727599")
        except:
            print("timeout, networking issues, try again later.")
            mydriver.close()
        while not exists:
            time.sleep(1)
            exists = os.path.exists(checkfilepath)
        mydriver.close()

    def download_master_2(self):
        checkfilepath = self.filepath_master
        download_master_box = self.download_master_box
        

        # This sentence takes care of deleting old mater report on downloads folder
        if os.path.exists(checkfilepath):
            subprocess.run("del /f C:\\Users\\016434613\\Downloads\\progress_dt_tasks_master_report.xlsx", shell=True, capture_output=True)

        all_files = glob.glob(download_master_box+"\\*.xlsx")
        all_files = sorted(all_files, reverse=True)
        
        copyfile(all_files[0],r'C:\Users\016434613\Downloads\progress_dt_tasks_master_report.xlsx')


    def delivery_report(self):
        filepath_ = self.filepath_tasks
        quarter = self.quarter

        df = pd.read_excel(filepath_,sheet_name="Tasks")
        df = df.rename(columns={'ROBOT NUMBER':'ROBOT_NUMBER'})

        df_lindo = df.loc[:,['ORIGIN RELEASE','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION TYPE','REGIONS','MANUAL EXECUTION DURATION (hours per year)','CURRENT VERSION ID']]
        df_lindo = df_lindo.rename(columns={'MANUAL EXECUTION DURATION (hours per year)':'SAVING HS','CURRENT VERSION ID':'VERSION ID'})

        df4 = df_lindo
        df4['ORIGIN RELEASE'] = df4['ORIGIN RELEASE'].apply(lambda x: str(x))
        df4['QUARTER'] = df4['ORIGIN RELEASE'].apply(lambda x: x[4:7]+x[11:15])

        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '1Q21' if x == 'Mar2021' else '1Q21' if x == 'Feb2021' else '1Q21' if x == 'Jan2021' else x)
        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '2Q21' if x == 'Jun2021' else '2Q21' if x == 'May2021' else '2Q21' if x == 'Apr2021' else x)
        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '3Q21' if x == 'Sep2021' else '3Q21' if x == 'Aug2021' else '3Q21' if x == 'Jul2021' else x)
        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '4Q21' if x == 'Dec2021' else '4Q21' if x == 'Nov2021' else '4Q21' if x == 'Oct2021' else x)
        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '1Q22' if x == 'Jan2022' else '1Q22' if x == 'Feb2022' else '1Q22' if x == 'Mar2022' else x)
        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '2Q22' if x == 'Jun2022' else '2Q22' if x == 'May2022' else '2Q22' if x == 'Apr2022' else x)
        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '3Q22' if x == 'Sep2022' else '3Q22' if x == 'Aug2022' else '3Q22' if x == 'Jul2022' else x)
        df4['QUARTER'] = df4['QUARTER'].apply(lambda x: '4Q22' if x == 'Dec2022' else '4Q22' if x == 'Nov2022' else '4Q22' if x == 'Oct2022' else x)

        df5 = df4.loc[df4['QUARTER']==quarter,]
        df5.drop(columns=["ORIGIN RELEASE"],inplace=True)

        filepath_ = self.filepath_master

        df_Development = pd.read_excel(filepath_,sheet_name="Development (Iterations)")

        df_Development = df_Development.loc[:,['VERSION ID','DEVELOPERS']]
        df_Development.drop_duplicates('VERSION ID',inplace=True)

        df_Development.reset_index(inplace=True, drop=True)

        df5 = df5.merge(df_Development, on="VERSION ID", how="left")

        df5.loc[df5['VERSION ID']=='6329f38e3d3f2f2ee3ebc99e','DEVELOPERS']='Dario Cesar Atach'
        df5.loc[df5['VERSION ID']=='633549dbaec8d48dde23dff8','DEVELOPERS']='Marián Chrást'
        df5.loc[df5['VERSION ID']=='633823c7ffd0c408ad843990','DEVELOPERS']='Branislav Podoba'
        df5.loc[df5['ROBOT_NUMBER']=='ATA053','DEVELOPERS']='Milan Babčanec'
        df5.loc[df5['ROBOT_NUMBER']=='ATA712','DEVELOPERS']='Richard Hantke'
        df5.loc[df5['ROBOT_NUMBER']=='WBA012','DEVELOPERS']='Rodrigo Maximiliano Cremella'
        

        pos = []
        valor = []
        cont=0

        for i in range(df5['DEVELOPERS'].size):
            x=re.search(",",df5['DEVELOPERS'][i])
            if x is not None:
                valor.append(df5['DEVELOPERS'][i])
                Devel = valor[cont].split(",")
                df5['DEVELOPERS'][i]=Devel[0]
                pos.append(i)
                cont+=1

        df10 = self.mgr_report()

        df5 = df5.merge(df10, on="DEVELOPERS", how="left")

        for t in range(len(pos)):
            df5['DEVELOPERS'][pos[t]]=valor[t]

        df5.loc[df5['DEVELOPERS']=="Andre Daniel Rodrigues",'Manager']="Andrej Csiaki"
        df5.loc[df5['DEVELOPERS']=="Martin Nicolas Benitez Alegre",'Manager']="Martin Campos"
        df5.loc[df5['DEVELOPERS']=="Tomas Funes",'Manager']="Martin Campos"
        df5.loc[df5['ROBOT_NUMBER']=="ODA139",'DEVELOPERS']="Ezequiel Ferlauto"
        df5.loc[df5['ROBOT_NUMBER']=="ODA149",'DEVELOPERS']="Ezequiel Ferlauto"
        df5.loc[df5['ROBOT_NUMBER']=="ODA146",'DEVELOPERS']="Ezequiel Ferlauto"
        df5.loc[df5['ROBOT_NUMBER']=="ODA147",'DEVELOPERS']="Ezequiel Ferlauto"
        df5.loc[df5['ROBOT_NUMBER']=="ODA144",'DEVELOPERS']="Ezequiel Ferlauto"
        df5.loc[df5['ROBOT_NUMBER']=="ODA143",'DEVELOPERS']="Bruno Secchiari"
        df5.loc[df5['ROBOT_NUMBER']=="ODA111",'DEVELOPERS']="Bruno Secchiari"
        df5.loc[df5['ROBOT_NUMBER']=="ODA178",'DEVELOPERS']="Bruno Secchiari"
        df5.loc[df5['ROBOT_NUMBER']=="ODA181",'DEVELOPERS']="Bruno Secchiari"

        df5['Count']=1
                
        df5 = df5.loc[:,['Manager','DEVELOPERS','Count','SAVING HS','QUARTER','ROBOT_NUMBER','TITLE','STATUS','AUTOMATION TYPE','REGIONS']]
        df5 = df5.rename(columns={'DEVELOPERS':'Developer'})
        df5.to_excel(r"C:\Users\016434613\Desktop\Delivery Report.xlsx", index=False)

    def dev_over90(self):
        filepath_ = self.filepath_master

        df_Versions = pd.read_excel(filepath_,sheet_name="Versions")

        df_Versions = df_Versions.loc[:,['VERSION ID','TASK ID','TASK VERSION (NUMBER)','STATUS','ROBOT NUMBER','TITLE','AUTOMATION TYPE','LOCATIONS OF MANUAL EXECUTION','READY FOR DEVELOPMENT']]
        df_Versions = df_Versions.rename(columns={'LOCATIONS OF MANUAL EXECUTION':'LOCATIONS'})
        df_Versions = df_Versions.loc[df_Versions['TASK VERSION (NUMBER)']==1]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="Discarded"]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="Sunset"]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="Closed"]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="In Production"]
        #df_Versions = df_Versions.loc[df_Versions['READY FOR DEVELOPMENT'].notnull()]
        df_Versions['READY FOR DEVELOPMENT'] = df_Versions['READY FOR DEVELOPMENT'].apply(lambda x: str(x))
        df_Versions['READY FOR DEVELOPMENT'] = df_Versions['READY FOR DEVELOPMENT'].apply(lambda x: x[8:10]+"/"+x[5:7]+"/"+x[0:4])

        df_Versions.fillna(value="?",inplace=True)

        df_Versions.reset_index(inplace=True, drop=True)
        #df_Versions

#        months = {"Dec":"12","Nov":"11","Oct":"10",
#        "Sep":"09","Aug":"08","Jul":"07","Jun":"06","May":"05",
#        "Apr":"04","Mar":"03","Feb":"02","Jan":"01"}


#        for i in range(df_Versions['READY FOR DEVELOPMENT'].size):
#            x = df_Versions['READY FOR DEVELOPMENT'][i]
#            m = x[3:6]
#            if m != "":
#                s = x[0:3]+months[m]+x[6:12]
#            else:
#                s = ""
#            df_Versions['READY FOR DEVELOPMENT'][i]=s


        df_Development = pd.read_excel(filepath_,sheet_name="Development (Iterations)")

        df_Development = df_Development.loc[:,['VERSION ID','STATUS','DEVELOPERS','STARTED','COMPLETED']]
        df_Development = df_Development.loc[df_Development['STATUS']!="Discarded"]
        df_Development = df_Development.loc[df_Development['STATUS']!="Sunset"]
        df_Development = df_Development.loc[df_Development['STATUS']!="Closed"]
        df_Development = df_Development.loc[df_Development['STATUS']!="In Production"]

        df_Development['STARTED'] = df_Development['STARTED'].apply(lambda x: str(x))
        df_Development['STARTED'] = df_Development['STARTED'].apply(lambda x: x[8:10]+"/"+x[5:7]+"/"+x[0:4])

        df_Development = df_Development.loc[:,['VERSION ID','DEVELOPERS','STARTED']]

        df_Development.fillna(value="?",inplace=True)

        df_Development.reset_index(inplace=True, drop=True)

#        for i in range(df_Development['STARTED'].size):
#            x = df_Development['STARTED'][i]
#            m = x[3:6]
#            s = x[0:3]+months[m]+x[6:12]
#            df_Development['STARTED'][i]=s


        df_Merge = df_Versions.merge(df_Development, on="VERSION ID", how="left")
        #df_Merge.drop(columns=['index_x','index_y'],inplace=True)
        df_Merge.dropna(inplace=True)

        df_Merge.reset_index(inplace=True, drop=True)
        #df_Merge.drop(columns=['index'],inplace=True)

        from datetime import datetime
        p = datetime.today().strftime('%d/%m/%Y')
        t = datetime.strptime(p, '%d/%m/%Y')

        valor = []
        for i in range(df_Merge['STARTED'].size):
            d1 = datetime.strptime(df_Merge['STARTED'][i],'%d/%m/%Y')
            dif = t - d1
            difD = dif.days
            valor.append(difD)

        df_Merge['DAYS']=valor
        df_Merge = df_Merge.loc[df_Merge['DAYS']>90]
        df_Merge.drop_duplicates('VERSION ID', inplace=True)

        df_Merge.reset_index(inplace=True, drop=True)

        df10 = self.mgr_report()

        pos = []
        valor = []
        cont=0

        #df_Merge['DEVELOPERS']
        for i in range(df_Merge['DEVELOPERS'].size):
            x=re.search(",",df_Merge['DEVELOPERS'][i])
            if x is not None:
                valor.append(df_Merge['DEVELOPERS'][i])
                Devel = valor[cont].split(",")
                df_Merge['DEVELOPERS'][i]=Devel[0]
                pos.append(i)
                cont+=1

        df_Merge = df_Merge.merge(df10, on="DEVELOPERS", how="left")

        for t in range(len(pos)):
            df_Merge['DEVELOPERS'][pos[t]]=valor[t]

        df_Merge['Count']=1
        df_Merge.loc[df_Merge['DEVELOPERS']=="Tomas Funes",'Manager']="Martin Campos"
        df_Merge.loc[df_Merge['DEVELOPERS']=="Andre Daniel Rodrigues",'Manager']="Andrej Csiaki"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA128",'DEVELOPERS']="Ezequiel Ferlauto"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA111",'DEVELOPERS']="Bruno Secchiari"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA140",'DEVELOPERS']="Ezequiel Ferlauto"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA137",'DEVELOPERS']="Ezequiel Ferlauto"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA146",'DEVELOPERS']="Ezequiel Ferlauto"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA135",'DEVELOPERS']="Ezequiel Ferlauto"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA147",'DEVELOPERS']="Ezequiel Ferlauto"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA144",'DEVELOPERS']="Ezequiel Ferlauto"
        df_Merge.loc[df_Merge['ROBOT NUMBER']=="ODA143",'DEVELOPERS']="Bruno Secchiari"
        df_Merge.loc[df_Merge['DEVELOPERS']=="Santiago Kitashima",'Manager']="Martin Campos"
        df_Merge.loc[df_Merge['DEVELOPERS']=="Maria Laura Bisaccia",'Manager']="Martin Campos"
        df_Merge.loc[df_Merge['DEVELOPERS']=="Ezequiel Ferlauto",'Manager']="Martin Campos"
        df_Merge.loc[df_Merge['DEVELOPERS']=="Bruno Secchiari",'Manager']="Martin Campos"
        df_Merge.loc[df_Merge['DEVELOPERS']=="Michele Lobina, Richard Nerodolík",'Manager']="Andrej Csiaki"

        df_Merge.to_excel(r"C:\Users\016434613\Desktop\dev over90.xlsx", index=False)

    def chg_over30(self):
        filepath_ = self.filepath_master

        df_Versions = pd.read_excel(filepath_,sheet_name="Versions")

        df_Versions = df_Versions.loc[:,['VERSION ID','TASK ID','TASK VERSION (NUMBER)','STATUS','ROBOT NUMBER','TITLE','AUTOMATION TYPE','LOCATIONS OF MANUAL EXECUTION','READY FOR DEVELOPMENT']]
        df_Versions = df_Versions.rename(columns={'LOCATIONS OF MANUAL EXECUTION':'LOCATIONS'})
        df_Versions = df_Versions.loc[df_Versions['TASK VERSION (NUMBER)']>1]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="Discarded"]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="Sunset"]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="Closed"]
        df_Versions = df_Versions.loc[df_Versions['STATUS']!="In Production"]
        #df_Versions = df_Versions.loc[df_Versions['READY FOR DEVELOPMENT'].notnull()]
        df_Versions['READY FOR DEVELOPMENT'] = df_Versions['READY FOR DEVELOPMENT'].apply(lambda x: str(x))
        df_Versions['READY FOR DEVELOPMENT'] = df_Versions['READY FOR DEVELOPMENT'].apply(lambda x: x[8:10]+"/"+x[5:7]+"/"+x[0:4])

        df_Versions.fillna(value="?",inplace=True)

        df_Versions.reset_index(inplace=True, drop=True)

#        months = {"Dec":"12","Nov":"11","Oct":"10",
#        "Sep":"09","Aug":"08","Jul":"07","Jun":"06","May":"05",
#        "Apr":"04","Mar":"03","Feb":"02","Jan":"01"}

#        for i in range(df_Versions['READY FOR DEVELOPMENT'].size):
#            x = df_Versions['READY FOR DEVELOPMENT'][i]
#            m = x[3:6]
#            if m != "":
#                s = x[0:3]+months[m]+x[6:12]
#            else:
#                s = ""
#            df_Versions['READY FOR DEVELOPMENT'][i]=s


        df_Development = pd.read_excel(filepath_,sheet_name="Development (Iterations)")

        df_Development = df_Development.loc[:,['VERSION ID','STATUS','DEVELOPERS','STARTED','COMPLETED']]
        df_Development = df_Development.loc[df_Development['STATUS']!="Discarded"]
        df_Development = df_Development.loc[df_Development['STATUS']!="Sunset"]
        df_Development = df_Development.loc[df_Development['STATUS']!="Closed"]
        df_Development = df_Development.loc[df_Development['STATUS']!="In Production"]

        df_Development['STARTED'] = df_Development['STARTED'].apply(lambda x: str(x))
        df_Development['STARTED'] = df_Development['STARTED'].apply(lambda x: x[8:10]+"/"+x[5:7]+"/"+x[0:4])

        df_Development = df_Development.loc[:,['VERSION ID','DEVELOPERS','STARTED']]

        df_Development.fillna(value="?",inplace=True)

        df_Development.reset_index(inplace=True, drop=True)

#        for i in range(df_Development['STARTED'].size):
#            x = df_Development['STARTED'][i]
#            m = x[3:6]
#            s = x[0:3]+months[m]+x[6:12]
#            df_Development['STARTED'][i]=s


        df_Merge = df_Versions.merge(df_Development, on="VERSION ID", how="left")
        df_Merge.dropna(inplace=True)

        df_Merge.reset_index(inplace=True, drop=True)

        from datetime import datetime
        p = datetime.today().strftime('%d/%m/%Y')
        t = datetime.strptime(p, '%d/%m/%Y')

        valor = []
        for i in range(df_Merge['STARTED'].size):
            d1 = datetime.strptime(df_Merge['STARTED'][i],'%d/%m/%Y')
            dif = t - d1
            difD = dif.days
            valor.append(difD)

        df_Merge['DAYS']=valor
        df_Merge = df_Merge.loc[df_Merge['DAYS']>30]
        df_Merge.drop_duplicates('VERSION ID', inplace=True)

        df_Merge.reset_index(inplace=True, drop=True)

        df10 = self.mgr_report()

        pos = []
        valor = []
        cont=0

        for i in range(df_Merge['DEVELOPERS'].size):
            x=re.search(",",df_Merge['DEVELOPERS'][i])
            if x is not None:
                valor.append(df_Merge['DEVELOPERS'][i])
                Devel = valor[cont].split(",")
                df_Merge['DEVELOPERS'][i]=Devel[0]
                pos.append(i)
                cont+=1

        df_Merge = df_Merge.merge(df10, on="DEVELOPERS", how="left")

        for t in range(len(pos)):
            df_Merge['DEVELOPERS'][pos[t]]=valor[t]

        df_Merge.loc[df_Merge['DEVELOPERS']=="Santiago Kitashima",'Manager']="Martin Campos"
        df_Merge.loc[df_Merge['DEVELOPERS']=="Maria Laura Bisaccia",'Manager']="Martin Campos"
        df_Merge['Count']=1
        #df_Merge
        df_Merge.to_excel(r"C:\Users\016434613\Desktop\chg over90.xlsx", index=False)

    def download_ideas_sd(self):
        checkfilepath=self.filepath_ideas
        exists = False

        if os.path.exists(checkfilepath):
            subprocess.run("del /f C:\\Users\\016434613\\Downloads\\progress_sd_tasks_master_report.xlsx", shell=True, capture_output=True)

        try:
            mydriver = webdriver.Chrome("chromedriver.exe")
        except:
            print("Update chrome driver version!")
        try:
            mydriver.get("https://progress.us1a.cirrus.ibm.com/api/rpt/sd/1300295498644/ms/ros4kf4irqedd/1/13004457294999")
        except:
            print("tiemout, networking issue, retry later!")
        while not exists:
            time.sleep(1)
            exists = os.path.exists(checkfilepath)
        mydriver.close()

    def ideas(self):
        filepath_ = self.filepath_master

        df_Ideas = pd.read_excel(filepath_,sheet_name="Ideas")

        df_Ideas = df_Ideas.rename(columns={'CREATED BY (NAME)':'DSL','CREATED BY (EMAIL)':'DSL MAIL','LOCATIONS OF MANUAL EXECUTION':'LOCATIONS','MANUAL EXECUTION DURATION (hours per year)':'SAVING HS'})
        df_Ideas = df_Ideas.loc[:,['IDEA ID','CREATED','DSL','DSL MAIL','STATUS','TITLE','AUTOMATION TYPE','LOCATIONS','SAVING HS']]
        #df_Ideas['CREATED'] = df_Ideas['CREATED'].apply(lambda x: str(x))
        #df_Ideas['CREATED'] = df_Ideas['CREATED'].apply(lambda x: x[4:7]+" "+x[11:15])
        df_Ideas['CREATED'] = "Not SDA"
        df_Ideas = df_Ideas.loc[df_Ideas['STATUS']=="Submitted"]
        df_Ideas.drop(columns=['STATUS'],inplace=True)

        df_ApprIdeas = pd.read_excel(filepath_,sheet_name="Ideas Approvals")
        df_ApprIdeas = df_ApprIdeas.loc[:,['IDEA ID','STATUS']]

        df_Ideas = df_Ideas.merge(df_ApprIdeas, on="IDEA ID", how="left")
        df_Ideas = df_Ideas.loc[df_Ideas['STATUS']=="Approved"]
        df_Ideas.drop(columns=['STATUS'],inplace=True)

        filepath_ = self.filepath_ideas

        df_Sdideas = pd.read_excel(filepath_,sheet_name="Ideas")

        df_Sdideas = df_Sdideas.rename(columns={'CREATED BY (NAME)':'DSL','CREATED BY (EMAIL)':'DSL MAIL','LOCATIONS OF MANUAL EXECUTION':'LOCATIONS','MANUAL EXECUTION DURATION (hours per year)':'SAVING HS'})
        df_Sdideas = df_Sdideas.loc[:,['IDEA ID','CREATED','DSL','DSL MAIL','STATUS','TITLE','AUTOMATION TYPE','LOCATIONS','SAVING HS']]
        df_Sdideas['CREATED'] = "SDA"
        df_Sdideas = df_Sdideas.loc[df_Sdideas['STATUS']=="Submitted"]
        df_Sdideas.drop(columns=['STATUS'],inplace=True)

        df_sdApprIdeas =  pd.read_excel(filepath_,sheet_name="Ideas Approvals")
        df_sdApprIdeas = df_sdApprIdeas.loc[:,['IDEA ID','STATUS']]

        df_Sdideas = df_Sdideas.merge(df_sdApprIdeas, on="IDEA ID", how="left")
        df_Sdideas = df_Sdideas.loc[df_Sdideas['STATUS']=="Approved"]
        df_Sdideas.drop(columns=['STATUS'],inplace=True)

        df_Ideas = df_Ideas.append(df_Sdideas)

        df_Ideas['Count']=1
        df_Ideas.to_excel(r"C:\Users\016434613\Desktop\Ideas.xlsx", index=False)

    def update_specification(self):
        with open('w3id_credentials','rb') as f:
            cred = pickle.load(f)

        filepath_=self.filepath_spec
        timeelem_list = []
        df_Spec = pd.read_excel(filepath_,sheet_name="Sheet1")
        list_ = df_Spec['TASK ID'].tolist()

        try:
            mydriver = webdriver.Chrome("chromedriver.exe")
        except:
            print("Update chrome driver version!")
        try:
            mydriver.get("https://progress.us1a.cirrus.ibm.com/digital-transformation/filter/own")
            w3id = mydriver.find_element_by_xpath('//*[@id="credsDiv"]/label')
            w3id.click()
            user = mydriver.find_element_by_xpath('//*[@id="user-name-input"]')
            user.send_keys(cred['user'])
            psw = mydriver.find_element_by_xpath('//*[@id="password-input"]')
            psw.send_keys(cred['password'])
            button = mydriver.find_element_by_xpath('//*[@id="login-button"]')
            button.click()
            time.sleep(15)

            for item_ in list_:
                mydriver.get("https://progress.us1a.cirrus.ibm.com/digital-transformation/task/"+item_)
                wait = WebDriverWait(mydriver, 60)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="container-3"]/div[1]/app-task-preview/div/div/task-preview-header/div/div[2]/div[2]/div[2]/button/span[1]/mat-icon')))
                #time.sleep(12)
                try:
                    timeelem = mydriver.find_elements_by_xpath('//*[@id="container-3"]/div[1]/app-task-preview/div/div/task-preview-header/div/div[2]/div[2]/div[1]/div[2]/div/span[2]')
                    timeelem_list.append(timeelem[0].get_attribute("textContent"))
                except:
                    timeelem_list.append('Issues loading')
            mydriver.close()
            df_Spec['Last_Updated']=timeelem_list
            if self.filepath_spec == r"C:\Users\016434613\Desktop\Specification.xlsx":
                df_Spec.to_excel(r"C:\Users\016434613\Desktop\Specification.xlsx", index=False)
                self.spec_completed = True
            else:
                df_Spec.to_excel(r"C:\Users\016434613\Desktop\Reports\Specification.xlsx", index=False)
                self.spec_completed = True         
        except:
            print("timeout, networking issues, try again later.")




    def add_days(self):
        if self.spec_completed:
            filepath_=self.filepath_spec
            df_Spec = pd.read_excel(filepath_,sheet_name="Sheet1")
            days_dict = {
                " 2 years ago ":730,
                " a year ago ":365,
                " 11 months ago ":330,
                " 10 months ago ":300,
                " 9 months ago ":270,
                " 8 months ago ":240,
                " 7 months ago ":210,
                " 6 months ago ":180,
                " 5 months ago ":150,
                " 4 months ago ":120,
                " 3 months ago ":90,
                " 2 months ago ":60,
                " a month ago ":30
                
            }

            key_list = list(days_dict.keys())
            for k in key_list:
                df_Spec.loc[df_Spec['Last_Updated']==k,'Days']=days_dict[k]
            if self.filepath_spec == r"C:\Users\016434613\Desktop\Specification.xlsx":
                df_Spec.to_excel(r"C:\Users\016434613\Desktop\Specification.xlsx", index=False)
                self.spec_completed = True
            else:
                df_Spec.to_excel(r"C:\Users\016434613\Desktop\Reports\Specification.xlsx", index=False)
                self.spec_completed = True 
        else:
            print("Specificaction update did not complete, I can not run!.")