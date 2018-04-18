#This module contains the code for controlling devices by giving output to GPIO pins.
#when the mode will be automatic we will take data from sensors and on the basis of sensor
#outout we will decide which appliances we want to turn on and which ones to turn off.
#when the mode will be manual this code will fetch data from Google Sheets given by user and give the output
#on GPIO pins accordingly. 


#import gspread for manipulating google spreadsheets, RPi.GPIO for using GPIO functions, 
#ServiceAccountCredentials from oauth2client.service_account for authorising access to API

import gspread
import RPi.GPIO as GPIO
import time
from threading import Thread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds' , 'https://www.googleapis.com/auth/drive']

#secret key for accessing account is present in client_secret.json file
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

#authorise access using credentials
client = gspread.authorize(creds)

#open all the sheets (Client, Status, Mode)
sheet1 = client.open('Client').sheet1
sheet2 = client.open('Status').sheet1
sheet3 = client.open('Mode').sheet1

#variables denoting the state of appliances
global L1,L2,F1,F2,mode

#function for printing the rows of given sheet, sheet name should be passed as arguments.
def printSheet(sheet) :
    row_count=len(sheet.get_all_records())+1
    for i in range(row_count) :
        RowInfo = sheet.row_values(i+1)
        print(RowInfo)


#GPIO.BCM option means that you are referring to the pins by the 'Broadcom SOC channel'
GPIO.setmode(GPIO.BCM)

#setting pins 4, 17, 23, 24 of Raspberry Pi's GPIO pins in GPIO.OUT mode so devices connected to them can act as 
#output devices
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)

#fetching current mode from Mode spreadsheet, mode 1 denotes manual mode and mode 0 denotes automatic mode.
mode = int(sheet3.cell(1,2).value.encode('utf-8'))

#lux contains the output of Light sensor, temperature contains the output of temperature sensor, lux_thresh1 and lux_thresh2
#are the thresholds for lux so we can decide below what level we have to turn lights on and either one or both of them
#should be turned on, and above what level we have to turn them off.
#Same is for temp_thresh1, temp_thresh2
#no_of_person contains the number of persons present in the room. We are calculating it by subutracting the no of persons exiting 
#the room from the number of people entered in room 
global lux, temperature, lux_thresh1, lux_thresh2, temp_thresh1, temp_thresh2, no_of_person

lux = 0
temperature = 0
lux_thresh1 = 400
lux_thresh2 = 200
temp_thresh2 = 20
temp_thresh1 = 30
no_of_person = 0

#setitng pin 8, 21 of Raspberry Pi's GPIO pins in GPIO.IN mode so devices connected to them can act as input devices.
#we are going to use these pins for connecting sensors.
#pin 8 and 21 is for entry PIR Sensor and exit PIR sensor respectively.
GPIO.setup(8,GPIO.IN)
GPIO.setup(21,GPIO.IN)

#function for continuosly calculating the number of person entering in room.
def PIR_Sensor():
        global no_of_person
        time.sleep(2)
        while True:
                if(GPIO.input(8)):
                        no_of_person += 1
                        print("no of person = ", no_of_person)
                        time.sleep(6)

#this function will continuous check the mode, it will continuously fetch the input given given by the user
# using google spreadsheet and will change state of devices accordingly using GPIO pins. And if the mode changes to automatic
#it will stop doing the above written functionality. This function will work for manual mode.
def t1():
                global mode
                print("t1")
                print(mode)
                while True:
                        if(mode == 1):
                                mode = int(sheet3.cell(1,2).value.encode('utf-8'))
                                time.sleep(2)

                                L1 = int(sheet1.cell(2,2).value.encode('utf-8'))
                                L2 = int(sheet1.cell(3,2).value.encode('utf-8'))
                                F1 = int(sheet1.cell(4,2).value.encode('utf-8'))
                                F2 = int(sheet1.cell(5,2).value.encode('utf-8'))

                                GPIO.output(4,L1)
                                GPIO.output(17,L2)
                                GPIO.output(23,F1)
                                GPIO.output(24,F2)

                                print(L1,L2,F1,F2)

#This code will execute in automatic mode. This function will continuously fetch the mode, and it will continuously fetch data 
#from sensors and will change the status of devices automatically.
def t2():
        global mode
        global no_of_person
        global temperature
        global lux
        global lux_thresh1, lux_thresh2, temp_thresh1, temp_thresh2

        print(mode)
        while True:
                if(mode == 0):
                       mode = int(sheet3.cell(1,2).value.encode('utf-8'))
                        time.sleep(2)
                        L1 = 0
                        L2 = 0
                        F1 = 0
                        F2 = 0
                        if(no_of_person >= 1):
                                if(temperature <= temp_thresh1 and temperature >= temp_thresh2):
                                        F1 = 1
                                elif(temperature > 30) :
                                        F1 = 1
                                        F2 = 1
                                if(lux <= lux_thresh1 and lux >= lux_thresh2):
                                        L1 = 1
                                elif(lux < lux_thresh2):
                                        L1 = 1
                                        L2 = 1


                        GPIO.output(4,L1)
                        GPIO.output(17,L2)
                        GPIO.output(23,F1)
                        GPIO.output(24,F2)

                        sheet2.update_cell(2,2,L1)
                        sheet2.update_cell(3,2,L2)
                        sheet2.update_cell(4,2,F1)
                        sheet2.update_cell(5,2,F2)


Thread(target=t1).start()
Thread(target=t2).start()
Thread(target = PIR_Sensor).start()






