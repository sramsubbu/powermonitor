import subprocess
from pathlib import Path

NOTIFICATION_SCRIPT_PATH = "{base_path}/macos/send_notification.sh"


class MacNotification:
    def __init__(self):
        self.APP_NAME = "powermonitor"
        self.cmd_script = self.get_script_path()

    def get_script_path(self):
        base_path = Path(__file__).parent.parent
        return NOTIFICATION_SCRIPT_PATH.format(base_path=base_path)

    def notify_user(self, message):
        subprocess.run(["bash", self.cmd_script, self.APP_NAME, message])


if __name__ == "__main__":
    obj = MacNotification()
    obj.notify_user("Test message")
