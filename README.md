# MetPoliceUploader
Python script to automate uploading reports to the Met portal

Currently the script is limited to uploading two videos at a time

Selenium and python must be installed on the users machine. 

1) The user must enter all the details they would usually enter into the Met portal into the xlsm file. The script reads the XLSM file and enters the detail into the Met portal. 

2) When the script is run, Python will prompt you for the file path of the xlsm file. Enter the full file path of the xlsm file. 

3) The script cannot enter the location of the incident. The script will show a pop-up and ask the user to enter the location. The user then needs to press 'OK' on the Python pop up.

4) the user must verify what the script has entered before clicking submit. the script will not click 'submit' on behald of the user. 

5) Video of script working here: https://youtu.be/0CdO1bIeoak 
