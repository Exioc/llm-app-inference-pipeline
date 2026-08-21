# ChatGPT
<small>`pkg: com.openai.chatgpt`</small>

---

## Description
Introducing ChatGPT for Android: OpenAI’s latest advancements at your fingertips.  
  
This official app is free, syncs your history across devices, and brings you the latest from OpenAI, including the new image generator.  
  
With ChatGPT in your pocket, you’ll find:  
  
· Image generation–Generate original images from a description, or transform existing ones with a few simple words.   
· Advanced Voice Mode–Tap the soundwave icon to have a real-time convo on the go. Settle a dinner table debate, or practice a new language.   
· Photo upload—Snap or upload a picture to transcribe a handwritten recipe or get info about a landmark.   
· Creative inspiration—Find custom birthday gift ideas or create a personalized greeting card.  
· Tailored advice—Talk through a tough situation, ask for a detailed travel itinerary, or get help crafting the perfect response.   
· Personalized learning—Explain electricity to a dinosaur-loving kid or easily brush up yourself on a historic event.  
· Professional input—Brainstorm marketing copy or map out a business plan.  
· Instant answers—Get recipe suggestions when you only have a few ingredients.  
· Screen share with Accessibility Services — In limited availability, users can choose to let ChatGPT help answer questions about screen details without requiring screenshot uploads.  
  
Join hundreds of millions of users and try the app captivating the world. Download ChatGPT today.  
  
Terms of service & privacy policy:  
https://openai.com/policies/terms-of-use  
https://openai.com/policies/privacy-policy

---

## Features
| **Feature name** | **Description** |
|---|---|
| Image Generation & Editing | Generates images from text descriptions or modifies existing images. |
| Advanced Voice Mode | Enables real-time voice conversations by tapping the soundwave icon. |
| Image Analysis & Transcription | Allows capturing or uploading photos to transcribe text or retrieve information about visual content. |
| Personalized & Creative Assistance | Generates creative ideas, advice, travel itineraries, and written content tailored to specific situations. |
| Educational & Learning Assistance | Explains complex concepts and adapts learning topics to specific audiences or knowledge levels. |
| Professional Assistance | Assists with business planning, brainstorming, and marketing content creation. |
| Ingredient-Based Recipe Suggestions | Generates recipe ideas based on available ingredients. |
| Screen Analysis via Accessibility Services| Analyzes active screen content to answer questions without screenshot uploads. |
| History Sync | Synchronizes user chat history across devices. |

---

## Permissions set 1
Permission Set 1 includes the permissions derived from the app description, as follows:

```json
[
    "CAMERA",
    "GET_ACCOUNTS",
    "RECORD_AUDIO",
    "READ_MEDIA_AUDIO",
    "READ_MEDIA_IMAGES",
    "READ_MEDIA_VISUAL_USER_SELECTED",
    "READ_EXTERNAL_STORAGE",
    "WRITE_EXTERNAL_STORAGE",
    "INTERNET",
    "READ_ASSIST_STRUCTURE_SCREEN_CONTENT",
    "FOREGROUND_SERVICE"
]
```
The following table maps the identified permissions to their corresponding features.

| **Feature name** | **Permissions** |
| --- | --- |
| Image Generation & Editing | `READ_MEDIA_IMAGES` `READ_MEDIA_VISUAL_USER_SELECTED` `READ_EXTERNAL_STORAGE` `WRITE_EXTERNAL_STORAGE`|
| Advanced Voice Mode |`RECORD_AUDIO`|
| Image Analysis & Transcription | `CAMERA` `READ_MEDIA_IMAGES` `xREAD_MEDIA_VISUAL_USER_SELECTED` `READ_EXTERNAL_STORAGE`|
| Personalized & Creative Assistance | — |
| Educational & Learning Assistance | — |
| Professional Assistance | `WRITE_EXTERNAL_STORAGE` |
| Ingredient-Based Recipe Suggestions | — |
| Screen Analysis via Accessibility Services | `READ_ASSIST_STRUCTURE_SCREEN_CONTENT` `FOREGROUND_SERVICE`|
| History Sync | `GET_ACCOUNTS` `INTERNET`|

---

## Permissions set 2
Permission Set 2 combines the app description with domain knowledge to define the expected permissions as follows:

```json
[
    "CAMERA",
    "GET_ACCOUNTS",
    "RECORD_AUDIO",
    "POST_NOTIFICATIONS",
    "POST_PROMOTED_NOTIFICATIONS",
    "READ_MEDIA_IMAGES",
    "READ_MEDIA_VISUAL_USER_SELECTED",
    "READ_EXTERNAL_STORAGE",
    "WRITE_EXTERNAL_STORAGE",
    "INTERNET",
    "ACCESS_NETWORK_STATE",
    "FOREGROUND_SERVICE",
    "FOREGROUND_SERVICE_MEDIA_PROJECTION",
    "FOREGROUND_SERVICE_MICROPHONE",
    "WAKE_LOCK",
    "MODIFY_AUDIO_SETTINGS",
    "VIBRATE",
    "READ_ASSIST_STRUCTURE_SCREEN_CONTENT"
]
```