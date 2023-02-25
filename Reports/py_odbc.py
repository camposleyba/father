import pyodbc
import pandas as pd
import pickle
import time
import os

start = time.time()

#file should be store in the same path
cred_file = "cred_db"
minor_codes = r"C:\Users\016434613\Desktop\Todo\Minor Codes.xlsx"
outfile = r"C:\Users\016434613\Desktop\dept1977_exp.xlsx"

if os.path.exists(cred_file):
    with open(cred_file,"rb") as f:
        cred_dict = pickle.load(f)


try:
    conn_string="DSN=DP1H;UID={};PWD={}".format(cred_dict['user'],cred_dict['psw'])
except:
    print("File cred_db does not exists")
conn = pyodbc.connect(conn_string)

sql = ''' SELECT CTY, DIV, LC, TOLI, MAJ, MINOR, SMIN, LERU, FID, SRC, ACCID, ACCTMO,
             ACCTYEAR, AMTLOC, AMTDLR, AMTLOC_REP, AMTDLR_REP, VOUCHER_NBR,
             OEM_PROD_ID, DESCR1, LOCFLD1
          FROM LRPCC.LADETAIL_PM_D
          WHERE (CTY = '613' AND MAJ = '601' AND LERU IN ('001977')
             AND LC IN ('01', '04')) '''

df =pd.read_sql(sql,conn)

df_Minor = pd.read_excel(minor_codes,sheet_name="REF (2)",converters={'Minor':str})
df_Minor = df_Minor.loc[:,['Minor','Desc']]
df_Minor = df_Minor.rename(columns={'Minor':'MINOR'})
df = df.merge(df_Minor, on="MINOR", how="left")
df.to_excel(outfile, index=False)

end = time.time()
mins = (end-start)/60.00
if mins < 1:
    mins = end-start
    minsstr = "Report created in: {:.2f} seconds".format(mins) 
    print(minsstr)
else:
    minsstr = "Report created in: {:.2f} minutes".format(mins)
    print(minsstr)