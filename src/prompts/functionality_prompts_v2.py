from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import json

from src.prompts.few_shot_en import (
    GOOGLE_ONE_INPUT, GOOGLE_ONE_OUTPUT
)

FUNCTIONALITY_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    # ("system", (
    # "Du bist ein erfahrener Product Owner und Business Analyst.\n"
    # "Deine Aufgabe ist es, aus einer App-Beschreibung alle technischen Funktionalitäten zu extrahieren.\n\n"
    # "FÜR JEDES FEATURE GILT EINE STRIKTE BELEGPFLICHT:\n"
    # "Das Feld 'reasoning' MUSS einen direkten, wortwörtlichen Verweis (Zitat in Anführungszeichen) "
    # "aus dem Originaltext enthalten, aus dem sich diese technische Funktionalität logisch ableiten lässt.\n\n"
    # "Antworte ausschließlich im vorgegebenen Ausgabe-Schema."
    # )),
    # ("system", (
    #     "Du bist ein erfahrener Product Owner und Business Analyst.\n"
    #     "Deine Aufgabe ist es, aus einer App-Beschreibung alle technischen Funktionalitäten zu extrahieren.\n\n"
    #     "FÜR JEDES FEATURE GILT DIESE STRUKTUR FÜR BELEGE:\n"
    #     "1. Das Feld 'reasoning' enthält die logische Kausalität. Nutze zwingend das Muster: "
    #     "'Der Text erwähnt explizit [KURZE SCHLÜSSELWÖRTER], woraus sich ableiten lässt, dass... Aus diesem Grund muss... existieren.'\n"
    #     "2. Das Feld 'source_quotes' liefert den ausführlichen Kontext. Packe dort alle vollständigen Sätze hinein, die das Feature beschreiben, inklusive aller Sätze mit Zusatzinformationen oder Bedingungen.\n\n"
    #     "Antworte ausschließlich im vorgegebenen Ausgabe-Schema."
    # )),
    ("system", (
    "You are an experienced Product Owner and Business Analyst.\n"
    "Your task is to extract all technical functionalities from an app description.\n\n"
    "THE FOLLOWING EVIDENCE STRUCTURE APPLIES TO EVERY FEATURE:\n"
    "1. The 'reasoning' field contains the logical causality. You must use the following pattern: "
    "'The text explicitly mentions [SHORT KEYWORDS], from which it can be inferred that... For this reason, the feature ... must exist.'\n"
    "2. The 'source_quotes' field provides the detailed context. Place all full sentences that describe the feature there, including all sentences containing additional information or conditions.\n\n"
    "Respond exclusively using the provided output schema."
    )),
    
    # -------------------------------------------------------------
    # START FEW-SHOT BEISPIELE (Der Dialog-Wechsel)
    # -------------------------------------------------------------

    # Beispiel 1 (Productivity)
    ("human", f"""Now analyze the following app:
    Title: {GOOGLE_ONE_LABEL}
    Description: {GOOGLE_ONE_DESCRIPTION}
    """),
    AIMessage(content=json.dumps(GOOGLE_ONE_OUTPUT, ensure_ascii=False)),

    # Beispiel 2 (Health)
    ("human", f"""Now analyze the following app:
    Title: {SAMSUNG_HEALTH_LABEL}
    Description: {SAMSUNG_HEALTH_DESCRIPTION}
    """),
    AIMessage(content=json.dumps(SAMSUNG_HEALTH_OUTPUT, ensure_ascii=False)),

    # Beispiel 3
    
    # Beispiel 4

    # Beispiel 5

    # -------------------------------------------------------------
    # ENDE FEW-SHOT BEISPIELE
    # -------------------------------------------------------------

    # ("human", (
    #     "Analysiere nun die folgende App:\n\n"
    #     "Titel: {label}\n"
    #     "Beschreibung: {description}\n\n"
    #     "Aufgabe:\n"
    #     "1. Extrahiere alle technischen Features gemäß des vorgegebenen Ausgabe-Schemas.\n"
    #     "2. WICHTIG: Nutze für das Feld 'reasoning' exakt dieses Textmuster: "
    #     "\"Der Text erwähnt explizit '[ZITAT]', was auf [LOGISCHE HERLEITUNG] hinweist.\""
    # ))
    # ("human", (
    #     "Analysiere nun die folgende App:\n\n"
    #     "Titel: {label}\n"
    #     "Beschreibung: {description}\n\n"
    #     "Aufgabe:\n"
    #     "1. Extrahiere alle technischen Features gemäß des vorgegebenen Ausgabe-Schemas.\n"
    #     "2. Beschränke Zitate im 'reasoning' auf die wesentlichen Kernbegriffe.\n"
    #     "3. Nutze 'source_quotes' für die ausführlichen Sätze und textlichen Zusatzinfos."
    # ))
    ("human", (
    "Now analyze the following app:\n\n"
    "Title: {label}\n"
    "Description: {description}\n\n"
    "Task:\n"
    "1. Extract all technical features according to the provided output schema.\n"
    "2. Restrict quotes within the 'reasoning' field to essential core terms/keywords only.\n"
    "3. Use 'source_quotes' for full sentences and relevant text-based additional information."
    ))
])
