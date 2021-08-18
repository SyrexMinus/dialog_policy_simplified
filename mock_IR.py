# coding: utf-8
import simplejson as json
import time

from core.mq.kafka.kafka_publisher import KafkaPublisher


kafka_config = {
    "publisher": {
        "conf": {
            "bootstrap.servers": "10.53.88.57:9093",
            "topic.metadata.refresh.interval.ms": 100000,

            "security.protocol": "SSL",
            "ssl.ca.location": "./kafka_dev_certs/ca",
            "ssl.certificate.location": "./kafka_dev_certs/cert",
            "ssl.key.location": "./kafka_dev_certs/key"
        },
        "poll_timeout": 0.01,
        "flush_timeout": 10000,
        "partitions_count": 3,
        "topic": {"messenger": "toDP"}
    }
}
headers = [('kafka_replyTopic', b'paToEis'), ('kafka_correlationId', b'\\xcd\\xf7\\xfe\\x14\\xa5\\xa1E%\\x84\\x9c$\\xca\\x03\\xb0c\\xd1')]


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
        data2 = {"messageId": self.mid, "sessionId": "b7abcdea-eac8-436a-a9ac-c7fff4d9e6eb",
                 "messageName": "RUN_APP", "payload": {"token": "***", "normalizedMessage": "Погода в Москве",
                                                             "device": {"platformType": "android",
                                                                        "platformVersion": "9", "surface": "SBERBOX",
                                                                        "surfaceVersion": "1.54.20200708131247",
                                                                        "features": {
                                                                            "appTypes": ["APK", "WEB_APP", "DIALOG"]},
                                                                        "capabilities": {"screen": {"available": True},
                                                                                         "mic": {"available": True},
                                                                                         "speak": {"available": True}},
                                                                        "deviceId": "GZ200301320000035",
                                                                        "deviceManufacturer": "SberDevices",
                                                                        "deviceModel": "sberbox",
                                                                        "additionalInfo": {}},
                                                             "app_info": {
                                                                 "projectId": "0de0ddcc-66af-4859-b0f7-77e034271a75",
                                                                 "applicationId": "fe0f6b1d-7525-427b-937d-48b7caeb82db",
                                                                 "appversionId": "a52d09ea-b781-4378-b37e-d422da8b58dc"
                                                             },
                                                             "server_action": {"app_info": {
                                                                 "projectId": "0de0ddcc-66af-4859-b0f7-77e034271a75",
                                                                 "applicationId": "fe0f6b1d-7525-427b-937d-48b7caeb82db",
                                                                 "appversionId": "a52d09ea-b781-4378-b37e-d422da8b58dc"
                                                             }}},
                 "uuid": {"userId": "333333333", "sub": "45345353", "userChannel": "B2C"}}
        data3 = {"messageId": self.mid, "sessionId": "0b9f4869-31fd-4c2d-8383-7cc2a069af1e",
                 "messageName": "MESSAGE_FROM_USER",
                 "payload": {"token": "***", "tokenType": "VPS_TOKEN", "message": "Запусти сомелье",
                             "device": {"platformType": "", "platformVersion": "", "surface": "SOMMELIER20",
        "surfaceVersion": "", "deviceId": "", "deviceManufacturer": "", "deviceModel": ""}},
        "uuid": {"userId": "33900543800001256825394286", "userChannel": "B2C"}},
        data4 = {"messageId": self.mid, "sessionId": "b7abcdea-eac8-436a-a9ac-c7fff4d9e6eb",
                 "messageName": "SERVER_ACTION", "payload": {"token": "***", "normalizedMessage": "Погода в Москве",
                                                             "device": {"platformType": "android",
                                                                        "platformVersion": "9", "surface": "SBERBOX",
                                                                        "surfaceVersion": "1.54.20200708131247",
                                                                        "features": {
                                                                            "appTypes": ["APK", "WEB_APP", "DIALOG"]},
                                                                        "capabilities": {"screen": {"available": True},
                                                                                         "mic": {"available": True},
                                                                                         "speak": {"available": True}},
                                                                        "deviceId": "GZ200301320000035",
                                                                        "deviceManufacturer": "SberDevices",
                                                                        "deviceModel": "sberbox",
                                                                        "additionalInfo": {}},
                                                             "app_info": {
                                                                 "projectId": "2c96f0b4-4be9-4fb6-b80f-f7f83395042e"
                                                             },
                                                             "meta": {"current_app": {"app_info": {
                                                                 "projectId": "2c96f0b4-4be9-4fb6-b80f-f7f83395042e"}}},
                                                             "server_action": {}},
                 "uuid": {"userId": "333333333", "sub": "45345353", "userChannel": "B2C"}}
        return json.dumps(data, ensure_ascii=False)


def main():
    publisher = KafkaPublisher(kafka_config)
    userId = "345435435353"
    chatId = "5"
    uuid = {
        "userChannel": "SBERBANK_MESSENGER",
        "userId"     : userId,
        "chatId"     : chatId
    }
    key = "{}_{}_{}".format(uuid["userChannel"], uuid["userId"], uuid["chatId"])
    user_message = "о погоде"
    # user_message = "давай поговорим по душам"
    user_message = "каннибал корпс"
    exit_message = "exit"
    message_id = 34545343
    TPS = 0.1
    while user_message != exit_message:
        try:
            # user_message = input(">")
            # if user_message != exit_message:
            message = MockToMessage(user_message, message_id)
            result = publisher.send(message.raw, key, "messenger", headers=headers)
            message_id += 1
            #print(message.raw)
            print("done")
            time.sleep(1/TPS)
        except Exception as e:
            print(e)
            publisher.close()
            return

    # wait to receive delivery_callback on last sent message
    time.sleep(2)
    publisher.close()


if __name__ == '__main__':
    main()