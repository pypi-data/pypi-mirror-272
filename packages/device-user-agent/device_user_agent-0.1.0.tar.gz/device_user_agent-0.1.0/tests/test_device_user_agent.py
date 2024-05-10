from unittest import TestCase, main


from device_user_agent.device_user_agent import DeviceUserAgent


class TestDeviceUserAgent(TestCase):
    def test_parsed_user_agent(self):
        raw_user_agent = "com.acmesoftware.dua/1.0.19 (iOS 17.2; iPhone 15 Pro Max; build:240322033) oem/Apple model/iPhone15,4 screen/1290*2796/3.0"  # noqa
        user_agent = DeviceUserAgent.parse(raw_user_agent)

        self.assertEqual(user_agent.package_name, "com.acmesoftware.dua")
        self.assertEqual(user_agent.app_version_name, "1.0.19")
        self.assertEqual(user_agent.os_name, "iOS")
        self.assertEqual(user_agent.os_version, "17.2")
        self.assertEqual(user_agent.device_name, "iPhone 15 Pro Max")
        self.assertEqual(user_agent.app_version_code, "240322033")
        self.assertEqual(user_agent.device_manufacturer, "Apple")
        self.assertEqual(user_agent.device_model, "iPhone15,4")
        self.assertEqual(user_agent.device_resolution, "1290*2796")
        self.assertEqual(user_agent.device_pixel_ratio, "3.0")


if __name__ == "__main__":
    main()
