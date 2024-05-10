# Device User Agent

Parser for user agent string built using [device_user_agent](https://pub.dev/packages/device_user_agent) flutter library.

## Usage
```python
from device_user_agent import DeviceUserAgent

user_agent = DeviceUserAgent.parse("com.acmesoftware.dua/1.0.19 (iOS 17.2; iPhone 15 Pro Max; build:240322033) oem/Apple model/iPhone15,4 screen/1290*2796/3.0")
print(user_agent)
```