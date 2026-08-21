# Alarm clock 
<small>`pkg: com.timy.alarmclock`</small>

---

## Description
Timy Alarm Clock will help you avoid accidentally turning off your alarm clock and falling asleep.  
  
To dismiss the alarm you will have to wake up some funny characters.  
  
**Main features:**  
Multiple alarms.  
Cute characters to wake up: Cat, dog, bunny, fox, crocodile, shark, duck, with three difficulty levels.  
Wake up with your tones or songs.  
Repeat option.  
Snooze.  
Independent volume control.  
  
Important: Device must be on to work.

---

## Features
| **Feature name** | **Description** |
|---|---|
| Multiple alarms | — |
| Characters to wake up | Deactivates alarms by completing a wake-up task with animal characters (cat, dog, bunny, fox, crocodile, shark, duck) across three difficulty levels. |
| Wake up with your tones or songs | — |
| Repeat option | — |
| Snooze | — |
| Independent volume control | — |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
"READ_MEDIA_AUDIO",
"USE_EXACT_ALARM"
]
```
The following table maps the identified permissions to their corresponding features.

| **Feature name** | **Permissions** |
| --- | --- |
| Multiple alarms | `USE_EXACT_ALARM` |
| Characters to wake up | — |
| Wake up with your tones or songs | `READ_MEDIA_AUDIO` |
| Repeat option | — |
| Snooze | — |
| Independent volume control | — |

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
"POST_NOTIFICATIONS",
"USE_FULL_SCREEN_INTENT", 
"READ_MEDIA_AUDIO",
"READ_EXTERNAL_STORAGE",
"FOREGROUND_SERVICE", 
"FOREGROUND_SERVICE_MEDIA_PLAYBACK",
"RECEIVE_BOOT_COMPLETED",
"WAKE_LOCK",
"VIBRATE", 
"USE_EXACT_ALARM"
]
```
