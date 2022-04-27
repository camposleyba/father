import ibm_db

conn=ibm_db.connect("DRIVER={IBM DB2 ODBC DRIVER};DATABASE=DP1H;HOSTNAME=usibmvrdp1h.ssiplex.pok.ibm.com;PORT=5520;UID=ar16434;PWD=No_tengocovid23",'','')

sql = "select cty, lc,maj,minor,smin,amtloc from lrpcc.ladetail_cm_d where cty='613'"
stmt = ibm_db.exec_immediate(conn, sql)

row = ibm_db.fetch_tuple(stmt)
while ( row ):
    for i in row:
         print(i)
    row = ibm_db.fetch_tuple(stmt)
ibm_db.close(conn)