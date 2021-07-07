from checkSlot import *
import time
from os import system, name
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
settings["daysLeftforDose2"] = int(input("How many Days are left for your Dose 2 ? (Enter 1 for Dose 1) : "))
settings["userAge"] = int(input("What is your Age ? : "))
settings["pincode"] = int(input("What is your Pincode ? (Enter your home pincode or the pincode of the vaccination center from where you wish to get vaccinated): "))
while True:
    dist,st=pincodeToStateDistrictConverter(settings["pincode"])
    stateid=getStateID(st)
    distid=getDistrictID(stateid,dist)
    centers=pingCOWIN(getDate(settings["daysLeftforDose2"]),distid)
    available,count=checkAvailability(centers,settings["userAge"])
    print(""+str(count)+" Center(s) Found - ",end="")
    print("\n")
    time.sleep(2)
    for i in range(len(available.keys())):
        print(available[i]['fee_type']+" Center Name "+available[i]['name'])
        print("Vaccine - "+available[i]['vaccine_fees'][0]["vaccine"]+" priced at Rs."+available[i]['vaccine_fees'][0]["fee"])
        for j in range(len(available[i]['sessions'])):
            if available[i]['sessions'][j]['min_age_limit'] < settings["userAge"]:
                print("Session "+str(j))
                print("Date - "+available[i]['sessions'][j]['date'])
                print("Min. Age - "+str(available[i]['sessions'][j]['min_age_limit']))
                print("Quantity of 1st Dose Available is "+str(available[i]['sessions'][j]['available_capacity_dose1']))
                print("Quantity of 2nd Dose Available is "+str(available[i]['sessions'][j]['available_capacity_dose2']))
                print("-------")
        print("\n ------------------------------ \n")
    time.sleep(300)
    clear()
    time.sleep(2)