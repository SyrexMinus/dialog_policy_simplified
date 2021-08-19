# coding: utf-8
import json

class MockToMessage:
    def __init__(self, msg, mid):
        self.msg = msg
        self.mid = mid

    @property
    def raw(self):
        data = {"messageId": self.mid, "sessionId": "b7abcdea-eac8-436a-a9ac-c7fff4d9e6eb",
                "messageName": "VOICE_FROM_USER",
                "payload": {"application": {"name": "okko"},
                            "meta": {"alarm": {"alarms": [], "timers": []}, "application": {"name": "okko"},
                                     "background_apps": [{"app_info": {"applicationId": "d7c7178e-99d8-4192-962f-34c3940a6fdf", "appversionId": "672af7be-23d8-4d9c-95a2-f3e72c722145", "frontendEndpoint": "ru.sberdevices.music", "frontendType": "APK", "projectId": "2c96f0b4-4be9-4fb6-b80f-f7f83395042e", "systemName": "music"}, "state": {"player": {"info": {"type": "audio"}, "type": "audio"}}}],
                                     "current_app": {"app_info": {"frontendEndpoint": "ru.sberdevices.starlauncher",
                                                                  "frontendType": "APK", "systemName": "launcher"},
                                                     "state": {}}, "debug_params": {},
                                     "deviceSleep": {"systemState": "working"},
                                     "location": {"lat": 55.74567794799805, "lon": 37.5528450012207, "timestamp": 1594294108680},
                                     "music": {"player": {"info": {"type": "audio"}, "type": "audio"}},
                                     "network": {"ip": "109.252.28.26"}, "time": {"timestamp": 1594294227980,
                                                                                  "timezone_id": "Europe/Moscow", "timezone_offset_sec": 10800},
                                     "timesync": {"unixtime": 1594294227.98}, "volume": {"percent": 100}},
                            "vk_user_id": 572017444, "smartBio": {"IdentifyResponse": {"ErrorCode": "10002"}},
                            "token": "***", "message": self.msg, "normalizedMessage": "Погода в Москве",
                            "device": {"platformType": "android", "platformVersion": "9",
                                       "surface": "SBERBOX", "surfaceVersion": "1.54.20200708131247",
                                       "features": {"appTypes": ["APK", "WEB_APP", "DIALOG"]},
                                       "capabilities": {"screen": {"available": True}, "mic": {"available": True},
                                                        "speak": {"available": True}}, "deviceId": "GZ200301320000035",
                                       "deviceManufacturer": "SberDevices", "deviceModel": "sberbox", "additionalInfo": {}},
                            "annotations": {"asr_sentiment": {"classes": ["positive", "neutral", "negative"],
                                                              "probas": [0.0021807738, 0.9393756, 0.058443636]}}},
                "uuid": {"userId": "4645645445", "sub": "564645654", "userChannel": "B2C"}}
        return json.dumps(data, ensure_ascii=False)