import pandas as pd
from urllib import request as req
import json

class centerLeader():

	def __init__(self, cnum='', clname=''):
		self.cnum = cnum
		self.clname = clname

	def centerLead(self, loc):
		self.loc = loc
		reportnames = []
		reportserial = []
		isMgr = []
		locality= []
		identity=[]
		emp_type = []
		role = []

		request = req.urlopen("https://unified-profile-api.us-south-k8s.intranet.ibm.com/v3/profiles/"+self.cnum+"/teamResolved")
		datos = request.read().decode()
		dictdatos = json.loads(datos)
		reports = dictdatos['content']['functional']['reports']
		for r in reports:
		    #method setdefault(key,[]) sirve para poner una primera key con una lista vacia, si no, tira error de que no existe la key
		    reportnames.append(r['nameDisplay'])
		    reportserial.append(r['uid'])
		    isMgr.append(r['isManager'])
		    emp_type.append(r['employeeType']['title'])
		    try:
		    	role.append(r['role'])
		    except:
		    	role.append('')
		    if self.clname == "Francisco del Castillo":
		    	try:
		    		l=r['address']['business']['locality']
		    		if l == "Buenos Aires":
		    			self.loc = "BA"
		    		elif l == "Bratislava":
		    			self.loc = "SK"
		    		else:
		    			self.loc = "USA"
		    	except:
		    		self.loc = "Other"
		    	locality.append(self.loc)
		    else:
		    	locality.append(self.loc)
		    try:
		    	identity.append(r['preferredIdentity'])
		    except:
		    	identity.append('')

		df_cl = pd.DataFrame(reportnames, columns=['Reports'])
		df_cl['Serials'] = reportserial
		df_cl['isManager'] = isMgr
		df_cl['Location'] = locality
		df_cl['Email'] = identity
		df_cl['Manager'] = self.clname
		df_cl['EmpType'] = emp_type
		df_cl['Job_title'] = role

		return df_cl

	def reportFunc(self, dataframe):
		reportnames_= []
		reportserial_= []
		isMgr_= []
		locality_= []
		identity_= []
		mgr_= []
		emp_type_=[]
		role_ = []


		for i in range(dataframe['Reports'].size):
		    request = req.urlopen("https://unified-profile-api.us-south-k8s.intranet.ibm.com/v3/profiles/"+dataframe['Serials'][i]+"/teamResolved")
		    datos = request.read().decode()
		    dictdatos = json.loads(datos)
		    try:
		        reports = dictdatos['content']['functional']['reports']
		        for r in reports:
		            reportnames_.append(r['nameDisplay'])
		            reportserial_.append(r['uid'])
		            emp_type_.append(r['employeeType']['title'])
		            try:
		            	role_.append(r['role'])
		            except:
		            	role_.append('')
		            try:
		                email = r['preferredIdentity']
		                identity_.append(r['preferredIdentity'])
		            except:
		                identity_.append('Contractor or LoA')
		            isMgr_.append(r['isManager'])
		            try:
		                location = r['address']['business']['locality']
		                locality_.append(self.loc)
		            except:
		                locality_.append('Contractor')
		            mgr_.append(dataframe['Reports'][i])
		    except:
		    	pass

		df_Reports = pd.DataFrame(reportnames_, columns=['Reports'])
		df_Reports['Serials'] = reportserial_
		df_Reports['isManager'] = isMgr_
		df_Reports['Manager'] = mgr_
		df_Reports['Location'] = locality_
		df_Reports['Email'] = identity_
		df_Reports['EmpType'] = emp_type_
		df_Reports['Job_title'] = role_

		return df_Reports

	def reportFuncDT(self, dataframedt):
		reportnames_dt= []
		reportserial_dt= []
		isMgr_dt= []
		locality_dt= []
		identity_dt= []
		mgr_dt= []
		emp_type_ = []
		role_ = []

		for i in range(dataframedt['Reports'].size):
		    request = req.urlopen("https://unified-profile-api.us-south-k8s.intranet.ibm.com/v3/profiles/"+dataframedt['Serials'][i]+"/teamResolved")
		    datos = request.read().decode()
		    dictdatos = json.loads(datos)
		    try:
		        reports = dictdatos['content']['functional']['reports']
		        for r in reports:
		            reportnames_dt.append(r['nameDisplay'])
		            reportserial_dt.append(r['uid'])
		            emp_type_.append(r['employeeType']['title'])
		            try:
		            	role_.append(r['role'])
		            except:
		            	role_.append('')
		            try:
		                email = r['preferredIdentity']
		                identity_dt.append(r['preferredIdentity'])
		            except:
		                identity_dt.append('Contractor or LoA')
		            isMgr_dt.append(r['isManager'])
		            try:
		                location = r['address']['business']['locality']
		                if location == "Buenos Aires":
		                	self.loc = "BA"
		                elif location == "Bratislava":
		                	self.loc = "SK"
		                else:
		                	self.loc = "USA"
		                locality_dt.append(self.loc)
		            except:
		                locality_dt.append('Contractor')
		            mgr_dt.append(dataframedt['Reports'][i])
		    except:
		        pass

		df_ReportsDT = pd.DataFrame(reportnames_dt, columns=['Reports'])
		df_ReportsDT['Serials'] = reportserial_dt
		df_ReportsDT['isManager'] = isMgr_dt
		df_ReportsDT['Manager'] = mgr_dt
		df_ReportsDT['Location'] = locality_dt
		df_ReportsDT['Email'] = identity_dt
		df_ReportsDT['EmpType'] = emp_type_
		df_ReportsDT['Job_title'] = role_

		return df_ReportsDT

	def calculateRepo(self, df):
		serial_list = df['Serials'].tolist()
		list_ = []
		for s in serial_list:
			request = req.urlopen("https://unified-profile-api.us-south-k8s.intranet.ibm.com/v3/profiles/"+s+"/teamResolved")
			datos = request.read().decode()
			dictdatos = json.loads(datos)
			try:
				reports = dictdatos['content']['functional']['reports']
				list_.append(len(reports))
			except:
				list_.append(0)
		return list_

