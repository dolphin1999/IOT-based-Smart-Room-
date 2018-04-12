from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
import gspread
from oauth2client.service_account import ServiceAccountCredentials
print("step1 done!")
scope = ['https://spreadsheets.google.com/feeds' , 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
print("step2 done!")
client = gspread.authorize(creds)

print("step3 done!")

sheet1 = client.open('Client').sheet1
sheet2 = client.open('Status').sheet1
sheet3 = client.open('Mode').sheet1

print("step4 done!")





def printSheet(sheet) :
	print("printSheet called")	
	row_count = len(sheet.get_all_records())+1
	for i in range(row_count) :
		RowInfo = sheet.row_values(i+1)
		print(RowInfo)


global mode

mode = 1


def getMode():
	print("getMode called")
	if int(sheet3.cell(1,2).value.encode('utf-8'))==1:
		return 1
	else:
		return 0
def setMode(mode_id):
	print("SetMode called")
	sheet3.update_cell(1,2,mode_id)

	if mode == 1:
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
    def ManualSelection(self):
	print("ManualSelection called")
    	self.ids.ManButton.disabled = True
	self.ids.AutoButton.disabled = False
	self.ids.S1.disabled = True
	self.ids.S2.disabled = True
	self.ids.S3.disabled = True
	self.ids.S4.disabled = True
	mode = 1
	setMode(mode)
	self.ids.L5.text = "AUTOMATIC MODE ON!"
	while(True):

		temp1 = int(sheet2.cell(2,2).value.encode('utf-8'))
		temp2 = int(sheet2.cell(3,2).value.encode('utf-8'))
		temp3 = int(sheet2.cell(4,2).value.encode('utf-8'))
		temp4 = int(sheet2.cell(5,2).value.encode('utf-8'))

		if temp1 == 1:
			self.ids.S1.text = "OFF"
			return 'down'
		else:
			self.ids.S1.text = "ON"
			return 'normal'

		if temp2 == 1:
			self.ids.S2.text = "OFF"
			return 'down'
		else:
			self.ids.S2.text = "ON"
			return 'normal'

		if temp3 == 1:
			self.ids.S3.text = "OFF"
			return 'down'
		else:
			self.ids.S3.text = "ON"
			return 'normal'

		if temp4 == 1:
			self.ids.S4.text = "OFF"
			return 'down'
		else:
			self.ids.S4.text = "ON"
			return 'normal'


    def AutomaticSelection(self):
	print("AutomaticSelection called")
    	self.ids.ManButton.disabled = False
	self.ids.AutoButton.disabled = True
	self.ids.S1.disabled = False
	self.ids.S2.disabled = False
	self.ids.S3.disabled = False
	self.ids.S4.disabled = False
	mode = 0
	setMode(mode)
	self.ids.L5.text = "MANUAL MODE ON!"

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

    def getState1(self):
	print("GetState1 called")

	temp = int(sheet2.cell(2,2).value.encode('utf-8'))

	if temp == 1:
		self.ids.S1.text = "OFF"
		self.ids.S1.background_color = (0,1,0,1)
		return 'down'
	else:
		self.ids.S1.text = "ON"
		self.ids.S1.background_color = (1,0,0,1)
		return 'normal'

    def getState2(self):
	print("GetState2 called")	
	temp = int(sheet2.cell(3,2).value.encode('utf-8'))

	if temp == 1:
		self.ids.S2.text = "OFF"
		return 'down'
	else:
		self.ids.S2.text = "ON"
		return 'normal'

    def getState3(self):
	print("GetState3 called")	
	temp = int(sheet2.cell(4,2).value.encode('utf-8'))

	if temp == 1:
		self.ids.S3.text = "OFF"
		return 'down'
	else:
		self.ids.S3.text = "ON"
		return 'normal'
    def getState4(self):
	print("GetState4 called")	
	temp = int(sheet2.cell(5,2).value.encode('utf-8'))

	if temp == 1:
		self.ids.S4.text = "OFF"
		return 'down'
	else:
		self.ids.S4.text = "ON"
		return 'normal'


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
		self.ids.S4.text = "ON"
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
