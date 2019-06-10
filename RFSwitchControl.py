# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 08:39:39 2019

@author: MARTIJ

template to connect to mini-circuits RF switch over Ethernet
and set the switch port positions
specifically set up for model RC-8SPDT-A18 which has 8 switch ports (a-h)

"""

import urllib.request
import sys


#### =============================================================================
#### Function takes the parameters for each switch position and the IP and sets the positions
#### There are input parameters at the bottom of the code that need to be commented out before  
####   before importing this code into another script
#### =============================================================================
def setSwitch(a,b,c,d,e,f,g,h,rfsw_ip):

    #### =============================================================================
    #### Function to send commands to the RF switch
    #### =============================================================================
    def Get_HTTP_Result(CmdToSend):
         ### Specify the IP address
         CmdToSend = "http://"+rfsw_ip+"/" + CmdToSend
         
         ### Send the HTTP command and try to read the result
         try:
             HTTP_Result = urllib.request.urlopen(CmdToSend)
             PTE_Return = HTTP_Result.read()
             
             ### The switch displays a web GUI for unrecognized commands
             if len(PTE_Return) > 100:
                 print ("Error, command not found:", CmdToSend)
                 PTE_Return = "Invalid Command!"
                 
         ### Catch an exception if URL is incorrect (incorrect IP or disconnected)
         except:
              print ("Error, no response from device; check IP address and connections.")
              PTE_Return = "No Response!"
              sys.exit() # Exit the script
             
         return PTE_Return
    
    
    #### =============================================================================
    #### set the switchport values 
    #### =============================================================================
    
    ###changes input parameter so it is readable by the device
    aIn = str(a-1)
    bIn = str(b-1)
    cIn = str(c-1)
    dIn = str(d-1)
    eIn = str(e-1)
    fIn = str(f-1)
    gIn = str(g-1)
    hIn = str(h-1)
    
    ### sends inputs to the switch
    #### When setting the switches positions here vs in the parameters section -  com->1=0 and com->2=1
    Get_HTTP_Result('SETA='+aIn)
    Get_HTTP_Result('SETB='+bIn)
    Get_HTTP_Result('SETC='+cIn)
    Get_HTTP_Result('SETD='+dIn)
    Get_HTTP_Result('SETE='+eIn)
    Get_HTTP_Result('SETF='+fIn)
    Get_HTTP_Result('SETG='+gIn)
    Get_HTTP_Result('SETH='+hIn)
    
    
    #### =============================================================================
    #### function to interpret the switch port values and print the results
    #### this section can be commented out and the program still works, only needs to be used 
    #### for verification purposes
    ####=============================================================================
    def Interpret_Switch_Port(Sw_Port, NoSwitches):
        ### Converts decimal switch port value into bits, each indicating a switch state
        ### NoSwitches should be set to the number of switches available (eg: 3 for RC-3SPDT-A18)
        
        ### Set the initial values
        Last_Remainder = int(Sw_Port)
        Sw_State = int(0)
        This_Remainder = int(0)
        First_Loop = True
        Sw_State_List = []  
        
        ### Loop for each switch
        for n in range(NoSwitches, -1, -1):
    
             ### Calculate each switch state by comparing to the byte value and the previous states
             This_Remainder = Last_Remainder - (Sw_State * (2**(n+1)))
             Sw_State = int(This_Remainder / 2**n)
             Last_Remainder = This_Remainder
            
             if First_Loop == False: ### Ignore the first pass as it doesn't relate to a switch
                Sw_State_List.append(Sw_State) ### Add each switch state to a list
                
             First_Loop = False
                
        return Sw_State_List
    
    
    ### Print the model number and serial number
    mn = Get_HTTP_Result("MN?")
    sn = Get_HTTP_Result("SN?")
    print ("Switch", mn, "/", sn)
    
    
    #### Checks the current position of each switchport and prints it out 
    #### Switchport states are not the switch position - 0=com->1 and 1=com->2
    #### Information does not come from the script inputs, it comes from querying the device
    
    Switch_States = Interpret_Switch_Port(Get_HTTP_Result("SWPORT?"), 8) 
    print ("Switchport positions are com->1=0 and com->2=1" )
    print ("Switch A =", Switch_States[7], "Switch B =", Switch_States[6], "Switch C =", Switch_States[5])
    print ("Switch D =", Switch_States[4], "Switch E =", Switch_States[3], "Switch F =", Switch_States[2])
    print ("Switch G =", Switch_States[1], "Switch H =", Switch_States[0])

    
#setSwitch (1,1,1,1,1,1,1,1,'10.230.2.160')  ### OTA path 3
#setSwitch (1,2,1,1,1,1,1,2,'10.230.2.160')  ### OTA path 1
#setSwitch (1,1,1,2,1,1,2,1,'10.230.2.160')  ### OTA path 2
#setSwitch(1,1,1,1,1,1,1,1,'10.169.7.15')   ### lab Path 2
#setSwitch(1,1,1,1,2,2,1,1,'10.169.7.15')   ### lab Path 1


