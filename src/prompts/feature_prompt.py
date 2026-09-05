from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
import json

from src.config.config import (
    google_one_few_shot,
    samsung_health_few_shot,
    petal_maps_gps_and_navigation_few_shot
)

SYSTEM_PROMPT = (
    "You are a Senior Requirements Analyst and Technical Documentation Auditor.\n"
    "Your objective is to systematically analyze app descriptions and extract ONLY explicitly mentioned features and capabilities. "
    "Do not infer, assume, or extrapolate implied capabilities, technical backends, or unstated workflows.\n\n"

    "### EXTRACTION RULES:\n"
    "1. STRICT LITERAL EXTRACTION:\n"
    "   - Extract a feature ONLY if it is explicitly stated in the text.\n"
    "   - Write a detailed, comprehensive description of the feature based strictly on the provided context.\n"
    "   - Do not add hypothesized functionality, external APIs, databases, or unmentioned systems.\n\n"

    "2. REASONING & DIRECT MAPPING:\n"
    "   - Explain how the extracted feature maps directly to the text snippet.\n"
    "   - Demonstrate the exact link between the explicit statement in the text and the documented feature.\n\n"

    "3. SOURCE QUOTES (VERBATIM EVIDENCE):\n"
    "   - For every extracted feature, provide 1 or more EXACT, verbatim text quotes from the input description.\n"
    "   - Never paraphrase or alter the source quotes.\n\n"

    "4. GRANULARITY & BUNDLING:\n"
    "   - Cohesive Bundle: Combine tightly coupled sub-capabilities mentioned together (e.g., 'send text messages and view typing indicators' -> Messaging System).\n"
    "   - Separate Entry: Isolate distinct capabilities into separate items (e.g., 'Photo Editing' vs. 'Cloud Storage').\n\n"

    "### OUTPUT FORMAT:\n"
    "All fields (title, description, reasoning) MUST be written in English. Strictly adhere to the required JSON schema."
)

HUMAN_PROMPT = (
    "Extract all explicitly mentioned features from the following app description according to your operational rules.\n\n"
    "App Title: {label}\n"
    "App Description:\n"
    "{description}"
)

FEATURE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    
    # -------------------------------------------------------------
    # START FEW-SHOT EXAMPLES 
    # -------------------------------------------------------------

    # Example 1
    ("human", "Now analyze the following app:\nTitle: " + google_one_few_shot["label"] + "\nDescription: " + google_one_few_shot["description"]),
    AIMessage(content=json.dumps(google_one_few_shot["output"], ensure_ascii=False)),

    #Example 2
    ("human", "Now analyze the following app:\nTitle: " + samsung_health_few_shot["label"] + "\nDescription: " + samsung_health_few_shot["description"]),
    AIMessage(content=json.dumps(samsung_health_few_shot["output"], ensure_ascii=False)),

    # Example 3
    ("human", "Now analyze the following app:\nTitle: " + petal_maps_gps_and_navigation_few_shot["label"] + "\nDescription: " + petal_maps_gps_and_navigation_few_shot["description"]),
    AIMessage(content=json.dumps(petal_maps_gps_and_navigation_few_shot["output"], ensure_ascii=False)),

    # -------------------------------------------------------------
    # END FEW-SHOT EXAMPLES
    # -------------------------------------------------------------

    ("human", HUMAN_PROMPT)
])
