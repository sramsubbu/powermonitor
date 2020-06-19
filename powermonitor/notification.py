from abc import ABCMeta, abstractmethod

class Notification(metaclass=ABCMeta):
    APP_NAME = "powermonitor"
    
    @abstractmethod
    def notify_user(self, message):
        pass


class LinuxNotification(Notification):
    def __init__(self):
        import notify2
        notify2.init(self.APP_NAME)
        self.notifier = notify2.Notification(self.APP_NAME, message=f"{self.APP_NAME} running")
        self.notifier.show()
    
    def notify_user(self, message):
        self.notifier.update(self.APP_NAME, message=message)
        self.notifier.show()

    def close(self):
        self.notifier.close()



