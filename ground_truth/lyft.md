# Lyft
<small>`pkg: me.lyft.android`</small>

---

## Description
Get where you’re going with Lyft.  
  
Whether you’re catching a flight, going out for the night, commuting to the office, or running errands in a rush, the Lyft app offers you multiple ways to get there.  
  
EASY TO USE  
Enter your destination. See your route and ride cost up front. Choose Priority Pickup to get going quick. Boom. Done. Simple  
  
CHOOSE YOUR WHEELS  
Choose from Wait & Save, Priority Pickup, Bikes & Scooters, Lyft XL, Lyft Lux, Transit, or even Rentals.  
  
AFFORDABLE RIDES  
Our Wait & Save option helps you get around for less. And you can find the fastest public transit routes, too.  
  
* Lyft ride types may vary by region. Check the app to see what is available in your city.  
—  
Prices vary based on market condition.  
  
By downloading the app, you agree to allow Lyft to collect your device's language settings.

---

## Features
| **Feature name**  | **Description** |
|---|---|
|Upfront Booking and Pricing| Route preview and exact price calculation based on destination input prior to booking. |
|Customized Ride Options| Selection of different service tiers based on pickup priority, price, and vehicle size. |
|Micro-Mobility and Rentals| In-app access to bikes, scooters, and rental cars. |
|Public Transit Integration| Search and navigation for local public transit routes. |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
  "ACCESS_COARSE_LOCATION",
  "ACCESS_FINE_LOCATION",
  "INTERNET"
]
```
The following table maps the derived permissions to the corresponding features.

| **Feature name** | **Permissions** |
| --- | --- |
|Upfront Booking and Pricing| `INTERNET` |
|Customized Ride Options| `INTERNET` `ACCESS_FINE_LOCATION` `ACCESS_COARSE_LOCATION`|
|Micro-Mobility and Rentals|`INTERNET` |
|Public Transit Integration| `ACCESS_FINE_LOCATION` `ACCESS_COARSE_LOCATION`|

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
  "CAMERA",
  "GET_ACCOUNTS",
  "ACCESS_COARSE_LOCATION",
  "ACCESS_FINE_LOCATION",
  "POST_NOTIFICATIONS",
  "CALL_PHONE",
  "INTERNET",
  "ACCESS_NETWORK_STATE",
  "FOREGROUND_SERVICE",
  "FOREGROUND_SERVICE_LOCATION",
  "WAKE_LOCK",
  "MODIFY_AUDIO_SETTINGS",
  "VIBRATE",
  "BLUETOOTH",
  "BLUETOOTH_ADMIN",
  "BLUETOOTH_SCAN",
  "BLUETOOTH_CONNECT"
]
```