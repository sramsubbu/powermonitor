""" queries the files in /sys filesystem to get the details of the battery"""
#import popup
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

def get_technology():
	"""get the technology of the battery [ex Li-ion]"""
	global path;
	filename=path+"technology";
	fp=open(filename,'r')
	tech=fp.read()
	fp.close()
	return tech.rstrip()


def get_model():
	""" get the model of the battery"""
	global path;
	filename=path+"model_name";
	fp=open(filename,'r');
	model=fp.read()
	fp.close()
	return model.rstrip()

