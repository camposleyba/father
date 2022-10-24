import warnings
import subprocess
import os
from selenium import webdriver
import time
from fast_reports import FastReports


start = time.time()

warnings.filterwarnings('ignore')

fr = FastReports()

fr.download_tasks()
fr.backlogsub()

end = time.time()
mins = (end-start)/60.00
if mins < 1:
    mins = end-start
    print('Reports created/updated in: {:.2f} seconds'.format(mins))
else:
    print('Reports created/updated in: {:.2f} minutes'.format(mins))