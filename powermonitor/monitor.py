#! /usr/bin/env python
from popup import Popup, SysTray
from time import sleep
import thread

path="/sys/class/power_supply/BAT0/";
def get_battery_power():
	"""gets the power level of the battery [in percent]"""
	global path;
	filename=path+"energy_full";
	fp=open(filename,"r");
	full=int(fp.read());
	fp.close();
	filename=path+"energy_now";
	fp=open(filename,"r")
	now=int(fp.read());
	charge=( float(now)*100 )/float(full);
	return charge;

def get_battery_status():
	"""get the status of battery [charging/charged/discharging]"""
	global path;
	filename=path+"status";
	fp=open(filename)
	status=fp.read()
	fp.close()
	return status.rstrip();

def popup(msg):
    """
	p=Popup(msg);
	p.main()
        """
    o = SysTray()
    o.popup(msg)
        

if __name__=="__main__":
	while(True):
            try:
		charge=int(get_battery_power())
		status=get_battery_status()
		if charge == 100 and status != "Discharging":
			popup("Battery Full. Unplug the charger.")
		elif charge <=10 and status == "Discharging":
			popup("Battery Low. Plug in charger. ");
		sleep(20);	
            except KeyboardInterrupt:
                print "Quitting"
                break
	

