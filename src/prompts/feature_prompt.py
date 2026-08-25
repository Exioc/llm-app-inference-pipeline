from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import json

from src.config.config import (
    google_one_few_shot,
    samsung_health_few_shot,
    petal_maps_gps_and_navigation_few_shot
)

# SYSTEM_PROMPT = (
#     "You are a Senior Requirements Analyst and Security Architecture Expert.\n"
#     "Your objective is to analyze app descriptions and extract user-facing features at the exact level of granularity required for Access Control & Permission Modeling (e.g., RBAC/ABAC).\n\n"

#     "### GRANULARITY PRINCIPLE (CRITICAL):\n"
#     "- Target Granularity = 'Functional User Task'.\n"
#     "- Do NOT split UI interactions into micro-features (e.g., do NOT extract 'click button', 'open camera', or 'read input' separately).\n"
#     "- Do NOT merge unrelated domain areas into macro-features (e.g., do NOT group 'User Profile Management' and 'In-App Payment' into 'User Account').\n"
#     "- A feature MUST be scoped as: [Action] + [Data/Resource Object] + [Context/Scope].\n"
#     "  * RIGHT: 'Upload profile picture in account settings'\n"
#     "  * TOO FINE: 'Access device storage' OR 'Click upload button'\n"
#     "  * TOO COARSE: 'Manage User Account'\n\n"

#     "### EXTRACTION RULES:\n"
#     "1. FEATURE TITLE FORMATTING:\n"
#     "   - Every feature 'title' MUST strictly follow the pattern: 'Action + Object + Scope'\n"
#     "   - Example: 'Record and Share Audio Message in Group Chat'\n\n"

#     "2. STRICT FACTUAL GROUNDING:\n"
#     "   - Extract features ONLY based on explicit statements or direct functional capabilities mentioned in the text.\n"
#     "   - Do not invent unmentioned third-party systems or external services.\n\n"

#     "3. MANDATORY RESOURCE & CONTEXT IDENTIFICATION:\n"
#     "   - For each feature, capture the primary Resource/Entity being acted upon and its Context/Scope in the description.\n\n"

#     "4. VERBATIM EVIDENCE:\n"
#     "   - Provide 1 or more EXACT, verbatim quotes from the input text in 'source_quotes' that justify the feature extraction.\n\n"

#     "### OUTPUT INSTRUCTIONS:\n"
#     "All fields MUST be written in English. Strictly fill out the required output schema."
# )

# SYSTEM_PROMPT = (
#     "You are a Senior Requirements Analyst and Technical Documentation Auditor.\n"
#     "Your objective is to systematically analyze app descriptions and extract ONLY explicitly mentioned features and capabilities. "
#     "Do not infer, assume, or extrapolate implied capabilities, technical backends, or unstated workflows.\n\n"

#     "### EXTRACTION RULES:\n"
#     "1. STRICT LITERAL EXTRACTION:\n"
#     "   - Extract a feature ONLY if it is explicitly stated in the text.\n"
#     "   - Write a detailed, comprehensive description of the feature based strictly on the provided context.\n"
#     "   - Do not add hypothesized functionality, external APIs, databases, or unmentioned systems.\n\n"

#     "2. REASONING & DIRECT MAPPING:\n"
#     "   - Explain how the extracted feature maps directly to the text snippet.\n"
#     "   - Demonstrate the exact link between the explicit statement in the text and the documented feature.\n\n"

#     "3. SOURCE QUOTES (VERBATIM EVIDENCE):\n"
#     "   - For every extracted feature, provide 1 or more EXACT, verbatim text quotes from the input description.\n"
#     "   - Never paraphrase or alter the source quotes.\n\n"

#     "4. GRANULARITY & BUNDLING:\n"
#     "   - Cohesive Bundle: Combine tightly coupled sub-capabilities mentioned together (e.g., 'send text messages and view typing indicators' -> Messaging System).\n"
#     "   - Separate Entry: Isolate distinct capabilities into separate items (e.g., 'Photo Editing' vs. 'Cloud Storage').\n\n"

#     "### OUTPUT FORMAT:\n"
#     "All fields (title, description, reasoning) MUST be written in English. Strictly adhere to the required JSON schema."
# )

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
    "All fields within the schema (title, description, reasoning) MUST be written in English. Respond exclusively "
    "using the enforced JSON output schema."
)

HUMAN_PROMPT = (
    "Extract all explicitly mentioned features from the following app description according to your operational rules.\n\n"
    "App Title: {label}\n"
    "App Description:\n"
    "{description}"
)

# HUMAN_PROMPT = (
#     "Analyze this app description and perform the feature extraction according to the rules.\n\n"
    
#     "App Title: {label}\n"
#     "App Description:\n"
#     "{description}\n\n"
    
#     "Execution Reminder:\n"
#     "1. Make the 'description' field as comprehensive and extensive as possible without omitting any scope or details.\n"
#     "2. In the 'reasoning' field, you must justify the feature's existence using the Aggregated Deduction Rule. "
#     "Clearly connect one or multiple literal clues (Fact 1, Fact 2, ..., Fact N) from the text to form your proof. "
#     "Explicitly state whether this is based on a direct evidence loop or a tight logical inference. "
#     "Do not invent or hypothesize about underlying technical systems, APIs, or software architectures."
# )

FEATURE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    
    # -------------------------------------------------------------
    # START FEW-SHOT EXAMPLES 
    # -------------------------------------------------------------

    # Example 1 (Productivity)
    ("human", "Now analyze the following app:\nTitle: " + google_one_few_shot["label"] + "\nDescription: " + google_one_few_shot["description"]),
        AIMessage(content=json.dumps(google_one_few_shot["output"], ensure_ascii=False)),

    #Example 2 (Health)
    ("human", "Now analyze the following app:\nTitle: " + samsung_health_few_shot["label"] + "\nDescription: " + samsung_health_few_shot["description"]),
    AIMessage(content=json.dumps(samsung_health_few_shot["output"], ensure_ascii=False)),

    # Example 3 (Maps & Navigation)
    ("human", "Now analyze the following app:\nTitle: " + petal_maps_gps_and_navigation_few_shot["label"] + "\nDescription: " + petal_maps_gps_and_navigation_few_shot["description"]),
    AIMessage(content=json.dumps(petal_maps_gps_and_navigation_few_shot["output"], ensure_ascii=False)),

    # -------------------------------------------------------------
    # END FEW-SHOT EXAMPLES
    # -------------------------------------------------------------

    ("human", HUMAN_PROMPT)
])
