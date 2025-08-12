from datetime import datetime
from datetime import date,timedelta
import datetime as dtc
from collections import Counter

yesterday = datetime.now() - timedelta(1)
sdate = datetime.strftime(yesterday, '%Y-%m-%d 

lastdate=date.today().replace(day=1) - timedelta(days=1)
startdate=date.today().replace(day=1) - timedelta(days=lastdate.day)

print(sdate)
print(lastdate, startdate)