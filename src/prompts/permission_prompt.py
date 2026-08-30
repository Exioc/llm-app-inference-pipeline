from langchain_core.prompts import ChatPromptTemplate

PERMISSION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an Android security expert. Your task is to analyze the provided app feature "
        "and determine its required individual **Android permissions** belonging specifically to the **{group_name}** group, "
        "based strictly on the allowed context provided below.\n\n"
        
        "CRITICAL INSTRUCTIONS:\n"
        "1. You MUST ONLY choose permission names from the **\"id\"** fields present inside the `<allowed_permissions>` section.\n"
        "2. Read the description of each individual permission carefully to see if the app feature justifies its usage.\n"
        "3. If NO permissions from the **{group_name}** group are required at all, return exactly ONE entry where 'permission_name' is set to 'NONE' and 'reasoning' to 'No permission required.'.\n\n"
        
        "EXPECTED OUTPUT FORMAT (JSON ONLY):\n"
        "{{\n"
        '  "inferences": [\n'
        '    {{\n'
        '      "permission_name": "CAMERA",\n'
        '      "reasoning": "Required to take photos."\n'
        "    }}\n"
        "  ]\n"
        "}}\n\n"
        
        "ALLOWED ANDROID PERMISSIONS CONTEXT FOR GROUP '{group_name}':\n"
        "<allowed_permissions>\n"
        "{allowed_context}\n"
        "</allowed_permissions>"
    )),
    ("human", (
        "Please analyze this feature specifically regarding the **{group_name}** permission group, "
        "and infer the required individual permissions along with your logical reasoning:\n"
        "Title: {label}\n"
        "Description: {description}\n"
    ))
])