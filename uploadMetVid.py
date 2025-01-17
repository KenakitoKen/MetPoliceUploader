#! python3
# creates report and uploads video to met portal. It does not click on 'submit'--. 
# The MET state that the user is committing a crime if they intentionally upload incorrect information, 
# therefore, the script WILL NOT click 'SUBMIT', but the user must manually check the details are correct.  
import requests, os, bs4, ctypes, os.path, pyautogui, time, openpyxl
from selenium import webdriver
from tkinter import messagebox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

wbFilePath = input("Enter the file path to the Excel sheet: ")
#load the values from the excel spreadsheet into variables
wb = openpyxl.load_workbook(wbFilePath)
sheet = wb['Sheet1']
firstName = sheet['B1'].value
surname = sheet['B2'].value
dob = sheet['B3'].value
#dob = dob.strftime("%d.%m.%Y")
day, month, year = dob.split('.')
email = sheet['B4'].value
phoneNumber = sheet['B5'].value
postcode = sheet['B6'].value
buildingName = sheet['B7'].value
buildingNumber = sheet['B8'].value
street = sheet['B9'].value
townOrCity = sheet['B10'].value
typeOfVehicle = sheet['B11'].value
registrationNumber = sheet['B12'].value
make = sheet['B13'].value
model = sheet['B14'].value
colour = sheet['B15'].value
dateOfIncident = sheet['B16'].value
#dateOfIncident = dateOfIncident.strftime("%d/%m/%Y")
dayofInc, monthOfInc, yearOfInc = dateOfIncident.split('.')
hourOfIncident = sheet['B17'].value
minuteOfIncident = sheet['B18'].value
descriptionOfIncidentTime = sheet['B19'].value
descriptionOfLocation = sheet['B20'].value
weatherConditions = sheet['B21'].value
lightConditions = sheet['B22'].value
roadSurfaceConditions = sheet['B23'].value
incidentDescription = sheet['B24'].value
roadTrafficOffence = sheet['B25'].value
filePathVidOne = sheet['B26'].value
descriptionOfVideoOne = sheet['B27'].value
filePathVidTwo = sheet['B28'].value
descriptionOfVideoTwo = sheet['B29'].value
youInvolvedAs = sheet['B30'].value
theyInvolvedAs = sheet['B31'].value

#add 1 to hour and minute to make it correct for number of keypresses (it starts at 0)
hourOfIncident += 1
minuteOfIncident += 1

#strTheyInvolvedAs will be used to set the car details--the HTML is either 'driver' or 'motorcyclist' so setting it here to make it dynamic
strTheyInvolvedAs = theyInvolvedAs

#initialise dictionary types. this will be used to select the tight option using keystrokes
InvolvedAsDict = {'Driver': "", 'Motorcyclist' : "[2]", 'Cyclist' : "[3]", 'Pedestrian' : "[4]"}
youInvolvedAs = InvolvedAsDict[youInvolvedAs]
theyInvolvedAs = InvolvedAsDict[theyInvolvedAs]

#initialise dictionary types. this will be used to select the tight option using keystrokes
weatherConditionsDict = {'Fine with little wind': 1, 'raining or drizzling with little wind': 2, 'snowing with little wind':3,\
'fine with high winds':4, 'raining or drizzling with high winds':5, 'snowing with high winds':6,\
'fog or mist' : 7, 'other weather':8, 'I don\'t know':9}
weatherConditions = weatherConditionsDict[weatherConditions]

#initialise dictionary types. this will be used to select the tight option using keystrokes
lightConditionsDict = {'Daylight':1, 'Darkness, street lights present and lit':2, 'Darkness, street lights present but unlit':3,\
'darkness, no street lighting':4, 'darkness, street lighting unknown':5, 'I don\'t know':6}
lightConditions = lightConditionsDict[lightConditions]

#initialise dictionary types. this will be used to select the tight option using keystrokes
roadSurfaceConditionsDict={'dry':1, 'wet or damp':2, 'snow':3, 'Frosty or icy':4,\
'flooded (surface water above 3cm)':5, 'I don\'t know':6}
roadSurfaceConditions = roadSurfaceConditionsDict[roadSurfaceConditions]

#initialise dictionary types. this will be used to select the tight option using keystrokes
theirVehicleDict = {'Car':1, 'Taxi or private hire car' : 2, 'Taxi or private hire car' : 3, 'Minibus (8-16)':4, 'Bus or coach (17+)':5, 'Agric Vehicle':6,\
'Tram or light rail':7, 'goods vehicle under 3.5 tonnes':8, 'Goods vehicle 3.5-7.4 tonnes':9, 'Goods vehicle (unknown weight)':10,\
'Heavy goods vehicle (7.5 tonnes or more)':11, 'Other vehicle':12, 'I don\'t know':12}
typeOfVehicle = theirVehicleDict[typeOfVehicle]

drivingOffenceDict = {'Careless or inconsiderate driving': "", 'driving through a red light':"[2]", 'Driving without due care':"[3]",\
'mobile phone use while driving':"[4]", 'no insurance':"[5]", 'no driving license':"[6]",\
'not complying with a traffic sign':"[7]", 'speeding':"[8]", 'stopping in the cycle box area':"[9]",\
'cycling close pass':"[10]"}
trafficOffenceList = list(roadTrafficOffence.split(","))

browser = webdriver.Firefox()
browser.maximize_window()
type(browser)
browser.get('https://www.met.police.uk/ro/report/rti/rti-a/report-a-road-traffic-incident/')

#this function will check if an image is on the screen
def imageChecker(image):
	coordinates = None
	while coordinates is None:
		coordinates = pyautogui.locateOnScreen(r'C:\Users\Ken\Documents\Python\MetPolice\\' + image + '.PNG')
		if coordinates is None:
			print ('image ' + image + ' not on screen, try again')
			time.sleep(5)
			#scroll mouse up so the image has a white background
			pyautogui.click(0, 330)
			pyautogui.scroll(100)
			continue
		else:
			print ('image ' + image + ' found')

#user manually selects where incident occured
messagebox.showinfo("Select location", "please select where the incident occured and select OK")

try:
	linkElem = browser.find_element_by_link_text("I'm fine with cookies")
	#linkElem = browser.find_element(By.link_text, "I'm fine with cookies")
    #linkElem = browser.find_element(By.link.text, "I'm fine with cookies")
	linkElem.click()
except:
	print ("I'm fine with cookies did not appear")
#Click yes after map location inputted
linkElem = browser.find_element_by_link_text('Yes')
linkElem.click()

#click no to 'did a vehical collide with someone'
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(.,\'No\')]')))
linkElem.click()

#click 'a possible driving offence'
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h3[contains(.,\'A possible driving offence\')]')))
linkElem.click()

#click less than 10 days ago
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h3[contains(.,\'Less than 10 days ago\')]')))
linkElem.click()

#click yes to video footage
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//h3[contains(.,\'Yes\')]')))
linkElem.click()

#click start
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(),\'Start\')]')))
linkElem.click()

#mark the chexkbox with check
#linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id=\'form-app\']/section/div[5]/div/fieldset/div[3]/label/span')))
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/div/label')))
linkElem.click()

#click next
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@name=\'__target-step-id\']')))
linkElem.click()

#enter first name
# linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id=\'YourDetailsWithoutGenderElementGroup-FirstNameTextBox\']')))
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH,'//div[3]/div/div/input')))
linkElem.send_keys(firstName)

#enter second name
#linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id=\'YourDetailsWithoutGenderElementGroup-SurnameTextBox\']')))
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[4]/div/div/input')))
linkElem.send_keys(surname)

#enter day of birth
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span/input')))
#linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id=\'YourDetailsWithoutGenderElementGroup-DateOfBirthDate\']')))
linkElem.send_keys(day)

#enter month of birth
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[2]/input')))
#linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id=\'YourDetailsWithoutGenderElementGroup-DateOfBirthDate\']')))
linkElem.send_keys(month)

#enter year of birth
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[3]/input')))
#linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id=\'YourDetailsWithoutGenderElementGroup-DateOfBirthDate\']')))
linkElem.send_keys(year)

#enter email address
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[6]/div/div/input')))
linkElem.send_keys(email)

#enter phone number
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[7]/div/div/input')))
linkElem.send_keys(phoneNumber)

#enter postcode
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//fieldset/div/input')))
linkElem.send_keys(postcode)

#click enter address manually
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/button')))
linkElem.click()

#enter building name
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//fieldset/div/div/fieldset/div/div/div/input')))
linkElem.send_keys(buildingName)

#enter building number
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//fieldset/div/div/fieldset/div[2]/div/div/input')))
linkElem.send_keys(buildingNumber)

#enter street
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/fieldset/div[2]/div/div/input')))
linkElem.send_keys(street)

#enter city
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/fieldset/div[3]/div/div/input')))
linkElem.send_keys(townOrCity)

# click next
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/button')))
linkElem.click()

# select what I was involved as
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/label')))
linkElem.click()

#select next
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/button')))
linkElem.click()

#the following checks if 'remove person involved' link exists--if it doesn, page has loaded 
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//button[2]')))

#select how they were involved															
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//fieldset/div/label')))
linkElem.click()
 
#ketstrokes to click on top of browser,and then select car in drop down
time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab'],interval=1); pyautogui.press(['down'], presses = typeOfVehicle, interval=1)

#enter car reg number
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[4]/div/div/input')))
linkElem.send_keys(registrationNumber)

#enter car make
if make is not None:
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[5]/div/div/input')))
	linkElem.send_keys(make)

#enter car model
if model is not None:
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[6]/div/div/input')))
	linkElem.send_keys(model)

#enter car colour
if colour is not None:
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[7]/div/div/input')))
	linkElem.send_keys(colour)

#select next
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/button')))
linkElem.click()

#enter day of incident
#linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@id=\'IncidentDetailsElementGroup-IncidentDateDate\']')))
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span/input')))
linkElem.send_keys(dayofInc)

#enter month of incident
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[2]/input')))
linkElem.send_keys(monthOfInc)

#enter year of incident
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[3]/input')))
linkElem.send_keys(yearOfInc)

#keystrokes to select hour of incident
time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab'], interval=1); pyautogui.press(['down'], presses = hourOfIncident, interval=.5)

#keystrokes to select minute of incident
time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab'], interval=1); pyautogui.press(['down'], presses = minuteOfIncident, interval=.5)

#enter description of time of incident
if descriptionOfIncidentTime is not None or descriptionOfIncidentTime != '':
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/div/div/input')))
	linkElem.send_keys(descriptionOfIncidentTime)

#desribing incident location here
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea')))
linkElem.send_keys(descriptionOfLocation)

#ketstrokes to set weather conditoins
time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab'], interval=1); pyautogui.press(['down'], presses = weatherConditions, interval=1)

#keystrokes to set light conditions
time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab'], interval=1); pyautogui.press(['down'], presses = lightConditions, interval=1)

#keystrokes to set road surface condtions
time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab'], interval=1); pyautogui.press(['down'], presses = roadSurfaceConditions, interval=1)

#describing incident description here
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[7]/div/div/textarea')))
linkElem.send_keys(incidentDescription)

#loop to select all traffic offences that apply:
for offence in trafficOffenceList:
	htmlOffence = drivingOffenceDict[offence]
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div' + htmlOffence + '/label')))
#linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@id=\'form-app\']/section/div[8]/div/fieldset/div[9]/fieldset/div' + htmlOffence + '/label/span')))
	linkElem.click()

#loop to click on cycling close pass twice--this will ensure cursor is at correct place for next step and keep the options selected as what user selected
i = 1 
while i < 3:
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/label')))
	linkElem.click()
	time.sleep(.5)
	i += 1

#keystrokes to upload evidence now
#time.sleep(5); pyautogui.click((910, 0)); pyautogui.typewrite(['tab', 'down'], interval=1)

#Select upload video evidence now
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//option[@value=\'Upload my evidence now\']')))
linkElem.click()

counter = 1 
while counter < 2:
	#enyter file path of first video
	# if counter == 1:
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type=\'file\']')))
	# else:
		# #linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '(//input[@type=\'file\'])[' + str(counter) + ']')))
		# linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type=\'file\']')))
	linkElem.send_keys(filePathVidOne); 
	
	#click upload
	#if counter == 1:
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/button[2]')))
	#else:
	#	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/button[2]')))
	linkElem.click()

	#call function to check image is on screen, passing the green logo image 
	imageChecker('uploadComplete')

	#type in description of incident fieldset/div. new webpage domx is here is not as consistent--can't use counter 
	#if counter == 1:
	linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/div/div/textarea')))
	#else:
		# linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/fieldset/div[2]/div[3]/div/div/textarea')))
	linkElem.send_keys(descriptionOfVideoOne); 

	#keystrokes to say video has not been edited
	time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab', 'down', 'down'], interval=1)
	
	# if counter == 1:
		# #click add another file
		# linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[5]/div/button')))
		# linkElem.click()
	# filePathVidOne = filePathVidTwo
	counter += 1

#keystrokes to say met police can share video with insureres
time.sleep(2); pyautogui.click((910, 0)); pyautogui.typewrite(['tab', 'tab', 'down'], interval=1)

#click next
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/button')))
linkElem.click()

#wait for 'incident details' link to become visible
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//li[5]/button')))

#click 'no' do did anyone witness incident question
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[2]/label')))
linkElem.click()

#click next
linkElem = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[3]/button')))
linkElem.click()

print ('Upload complete, please verify details')
