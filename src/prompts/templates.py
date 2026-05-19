from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import json

EXAMPLE_FEATURES = [
    {
        "functionality": "Schritterkennung",
        "description": "Die App erfasst automatisch die Anzahl der Schritte des Nutzers.",
        "reasoning": "In der Beschreibung wird erwähnt, dass die App 'automatisch Schritte' erfasst. Dies impliziert eine Funktion, die Schritte zählt."
    },
    {
        "functionality": "Kalorienverbrauchserfassung",
        "description": "Die App erfasst den Kalorienverbrauch des Nutzers.",
        "reasoning": "Die Erwähnung von 'Kalorienverbrauch' impliziert eine Funktion zur Messung des Energieumsatzes."
    },
    {
        "functionality": "Erfassung körperlicher Aktivitäten",
        "description": "Die App erkennt und erfasst verschiedene Arten von körperlichen Aktivitäten wie Laufen oder Radfahren.",
        "reasoning": "Der Text nennt explizit 'körperliche Aktivitäten wie Laufen oder Radfahren', was eine Erkennungslogik voraussetzt."
    },
    {
        "functionality": "Statistikauswertung",
        "description": "Die App zeigt die Fortschritte des Nutzers in übersichtlichen Statistiken an.",
        "reasoning": "Die Passage 'Fortschritte in übersichtlichen Statistiken' deutet auf eine Datenvisualisierungs-Komponente hin."
    },
    {
        "functionality": "Fitnessziel-Setzung",
        "description": "Die App hilft dem Nutzer, persönliche Fitnessziele zu setzen und zu erreichen.",
        "reasoning": "Der Satz 'hilft dabei, persönliche Fitnessziele zu erreichen' impliziert ein Ziel-Management-System."
    },
    {
        "functionality": "Bewegungserinnerung",
        "description": "Die App kann den Nutzer an Bewegung erinnern, wenn dieser zu lange inaktiv war.",
        "reasoning": "Die Aussage 'kann sie an Bewegung erinnern' bestätigt eine Benachrichtigungsfunktion bei Inaktivität."
    }
]

APP_ANALYSIS_PROMPT_WITH_EXAMPLE = ChatPromptTemplate.from_messages([
    ("system", (
        "Du bist ein erfahrener Product Owner und Business Analyst. "
        "Deine Aufgabe ist es, aus einer App-Beschreibung alle technischen Funktionalitäten zu extrahieren. "
        "Antworte strikt im vorgegebenen JSON-Format."
    )),
    
    # Start FEW-SHOT BEISPIEL
    ("human", (
        "Analysiere die folgende App:\n\n"
        "Titel: FitnessTracker\n"
        "Beschreibung: Eine Fitness-Tracker-App erfasst automatisch Schritte, "
        "Kalorienverbrauch und körperliche Aktivitäten wie Laufen oder Radfahren. "
        "Sie zeigt Fortschritte in übersichtlichen Statistiken und hilft dabei, "
        "persönliche Fitnessziele zu erreichen. Zusätzlich kann sie an Bewegung "
        "erinnern und motiviert durch tägliche Ziele oder Challenges."
    )),
    AIMessage(content=json.dumps({"features": EXAMPLE_FEATURES}, ensure_ascii=False)),
    # Ende FEW-SHOT BEISPIEL

    ("human", (
        "Analysiere nun die folgende App:\n\n"
        "Titel: {label}\n"
        "Beschreibung: {description}\n\n"
        "Extrahiere alle Features mit Beschreibung und deinem Reasoning."
    ))
])
