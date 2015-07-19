
import pynotify

class Popup:
	def __init__(self,msg):
		self.d=gtk.MessageDialog(type=gtk.MESSAGE_WARNING,buttons=gtk.BUTTONS_NONE);
		self.d.set_markup(msg);
		self.d.show()
		self.d.connect("destroy",self.quit);

	def quit(self,widget):
		gtk.main_quit()

	def main(self):
		gtk.main()


class SysTray:
    def __init__(self):
        pynotify.init("PM")
        self.notify = pynotify.Notification("Initialising")
        self.notify.show()

    def popup(self,msg):
        self.notify.update(msg)
        self.notify.show()



