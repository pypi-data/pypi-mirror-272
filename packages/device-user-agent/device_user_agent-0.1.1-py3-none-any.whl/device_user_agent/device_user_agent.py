from re import compile
from pydantic import BaseModel


class DeviceUserAgent(BaseModel):
    package_name: str
    app_version_name: str
    os_name: str
    os_version: str
    device_name: str
    app_version_code: str
    device_manufacturer: str
    device_model: str
    device_resolution: str
    device_pixel_ratio: str

    @classmethod
    def parse(cls, user_agent: str) -> "DeviceUserAgent | None":
        user_agent_pattern = r"(?P<package_name>.+)/(?P<app_version_name>.+) \((?P<os_name>.+) (?P<os_version>.+); (?P<device_name>[\w\s]+); build:(?P<app_version_code>\d+)\) oem/(?P<device_manufacturer>.+) model/(?P<device_model>.+) screen/(?P<device_resolution>\d+\*\d+)/(?P<device_pixel_ratio>.+)"  # noqa
        regex = compile(user_agent_pattern)
        match = regex.match(user_agent)

        if match:
            return cls(**match.groupdict())
