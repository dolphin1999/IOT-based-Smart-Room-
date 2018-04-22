
'''

What this code is gonna do ?? 
Basically there are three Gspreadsheets named as "mode", "client" and "status" have been created with working as follows :

1) Mode := this sheet will contain on which mode user wants to operate the appliances of home 
   	   Mode = 0 i.e. Automatic Mode : User will tell raspberry pi to control the home as per data from sensors . 
   	   Mode = 1 i.e. Manual Mode : USer will control according to his/her constumized needs .

2) Client := If in manual mode then client will click on particular lights / fans icon to make them on/off as per his/her choice . And that
             information of which appliances need to be on/off will set into "Client" sheet on cloud.  Client (User who is using app) will  
             have the power to modify this sheet only. Now Raspberry Pi end will fetch this "Client" sheet and can read from there what it has
             to do and control the appliances accordingly . 

3) Status := If in Automatic mode then User atleast should get to know what is the status of appliances at home :P . Which devices are on and 
             which are off. Hence Raspberry Pi end will update values / status in "status" sheet and user end will access that sheet and in 
             application it will show the status accordingly .
             Raspberry pi will get data from sensors :- Temperature sensor, PIR sensor , Light sensor (Digital) . and according to that data 
             algorithm will find out which devices should be in which state , without human interection . i.e. Aplliances will get controlled 
             automatically . 

SIMPLE !! 
     

'''


'''
Import kivy files/directories to use
'''

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

'''
import gspread python library to access google spreadsheets

Manage your spreadsheets with gspread in Python.

Features:

    Google Sheets API v4.
    Open a spreadsheet by its title or url.
    Extract range, entire row or column values.
    Python 3 support.

'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from threading import Thread

global a1,a2,a3,a4

a1 = 1
a2 = 1
a3 = 1
a4 = 1

print("step1 done!")
scope = ['https://spreadsheets.google.com/feeds' , 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope) #get credentials for api use from client_secret.json

print("step2 done!")

#authorize the account for using gspread api

client = gspread.authorize(creds)

print("step3 done!")

# Open Client worksheet from spreadsheet with one shot
sheet1 = client.open('Client').sheet1
print("clientdone")


# Open Status worksheet from spreadsheet with one shot
sheet2 = client.open('Status').sheet1
print("statusdone")


# Open Mode worksheet from spreadsheet with one shot
sheet3 = client.open('Mode').sheet1

print("step4 done!")



#function to print values of any sheet

def printSheet(sheet) :
	print("printSheet called")	
	row_count = len(sheet.get_all_records())+1
	for i in range(row_count) :
		RowInfo = sheet.row_values(i+1)
		print(RowInfo)



#initially mode will be manual
global mode

mode = 1

#function to fetch the present mode from "Mode" Gsheet

def getMode():
	print("getMode called")
	if int(sheet3.cell(1,2).value.encode('utf-8'))==1:
		return 1
	else:
		return 0

#Function to set mode as per user choice in "mode" GSheet and if mode is changed to manual then update "client" sheet (sheet1) to the values #same as "status" sheet(sheet2)
 

def setMode(mode_id):
	print("SetMode called")
	sheet3.update_cell(1,2,mode_id)
	if mode_id == 1:
		sheet1.update_cell(2,2,int(sheet2.cell(2,2).value.encode('utf-8')))
		sheet1.update_cell(3,2,int(sheet2.cell(3,2).value.encode('utf-8')))
		sheet1.update_cell(4,2,int(sheet2.cell(4,2).value.encode('utf-8')))
		sheet1.update_cell(5,2,int(sheet2.cell(5,2).value.encode('utf-8')))

mode = getMode()






print("get mode done")




class RootWidget(FloatLayout):
    '''This is the class representing your root widget.
       By default it is inherited from BoxLayout,
       you can use any other layout/widget depending on your usage.
    '''

    
    #fuction to disable / enable buttons and to change mode appropriately when mode changes from manual to automatic
    def ManualSelection(self):
	print("ManualSelection called")
    	self.ids.ManButton.disabled = True
	self.ids.AutoButton.disabled = False
	self.ids.S1.disabled = True
	self.ids.S2.disabled = True
	self.ids.S3.disabled = True
	self.ids.S4.disabled = True
	mode = 0
	setMode(mode)
	self.ids.L5.text = "AUTOMATIC MODE ON!"
	Thread(target=self.update).start()


    
    #function to update in app if mode is automatic directly by fetching from "status" sheet (sheet2) 
    def update(self):
	mode = getMode()
	while(mode == 0):
			mode = getMode()
			print(mode)
			temp1 = int(sheet2.cell(2,2).value.encode('utf-8'))
			temp2 = int(sheet2.cell(3,2).value.encode('utf-8'))
			temp3 = int(sheet2.cell(4,2).value.encode('utf-8'))
			temp4 = int(sheet2.cell(5,2).value.encode('utf-8'))
			print("values fetched ")
			if temp1 == 0:
				self.ids.S1.text = "OFF"
				self.ids.S1.state = "normal"
			else:
				self.ids.S1.text = "ON"
				self.ids.S1.state = "down"
				
			if temp2 == 0:
				self.ids.S2.text = "OFF"
				self.ids.S2.state = "normal"
			else:
				self.ids.S2.text = "ON"
				self.ids.S2.state = "down"

			if temp3 == 0:
				self.ids.S3.text = "OFF"
				self.ids.S3.state = "normal"
			else:
				self.ids.S3.text = "ON"
				self.ids.S3.state = "down"

			if temp4 == 0:
				self.ids.S4.text = "OFF"
				self.ids.S4.state = "normal"
			else:
				self.ids.S4.text = "ON"
				self.ids.S4.state = "down"
			print("ended update")
	while(True):
		return

    #fuction to disable / enable buttons and to change mode appropriately whn mode changes from automatic to manual
    def AutomaticSelection(self):
	print("AutomaticSelection called")
    	self.ids.ManButton.disabled = False
	self.ids.AutoButton.disabled = True
	self.ids.S1.disabled = False
	self.ids.S2.disabled = False
	self.ids.S3.disabled = False
	self.ids.S4.disabled = False
	mode = 1
	setMode(mode)
	self.ids.L5.text = "MANUAL MODE ON!"
	self.getState1()
	self.getState2()
	self.getState3()
	self.getState4()


    #app will start by calling this function . As soon as "START" button will get pressed it will disable/ enable buttons accordingly . As in 
    #automatic mode all buttons referring to devices should be disabled just thier status should be shown.

    def startState(self):
	print("Start called")
        global mode
	sheet1.update_cell(2,2,int(sheet2.cell(2,2).value.encode('utf-8')))
	sheet1.update_cell(3,2,int(sheet2.cell(3,2).value.encode('utf-8')))
	sheet1.update_cell(4,2,int(sheet2.cell(4,2).value.encode('utf-8')))
	sheet1.update_cell(5,2,int(sheet2.cell(5,2).value.encode('utf-8')))
	print("STARTED:")
	printSheet(sheet1)
	self.ids.RefreshButton.disabled = True
	if mode == 1:
		    	self.ids.ManButton.disabled = False
			self.ids.AutoButton.disabled = True
			self.ids.S1.disabled = False
			self.ids.S2.disabled = False
			self.ids.S3.disabled = False
			self.ids.S4.disabled = False
			mode = 1
			setMode(mode)
			self.ids.L5.text = "MANUAL MODE ON!"
	else:
		    	self.ids.ManButton.disabled = True
			self.ids.AutoButton.disabled = False
			self.ids.S1.disabled = True
			self.ids.S2.disabled = True
			self.ids.S3.disabled = True
			self.ids.S4.disabled = True
			mode = 0
			setMode(mode)
			self.ids.L5.text = "AUTOMATIC MODE ON!"
			Thread(target=self.update).start()

    '''
       GetState functions called by buttons , when they need to fetch what is the current status of particular appliance to show it on/off. 
    '''
					
    def getState1(self):
	print("GetState1 called")

	temp = int(sheet2.cell(2,2).value.encode('utf-8'))

	if temp == 0:
		self.ids.S1.text = "OFF"
		return 'normal'
	else:
		self.ids.S1.text = "ON"
		return 'down'

    def getState2(self):
	print("GetState2 called")	
	temp = int(sheet2.cell(3,2).value.encode('utf-8'))

	if temp == 0:
		self.ids.S2.text = "OFF"
		return 'normal'
	else:
		self.ids.S2.text = "ON"
		return 'down'

    def getState3(self):
	print("GetState3 called")	
	temp = int(sheet2.cell(4,2).value.encode('utf-8'))

	if temp == 0:
		self.ids.S3.text = "OFF"
		return 'normal'
	else:
		self.ids.S3.text = "ON"
		return 'down'
    def getState4(self):
	print("GetState4 called")	
	temp = int(sheet2.cell(5,2).value.encode('utf-8'))

	if temp == 0:
		self.ids.S4.text = "OFF"
		return 'normal'
	else:
		self.ids.S4.text = "ON"
		return 'down'


    '''
       setState functions called by buttons , when in manual mode to set status of appliance as per user in client sheet(sheet1)
 
    '''
    def setState1(self):
	print("SetState1 called")
	if self.ids.S1.state == 'normal':
		self.ids.S1.text = "OFF"
		sheet1.update_cell(2,2,0)
		printSheet(sheet1)
	elif self.ids.S1.state == 'down':
		self.ids.S1.text = "ON"
		sheet1.update_cell(2,2,1)
		printSheet(sheet1)

    def setState2(self):
	print("SetState2 called")
	if self.ids.S2.state == 'normal':
		self.ids.S2.text = "OFF"

		sheet1.update_cell(3,2,0)
		printSheet(sheet1)
	elif self.ids.S2.state == 'down':
		self.ids.S2.text = "ON"
		sheet1.update_cell(3,2,1)
		printSheet(sheet1)

    def setState3(self):
	print("SetState3 called")	
	if self.ids.S3.state == 'normal':
		self.ids.S3.text = "OFF"
		sheet1.update_cell(4,2,0)
		printSheet(sheet1)

	elif self.ids.S3.state == 'down':
		self.ids.S3.text = "ON"
		sheet1.update_cell(4,2,1)
		printSheet(sheet1)

    def setState4(self):
	print("SetState4 called")	
	if self.ids.S4.state == 'normal':
		self.ids.S4.text = "OFF"
		sheet1.update_cell(5,2,0)
		printSheet(sheet1)
	elif self.ids.S4.state == 'down':
		self.ids.S4.text = "ON"
		sheet1.update_cell(5,2,1)
		printSheet(sheet1)

    def Condition1(self):
	temp = int(sheet2.cell(2,2).value.encode('utf-8'))

	if temp == 0:
		return 'OFF'
	else:
		return 'ON'
    def Condition2(self):
	temp = int(sheet2.cell(3,2).value.encode('utf-8'))

	if temp == 0:
		return 'OFF'
	else:
		return 'ON'
    def Condition3(self):
	temp = int(sheet2.cell(4,2).value.encode('utf-8'))

	if temp == 0:
		return 'OFF'
	else:
		return 'ON'
    def Condition4(self):
	temp = int(sheet2.cell(5,2).value.encode('utf-8'))

	if temp == 0:
		return 'OFF'
	else:
		return 'ON'


class MainApp(App):
    '''This is the main class of your app.
       Define any app wide entities here.
       This class can be accessed anywhere inside the kivy app as,
       in python::
         app = App.get_running_app()
         print (app.title)
       in kv language::
         on_release: print(app.title)
       Name of the .kv file that is auto-loaded is derived from the name
       of this class::
         MainApp = main.kv
         MainClass = mainclass.kv
       The App part is auto removed and the whole name is lowercased.
    '''

    def build(self):
        return RootWidget()

if '__main__' == __name__:

	MainApp().run()
