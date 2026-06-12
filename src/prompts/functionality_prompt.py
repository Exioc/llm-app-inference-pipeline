from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import json

from src.prompts.functionality_few_shot import (
    GOOGLE_ONE_LABEL,
    GOOGLE_ONE_DESCRIPTION,
    GOOGLE_ONE_OUTPUT,
    SAMSUNG_HEALTH_LABEL,
    SAMSUNG_HEALTH_DESCRIPTION,
    SAMSUNG_HEALTH_OUTPUT,
    PETAL_MAPS_GPS_AND_NAVIGATION_LABEL,
    PETAL_MAPS_GPS_AND_NAVIGATION_DESCRIPTION,
    PETAL_MAPS_GPS_AND_NAVIGATION_OUTPUT
)

SYSTEM_PROMPT = (
    "You are an expert Product Owner and Technical Business Analyst.\n"
    "Your job is to read an app description, identify its core features, and document them comprehensively.\n\n"
    
    "STEP 1: FEATURE EXTRACTION & COMPREHENSIVE DESCRIPTION\n"
    "Identify a functionality. Write a highly detailed description of it. Do not summarize or shorten it—include "
    "all capabilities, scope, conditions, and limitations mentioned in the text.\n\n"
    
    "STEP 2: REASONING VIA DETECTION (DIRECT VS. INFERENCE)\n"
    "Explain exactly HOW you detected the feature from the text. Your reasoning must show the path from the text clue to the feature:\n"
    "- Direct Path: The text explicitly names the capability (e.g., text says 'edit your profile picture' -> feature is Profile Customization).\n"
    "- Inference Path: The text uses an indirect phrase or contextual fact (e.g., text says 'stay in touch with your family' -> you logically infer "
    "that a communication feature like a 'Chat or Messaging System' must exist, because staying in touch requires a communication medium).\n\n"
    
    "CRITICAL GRANULARITY RULE:\n"
    "Bundle sub-features that fundamentally rely on each other to make sense and cannot stand alone (e.g., text messaging + typing indicators "
    "belong in one cohesive framework). Isolate a feature into a separate entry ONLY if a completely distinct capability, unique media type, "
    "or different interaction method (e.g., video streaming or file storage) is introduced.\n\n"
    
    "OUTPUT LANGUAGE:\n"
    "All fields within the schema (functionality, description, reasoning) MUST be written in English. Respond exclusively "
    "using the enforced JSON output schema."
)

HUMAN_PROMPT = (
    "Analyze this app description and perform the feature extraction according to the rules.\n\n"
    
    "App Title: {label}\n"
    "App Description:\n"
    "{description}\n\n"
    
    "Execution Reminder:\n"
    "1. Make the 'description' field as comprehensive and extensive as possible without omitting any scope or details.\n"
    "2. In the 'reasoning' field, you must justify the feature's existence using the Aggregated Deduction Rule. "
    "Clearly connect one or multiple literal clues (Fact 1, Fact 2, ..., Fact N) from the text to form your proof. "
    "Explicitly state whether this is based on a direct evidence loop or a tight logical inference. "
    "Do not invent or hypothesize about underlying technical systems, APIs, or software architectures."
)

# 3. Baue das Template zusammen und übergib die Variablen als Rollen-Tupel
FUNCTIONALITY_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    
    # -------------------------------------------------------------
    # START FEW-SHOT BEISPIELE (Der Dialog-Wechsel)
    # -------------------------------------------------------------

    # Beispiel 1 (Productivity)
    ("human", "Now analyze the following app:\nTitle: " + GOOGLE_ONE_LABEL + "\nDescription: " + GOOGLE_ONE_DESCRIPTION),
    AIMessage(content=json.dumps(GOOGLE_ONE_OUTPUT, ensure_ascii=False)),

    #Beispiel 2 (Health)
    ("human", "Now analyze the following app:\nTitle: " + SAMSUNG_HEALTH_LABEL + "\nDescription: " + SAMSUNG_HEALTH_DESCRIPTION),
    AIMessage(content=json.dumps(SAMSUNG_HEALTH_OUTPUT, ensure_ascii=False)),

    # Beispiel 3 (Maps & Navigation)
    ("human", "Now analyze the following app:\nTitle: " + PETAL_MAPS_GPS_AND_NAVIGATION_LABEL + "\nDescription: " + PETAL_MAPS_GPS_AND_NAVIGATION_DESCRIPTION),
    AIMessage(content=json.dumps(PETAL_MAPS_GPS_AND_NAVIGATION_OUTPUT, ensure_ascii=False)),

    # -------------------------------------------------------------
    # ENDE FEW-SHOT BEISPIELE
    # -------------------------------------------------------------

    ("human", HUMAN_PROMPT)
])
