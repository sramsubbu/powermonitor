from daemon import DaemonContext
from time import sleep

from .notification import notification_factory
from .query import get_status


LOW_BATTERY_MSG = "Battery is almost drained. Please plug in the charger"
BATTERY_FULL_MSG = "Battery is full. Please unplug the charger to save battery life"
SLEEP_INTERVAL = 5
BATTERY_FULL_THRESHOLD = 100
BATTERY_LOW_THRESHOLD = 15


def check_battery_status(notifier):
    status = get_status()
    if status.percent == BATTERY_FULL_THRESHOLD:
        if status.power_plugged:
            notifier.notify_user(BATTERY_FULL_MSG)
    if status.percent < BATTERY_LOW_THRESHOLD:
        if not status.power_plugged:
            notifier.notify_user(LOW_BATTERY_MSG)


def monitor_event_loop():
    notifier = notification_factory()
    notifier.notify_user("Started the app...")

    while True:
        check_battery_status(notifier)
        sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    monitor_event_loop()
