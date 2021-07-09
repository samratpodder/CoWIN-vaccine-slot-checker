import time
from datetime import timedelta, datetime
import os,sys
import requests,json


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'}
settings = {
  "daysLeftforDose2":0,
  "pincode":700047,
  "userAge": 20
}


def getDate(postdays=1):
    """
    Function to get the next date => Today + 1 day
    Returns
    -------
    date : String
        Next date in DD-MM-YYYY format
    """
    tomorrow = (datetime.today() + timedelta(postdays)).strftime("%d-%m-%Y")
    return tomorrow
def getStateID(state):
  state_id=''
  url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
  try:
      response = requests.get(url,headers=headers)
      parsed_response = json.loads(response.text)
      state_length = len(parsed_response['states'])
      for idx in range(state_length):
          if((parsed_response['states'][idx]['state_name']).lower().replace(" ", "") == state.lower().replace(" ", "")):
              state_id = parsed_response['states'][idx]['state_id']
              return(state_id)
  except Exception as e:
      print(e)
def pincodeToStateDistrictConverter(pincode):
    district = ''
    state = ''
    india_post_url = "https://api.postalpincode.in/pincode/{pin}".format(pin = pincode)
    try:
        response = requests.get(india_post_url,headers=headers)
        parsed_response = json.loads(response.text)
        if(parsed_response[0]["Status"] == "Success"):
            district = parsed_response[0]['PostOffice'][0]['District']
            state = parsed_response[0]['PostOffice'][0]['State']
        return district,state
    except Exception as e:
        print(e)
def checkAvailability(payload, age):
    """
    Function to check availability in the hospitals based on
    user age from the json response from the public API
    Parameters
    ----------
    payload : JSON
    age: INT
    Returns
    -------
    available_centers_str : String
        Available hospitals
    total_available_centers : Integer
        Total available hospitals
    """
    available_centers = dict()
    unavailable_centers = set()
    available_centers_str = False
    total_available_centers = 0
    
    if('centers' in payload.keys()):
       length = len(payload['centers'])
       if(length>1):
            for i in range(length):
                sessions_len = len(payload['centers'][i]['sessions'])
                for j in range(sessions_len):
                    if((payload['centers'][i]['sessions'][j]['available_capacity']>0) and
                       (payload['centers'][i]['sessions'][j]['min_age_limit']<=age)):
                        available_centers[total_available_centers]=payload['centers'][i]
                        total_available_centers +=1
                        break
    
    return available_centers,total_available_centers
def getDistrictID(st_id, lookout_district):
    districtid = ''
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{st}".format(st = st_id)
    try:
        response = requests.get(url,headers=headers)
        parsed_response = json.loads(response.text)
        district_length = len(parsed_response['districts'])
        for idx in range(district_length):
            if((parsed_response['districts'][idx]['district_name']).lower().replace(" ", "") == lookout_district.lower().replace(" ", "")):
                district_id = parsed_response['districts'][idx]['district_id']
        return (district_id)
    except Exception as e:
        print(e)
        return 733 #NEEDS IMMEDIATE ATTENTION
def pingCOWIN(date,district_id):
    """
    Function to ping the COWIN API to get the latest district wise details
    Parameters
    ----------
    date : String
    district_id : String
    
    Returns
    -------
    json
    """
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={district_id}&date={date}".format(district_id = district_id, date = date)
    response = requests.get(url,headers=headers)
    return json.loads(response.text)
def getAvailableNames(payload, age):
    """
    Function to check availability in the hospitals based on
    user age from the json response from the public API
    Parameters
    ----------
    payload : JSON
    age: INT
    Returns
    -------
    available_centers_str : String
        Available hospitals
    total_available_centers : Integer
        Total available hospitals
    """
    available_centers = set()
    unavailable_centers = set()
    available_centers_str = False
    total_available_centers = 0
    
    if('centers' in payload.keys()):
       length = len(payload['centers'])
       if(length>1):
            for i in range(length):
                sessions_len = len(payload['centers'][i]['sessions'])
                for j in range(sessions_len):
                    if((payload['centers'][i]['sessions'][j]['available_capacity']>0) and
                       (payload['centers'][i]['sessions'][j]['min_age_limit']<=age)):
                        available_centers.add(payload['centers'][i]['name'])
            available_centers_str =  ", ".join(available_centers)
            total_available_centers = len(available_centers)
    
    return available_centers_str,total_available_centers


if __name__ == "__main__":
    settings["daysLeftforDose2"] = int(input("How many Days are left for your Dose 2 ? (Enter 1 for Dose 1) : "))
    settings["userAge"] = int(input("What is your Age ? : "))
    settings["pincode"] = int(input("What is your Pincode ? (Enter your home pincode or the pincode of the vaccination center from where you wish to get vaccinated): "))
    dist,st=pincodeToStateDistrictConverter(settings["pincode"])
    print(dist,st)
    stateid=getStateID(st)
    print(stateid)
    distid=getDistrictID(stateid,dist)
    print(distid)
    centers=pingCOWIN(getDate(settings["daysLeftforDose2"]),distid)
    available,count=checkAvailability(centers,settings["userAge"])
    # centerNames,_ = getAvailableNames(centers,settings['userAge'])
    print(""+str(count)+" Center(s) Found - ",end="")
    # print(centerNames)
    print("\n")
    time.sleep(2)
    for i in range(len(available.keys())):
        print("A "+available[i]['fee_type']+" Center Named "+available[i]['name']+" at address "+available[i]['address']+" is available from "+available[i]['from']+" to "+available[i]['to'])
        if available[i]['fee_type'] == 'Paid':
            print("Vaccine - "+available[i]['vaccine_fees'][0]["vaccine"]+" priced at Rs."+available[i]['vaccine_fees'][0]["fee"]+"(inclusive of all service charges and 5% GST,if applicable)")
        for j in range(len(available[i]['sessions'])):
            if available[i]['sessions'][j]['min_age_limit'] < settings["userAge"]:
                print("Session ID - "+available[i]['sessions'][j]['session_id'])
                print("Date - "+available[i]['sessions'][j]['date'])
                print("Min. Age - "+str(available[i]['sessions'][j]['min_age_limit']))
                if available[i]['fee_type'] == 'Free':
                    print("Vaccine Name - "+available[i]['sessions'][j]['vaccine'])
                print("Quantity of 1st Dose Available is "+str(available[i]['sessions'][j]['available_capacity_dose1']))
                print("Quantity of 2nd Dose Available is "+str(available[i]['sessions'][j]['available_capacity_dose2']))
                print("Time Slots "+str(available[i]['sessions'][j]['slots']))
                print("-------")
                # time.sleep(0.5)
        print("\n ------------------------------ \n")