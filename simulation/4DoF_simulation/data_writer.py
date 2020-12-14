# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 2019

@author: Feng Zeyuan
@Contributors: CUHKSZ
"""

import time
import xlsxwriter
import random
from collections import deque
import globalvar as gl
import os




def run():
    global heading_angle
    global rudder
    global sail

   
    
    try:
        print('Starting Current Sensor')
        print('Collecting Sensor Values...')
        start = time.time() # Start Time
        sensor_times=0

        DataPoints = deque(maxlen=None) # Creating Array of datatype Deque to store values

        
        while True:   
            sensor_times=(sensor_times+1)%15         
            frequency=gl.get_value('frequency')
            if gl.get_value('flag'):
                
                break
            
            try:
                roll=float('{0:.2f}'.format(gl.get_value('roll')))
                ruddervalue= float('{0:.2f}'.format(gl.get_value('rudder')))
                sailvalue= float('{0:.2f}'.format(gl.get_value('sail')))
                currentvalue = round(gl.get_value('current')) # Rounding off values to nearest integer
                voltagevalue = float('{0:.1f}'.format(gl.get_value('voltage'))) # Floating point up to one decimal point
                powervalue = round(currentvalue*voltagevalue)
                timevalue = float('{0:.1f}'.format(time.time()-start)) # Elapsed time in Seconds with 1 decimal point floating number 
                headingvalue = float('{0:.2f}'.format(gl.get_value('heading_angle')))
                DataPoints.append([timevalue, ruddervalue, sailvalue, gl.get_value('x'),gl.get_value('y'),
                roll,headingvalue,gl.get_value('desired_angle'), 0,gl.get_value('v'),
                gl.get_value('u'),gl.get_value('p'),gl.get_value('w'),currentvalue, voltagevalue,powervalue,
                gl.get_value('keeping_state'),gl.get_value('tacking_angle'),gl.get_value('target_v')]) # Updating DataPoints Array
            except DeviceRangeError:
                print('Device Range Error')

            time.sleep(1/frequency) # Reading value after 0.5 second
        
    except:        
        print('Exception Occurred, Current Sensor Stopped \n')

    
    # Wt = input('Do you want to store the sensor values Y/N? ')

    # if Wt == 'Y':
    writing(DataPoints)
    # else:
    #     print('Ending without saving sensor data \n')

    print('Sensor Stopped!\n')
#------------------------------------------------

def writing(Data):
    print('Start writing data')
    file_name=input('Please input file name')
    target='target:[3,6]'
    
    runDate = time.ctime() 
    ##{'constant_memory': True},
    # workbook = xlsxwriter.Workbook('/data/%s.xlsx'%file_name,{'constant_memory': True})  # Creating XLSX File for Data Keeping 
    workbook = xlsxwriter.Workbook('%s.xlsx'%file_name,{'constant_memory': True})
    worksheet = workbook.add_worksheet() # Generating worksheet
    
    bold = workbook.add_format({'bold':True}) # Formating for Bold text

    worksheet.write('A1', 'Time', bold) # Writing Column Titles
    worksheet.write('B1', 'rudder', bold)
    worksheet.write('C1', 'sail', bold)
    worksheet.write('D1', 'x', bold)
    worksheet.write('E1', 'y', bold)
    worksheet.write('F1', 'roll', bold)
    worksheet.write('G1', 'Heading Angle', bold)
    worksheet.write('H1', 'desired yaw', bold)
    worksheet.write('I1', 'desired roll', bold)
    worksheet.write('J1', 'v', bold)
    worksheet.write('K1', 'u', bold)
    worksheet.write('L1', 'p', bold)
    worksheet.write('M1', 'w', bold)
    worksheet.write('N1', 'Current (mA)', bold)
    worksheet.write('O1', 'Voltage (v)', bold)
    worksheet.write('P1', 'Power (mW)', bold)
    worksheet.write('Q1', 'Keeping State', bold)
    worksheet.write('R1',"tacking angle",bold)
    worksheet.write('S1',"target v",bold)
    worksheet.write('T1', 'Start Time', bold)
    worksheet.write('T2', runDate)
    worksheet.write('T3', target)
    worksheet.write('T4', 'dM:1.8,dT:1')
    

    row = 1 # Starting Row (0 indexed)
    col = 0 # Starting Column (0 indexed) 
    

    n = len(Data) # Total number of rows
    print('Total number of rows: ',n)

    print('Writing Data into Worksheet')
        

    for values in (Data):
        # Writing Data in XLSX file
        i=0
        col=0
        for value in values:
            worksheet.write(row, col+i, value)
            i+=1
        row+=1

    
    workbook.close() # Closing Workbook 
    time.sleep(1)
    print('Sensor Writing successfull \n')
    
#-------------------------------------------------
# sensor()