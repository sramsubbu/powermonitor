from abc import ABCMeta, abstractmethod
import platform

class Notification(metaclass=ABCMeta):
    APP_NAME = "powermonitor"
    
    @abstractmethod
    def notify_user(self, message):
        pass


def get_linux_notification():
    from .notify_linux import LinuxNotification
    return LinuxNotification()

def get_windows_notification():
    from .notify_windows import WindowsNotification
    return WindowsNotification()


def notification_factory():
    notification_factory_dict = {
        "Linux": get_linux_notification,
        "Windows": get_windows_notification
    }
    system = platform.system()
    try:
        action = notification_factory_dict[system]
    except KeyError:
        raise RuntimeError(f"Platform '{system}' is not supported")
    return action()


