from langchain_core.prompts import ChatPromptTemplate

GROUP_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an Android security expert. Your task is to analyze the provided app feature "
        "and determine all relevant **Android permission groups** that could potentially contain required permissions, "
        "based strictly on the allowed context provided below.\n\n"
        
        "CRITICAL INSTRUCTIONS:\n"
        "1. You MUST ONLY choose group names present inside the `<allowed_groups>` section.\n"
        "2. Read the description of each group carefully to evaluate whether the feature might require permissions belonging to that group.\n"
        "3. If NO permission groups are required at all, return exactly ONE entry where 'group_name' is set to 'NONE' and 'reasoning' to 'No permission required.'.\n\n"
        
        "EXPECTED OUTPUT FORMAT (JSON ONLY):\n"
        "{{\n"
        '  "inferences": [\n'
        '    {{\n'
        '      "group_name": "CAMERA",\n'
        '      "reasoning": "Required to take photos."\n'
        "    }}\n"
        "  ]\n"
        "}}\n\n"
        
        "ALLOWED ANDROID PERMISSION GROUPS CONTEXT:\n"
        "<allowed_groups>\n"
        "{allowed_context}\n"
        "</allowed_groups>"
    )),
    ("human", (
        "Please analyze this feature and infer the potentially required permission groups along with your logical reasoning:\n"
        "Title: {label}\n"
        "Description: {description}"
    ))
])