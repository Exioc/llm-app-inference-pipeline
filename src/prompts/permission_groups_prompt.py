from langchain_core.prompts import ChatPromptTemplate

PERMISSION_GROUPS_PROMPT = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an Android security expert. Your task is to analyze the provided app feature "
            "and determine its required Android permission groups.\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. You must keep the 'title' and 'description' exactly as provided. Do not alter them.\n"
            "2. Fill the 'groups' list with the correct permission categories.\n"
            "3. If the feature doesn't need any permissions, set 'groups' to ['NONE']."
        )),
        ("human", (
            "Please analyze this feature and fill in the missing permission groups:\n"
            "Title: {label}\n"
            "Description: {description}"
        ))
    ])