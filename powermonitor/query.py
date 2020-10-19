from abc import ABCMeta, abstractmethod
from pathlib import Path

import ctypes
import platform

class PowerStatus(metaclass=ABCMeta):
    CHARGING = 1
    DISCHARGING = 2
    @abstractmethod
    def get_adapter_status(self):
        pass

    @abstractmethod
    def get_battery_power(self):
        pass


class LinuxPowerStatus(PowerStatus):
    def __init__(self):
        self.base_path = Path("/sys/class/power_supply/")

    def _get_device_path(self):
        devices = list(self.base_path.iterdir())
        battery_devices = []
        for device in devices:
            with open(device/"type") as fp:
                content = fp.read().strip()
                if content == 'Battery':
                    battery_devices.append(device)
        return battery_devices[0]

    def _get_device_events(self):
        device_path = self._get_device_path()
        with open(device_path / "uevent") as fp:
            contents = fp.read()
        events = contents.splitlines()
        events = [event.strip() for event in events]
        events = [event.split('=') for event in events]
        events = dict(events)
        return events

    def dump(self):
        events = self._get_device_events()
        battery_events = {name.title():value for name, value in events.items()}
        return battery_events

    def get_battery_power(self):
        battery_events = self._get_device_events()
        full_charge = battery_events['POWER_SUPPLY_CHARGE_FULL']
        current_charge = battery_events['POWER_SUPPLY_CHARGE_NOW']
        charge_percent = ( float(current_charge) / float(full_charge) ) * 100
        charge_percent = round(charge_percent, 3)
        return charge_percent
        

    def get_adapter_status(self):
        battery_events = self._get_device_events()
        adapter_status = battery_events['POWER_SUPPLY_STATUS'].strip()
        return adapter_status
        


class WindowsPowerStatus(PowerStatus):
    def _get_details(self):
        import ctypes
        from ctypes import wintypes

        class SYSTEM_POWER_STATUS(ctypes.Structure):
            _fields_ = [
                ('ACLineStatus', wintypes.BYTE),
                ('BatteryFlag', wintypes.BYTE),
                ('BatteryLifePercent', wintypes.BYTE),
                ('Reserved1', wintypes.BYTE),
                ('BatteryLifeTime', wintypes.DWORD),
                ('BatteryFullLifeTime', wintypes.DWORD),
            ]

        SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)

        GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
        GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
        GetSystemPowerStatus.restype = wintypes.BOOL

        status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(ctypes.pointer(status)):
            raise ctypes.WinError()
        details = {
            'Charging': bool(status.ACLineStatus),
            'BatteryPercent': status.BatteryLifePercent
        }
        return details

    def get_adapter_status(self):
        details = self._get_details()
        return details['Charging']

    def get_battery_power(self):
        details = self._get_details()
        return details['BatteryPercent']


def power_status_factory():
    status_class_dict = {
        'Linux': LinuxPowerStatus,
        'Windows': WindowsPowerStatus
    }
    system = platform.system()
    try:
        klass = status_class_dict[system]
    except KeyError:
        raise RuntimeError(f"Platform '{system}' not supported") from None
    else:
        return klass()
