# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:40:40 2019

@author: MARTIJ

This script is to test loading the RF switch parameters from a configuration file
"""
import RFSwitchControl

#### =============================================================================
#### Code to load the configuration file and pull parameters
#### =============================================================================

### load function 
def load_config(filename='config.sample'):
    import os  
    import configparser
    config = configparser.ConfigParser()
    this_dir = os.path.abspath(os.path.dirname(__file__))
    config.read(this_dir + '/' + filename)
    if config.has_section('TestConfig'):
        return {name:val for (name, val) in config.items('TestConfig')}
    else:
        print ('Unable to read file %s with section TestConfig', filename)
        print ('Make sure a file named config lies in the directory %s',  this_dir)
        raise Exception('Unable to find config file')
   
config=load_config()         ### calls load function
path=str(config['path'])     ### pulls parameters


#### =============================================================================
#### Set RF switch to port positions depending on 
####   setting pulled from config file
#### =============================================================================

if path == 'lab1':
    RFSwitchControl.setSwitch(1,1,1,1,2,2,1,1,'10.169.7.15')
elif path == 'lab2':
    RFSwitchControl.setSwitch(1,1,1,1,1,1,1,1,'10.169.7.15')
elif path == 'ota1':
    RFSwitchControl.setSwitch (1,2,1,1,1,1,1,2,'10.230.2.160') 
elif path == 'ota2':
    RFSwitchControl.setSwitch (1,1,1,2,1,1,2,1,'10.230.2.160')
elif path == 'ota3':
    RFSwitchControl.setSwitch (1,1,1,1,1,1,1,1,'10.230.2.160')



