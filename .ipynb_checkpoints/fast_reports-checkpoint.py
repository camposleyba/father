import pandas as pd
import re

filepath_= r"C:\Users\016434613\Downloads\progress_dt_tasks_details_report.xlsx"

def backlogsub():
    '''This function creates the backlog report on a spreadsheet. It uses pandas functions to rename columns, 
    subtract not needed data/columns and filter the information. Also it modifies the date on certified field keeping only Month Year.
    Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
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

def specsub():
    '''This function creates the specification report on a spreadsheet. It uses pandas functions to rename columns, 
    subtract not needed data/columns and filter the information. Also it modifies the date on certified field keeping only Month Year.
    Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
    df_Spec  = pd.read_excel(filepath_,sheet_name="Tasks")
    df_Spec = df_Spec.rename(columns={'DSL/SUPERVISOR (NAME)':'DSL','DSL/SUPERVISOR (EMAIL)':'DSL EMAIL','ROBOT NUMBER':'ROBOT_NUMBER','AUTOMATION TYPE':'AUTOMATION_TYPE','MANUAL EXECUTION DURATION (hours per year)':'SAVING HS'})
    df_Spec = df_Spec.loc[:,['TASK ID','CERTIFIED','DSL','DSL EMAIL','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION_TYPE','REGIONS','SAVING HS']]
    df_Spec = df_Spec.loc[df_Spec['STATUS']=="Specification"]
    df_Spec['CERTIFIED'] = df_Spec['CERTIFIED'].apply(lambda x: str(x))
    df_Spec['CERTIFIED'] = df_Spec['CERTIFIED'].apply(lambda x: x[4:7]+" "+x[11:15])
    df_Spec.loc[df_Spec['CERTIFIED']=='fin ','CERTIFIED']=""
    df_Spec = df_Spec.loc[df_Spec['ROBOT_NUMBER'].isnull()==True]
    df_Spec.drop(columns=['ROBOT_NUMBER','STATUS'],inplace=True)
    df_Spec['Count']=1
    df_Spec.to_excel(r"C:\Users\016434613\Desktop\Specification.xlsx", index=False)

#df_Spec

def validsub():
    '''This function creates the validation report on a spreadsheet. It uses pandas functions to rename columns, 
    subtract not needed data/columns and filter the information. Also it modifies the date on certified field keeping only Month Year.
    Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
    df_Val = pd.read_excel(filepath_,sheet_name="Tasks")
    df_Val = df_Val.rename(columns={'DSL/SUPERVISOR (NAME)':'DSL','DSL/SUPERVISOR (EMAIL)':'DSL EMAIL','ROBOT NUMBER':'ROBOT_NUMBER','AUTOMATION TYPE':'AUTOMATION_TYPE','MANUAL EXECUTION DURATION (hours per year)':'SAVING HS'})
    df_Val = df_Val.loc[:,['TASK ID','CERTIFIED','DSL','DSL EMAIL','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION_TYPE','REGIONS','SAVING HS']]
    df_Val = df_Val.loc[df_Val['STATUS']=="Validation"]
    df_Val['CERTIFIED'] = df_Val['CERTIFIED'].apply(lambda x: str(x))
    df_Val['CERTIFIED'] = df_Val['CERTIFIED'].apply(lambda x: x[4:7]+" "+x[11:15])
    df_Val.loc[df_Val['CERTIFIED']=='fin ','CERTIFIED']=""
    df_Val = df_Val.loc[df_Val['ROBOT_NUMBER'].isnull()==True]
    df_Val.drop(columns=['ROBOT_NUMBER','STATUS'],inplace=True)
    df_Val['Count']=1
    df_Val.to_excel(r"C:\Users\016434613\Desktop\Validation.xlsx", index=False)

#df_Val

def changesub():
    '''This function creates the changes report and the changes_ report on different spreadsheets. It uses pandas functions to rename columns, 
    subtract not needed data/columns and filter the information and customize some fields.
    This function is also using the regular expresion library to find out if a 
    value from a certain list of keywords is found on the changes summary field on the report, if that is the case it highlights it by
    changing the actual value of the field and additionaly adding a 1 to a new column called prob_poor_desing if there is no keyword find it adds a 0
    instead.
    Finally adds an extra column with count 1 to make it easier on the cognos dashboard to make opeartions on the data'''
    df_chg = pd.read_excel(filepath_,sheet_name="Tasks")
    df_chg = df_chg.rename(columns={'DSL/SUPERVISOR (NAME)':'DSL','DSL/SUPERVISOR (EMAIL)':'DSL EMAIL','ROBOT NUMBER':'ROBOT_NUMBER',
                                    'AUTOMATION TYPE':'AUTOMATION_TYPE','MANUAL EXECUTION DURATION (hours per year)':'SAVING HS',
                                   'LOCATIONS OF MANUAL EXECUTION':'LOCATIONS'})
    df_chg = df_chg.loc[:,['TASK ID','ROBOT VERSION','CHANGE SUMMARY','DSL','DSL EMAIL','STATUS','ROBOT_NUMBER','TITLE','AUTOMATION_TYPE','REGIONS','LOCATIONS','SAVING HS']]
    df_chg = df_chg.loc[df_chg['STATUS']=="In Production"]
    df_chg = df_chg.loc[df_chg['ROBOT VERSION']>1]
    df_chg.drop(columns=['STATUS','ROBOT VERSION'],inplace=True)
    df_chg.to_excel(r"C:\Users\016434613\Desktop\Changes.xlsx", index=False)

    df_chg2 = pd.read_excel(r"C:\Users\016434613\Desktop\Changes.xlsx",sheet_name="Sheet1")
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