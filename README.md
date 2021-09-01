# Dialog policy simplified

Simple version of dialog policy system.

# Algorithm
1. The message is sent to the system via *rest* into *Dialog Policy (DP)*
2. *DP* send request `CLASSIFY_TEXT` to *Intent Recognizer (IR)* to classify message
3. IR send back to the *DP* result of classification `CLASSIFICATION_RESULT` - intent, projects
4. *DP* send a request `MESSAGE_TO_SKILL` to each *Smart App(SA)* classified
5. Each *SA* response `ANSWER_TO_USER` to *DP*
6. When *DP* got all responces from *SA*s, *DP* sends to *IR* `BLENDER_REQUEST` with all `ANSWER_TO_USER`s included
7. *IR* respond `BLENDER_RESPONSE` to *DP*
8. *DP* respond `ANSWER_TO_USER` via *rest*

# Requirements
- Python 3.7.8

# Usage
1. Download and turn up *kafka* https://kafka.apache.org/quickstart
2. Create in kafka *topics* `to_IR`, `to_smart_app`, `IR_response`, `smart_app_response`
3. `pip install confluent_kafka`
4. `pip install aiohttp`
5. `python manage.py` (as 1st process)
6. `python intent_recognizer_manage.py` (as 2nd process)
7. `python smart_app_manage.py` (as 3rd process)
8. Send a *message* http://0.0.0.0:8080/your_message
