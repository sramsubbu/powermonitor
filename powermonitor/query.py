import psutil


def get_status():
    return psutil.sensors_battery()
