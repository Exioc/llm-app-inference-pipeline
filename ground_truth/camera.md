# Camera for Android
<small>`pkg: photo.camera.hdcameras `</small>

---

## Description
Camera for Android will allow you to make excellent pictures，that is a very fast and simple way to capture moments.  
You can easily to shoot excellent photos, utilizing all advantage of your phone or tablet.  
Features:  
\- Camera, video recorder & panorama features  
\- White balance settings(Incandescent, Fluorescent, Auto, Daylight,Cloudy)  
\- Screen mode settings(Action, Night, Sunset, Play)  
\- Dynamic user interface (phone/tablet)  
\- Pinch to zoom  
\- Smart panorama shooting   
\- Wide screen pictures  
\- Picture quality setting  
\- Exposure  
\- Location targeting  
\- Configurable volume keys  
\- Countdown Timer

---

## Features
| **Feature name** | **Description** |
|---|---|
| Multi-Mode Capture | Supports photo, video, smart panorama, and widescreen shooting modes. |
| Dynamic user interface | — |
| Scene Modes | Screen mode settings (Action, Night, Sunset, Play) |
| Manual Camera Controls | Customizable white balance, exposure levels, and picture quality settings. |
| Geotagging | Location targeting |
| Configurable volume keys | — |
| Countdown Timer | — |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
  "CAMERA",
  "RECORD_AUDIO",
  "WRITE_EXTERNAL_STORAGE",
  "ACCESS_FINE_LOCATION",
  "ACCESS_COARSE_LOCATION"
]
```
The following table maps the identified permissions to their corresponding features.

| **Feature name** | **Permissions** |
| --- | --- |
| Multi-Mode Capture | `CAMERA` `RECORD_AUDIO` `WRITE_EXTERNAL_STORAGE`|
| Dynamic user interface | — |
| Scene Modes | — |
| Manual Camera Controls | — |
| Geotagging | `ACCESS_FINE_LOCATION` `ACCESS_COARSE_LOCATION` |
| Configurable volume keys | — |
| Countdown Timer | — |

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
  "CAMERA",
  "ACCESS_COARSE_LOCATION",
  "ACCESS_FINE_LOCATION",
  "ACCESS_MEDIA_LOCATION",
  "RECORD_AUDIO",
  "READ_MEDIA_AUDIO",
  "READ_MEDIA_IMAGES",
  "READ_MEDIA_VIDEO",
  "READ_MEDIA_VISUAL_USER_SELECTED",
  "READ_EXTERNAL_STORAGE",
  "WRITE_EXTERNAL_STORAGE",
  "WAKE_LOCK"
  "VIBRATE"
]
```