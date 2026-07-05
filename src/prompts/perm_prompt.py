from langchain_core.prompts import ChatPromptTemplate

PERM_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an Android security expert. Your task is to analyze the provided app feature "
        "and determine its required individual **Android permissions** belonging specifically to the **{group_name}** group, "
        "based **strictly** on the allowed context provided below.\n\n"
        
        "CRITICAL INSTRUCTIONS:\n"
        "1. You MUST ONLY choose permission names from the **\"id\"** fields present inside the `<allowed_permissions>` section.\n"
        "2. Read the description of each individual permission carefully to see if the app feature justifies its usage.\n"
        "3. For EVERY actual permission you select (using its exact **\"id\"**), you MUST write a "
        "   clear logical reasoning. Setting 'reasoning' to null or leaving it empty for a valid permission is strictly FORBIDDEN.\n"
        "4. Only if the feature does not require ANY permissions from the **{group_name}** group at all, return exactly ONE entry "
        "   where 'permission_name' is set to 'NONE' and 'reasoning' is set strictly to null.\n\n"
        
        "ALLOWED ANDROID PERMISSIONS CONTEXT FOR GROUP '{group_name}':\n"
        "<allowed_permissions>\n"
        "{allowed_context}\n"
        "</allowed_permissions>"
    )),
    ("human", (
        "Please analyze this feature specifically regarding the **{group_name}** permission group, "
        "and infer the required individual permissions along with your logical reasoning:\n"
        "Feature Title: {label}\n"
        "Feature Description: {description}\n\n"
        "Target Permission Group to evaluate: {group_name}"
    ))
])