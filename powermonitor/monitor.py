
from time import sleep

from .notification import notification_factory
from .query import power_status_factory

import logging

def monitor_event_loop():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s')
    SLEEP_INTERVAL = 5
    BATTERY_FULL_MSG = 'Battery is full. Please unplug the charger to save battery life'
    LOW_BATTERY_MSG = 'Battery is almost drained. Please plug in the charger'
    LOW_BATTER_LEVEL = 15
    power = power_status_factory()
    notifier = notification_factory()
    while True:
        adapter_status = power.get_adapter_status()
        power_level = power.get_battery_power()
        if adapter_status == 'Full':
            notifier.notify_user(BATTERY_FULL_MSG)
        elif adapter_status == 'Discharging':
            level = int(power_level)
            if level <= LOW_BATTER_LEVEL:
                notifier.notify_user(LOW_BATTERY_MSG)
        logging.info(f"Battery status: {adapter_status}")
        logging.info(f"Current battery level: {power_level}")
        sleep(SLEEP_INTERVAL)


def main():
    from daemon import DaemonContext
    with DaemonContext():
        monitor_event_loop()


if __name__ == "__main__":
    main()
