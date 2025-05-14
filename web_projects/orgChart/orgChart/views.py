from django.shortcuts import render
import pandas as pd
from urllib import request as req
import json
import requests
import warnings
from pathlib import Path


class manager():
    
	def __init__(self, cnum='', clname=''):
		self.cnum = cnum
		self.clname = clname

	def _fetch_json(self, endpoint, cnum_override=None):
		"""Fetch JSON data from the given endpoint."""
		host = cnum_override if cnum_override else self.cnum
		url = f"https://w3-unifiedprofile-api.dal1a.cirrus.ibm.com/v3/profiles/{host}/{endpoint}"
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response.json()
		except requests.RequestException as e:
			warnings.warn(f"Request error for {url}: {e}")
			return {}

	def data_from_spreadsheet(self):
		input_route = Path.home() / 'Box' / 'OrgChart' / 'For_Org_Chart.xlsx'
		df = pd.read_excel(input_route, sheet_name='Sheet1')
		return df

	def reports_self_rows(self):
		ref_data = self.data_from_spreadsheet()
		team_data = self._fetch_json("teamResolved")
		profile_data = self._fetch_json("profile")
		functional = team_data["content"]["functional"]
		# incty = team_data['content']['in']
		reports = functional.get("reports", [])
  
		report_rows = []

		if len(reports)>=1:
			for rep in reports:
				if rep.get("employeeType", {}).get("isEmployee"):
					yos = ref_data.loc[ref_data['Employee'] == rep.get("nameDisplay", ""), 'Years of Service']
					bkgrnd = ref_data.loc[ref_data['Employee'] == rep.get("nameDisplay", ""), 'Background']
					skls = ref_data.loc[ref_data['Employee'] == rep.get("nameDisplay", ""), 'Skills']
					row = {
						"Employee": rep.get("nameDisplay", ""),
						"Serial": rep.get("uid", ""),
						"Role": rep.get("role", "No role in BP"),
						"Years": yos.values[0] if not yos.empty else '',
						"Background": bkgrnd.values[0] if not yos.empty else '',
						"skills": skls.values[0] if not yos.empty else '',
						"photo_url": f"https://w3-unifiedprofile-api.dal1a.cirrus.ibm.com/v3/image/{rep.get('uid','')}"
					}
					# Use the helper to extract level data.
					report_rows.append(row)
		try:
			content = profile_data["content"]
			yos_self = ref_data.loc[ref_data['Employee'] == content.get("nameDisplay", ""), 'Years of Service']
			bkgrnd_self = ref_data.loc[ref_data['Employee'] == content.get("nameDisplay", ""), 'Background']
			skls_self = ref_data.loc[ref_data['Employee'] == content.get("nameDisplay", ""), 'Skills']
			self_row = {
				"Employee": content.get("nameDisplay", ""),
				"Serial": content.get("uid", ""),
				"Role": content.get("role", "No role in BP"),
				"Years": yos_self.values[0] if not yos.empty else '',
				"Background": bkgrnd_self.values[0] if not yos.empty else '',
				"skills": skls_self.values[0] if not yos.empty else '',
				"photo_url": f"https://w3-unifiedprofile-api.dal1a.cirrus.ibm.com/v3/image/{content.get('uid','')}"
			}
			# For self, using similar level logic:
			report_rows.append(self_row)
		except (KeyError, TypeError):
			warnings.warn("Unexpected data structure in profile data")
   
		df = pd.DataFrame(report_rows)
		df.reset_index(drop=True, inplace=True)
		return df


def home(request):
	cnum = request.GET.get('q', '')  # Gets the value entered in the search input
	if cnum:
		cnumber = cnum
	else:
		cnumber = '016434613'
	name = ''
	mgr = manager(cnumber,name)
	df_data = mgr.reports_self_rows()
	df_data = df_data.sort_values(by='Years', ascending=False)
	name = df_data.loc[df_data['Serial']==cnumber, "Employee"].values[0]
	mgr_dict = df_data[df_data['Employee'] == name].to_dict(orient="records")
	emp_dict = df_data[df_data['Employee'] != name].to_dict(orient="records")
	context = {
		'manager':mgr_dict,
		'team_members':emp_dict
	}
	return render(request, 'home.html', context)