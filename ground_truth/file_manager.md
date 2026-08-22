# File Manager
<small>`pkg: com.chaozhuo.filemanager`</small>

---

## Description
File Manager is a file management tool running on Android system, which supports touch screen, external mouse/keyboard and telecontroller, it provides a easy way to manage files on both your local disks and the file servers in your local network.  
At present, the UI is specially tuned for large screen device only.  
  
Paid to remove ads supported.

---

## Features
| **Feature name** | **Description** |
|---|---|
|Multi-Input Support| Supports touchscreens, external keyboards, mice, and remote controllers. |
|Local Storage Management| Manages files stored on local drives. |
|Network Storage Management| Manages files on file servers in the local network. |
|Large-Screen Optimization| Adapts the user interface for displays on large screens. |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
  "READ_EXTERNAL_STORAGE",
  "WRITE_EXTERNAL_STORAGE",
  "INTERNET",
  "ACCESS_LOCAL_NETWORK"
]
```
The following table maps the derived permissions to the corresponding features.

| **Feature name** | **Permissions** |
|---|---|
|Multi-Input Support| — |
|Local Storage Management| `READ_EXTERNAL_STORAGE` `WRITE_EXTERNAL_STORAGE` |
|Network Storage Management| `INTERNET` `ACCESS_LOCAL_NETWORK`|
|Large-Screen Optimization| — |

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
  "READ_EXTERNAL_STORAGE",
  "WRITE_EXTERNAL_STORAGE",
  "INTERNET",
  "ACCESS_NETWORK_STATE",
  "ACCESS_LOCAL_NETWORK"
  "FOREGROUND_SERVICE",
  "WAKE_LOCK",
  "BLUETOOTH",
  "BLUETOOTH_CONNECT"
]
```