from pathlib import Path
import psutil
import wmi
import json


class ExtractSystem:
    def __init__(self):
        c = wmi.WMI()
        cpu = c.Win32_Processor()[0].Name
        ram = round(psutil.virtual_memory().total / (1024**3), 2)
        gpu = [c.Win32_VideoController()[x].Name for x in range(len(c.Win32_VideoController()))]
        storage_devices = []
        for disk in c.Win32_DiskDrive():
            # Convert bytes to GB
            size_gb = round(int(disk.Size) / (1024**3), 2)
            storage_devices.append({
                "name": disk.Caption,
                "size": f"{size_gb}GB"
            })
        self.system_info = {
            "hardware_info": {
                "cpu": {
                    "model": cpu
                },
                "memory": {
                    "total": f"{ram}GB"
                },
                "gpu": {
                    "devices": gpu
                },
                "storage": {
                    "devices": storage_devices
                }
            }
        }

    def output_json(self):
        output_path = Path("assets/system_info.json")
        with open(output_path, 'w') as f:
            json.dump(self.system_info, f, indent=2)
        return output_path
