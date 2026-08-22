# Waze Navigation & Live Traffic
<small>`pkg: com.waze`</small>

---

## Description
Know what's ahead on the road with the help from other drivers. Waze is a live map that harnesses the local knowledge of tens of millions of drivers around the world. Drivers safely and confidently reach their everyday destinations thanks to Waze map’s GPS navigation, live traffic updates, real-time safety alerts (including roadworks, accidents, crashes, police, potholes and more), and accurate ETAs.  
  
Make your next drive more predictable and stress-free:  
• Get there faster with real-time directions, accurate ETAs and automatic rerouting based on live traffic, incidents and road closures  
• Even if you know the way, avoid surprises on the road ahead with safety alerts for accidents, crashes, roadworks, objects on the road, potholes, speed bumps, sharp curves, bad weather, emergency vehicles, railway crossings and more  
• Steer clear of tickets by knowing where police and red light and speed cameras are located  
• Share what’s happening on the road with other drivers by reporting live incidents and hazards  
• Stay informed of upcoming speed limit changes, and keep your speedometer in check   
• Know which lane to be in with multi-lane guidance   
• See toll pricing and choose to avoid tolls along your routes  
• Add road passes and vignettes for HOV lanes and restricted traffic zones  
• Find petrol/fuel stations and prices and EV charging stations along your route  
• Locate and compare parking lots and their prices near your destination  
• Use voice-guided turn-by-turn navigation from a variety of languages, local accents and your favourite celebrities  
• Plan your next drive by checking ETAs by future departure or arrival times  
• Use your favourite audio apps (for podcasts, music, news, audiobooks) directly within Waze   
• Sync Waze to your car’s built-in display through Android Auto  
  
* Some features are not available in all countries  
  
* Waze navigation is not intended for emergency or oversized vehicles  
  
You can manage your in-app Waze privacy settings at any time. Learn more about the Waze privacy policy here, www.waze.com/legal/privacy.

---

## Features
| **Feature name** | **Description** |
|---|---|
| GPS Navigation & Routing | Turn-by-turn navigation with real-time directions, accurate ETAs, automatic traffic rerouting, multi-lane guidance, time-based trip planning, and multilingual voice instructions. |
| Live Traffic & Incident Alerts | Real-time updates and hazard alerts for accidents, roadworks, road objects, potholes, speed bumps, sharp curves, bad weather, emergency vehicles, and railway crossings. |
| Speed & Trap Alerts | Notifications for speed limit changes, stationary speed cameras, red-light cameras, and user-reported police presence. |
| Community-Based Reporting | In-app reporting tool for active road hazards, incidents, and hazards shared across the user network. |
| Tolls, Vignettes, and Road Passes | Displays toll prices, offers alternative routes to avoid tolls, and manages road passes and vignettes for HOV lanes and restricted zones. |
| Fuel & Parking Search | Price comparison and location search for fuel stations, EV charging stations, and parking spaces along the route or near the destination. |
| Media & In-Car Integration | Direct in-app playback for audio apps (podcasts, music, news, audiobooks) and screen mirroring via Android Auto. |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
    "ACCESS_COARSE_LOCATION",
    "ACCESS_FINE_LOCATION",
    "POST_NOTIFICATIONS",
    "INTERNET"
]
```
The following table maps the identified permissions to their corresponding features.

| **Feature name** | **Permissions** |
| --- | --- |
| GPS Navigation & Routing | `ACCESS_FINE_LOCATION` `ACCESS_COARSE_LOCATION`|
| Live Traffic & Incident Alerts | `POST_NOTIFICATIONS` `INTERNET`|
| Speed & Trap Alerts | `POST_NOTIFICATIONS`|
| Community-Based Reporting | `INTERNET`|
| Tolls, Vignettes, and Road Passes | `INTERNET`|
| Fuel & Parking Search | `INTERNET`|
| Media & In-Car Integration | — |

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
    "GET_ACCOUNTS",
    "ACCESS_COARSE_LOCATION",
    "ACCESS_FINE_LOCATION",
    "RECORD_AUDIO",
    "POST_NOTIFICATIONS",
    "POST_PROMOTED_NOTIFICATIONS",
    "READ_PHONE_STATE",
    "READ_BASIC_PHONE_STATE",
    "INTERNET",
    "ACCESS_NETWORK_STATE",
    "ACCESS_WIFI_STATE",
    "FOREGROUND_SERVICE",
    "FOREGROUND_SERVICE_LOCATION",
    "FOREGROUND_SERVICE_MEDIA_PLAYBACK",
    "FOREGROUND_SERVICE_MICROPHONE",
    "MODIFY_AUDIO_SETTINGS",
    "BROADCAST_STICKY",
    "WAKE_LOCK",
    "VIBRATE",
    "BLUETOOTH",
    "BLUETOOTH_ADMIN",
    "BLUETOOTH_SCAN",
    "BLUETOOTH_CONNECT"
]
```