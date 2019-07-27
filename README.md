# SOC_T1_Public_Breaches_Probing
Offers a python script to probe publicly disclosed breaches dumps. 
The script use public API that responds to queries regarding emails, usernames, passwords etc. 
The first version of this package focuses on emails probing.
This could come handy when you want to learn your corporate emails exposure after a breach, especially if corporate users use their
corporate emails in public websites.

Use these python scripts to query https://haveibeenpwned.com and other websites for leaked emails in previous breaches

Python Script developped with Python 3.5

Uses the requests library: http://docs.python-requests.org/en/master/

Usage:
1. Put the emails.txt and output.txt in the same directory as _search_Emails_Breaches.py or _search_Emails_Breaches.exe. 
2. Fill in emails.txt with emails that you want to search breaches for, each email in a separate file.
3. From within the same directory, open a cmd and run the python script _search_Emails_Breaches.py or _search_Emails_Breaches.exe.
4. Results will be put in output.txt file.
5. Ne need to delete the output.txt file afterwards. The program will check the API and if there are no new breaches for the given email, it will not update the file for that email addresse.
