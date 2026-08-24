# Alipay
<small>`pkg: com.eg.android.AlipayGphone`</small>

---

## Description
Alipay is a leading open platform for payments and digital services in China.  
  
Users with a Chinese ID and bank account can use Alipay to make payments online and in person at various merchants outside of China as they travel for leisure, business, or study.   
  
Foreign visitors to China can connect their credit card to take advantage of Alipay’s widespread acceptance by tens of millions of merchants across the country. Alipay is not designed or intended for use by foreign users in their home country or anywhere outside of China.

---

## Features
| **Feature name** | **Description** |
|---|---|
|Cross-Border Payments| Enables users with a Chinese ID and bank account to make online and in-person payments abroad. |
|Foreign Credit Card Integration| Allows visitors in China to link credit cards for local payments. |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
  "NFC",
  "NFC_TRANSACTION_EVENT",
  "INTERNET"
]
```
The following table maps the derived permissions to the corresponding features.  

| **Feature name** | **Permissions** |
|---|---|
|Cross-Border Payments| `INTERNET` `NFC` `NFC_TRANSACTION_EVENT`|
|Foreign Credit Card Integration| `INTERNET` `NFC` `NFC_TRANSACTION_EVENT`|

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
  "CAMERA",
  "ACCESS_COARSE_LOCATION",
  "ACCESS_FINE_LOCATION",
  "GET_ACCOUNTS",
  "NFC",
  "NFC_TRANSACTION_EVENT",
  "POST_NOTIFICATIONS",
  "READ_MEDIA_IMAGES",
  "READ_MEDIA_VIDEO",
  "READ_MEDIA_VISUAL_USER_SELECTED",
  "WRITE_EXTERNAL_STORAGE",
  "READ_EXTERNAL_STORAGE"
  "INTERNET",
  "ACCESS_NETWORK_STATE",
  "FOREGROUND_SERVICE",
  "BROADCAST_STICKY",
  "WAKE_LOCK",
  "HIDE_OVERLAY_WINDOWS", 
  "VIBRATE",
  "DETECT_SCREEN_CAPTURE",
  "DETECT_SCREEN_RECORDING",
  "USE_BIOMETRIC",
  "USE_FINGERPRINT"
]
```