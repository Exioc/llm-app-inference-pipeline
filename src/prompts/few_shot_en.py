import json

GOOGLE_ONE_LABEL = "Google One"

GOOGLE_ONE_DESCRIPTION = "The Google One app lets you automatically back up your phone and manage your Google cloud storage.<br>  • Automatically back up the important things on your phone, like photos, contacts and messages using your 15 GB of storage that comes with every Google account. If you break, lose or upgrade your phone, you can restore everything to your new Android device.<br>  • Manage your existing Google account storage across Google Drive, Gmail and Google Photos.<br><br>  Upgrade to a Google One membership to get even more:<br>  • Get as much storage as you need for your important memories, projects and digital files. Choose the plan that works best for you."

GOOGLE_ONE_OUTPUT = {
  "features": [
    {
        "functionality": "Automated Data Backup",
        "description": "The app automatically backs up personal smartphone content such as photos, contacts, and text messages in the background. For this free basic backup, the app provides a storage limit of 15 GB per Google account.",
        "reasoning": "The text explicitly mentions 'Automatically back up the important things' in connection with '15 GB of storage', from which it can be inferred that an automated data upload function is available. For this reason, a background service must be implemented in the app that reads local system data and transfers it to cloud servers.",
        "source_quotes": [
            "The Google One app lets you automatically back up your phone",
            "Automatically back up the important things on your phone, like photos, contacts and messages using your 15 GB of storage that comes with every Google account."
        ]
    },
    {
        "functionality": "Centralized Storage Management",
        "description": "The app provides a central management interface to monitor used and available cloud storage space across various Google services (Drive, Gmail, and Photos).",
        "reasoning": "The text explicitly mentions 'Manage your existing Google account storage across...', from which it can be inferred that the app acts as an aggregator. For this reason, a dashboard interface must exist that reads storage data from separate Google ecosystems and summarizes it visually.",
        "source_quotes": [
            "manage your Google cloud storage.",
            "Manage your existing Google account storage across Google Drive, Gmail and Google Photos."
        ]
    },
    {
        "functionality": "Data Recovery (Disaster Recovery)",
        "description": "Allows the user to completely restore previously backed-up data onto a new Android device in the event of device loss, damage, or a smartphone upgrade.",
        "reasoning": "The text explicitly mentions 'If you break, lose or upgrade... you can restore everything', from which it can be inferred that a classic recovery process is supported. For this reason, a dedicated technical routine for data querying and local system restoration must be integrated.",
        "source_quotes": [
            "If you break, lose or upgrade your phone, you can restore everything to your new Android device."
        ]
    },
    {
        "functionality": "Scalable Storage Upgrade",
        "description": "Users can purchase a paid Google One subscription to flexibly adjust their storage limit across different subscription tiers (subscription plans) based on their individual needs.",
        "reasoning": "The text explicitly mentions 'Upgrade to a Google One membership' combined with 'Choose the plan', from which it can be inferred that the app features an interface to a payment system. For this reason, an in-app billing process and a dynamic storage scaling mechanism on the server side must exist.",
        "source_quotes": [
            "Upgrade to a Google One membership to get even more:",
            "Get as much storage as you need for your important memories, projects and digital files. Choose the plan that works best for you."
        ]
    }
  ]
}
SAMSUNG_HEALTH_LABEL = "Samsung Health"

SAMSUNG_HEALTH_DESCRIPTION = "Start healthy habits for yourself with Samsung Health on Wear OS Powered by Samsung.<br><br>Samsung Health has various features to help you manage your health. As the app allows you to automatically record many activities, creating a healthy lifestyle is easier and simpler than ever.<br><br>Check various health records on the Samsung Health home screen. Easily add and edit the items that you want to manage such as daily steps, activity time, and body weight, simply by long pressing the screen.<br><br>Samsung Health helps you record and manage your fitness activities, such as running, cycling, swimming, etc. Also, Galaxy Watch wearables user can now exercise more effectively through Life Fitness, Technogym and Corehealth.<br><br>Develop healthy eating habits with Samsung Health, with which you can record your meals and snacks every day.<br><br>Work hard and always maintain your best condition with Samsung Health. Set goals that work for your own level, and keep track of your daily condition including your activity amount, workout intensity, state of sleep, heart rate, stress, oxygen level in the blood, etc. <br><br>Monitor your sleep patterns in more detail with Galaxy Watch. Make your mornings more refreshing by improving the quality of your sleep through sleep levels and sleep scores.<br><br>Challenge yourself against your friends and family to become healthier in a more fun and interactive way with Samsung Health Together.<br><br>Samsung Health has prepared videos of expert coaches who will teach you new fitness programs including stretching, weight loss, endurance training, and more.<br><br>Discover powerful meditation tools on Mindfulness that will help you relieve stress throughout your day.<br><br>(Some contents are only available through an optional paid subscription. Content is available in English, German, Spanish, French, Portuguese and Korean.)<br><br>Women&#39;s health offers helpful support in menstrual cycle tracking, related symptom management and personalized insights and contents through your partner, Glow. The Galaxy and other wearables are now ready to support the women we love every step of their way.<br><br>Requires Wear OS 2.0(Android 11) or later. Some mobile devices are not synced. Detailed features may vary depending on the user’s country of residence, region, network carrier, model of the device, etc.<br><br>Supports over 70 languages, including English, French, and Chinese. An English language version is available for the rest of the world.<br><br>Please note that Samsung Health is intended for fitness and wellness purposes only and is not intended for use in the diagnosis of disease or other conditions, or in the cure, mitigation, treatment, or prevention of disease.<br><br>The following permissions are required for the app service. For optional permissions, the default functionality of the service is turned on, but not allowed.<br><br>Required permissions<br>- Body Sensors : Used to measure heart rate, oxygen saturation, and stress. <br>- Physical activity : Used to count your steps and detect workouts.<br><br>Optional permissions<br>- Location : Your location data is collected when you are using the exercises tracker and the steps tracker.<br>- Files and media : You can import/export your exercise data, save exercise photos, save/load food photos."

SAMSUNG_HEALTH_OUTPUT = {
  "features": [
    { 
      "functionality": "Automated Activity Tracking",
      "description": "The app automatically records sports and everyday activities in the background, making it easier for users to document their lifestyle without manual inputs.",
      "reasoning": "The text explicitly mentions 'automatically record many activities', from which it can be inferred that the app features sensor-based background detection. Since the goal is described as 'easier and simpler than ever', a technical automation must exist to relieve the user from manual logging.",
      "source_quotes": [
        "Samsung Health has various features to help you manage your health.",
        "As the app allows you to automatically record many activities, creating a healthy lifestyle is easier and simpler than ever."
      ]
    },
    { 
      "functionality": "Central Health Dashboard",
      "description": "The app provides an overview page on the home screen to directly view various personal health metrics, such as daily steps and activity time.", 
      "reasoning": "The text explicitly mentions 'Check various health records on the home screen', from which it can be inferred that the app features a central user interface (dashboard) that serves as a repository for different measurements. For this reason, a visual display function for this data must exist.",
      "source_quotes": [
        "Check various health records on the home screen.",
        "such as daily steps and activity time."
      ] 
    },
    { 
      "functionality": "Dashboard Personalization",
      "description": "Users can flexibly add or edit the widgets and data fields displayed on the home screen to customize the management of their health metrics individually.",
      "reasoning": "The text explicitly mentions 'Easily add and edit the items', from which it can be inferred that the home screen does not have a rigid layout. Since the user can manage elements themselves based on 'that you want to manage', a technical configuration and editing function must exist within the user interface.",
      "source_quotes": [
        "Easily add and edit the items that you want to manage such as daily steps and activity time."
      ] 
    },
    { 
      "functionality": "Manual and Sensor-Based Activity Recording",
      "description": "The app enables the documentation and tracking of various sports such as running, cycling, and swimming.",
      "reasoning": "The text explicitly mentions 'Record and manage your fitness activities', from which it can be inferred that the app has modules for data collection and workout storage. Since specific outdoor and indoor sports like 'running, cycling, swimming' are named, a corresponding tracking infrastructure must exist within the app.",
      "source_quotes": [
        "Record and manage your fitness activities, such as running, cycling, swimming, etc."
      ] 
    },
    { 
      "functionality": "Gym Equipment Synchronization (Hardware-Bound, Third-Party Integration)",
      "description": "In combination with a Galaxy Watch, the app enables a connection to external fitness equipment from manufacturers like Life Fitness, Technogym, and Corehealth to synchronize workout data.",
      "reasoning": "The text explicitly mentions 'through Life Fitness, Technogym and Corehealth', from which it can be inferred that an IoT interface or API to these specific third-party ecosystems exists. For this reason, a pairing or data transfer function for external fitness equipment must be present.", 
      "source_quotes": [
        "Also, Galaxy Watch wearables user can now exercise more effectively through Life Fitness, Technogym and Corehealth."
      ]
    },
    { 
      "functionality": "Nutritional and Meal Tracking",
      "description": "The app offers functionalities for the digital logging of daily main meals and snacks to support the user in building healthy eating habits.",
      "reasoning": "The text explicitly mentions 'recording your daily meals and snacks', from which it can be inferred that a food input and logging system is present. For this reason, a database structure and a user interface for recording nutritional values and calories must exist within the app.",
      "source_quotes": [
        "Create healthy eating habits by recording your daily meals and snacks with Samsung Health."
      ]
    },
    { 
      "functionality": "Goal Setting and Vital Signs Tracking",
      "description": "The app allows users to set individual goals and monitor daily activity, workout intensity, heart rate, stress, and blood oxygen levels.", 
      "reasoning": "The text explicitly mentions 'Set goals' and 'keep track of your daily condition including your activity amount, workout intensity, heart rate, stress, oxygen level', from which it can be inferred that a central function for personal health management is available. For this reason, interfaces to biometric sensors must exist.",
      "source_quotes": [
        "Set goals that work for your own level",
        "keep track of your daily condition including your activity amount, workout intensity, heart rate, stress, oxygen level in the blood, etc."
      ] 
    },
    { 
      "functionality": "Sleep Monitoring and Analysis (Hardware-Bound)",
      "description": "In connection with a compatible smartwatch (Galaxy Watch), the app enables a detailed analysis of sleep patterns, sleep stages, and the calculation of a sleep score to improve sleep quality.", 
      "reasoning": "The text explicitly mentions 'with Galaxy Watch' to 'Monitor your sleep patterns', from which it can be inferred that a pairing function with an external smartwatch is supported. For this reason, a hardware-bound synchronization or Bluetooth interface must exist.", 
      "source_quotes": [
        "Monitor your sleep patterns in more detail with Galaxy Watch.",
        "improving the quality of your sleep through sleep levels and sleep scores"
      ] 
    },
    { 
      "functionality": "Social Challenges (Samsung Health Together)",
      "description": "The app provides an interactive platform to compete in fitness challenges with friends and family members and pursue health goals together.",
      "reasoning": "The text explicitly mentions 'Challenge yourself against your friends', from which it can be inferred that a social interaction component (gamification) is available that goes beyond the purely individual use of the app. For this reason, a network and contact interface must exist.",
      "source_quotes": [
        "Challenge yourself against your friends and family to become healthier in a more fun and interactive way with Samsung Health Together."
      ] 
    },
    {
      "functionality": "Video-Based Fitness Coaching",
      "description": "The app provides guided workout videos from professional trainers covering various fitness programs such as stretching, weight loss, and more.", 
      "reasoning": "The text explicitly mentions 'videos' in combination with 'expert coaches', from which it can be inferred that the app does not only offer text-based plans but possesses a visual, guided coaching function instead. For this reason, a video-streaming component must be implemented.", 
      "source_quotes": [
        "Samsung Health has prepared videos of expert coaches who will teach you new fitness programs including stretching, weight loss, and more."
      ]
    },
    { 
      "functionality": "Mindfulness and Meditation Exercises",
      "description": "The app provides meditation tools and mindfulness exercises designed to support the user in relieving daily stress.",
      "reasoning": "The text explicitly mentions 'Discover meditation tools' for the purpose to 'help you relieve stress', from which it can be inferred that a functional support system for stress management is available. For this reason, an audio- or text-based relaxation module exists.",
      "source_quotes": [
        "Discover meditation tools on Mindfulness that will help you relieve stress throughout your day."
      ] 
    },
    { 
      "functionality": "Menstrual Cycle Tracking (Third-Party Integration)",
      "description": "In cooperation with the partner 'Natural Cycles', the app offers features for logging the menstrual cycle, managing related symptoms, and providing personalized insights and content.",
      "reasoning": "The text explicitly mentions 'helpful support in menstrual cycle tracking' in connection with 'through your partner, Natural Cycles', from which it can be inferred that the app processes cycle data but relies on an external software integration for this feature. For this reason, a partner API must exist.", 
      "source_quotes": [
        "Cycle tracking offers helpful support in menstrual cycle tracking, related symptom management and personalized insights and contents through your partner, Natural Cycles."
      ] 
    },
    {
      "functionality": "Hardware-Based Data Security (Samsung Knox Integration)", 
      "description": "The app integrates a hardware-backed security architecture to protect private health data on a system level against unauthorized access. This security feature is exclusively available for devices released after August 2016 and is blocked on rooted smartphones for safety reasons.",
      "reasoning": "The text explicitly mentions 'Knox enabled Samsung Health service', from which it can be inferred that a hardware-level security component is integrated. The phrases 'released after August 2016' and 'not be available from rooted mobile' serve as direct technical constraints. For this reason, system-level architecture checks must exist.",
      "source_quotes": [
        "Samsung Health protects your private health data securely.",
        "All Samsung Galaxy models released after August 2016, Knox enabled Samsung Health service will be available.",
        "Please note that Knox enabled Samsung Health service will not be available from rooted mobile."
      ]
    },
    {
      "functionality": "Global Language Support",
      "description": "The app features a multilingual user interface supporting over 70 languages, including English, French, and Chinese, to ensure worldwide usability.",
      "reasoning": "The text explicitly mentions 'Supports over 70 languages', from which it can be inferred that the app has the technical capability to dynamically adapt its UI to various native languages. The addition regarding the English version for the 'rest of the world' confirms the existence of a global fallback system.",
      "source_quotes": [
        "Supports over 70 languages, including English, French, and Chinese.",
        "An English language version is available for the rest of the world."
      ]
    }
  ]
}