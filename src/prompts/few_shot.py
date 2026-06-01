import json

GOOGLE_ONE_LABEL = "Google One"

GOOGLE_ONE_DESCRIPTION = "The Google One app lets you automatically back up your phone and manage your Google cloud storage.<br>  • Automatically back up the important things on your phone, like photos, contacts and messages using your 15 GB of storage that comes with every Google account. If you break, lose or upgrade your phone, you can restore everything to your new Android device.<br>  • Manage your existing Google account storage across Google Drive, Gmail and Google Photos.<br><br>  Upgrade to a Google One membership to get even more:<br>  • Get as much storage as you need for your important memories, projects and digital files. Choose the plan that works best for you."

GOOGLE_ONE_OUTPUT = {
  "features": [
    {
        "functionality": "Automatisierte Datensicherung",
        "description": "Die App sichert im Hintergrund automatisch persönliche Smartphone-Inhalte wie Fotos, Kontakte und Textnachrichten. Für diese kostenlose Basissicherung stellt die App ein Speicherlimit von 15 GB pro Google-Konto bereit.",
        "reasoning": "Der Befehl 'Automatically back up the important things' in Verbindung mit der Zuweisung von '15 GB of storage' belegt eine automatisierte Daten-Upload-Funktion. Aus diesem Grund muss in der App ein Hintergrunddienst implementiert sein, der lokale Systemdaten ausliest und an Cloud-Server überträgt.",
        "source_quotes": [
        "The Google One app lets you automatically back up your phone",
        "Automatically back up the important things on your phone, like photos, contacts and messages using your 15 GB of storage that comes with every Google account."
        ]
    },
    {
        "functionality": "Zentralisiertes Speicher-Management",
        "description": "Die App bietet eine zentrale Verwaltungsoberfläche, um den verbrauchten und verfügbaren Cloud-Speicherplatz über die verschiedenen Google-Dienste (Drive, Gmail und Photos) hinweg zu überwachen.",
        "reasoning": "Die Formulierung 'Manage your existing Google account storage across...' zeigt, dass die App als Aggregator fungiert. Aus diesem Grund muss eine Dashboard-Schnittstelle existieren, die Speicherdaten aus separaten Google-Ökosystemen ausliest und visuell zusammenfasst.",
        "source_quotes": [
        "manage your Google cloud storage.",
        "Manage your existing Google account storage across Google Drive, Gmail and Google Photos."
        ]
    },
    {
        "functionality": "Datenwiederherstellung (Disaster Recovery)",
        "description": "Ermöglicht es dem Nutzer, im Falle eines Geräteverlusts, Schadens oder Smartphone-Wechsels, die zuvor in der Cloud gesicherten Daten vollständig auf einem neuen Android-Gerät einzuspielen.",
        "reasoning": "Das Szenario 'If you break, lose or upgrade... you can restore everything' beschreibt einen klassischen Recovery-Prozess. Aus diesem Grund muss eine dedizierte technische Routine zur Daten-Abfrage und lokalen System-Wiederherstellung integriert sein.",
        "source_quotes": [
        "If you break, lose or upgrade your phone, you can restore everything to your new Android device."
        ]
    },
    {
        "functionality": "Skalierbares Speicher-Upgrade",
        "description": "Nutzer können ein kostenpflichtiges Google One Abonnement abschließen, um das Speicherplatz-Limit flexibel über verschiedene Abonnement-Stufen (Tarifpläne) hinweg an ihren individuellen Bedarf anzupassen.",
        "reasoning": "Die Aufforderung 'Upgrade to a Google One membership' kombiniert mit 'Choose the plan' beweist, dass die App eine Schnittstelle zu einem Bezahlsystem besitzt. Aus diesem Grund muss eine In-App-Kaufabwicklung und eine dynamische Speicher-Skalierung auf Serverebene existieren.",
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
      "functionality": "Automatisierte Aktivitätsverfolgung",
      "description": "Die App erfasst sportliche und alltägliche Aktivitäten im Hintergrund automatisch, um dem Nutzer die Dokumentation seines Lebensstils ohne manuelle Eingaben zu erleichtern.",
      "reasoning": "Aus der Formulierung 'automatically record many activities' lässt sich ableiten, dass die App über eine Sensor-gestützte Hintergrund-Erkennung verfügt. Da das Ziel als 'easier and simpler than ever' beschrieben wird, muss ein technischer Automatismus existieren, der dem Nutzer die manuelle Protokollierung abnimmt.",
      "source_quotes": [
        "Samsung Health has various features to help you manage your health.",
        "As the app allows you to automatically record many activities, creating a healthy lifestyle is easier and simpler than ever."
      ]
    },
    { 
      "functionality": "Zentrales Gesundheits-Dashboard",
      "description": "Die App bietet eine Übersichtsseite auf dem Startbildschirm, um verschiedene persönliche Gesundheitsdaten wie tägliche Schritte und die Aktivitätszeit direkt einzusehen.", 
      "reasoning": "Der direkte Aufruf 'Check various health records on the home screen' beweist, dass die App über eine zentrale Benutzeroberfläche (Dashboard) verfügt, die als Sammelbecken für unterschiedliche Messwerte dient. Aus diesem Grund muss eine visuelle Anzeige-Funktion für diese Daten existieren.",
      "source_quotes": [
        "Check various health records on the home screen.",
        "such as daily steps and activity time."
      ] 
    },
    { 
      "functionality": "Dashboard-Personalisierung",
      "description": "Nutzer können die auf dem Startbildschirm angezeigten Widgets und Datenfelder flexibel hinzufügen oder bearbeiten, um die Verwaltung ihrer Gesundheitswerte individuell anzupassen.",
      "reasoning": "Die Handlungsaufforderung 'Easily add and edit the items' zeigt, dass der Startbildschirm kein starres Layout hat. Da der Nutzer Elemente selbst verwalten kann ('that you want to manage'), muss eine technische Konfigurations- und Editier-Funktion innerhalb der Benutzeroberfläche existieren.",
      "source_quotes": [
        "Easily add and edit the items that you want to manage such as daily steps and activity time."
      ] 
    },
    { 
      "functionality": "Manuelle und sensorbasierte Aktivitätsaufzeichnung",
      "description": "Die App ermöglicht die Dokumentation und das Tracking verschiedener Sportarten wie Laufen, Radfahren und Schwimmen.",
      "reasoning": "Die Handlungsaufforderung 'Record and manage your fitness activities' beweist, dass die App über Module zur Datenerfassung und Speicherung von Workouts verfügt. Da spezifische Outdoor- und Indoor-Sportarten ('running, cycling, swimming') genannt werden, muss eine entsprechende Tracking-Infrastruktur in der App existieren.",
      "source_quotes": [
        "Record and manage your fitness activities, such as running, cycling, swimming, etc."
      ] 
    },
    { 
      "functionality": "Synchronisation mit Studio-Fitnessgeräten (Hardware-gebunden, Drittanbieter-Integration)",
      "description": "In Kombination mit einer Galaxy Watch ermöglicht die App eine Verbindung zu externen Fitnessgeräten von Herstellern wie Life Fitness, Technogym und Corehealth, um Trainingsdaten zu synchronisieren.",
      "reasoning": "Der Verweis, dass Nutzer 'through Life Fitness, Technogym and Corehealth' effektiver trainieren können, lässt darauf schließen, dass eine IoT-Schnittstelle oder API zu diesen spezifischen Drittanbieter-Ökosystemen existiert. Aus diesem Grund muss eine Kopplungs- oder Datentransfer-Funktion für externe Fitnessgeräte vorhanden sein.", 
      "source_quotes": [
        "Also, Galaxy Watch wearables user can now exercise more effectively through Life Fitness, Technogym and Corehealth."
      ]
    },
    { 
      "functionality": "Ernährungs- und Mahlzeitentracking",
      "description": "Die App bietet Funktionen zur digitalen Protokollierung der täglichen Hauptmahlzeiten und Zwischenmahlzeiten, um den Nutzer beim Aufbau gesunder Essgewohnheiten zu unterstützen.",
      "reasoning": "Die Handlungsaufforderung 'recording your daily meals and snacks' belegt direkt die Existenz eines Eingabe- und Protokollierungssystems für Lebensmittel. Aus diesem Grund muss in der App eine Datenbankstruktur sowie eine Benutzeroberfläche zur Erfassung von Nährwerten und Kalorien existieren.",
      "source_quotes": [
        "Create healthy eating habits by recording your daily meals and snacks with Samsung Health."
      ]
    },
    { 
      "functionality": "Zielsetzung und Vitaldaten-Verfolgung",
      "description": "Die App ermöglicht es, individuelle Ziele zu setzen und die tägliche Aktivität, Workout-Intensität, Herzfrequenz, Stress und den Sauerstoffgehalt im Blut zu überwachen.", 
      "reasoning": "Aus den Formulierungen zur Zielanpassung ('Set goals') und der lückenlosen Überwachung diverser Vitalwerte ('heart rate, stress, oxygen level') lässt sich eine zentrale Funktion zum persönlichen Gesundheitsmanagement ableiten. Aus diesem Grund müssen Schnittstellen zu biometrischen Sensoren existieren.",
      "source_quotes": [
        "Set goals that work for your own level",
        "keep track of your daily condition including your activity amount, workout intensity, heart rate, stress, oxygen level in the blood, etc."
      ] 
    },
    { 
      "functionality": "Schlafüberwachung und -analyse (Hardware-gebunden)",
      "description": "In Verbindung mit einer kompatiblen Smartwatch (Galaxy Watch) ermöglicht die App eine detaillierte Analyse von Schlafmustern, Schlafphasen und die Berechnung eines Schlaf-Scores zur Verbesserung der Schlafqualität.", 
      "reasoning": "Der Text beschreibt das Feature explizit als Kopplungsfunktion mit einer externen Smartwatch ('with Galaxy Watch'), um Schlafmuster zu überwachen. Aus diesem Grund muss eine Bluetooth- oder Synchronisationsschnittstelle zur Hardware existieren.", 
      "source_quotes": [
        "Monitor your sleep patterns in more detail with Galaxy Watch.",
        "improving the quality of your sleep through sleep levels and sleep scores"
      ] 
    },
    { 
      "functionality": "Soziale Herausforderungen (Samsung Health Together)",
      "description": "Die App bietet eine interaktive Plattform, um sich in Fitness-Herausforderungen mit Freunden und Familienmitgliedern zu messen und gemeinsam gesundheitliche Ziele zu verfolgen.",
      "reasoning": "Der Aufruf 'Challenge yourself against your friends' beweist die Existenz einer sozialen Interaktionskomponente (Gamification), die über die reine Eigennutzung der App hinausgeht. Aus diesem Grund muss eine Netzwerk- und Kontakte-Schnittstelle existieren.",
      "source_quotes": [
        "Challenge yourself against your friends and family to become healthier in a more fun and interactive way with Samsung Health Together."
      ] 
    },
    {
      "functionality": "Video-basiertes Fitness-Coaching",
      "description": "Die App stellt angeleitete Trainingsvideos von professionellen Trainern bereit, die verschiedene Fitnessprogramme wie Dehnübungen und Gewichtsreduktion abdecken.", 
      "reasoning": "Die explizite Nennung von 'videos' in Kombination mit 'expert coaches' belegt, dass die App nicht nur Textpläne anbietet, sondern eine visuelle, angeleitete Coaching-Funktion besitzt. Aus diesem Grund muss eine Videostreaming-Komponente implementiert sein.", 
      "source_quotes": [
        "Samsung Health has prepared videos of expert coaches who will teach you new fitness programs including stretching, weight loss, and more."
      ]
    },
    { 
      "functionality": "Achtsamkeits- und Meditationsübungen",
      "description": "Die App stellt Meditationswerkzeuge und Achtsamkeitsübungen bereit, die den Nutzer dabei unterstützen, alltäglichen Stress abzubauen.",
      "reasoning": "Der direkte Aufruf 'Discover meditation tools' in Kombination mit dem Zweck 'help you relieve stress' belegt die Existenz einer funktionalen Unterstützung zur Stressbewältigung. Aus diesem Grund existiert ein Audio- oder Text-basiertes Entspannungsmodul.",
      "source_quotes": [
        "Discover meditation tools on Mindfulness that will help you relieve stress throughout your day."
      ] 
    },
    { 
      "functionality": "Menstruations- und Zyklustracking (Drittanbieter-Integration)",
      "description": "In Kooperation mit dem Partner 'Natural Cycles' bietet die App Funktionen zur Protokollierung des Menstruationszyklus, zur Verwaltung damit verbundener Symptome sowie personalisierte Auswertungen und Inhalte.",
      "reasoning": "Die Formulierung 'helpful support in menstrual cycle tracking' in Verbindung mit dem Verweis 'through your partner, Natural Cycles' belegt, dass die App Zyklusdaten verarbeitet, das Feature jedoch auf einer externen Software-Integration basiert.", 
      "source_quotes": [
        "Cycle tracking offers helpful support in menstrual cycle tracking, related symptom management and personalized insights and contents through your partner, Natural Cycles."
      ] 
    },
    {
      "functionality": "Hardware-basierte Datensicherheit (Samsung Knox Integration)", 
      "description": "Die App integriert eine hardwaregestützte Sicherheitsarchitektur, um private Gesundheitsdaten auf Systemebene vor unbefugtem Zugriff zu schützen. Dieses Sicherheitsfeature ist exklusiv für Geräte ab dem Veröffentlichungsjahr 2016 verfügbar und wird auf gerooteten Smartphones aus Sicherheitsgründen blockiert.",
      "reasoning": "Der Begriff 'Knox enabled Samsung Health service' belegt die Integration einer hardwarenahen Sicherheitskomponente. Die Phrasen 'released after August 2016' und 'not be available from rooted mobile' dienen als direkte Belege für die technischen Hardware- und Software-Einschränkungen dieses Features.",
      "source_quotes": [
        "Samsung Health protects your private health data securely.",
        "All Samsung Galaxy models released after August 2016, Knox enabled Samsung Health service will be available.",
        "Please note that Knox enabled Samsung Health service will not be available from rooted mobile."
      ]
    },
    {
      "functionality": "Globale Sprachunterstützung",
      "description": "Die App bietet eine mehrsprachige Benutzeroberfläche mit Unterstützung für über 70 Sprachen, darunter Englisch, Französisch und Chinesisch, um eine weltweite Nutzbarkeit zu gewährleisten.",
      "reasoning": "Die explizite Angabe 'Supports over 70 languages' belegt direkt die technische Fähigkeit der App, die Benutzeroberfläche dynamisch an verschiedene Landessprachen anzupassen. Der Zusatz über die englische Version für den 'rest of the world' bestätigt zudem die Existenz eines globalen Fallback-Systems.",
      "source_quotes": [
        "Supports over 70 languages, including English, French, and Chinese.",
        "An English language version is available for the rest of the world."
      ]
    }
  ]
}


# GOOGLE_ONE_OUTPUT = [
#     {
#         "functionality": "Automatische Sicherung von Telefoninhalten",
#         "description": "Die App sichert automatisch wichtige Inhalte auf dem Telefon, wie Fotos, Kontakte und Nachrichten im Cloud-Speicher.",
#         "reasoning": "Der Text erwähnt explizit 'Automatically back up the important things on your phone, like photos, contacts and messages', was auf eine zentrale, automatisierte Datensicherungsfunktion hinweist."
#     },

#     {
#         "functionality": "Verwaltung des Cloud-Speichers",
#         "description": "Die App ermöglicht die Verwaltung des Google Cloud-Speichers über verschiedene Dienste wie Google Drive, Gmail und Google Photos.",
#         "reasoning": "Der Text erwähnt 'manage your existing Google account storage across Google Drive, Gmail and Google Photos', was auf eine umfassende Speicher-Verwaltungsfunktion hinweist."
#     },

#     {
#         "functionality": "Wiederherstellung von Sicherungen",
#         "description": "Die App ermöglicht die Wiederherstellung der gesicherten Daten auf einem neuen Android-Gerät.",
#         "reasoning": "Der Text erwähnt 'If you break, lose or upgrade your phone, you can restore everything to your new Android device.', was darauf schließen lässt, dass eine Wiederherstellungs-Funktion vorhanden ist."
#     },

#     {
#         "functionality": "Anpassbarer Cloud-Speicher",
#         "description": "Die App bietet die Möglichkeit, den Speicherplatz flexibel anzupassen.",
#         "reasoning": "Der Text erwähnt 'Get as much storage as you need […] Choose the plan that works best for you. ', was auf eine flexible Speicheranpassung hinweist."
#     }
# ]

