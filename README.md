# CoWIN-vaccine-slot-checker
A Python Script to track available vaccine slots on CoWIN (cowin.gov.in) Vaccinator Application using APIs from  API Setu (apisetu.gov.in) (The appointment availability data is cached and may be up to 5 minutes old. Further, these APIs are subject to a rate limit of 100 API calls per 5 minutes per IP.) 
-To check for Slots use the checkSlot.py.
-To get a list of available centers use the crawler.py which updates every 5 minutes. The 5 minute time gap is recommened keeping the Rate Limitting in mind.
-The Notebook is not important