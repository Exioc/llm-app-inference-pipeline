# Pinterest
<small>`pkg: com.pinterest`</small>

---

## Description
Pinterest is a place of endless possibilities. You can:  
\- Discover everyday inspiration  
\- Shop styles you love  
\- Try and learn something new  
  
Create boards, save Pins and make collages of all your inspiration. Unlock billions of ideas, from fashion tips 👠 and easy recipes 🍜 to DIY projects 🛠️ and fresh ways to redo your space. Creating the life you love?  
  
It's Possible.

---

## Features
| **Feature name** | **Description** |
|---|---|
| Content Discovery | Browses content across categories such as fashion tips, recipes, DIY projects, and home decor. |
| In-App Shopping | ? Browse and shop styles and products|
| Content Organization | Saves individual content items (Pins) and organizes them into custom boards. |
| Collage Creation | Combines saved elements into visual collages. |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
  "INTERNET",
  "ACCESS_NETWORK_STATE"
]
```
The following table maps the identified permissions to their corresponding features.

| **Feature name** | **Permissions** |
| --- | --- |
| Content Discovery | `INTERNET` `ACCESS_NETWORK_STATE` |
| In-App Shopping | `INTERNET` `ACCESS_NETWORK_STATE` |
| Content Organization | — |
| Collage Creation | — |

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
  "CAMERA",
  "GET_ACCOUNTS",
  "POST_NOTIFICATIONS",
  "READ_MEDIA_IMAGES",
  "READ_MEDIA_VIDEO",
  "READ_MEDIA_VISUAL_USER_SELECTED",
  "READ_EXTERNAL_STORAGE",
  "INTERNET",
  "ACCESS_NETWORK_STATE",
  "FOREGROUND_SERVICE",
  "FOREGROUND_SERVICE_DATA_SYNC",
  "WAKE_LOCK",
  "VIBRATE"
]
```