from dotenv import load_dotenv
load_dotenv()

from src.models.schema import PipelineState, AppAnalysis, FeatureExtraction
from src.chains.pipeline import build_pipeline

def main() -> None:
    
    pipeline = build_pipeline()

    # initial_data = {
    #     "app_title": "FitnessTracker",
    #     "app_description": "Eine Fitness-Tracker-App erfasst automatisch Schritte, Kalorienverbrauch und körperliche Aktivitäten wie Laufen oder Radfahren. Sie zeigt Fortschritte in übersichtlichen Statistiken und hilft dabei, persönliche Fitnessziele zu erreichen. Zusätzlich kann sie an Bewegung erinnern und motiviert durch tägliche Ziele oder Challenges."
    # }
    
    initial_data = {
    "app_title": "TrailBlaze Pro",
    "app_description": "TrailBlaze Pro ist der ultimative Begleiter für alle Outdoor-Begeisterten, die sich abseits bekannter Wege bewegen wollen. Die App bietet hochauflösende topografische Karten, die sich für die Nutzung ohne Internetempfang vollständig für ganze Regionen lokal auf dem Gerät speichern lassen. Mit dem intelligenten Routenplaner können Nutzer individuelle Touren erstellen, wobei das System automatisch zwischen Profilen für Wandern, Rennrad oder Mountainbike unterscheidet und dabei Faktoren wie Steigung, Bodenbeschaffenheit und Verkehrslage berücksichtigt. Während der Tour führt eine präzise Sprachnavigation sicher über jeden Pfad, während der integrierte barometrische Höhenmesser und der digitale Kompass in Echtzeit Daten zur aktuellen Position liefern. Für zusätzliche Sicherheit sorgt das Live-Standort-Tracking, mit dem die eigene Position in Echtzeit mit Notfallkontakten geteilt werden kann, sowie ein umfangreiches Verzeichnis wichtiger Wegpunkte wie Trinkwasserstellen, Schutzhütten, Ladestationen für E-Bikes und Berggipfel."
    }

    # Pipeline ausführen
    final_state = pipeline.invoke(initial_data)

    # Ausgabe der Ergebnisse
    print(f"Input: {final_state['app_title']}")
    print(f"Stage 1 Log: {final_state['stage1_result']}")
    print(f"Stage 2 Features: {final_state['stage2_result'].features[0].functionality}")
    print(f"Stage 3 Log: {final_state['stage3_result']}")

if __name__ == "__main__":
    main()




