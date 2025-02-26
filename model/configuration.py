from pydantic import BaseModel, Field
from typing import List, Optional

class ConfigItem(BaseModel):
    value: str
    description: str

class SystemConfiguration(BaseModel):
    languages: List
    keyboard_layouts: List
    display_managers: List
    window_managers: List
    graphics_drivers: List
    bootloaders: List
    kernels: List
    package_managers: List
    icon_themes: List
    system_themes: List
    external_apps: List
    file_systems: List
    performance_optimization: List
    security_settings: List
    timezones: List
    networking: List
    firewall_configs: List
    systemd_service_configs: List
    ssh_configs: List
    logging_configs: List

class InstallationRecommendation(BaseModel):
    recommendation: List[SystemConfiguration]
    analysis: str