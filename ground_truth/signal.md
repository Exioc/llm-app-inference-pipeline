# Signal Private Messenger
<small>`pkg: org.thoughtcrime.securesms`</small>

---

## Description
Signal is a messaging app with privacy at its core. It is free and easy to use, with strong end-to-end encryption that keeps your communication completely private.  
  
• Send texts, voice messages, photos, videos, GIFs, and files for free. Signal uses your phone’s data connection, so you avoid SMS and MMS fees.  
  
• Call your friends with crystal-clear encrypted voice and video calls. Group calls supported for up to 50 people.  
  
• Stay connected with group chats up to 1,000 people. Control who can post and manage group members with admin permission settings.  
  
• Share image, text, and video Stories that disappear after 24 hours. Privacy settings keep you in charge of exactly who can see each Story.  
  
• Signal is built for your privacy. We know nothing about you or who you’re talking to. Our open source Signal Protocol means that we can’t read your messages or listen to your calls. Neither can anyone else. No back doors, no data collection, no compromises.  
  
• Signal is independent and not for profit; a different kind of tech from a different kind of organization. As a 501c3 nonprofit we are supported by your donations, not by advertisers or investors.  
  
• For support, questions, or more information please visit https://support.signal.org/  
  
To check out our source code, visit https://github.com/signalapp  
  
Follow us on Twitter @signalapp and Instagram @signal_app

---

## Features
| **Feature name** | **Description** |
|---|---|
|End-to-End Encryption| Automatically encrypts all messages and calls to prevent third-party access. |
|Multimedia Messaging| Transmission of text, voice messages, files, and media via internet connection. |
|Voice and Video Calling| Supports individual and group audio and video calls for up to 50 participants. |
|Group Chats and Admin Controls| Group chats for up to 1,000 members with admin settings for member management and posting permissions. |
|Short-Lived Stories| Temporary text, image, and video stories that expire after 24 hours with customizable visibility settings. |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
  "CAMERA",
  "RECORD_AUDIO",
  "READ_MEDIA_IMAGES",
  "READ_MEDIA_VIDEO",
  "READ_MEDIA_VISUAL_USER_SELECTED",
  "READ_EXTERNAL_STORAGE",
  "WRITE_EXTERNAL_STORAGE",
  "INTERNET"
]
```
The following table maps the derived permissions to the corresponding features.

| **Feature name** | **Permissions** |
| --- | --- |
|End-to-End Encryption| `INTERNET`|
|Multimedia Messaging| `RECORD_AUDIO` `READ_MEDIA_IMAGES` `READ_MEDIA_VIDEO` `READ_MEDIA_VISUAL_USER_SELECTED` `READ_EXTERNAL_STORAGE` `WRITE_EXTERNAL_STORAGE` `INTERNET`|
|Voice and Video Calling| `CAMERA` `RECORD_AUDIO` `INTERNET`|
|Group Chats and Admin Controls| `INTERNET`|
|Short-Lived Stories| `READ_MEDIA_IMAGES` `READ_MEDIA_VIDEO` `READ_MEDIA_VISUAL_USER_SELECTED` `READ_EXTERNAL_STORAGE` `INTERNET`|

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
  "CAMERA",
  "READ_CONTACTS",
  "WRITE_CONTACTS",
  "ACCESS_COARSE_LOCATION",
  "ACCESS_FINE_LOCATION",
  "RECORD_AUDIO",
  "POST_NOTIFICATIONS",
  "USE_FULL_SCREEN_INTENT",
  "READ_PHONE_STATE",
  "READ_CALL_STATE",
  "MANAGE_OWN_CALLS",
  "READ_PHONE_NUMBERS",
  "READ_MEDIA_IMAGES",
  "READ_MEDIA_VIDEO",
  "READ_MEDIA_VISUAL_USER_SELECTED",
  "READ_EXTERNAL_STORAGE",
  "WRITE_EXTERNAL_STORAGE",
  "INTERNET",
  "ACCESS_NETWORK_STATE",
  "NEARBY_WIFI_DEVICES",
  "FOREGROUND_SERVICE",
  "FOREGROUND_SERVICE_CAMERA",
  "FOREGROUND_SERVICE_DATA_SYNC",
  "FOREGROUND_SERVICE_MEDIA_PLAYBACK",
  "FOREGROUND_SERVICE_MEDIA_PROJECTION",
  "FOREGROUND_SERVICE_MICROPHONE",
  "FOREGROUND_SERVICE_PHONE_CALL",
  "FOREGROUND_SERVICE_REMOTE_MESSAGING",
  "RECEIVE_BOOT_COMPLETED",
  "BROADCAST_STICKY",
  "WAKE_LOCK",
  "MODIFY_AUDIO_SETTINGS",
  "VIBRATE",
  "USE_BIOMETRIC",
  "USE_FINGERPRINT",
  "BLUETOOTH",
  "BLUETOOTH_CONNECT"
]
```