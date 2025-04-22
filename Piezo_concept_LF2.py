import serial
import time
import os
import subprocess

"""
Author: Ozora Iso
Contact: ootyanfmarinos04@gmail.com
Date: 2025-04-22
Purpose: This program manipulate the Piezo Concept nanopositioning system
         (Author checked the operation with LF2:100)
"""

class Piezoconcept():
    # Open the serial connection
    '''
    A class for the Piezo concept nanopositioning system    
    '''
    def __init__(self, port=None):
        #self.termination_character = '\n'
        self.ser = serial.Serial(
            port=port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
            timeout=1  # Timeout in seconds
        )

        self.position_x = 0.0
        self.position_y = 0.0

    def close(self):
        self.ser.close()
        
    def MOVRX(self, value, unit="n"):
        '''
        A command for relative movement, where the default units is nm
        '''
        MOVRX_cmd = "MOVRX "+str(value)+unit+"\n"
        self.ser.write(MOVRX_cmd.encode('utf-8'))

    def MOVRY(self, value, unit="n"):
        '''
        A command for relative movement, where the default units is nm
        '''
        if unit == "n":
            multiplier=1
        if unit == "u":
            multiplier=1E3

        ''' concatenate the command letter '''
        MOVRY_cmd = "MOVRY "+str(value)+unit+"\n"
        self.ser.write(MOVRY_cmd.encode('utf-8'))

    def MRXYZ(self, value_x, value_y, value_z=0, unit="n"):
        '''
        A command for relative movement in all axes, where the default units is nm
        '''
        MRXYZ_cmd = "MRXYZ "+str(value_x)+unit+" "+str(value_y)+unit+" "+str(value_z)+unit+"\n"
        self.ser.write(MRXYZ_cmd.encode('utf-8'))
        
    def MOVEX(self, value, unit="n"):
        '''
        An absolute movement command, will print an error to the console 
        if you moveoutside of the range(100um) default unit is nm
        '''
        MOVEX_cmd = "MOVEX "+str(value)+unit+"\n"
        self.ser.write(MOVEX_cmd.encode('utf-8'))

    def MOVEY(self, value, unit="n"):
        '''
        An absolute movement command, will print an error to the console 
        if you moveoutside of the range(100um) default unit is nm
        '''
        MOVEY_cmd = "MOVEY "+str(value)+unit+"\n"
        self.ser.write(MOVEY_cmd.encode('utf-8'))

    def MOXYZ(self, value_x, value_y, value_z=0, unit="n"):
        '''
        An absolute movement command, will print an error to the console 
        if you moveoutside of the range(100um) default unit is nm
        '''
        MOXYZ_cmd = "MOXYZ "+str(value_x)+unit+" "+str(value_y)+unit+" "+str(value_z)+unit+"\n"
        self.ser.write(MOXYZ_cmd.encode('utf-8'))
        
            
    def recenter(self):
        '''
        Moves the stage to the center position
        '''
        self.MOVEX(50,unit = "u")
        self.MOVEY(50,unit = "u")
        self.GET_X()
        self.GET_Y()

    def GET_X(self):
        self.ser.write(b'GET_X\n')

        while True:
            GET_X_return = self.ser.readline().decode('utf-8',errors='ignore').strip()
            if GET_X_return and GET_X_return[-1] == "m":
                print("X position: " + str(GET_X_return))
                break

    def GET_Y(self):
        self.ser.write(b'GET_Y\n')
        '''
        Repeat until the GET_Y command return the Y position
        '''
        while True:
            GET_Y_return = self.ser.readline().decode('utf-8',errors='ignore').strip()
            if GET_Y_return and GET_Y_return[-1] == "m":
                print("Y position: " + str(GET_Y_return))                
                break

    def GEXYZ(self):
        '''
        This function works in the same as GET_X
        but allows to acquire the position of the 3 axis at the same time
        '''
        self.ser.write(b'GEXYZ\n')

        while True:
            GEXYZ_return = self.ser.readline().decode('utf-8',errors='ignore').strip()
            print(GEXYZ_return)
            if GEXYZ_return == "Third Axis :":
                break

    def STIME(self, value_time, unit="m"):
        '''
        This command allows the modification of the time between 2 points
        which are sent by the RAM memory of the USB interface to the nanopositioner
        '''
        STIME_cmd = "STIME "+str(value_time)+unit+"\n"
        self.ser.write(STIME_cmd.encode('utf-8'))

    def SHTIM(self, value_time, unit="m"):
        '''
        This command allows you to set the shooting time of your acquisition when
        using the CHAIO function with the prefix t. The TTL pulses will then be set
        to the optimal position
        '''
        SHTIM_cmd = "SHTIM "+str(value_time)+unit+"\n"
        self.ser.write(SHTIM_cmd.encode('utf-8'))
        
    def GTIME(self):
        '''
        This command allows you to know the time between each point
        '''
        self.ser.write(b'GTIME\n')

        while True:
            GTIME_return = self.ser.readline().decode('utf-8',errors='ignore').strip()
            print(GTIME_return)
            if GTIME_return and GTIME_return[-1] == 's':
                break

    def SWF_X(self, steps=100, start=0, unit_start="m", end=0, unit_end="m"):
        '''
        THis command allows you to set up a ramp waveform form the X axis.
        Example: "SWF_X" loads a waveform of 100 equal sized steps from 0u to 100u
        '''
        SWF_X_cmd = "SWF_X "+str(steps)+" "+str(start)+unit_start+" "+str(end)+unit_end+"\n"
        self.ser.write(SWF_X_cmd.encode('utf-8'))

    def SWF_X(self, steps=100, start=0, unit_start="m", end=0, unit_end="m"):
        '''
        This command allows you to set up a ramp waveform form the X axis.
        Example: "SWF_Y" loads a waveform of 100 equal sized steps from 0u to 100u
        '''
        SWF_Y_cmd = "SWF_Y "+str(steps)+" "+str(start)+unit_start+" "+str(end)+unit_end+"\n"
        self.ser.write(SWF_Y_cmd.encode('utf-8'))

    def RUNWF(self):
        '''
        This command allows to launch the scan defined by the function SWF_X, SWF_Y, and SWF_Z.
        X axis is the first axis. Y axis is the second axis. Z axis is the third axis.
        One should write <<RUNWF>>
        '''
        self.ser.write(b'RUNWF\n')

    def RUXYZ(self):
        '''
        This command is the same as RUNWF but also works for all axies in every sequences
        Example: RUZXY, RUYXZ, ...
        '''
        self.ser.write(b'RUXYZ\n')

    def RUXY_(self):
        '''
        This command is the same as RUNWF but works for 2 axes in every sequences.
        Example: RUZX_, RUYX_,...
        '''
        self.ser.write(b'RUXY_\n')

    def RUX__(self):
        '''
        This command is the same as RUNWF but works only for 1 axis in all orders
        '''
        self.ser.write(b'RUX__\n')

    def RUY__(self):
        '''
        This command is the same as RUNWF but works only for 1 axis in all orders
        '''
        self.ser.write(b'RUY__\n')

    def RUZ__(self):
        '''
        This command is the same as RUNWF but works only for 1 axis in all orders
        '''
        self.ser.write(b'RUZ__\n')

    def REXYZ(self):
        '''
        This command is the same as RUXYZ and RUXZ_
        but with the first axis going back and forth
        '''
        self.ser.write(b'REXYZ\n')

    def REXY_(self):
        '''
        This command is the same as RUXYZ and RUXZ_
        but with the first axis going back and forth
        '''
        self.ser.write(b'REXY_\n')

    def SWF_A(self, repeat_num=2):
        '''
        It is possible to run the RUXYZ several but defining an arbitrary value called A.
        The value you will give to A will allow to define the number of repetition of a RUXYZ function,
        by using RXYZA
        '''
        SWF_A_cmd = "SWF_A "+str(repeat_num)+"\n"
        self.ser.write(SWF_A_cmd.encode('utf-8'))

    def RXYZA(self):
        '''
        THis command allows to repeat several times
        '''
        self.ser.write(b'RXYZA\n')

    def PAUSE(self):
        '''During a move with RUNWF,RUX__,RUXY_,RUXYZ or RUN3D,
        this function allows you to pause it
        '''
        self.ser.write(b'PAUSE\n')

    def PLAYY(self):
        '''During a move with RUNWF,RUX__,RUXY_,RUXYZ or RUN3D,
        this function allows you to restart it
        '''
        self.ser.write(b'PAUSE\n')

    def STOPP(self):
        '''
        During a move with RUNWF,RUX__,RUXY_,RUXYZ or RUN3D,
        this function allows you to stop it
        '''
        self.ser.write(b'STOPP\n')

    def ARB3D(self, alloc_points=10):
        '''
        This command parepares the controller for receiving a sequence of arbitrary 3D locations.
        Data storage is allocated for the data when ARB3D is executed, data points must then be
        loaded using ADD3D. The maximum number of 3D corrdinate that can be allocated is about 2000.
        '''
        ARB3D_cmd = "ARB3D "+str(alloc_points)+"\n"
        self.ser.write(ARB3D_cmd.encode('utf-8'))

    def RUN3D(self):
        '''
        THis command runs the stored sequence of 3D locations.
        Example: <<RUN3D>>
        '''
        self.ser.write(b'RUN3D\n')

    def ADD3D(self, posi_x, posi_y, posi_z=0, unit="u"):
        '''
        This command allows adding a 3D location to the 3D position list.
        Example: <<ADD3D 10u 10u 0u>> This command alloctes storage for one location.
        Specify all axes locations using the same number format as MOVEX
        '''
        ADD3D_cmd = "ADD3D "+str(posi_x)+unit+" "+str(posi_y)+unit+" "+str(posi_z)+unit+"\n"
        self.ser.write(ADD3D_cmd.encode('utf-8'))
        print(ADD3D_cmd)
        
    def ARBWF(self, x=0, y=0, z=0):
        '''
        This command prepares the controller for receiving arbitrary waveform data.
        Data sotrage is allocated for the data when ARBWF is executed,
        data points musb then be loaded using ADDPn
        Example: <<ARBWF 100 20 10>> This allocates storage for 100 X axis data points,
        20 Y axis data points and 10 Z axis data point
        '''
        ARBWF_cmd = "ARBWF "+str(x)+" "+str(y)+" "+ str(z)+"\n"
        self.ser.write(ARBWF_cmd.encode('utf-8'))

    def ADDPX(self, x=0, unit="u"):
        '''
        This command allows adding of data points to a waveforms.
        This command is only valid when used after ARBWF has been used to allocate
        data storage for the appropriate waveform data
        '''
        ADDPX_cmd = "ADDPX "+str(x)+unit+"\n"
        self.ser.write(ADDPX_cmd.encode('utf-8'))

    def ADDPY(self, y=0, unit="u"):
        '''
        This command allows adding of data points to a waveforms.
        This command is only valid when used after ARBWF has been used to allocate
        data storage for the appropriate waveform data
        '''
        ADDPY_cmd = "ADDPY "+str(y)+unit+"\n"
        self.ser.write(ADDPY_cmd.encode('utf-8'))
        
    def _RAZ_(self):
        '''
        This commands set all the outputs of the DAC to 0V
        '''
        self.ser.write(b'_RAZ_\n')

    def REOFF(self):
        '''
        This function allows to disable the answers of the controller in order to reduce the latency.
        Warning: with this function the controller will not give answer until you reactive it with RE_ON.
        The only command which will give an answer will be "INFOS" adn "SERIE"
        '''
        self.ser.write(b'REOFF\n')
        
    def RE_ON(self):
        '''
        This function allows you to activate the answers of the controller when it has been
        previously
        '''
        self.ser.write(b'RE_ON\n')
        
    def INFOS(self):
        self.ser.write(b'INFOS\n')
        while True:
            INFOS_line = self.ser.readline().decode('utf-8',errors='ignore').strip()
            print(INFOS_line)

            if INFOS_line == "Travel range Y : 100 m":  # or any other condition
                break
            
    def HELP_(self):
        self.ser.write(b'HELP_\n')
        while True:
            HELP_line = self.ser.readline().decode('utf-8',errors='ignore').strip()
            print(HELP_line)

            if HELP_line == "To exit the help menu please write QUITT":  # or any other condition
                break                    

    def DISIO(self, TTL_port=1):
        '''
        This command displays the setyp of the TTL ports.
        DISIO must be used with a TTL port number (1-4)
        '''
        DISIO_cmd = "DISIO "+str(TTL_port)+"\n"
        self.ser.write(DISIO_cmd.encode('utf-8'))
        while_stop_word = {"axis1", "axis2", "axis3"} #Key word to stop readline()
        
        while True:
            DISIO_line = self.ser.readline().decode('utf-8',errors='ignore').strip()
            print(DISIO_line)

            if DISIO_line.lower() in while_stop_word:
                break

    def CHAIO(self, parameter=""):
        '''
        This command allows setting the parameters of the 4 TTL IO ports.

        Format of disable commands:
        <<CHAIO [channel]d>> where [channel] is TTL port 1-4
        
        Format of Input commands:        
        <<CHAIO [channel]i[axis][modifier]>>where
        [channel] is TTL port 1-4,
        [axis] is the axis to trigger 1-3 and
        [modifier] is either 'f' or 'r' designating triggering of the axis
        occurring on falling or rising edge of the TTL signal respectively.
        Example: <<CHAIO 1i1r>> Sets TTL 1 as an input, triggering motion
        on the 1st axis on the rising edge

        Format of Output commands:
        <<CHAIO [channel]o[axis][modifier]>>where
        [channel] is TTL port 1-4,
        [axis] is the axis that generates TTL pulses
        [modifier] is either 's' or 'e' designating TTL pulses occurring
        at the start or end of motion respectively
        Example: <<CHAIO 1o1s>> Sets TTL 1 as an outpu, providing pulses
        at the starts of motion of the first axis

        Format of Ouptut on a given step number:
        <<CHAIO [channel]o[axis]n[step number]>>where
        [channel] is TTL port 1-4,
        [axis] is the axis that generates TTL pulses
        'n' designating step number is to be provided.

        Format of TL signal output
        <<CHAIO [channel]o[axis]g[start step number]-[end step number]>> where
        [channel] is TTL port 1-4,
        [axis] is the axis that generates TTL pulses
        'g' designating TTL gate behaviour
        [start step number] is an integer number within the step range as specified
        in ARBWF or SWF_n commands (e.g. for a wavefrom of 50 steps, the valid range
        of step numbers is 0-49
        '''
        CHAIO_cmd = "CHAIO "+parameter+"\n"
        self.ser.write(CHAIO_cmd.encode('utf-8'))        
            
if __name__ == "__main__":
    '''
    Basic test, should open the Z stage and print its info before closing. 
    Obvisouly the comport has to be correct!
    '''
    subprocess.run(['sudo', 'chmod', '777', '/dev/ttyUSB2']) # Change permission on the port with root user
    Stage = Piezoconcept(port = '/dev/ttyUSB2')

    '''Test for INFOS'''
    # Stage.INFOS()

    '''Test for MOVRX'''
    # Stage.GET_X()
    # Stage.MOVRX(-1,"u")
    # time.sleep(1)
    # Stage.GET_X()

    '''Test for MOVRY'''
    # Stage.GET_Y()
    # Stage.MOVRY(+1,"u")
    # time.sleep(1)
    # Stage.GET_Y()

    '''Test for recentre'''
    # Stage.recenter()

    '''Test for MOVEX'''
    # Stage.GET_X()
    # Stage.MOVEX(90,"u")
    # time.sleep(1)
    # Stage.GET_X()
    
    '''Test for MOVEY'''
    # Stage.GET_Y()
    # Stage.MOVEY(90, "u")
    # time.sleep(1)
    # Stage.GET_Y()

    '''Test for HELP_ '''
    # Stage.HELP_()

    '''Test for MOVEXYZ'''
    # Stage.GET_X()
    # Stage.GET_Y()
    # Stage.MOXYZ(30, 30, 0, "u") #Z value should be 0 as LF2 is 2-Axis stage
    # time.sleep(1)
    # Stage.GET_X()
    # Stage.GET_Y()

    '''Test for MRXYZ'''
    # Stage.GET_X()
    # Stage.GET_Y()
    # Stage.MRXYZ(1, 1, 0, "u") #Z value should be 0 as LF2 is 2-Axis stage
    # time.sleep(1)
    # Stage.GET_X()
    # Stage.GET_Y()

    '''Test for GEXYZ'''
    # Stage.GEXYZ()
    # Stage.MOVRX(1,"u")
    # Stage.MOVRY(2,"u")
    # time.sleep(1)
    # Stage.GEXYZ()

    '''Test for GTIME'''
    # Stage.GTIME()

    '''Test for STIM'''
    # Stage.GTIME()
    # Stage.STIME(10, "m")
    # time.sleep(1)
    # Stage.GTIME()

    '''Test for SHTIM'''
    # Stage.GTIME()
    # Stage.SHTIM(50,"u")
    # time.sleep(1)
    # Stage.GTIME()

    '''Test for _RAZ_'''
    # Stage._RAZ_()

    '''Test for SWF_X'''
    # Stage.GET_X()
    # Stage.SWF_X(100, 0, "u", 100, "u")
    # time.sleep(10)
    # Stage.GET_X()

    '''Test for SWF_Y'''
    # Stage.GET_Y()
    # Stage.SWF_X(100, 0, "u", 100, "u")
    # time.sleep(1)
    # Stage.GET_Y()

    '''Test for RUNWF'''
    #Stage.RUNWF()

    '''Test for RUXYZ'''
    #Stage.RUXYZ()

    '''Test for RUXY_'''
    # Stage.RUXY_()

    '''Test for RUX__ and RUY__'''
    # Stage.RUX__()
    # Stage.RUY__()
    
    '''Test for DISIO'''
    # Stage.DISIO(1)

    '''Test for ARBWF'''
    # Stage.ARBWF(p10, 10, 10)

    '''Test for ADDPX'''
    # Stage.ARBWF(10, 10, 10)    
    # Stage.ADDPX(100, "u")

    '''Test for ADDPY'''
    # Stage.ARBWF(10, 10, 10)        
    # Stage.ADDPY(100, "u")

    '''Test for REXYZ and REXY_'''
    # Stage.REXYZ()
    # Stage.REXY_()

    '''Test for SWF_A and RXYZA'''
    # Stage.SWF_A(10)
    # Stage.RXYZA()

    '''Test for PAUSE PLAYY and STOPP'''
    # Stage.PAUSE()
    # Stage.PLAYY()
    # Stage.STOPP()

    '''Test for allocation point'''
    # Stage.ARB3D(10)
    # Stage.ADD3D(20, 10, 10, "u")
    # Stage.RUN3D()

    '''Test for CHAIO'''
    Stage.CHAIO("1o1s")
    Stage.DISIO(TTL_port=1)
    Stage.CHAIO("2o2s")
    Stage.DISIO(TTL_port=2)
    
    Stage.close()
