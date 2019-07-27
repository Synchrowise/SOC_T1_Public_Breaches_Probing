import json
import requests
from pprint import pprint
import time
import datetime
import os.path
import sys

#documentation: https://haveibeenpwned.com/API/v2
#Github code : https://github.com/Synchrowise/SOC_T1_Public_Breaches_Probing

#Initiate a counter variable
i=1

#Specifying these headers seem to be important for haveibeenpwned.com. Otherwise the server either rejects the client or Cloudfare challenges it via Javascript
#The 'Accept': 'application/vnd.haveibeenpwned.v2+json' header ensures we query the v2 API
headers = {
					'User-Agent': 'Pwnage-Checker-For-Synchrowise',
					'Accept': 'application/vnd.haveibeenpwned.v2+json'
					}
if not os.path.exists('./emails.txt'):

	print("\n emails.txt not found! I'll put it for you in the same directory. Please fill it with e-mail addresses each one in a separate line. After doing that rerun the program.\n")
	emails = open("emails.txt", "w")
	emails.close()
	sys.exit(1)


#Compute the number of lines in the file
num_lines = sum(1 for line in open("emails.txt"))

with open("emails.txt","r") as emails:
	for email in emails:
		
		#At each line in the input file we initialize a variable that assumes the seeked record hasn't been found yet
		already_found_record = False
		
		#if the counter doesn't correspond to the last line
		if i < num_lines:
			#Truncate the last character from the line which is \n. We don't need \n because it will interfere with future string searches (find function)
			email=email[:-1]
		
		#Saving the current date ant time
		search_Date=str(datetime.datetime.now())[:-7].replace(":","-").replace(" ","_")
		
		#Checking for the presence of the output.txt file and creating it if necessary
		
		if not os.path.exists('./output.txt'):
			output = open("output.txt", "a")
	
		#Opening previous searches that are stored in the "output.txt" file
		previous_searches = open("output.txt","r")
		
		#Querying haveibeenpwned.com API
		response = requests.get("https://haveibeenpwned.com/api/breachedaccount/"+email,headers=headers)
			
		#Applying some rate limiting. Otherwise the server will force you to do it...check documentation to learn rate limits
		print("\nSleeping 10s to limit requests rate!\n")
				
		time.sleep(10)
		
		#Our potential new record to be written is initialized with the email address
		record = email
		
		#The record timestamp helps to keep track of query date
		record_timestamp=";Search_Date:"+search_Date+"\n"	
		
		#If the response isn't empty
		if(response):
			
			#Saving the response with respect to the json format so that we can exploit its tree later
			json_data = json.loads(response.text)
			
			#Creating our record by querying the json variable to add interesting data and by separating fild names by ";" for csv preparation
			record = record+";Breach_Source:https://haveibeenpwned.com"+";json_payload:{"+"'Domain':"+json_data[0]['Domain']+",'BreachDate':"+json_data[0]['BreachDate']+",'ModifiedDate':"+json_data[0]['ModifiedDate']+",'DataClasses':"+str(json_data[0]['DataClasses'])+",'IsVerified':"+str(json_data[0]['IsVerified'])+"}"

		#if the record is already stored in "output.txt" change the already_found_record to True
		for previous_record in previous_searches:
				if previous_record.find(record) != -1:
					already_found_record = True
					break
		
		#Update "output.txt" only if the record is new
		if not already_found_record:
			output.write(record+record_timestamp)
			
			
		
		#increment counters
		i=i+1
		
		previous_searches.close()
	
emails.close()
