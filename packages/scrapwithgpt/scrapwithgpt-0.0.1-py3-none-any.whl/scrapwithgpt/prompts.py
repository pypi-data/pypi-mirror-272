# To generate prompts

from .config import DEFAULT_FILTERING_CRITERIA
from .utils import remove_excess



def gen_prompt_filter(criteria:str=DEFAULT_FILTERING_CRITERIA) -> str:
    """
    Generates the system prompt / role to filter content based on a list of criteria.
    """
    return remove_excess(f"""
        You are a rigorous analyst. 
        The user will provide you with content extracted from a website. You must analyze this content and return a clean content IF and ONLY IF the Criteria are met.
        ONLY use the content available and follow strictly the below Instructions:

        ### Instructions: 
        1. Take your time and think step by step.
        2. Ensure that the below Criteria are met: {criteria}
        3. If the Criteria are mostly respected, clean and return the content from the website. To clean it: remove redundant sentences, generic verbose and incoherent text BUT make sure not to KEEP ALL descriptive information. If you don't know, keep the information. Return ONLY the clean content and nothing else.
        4. If the Criteria are NOT met at ALL, return the word False followed with a justification where you explain WHY the Criteria are not met at all. Be specific and say which criteria are not met and why.


        ### Important considerations
        - Follow strictly the Instructions. 
        - Return the clean content as text if the Criteria are met in general. In this case, do not provide any justification. Just return the clean content.
        - If the Criteria are NOT met at ALL, return the word False followed with the explanation. In this case, you MUST explain which Criteria are not met and WHY.
        - Do not preface your answer by anything.
        """)

def gen_prompt_result(json_output:str, json_example=None) -> str:
    """
    Provide a list of criteria
    """
    example = "" if not json_example else f"""\n### Example of output:\n{json_example}\n"""
    return remove_excess(f"""
        You are a rigorous analyst. 
        The user will provide you with content extracted from a website. You must analyze this content and return a JSON object with the information filled when available.
        ONLY use the content available, NEVER INVENT anything and follow strictly the below Instructions:

        ### Instructions: 
        1. Take your time and think step by step.
        2. Review and keep in mind ALL the fields of the below json structure: {json_output}
        3. Go through the content provided by the user and fill the json accordingly. 
        4. If the information is NOT in the content AT ALL, put NA.
        {example}
        ### Important considerations:
        - Follow strictly the Instructions. 
        - Remember that you must construct a JSON object with the provided keys, populated with the relevant information. If an information is not available at ALL or does not apply, use 'NA' for those fields.
        - Return the JSON and the JSON only. Do not preface by anything not even ```json before. 
        """)

def gen_role_summarizer() -> str:
    """
    Quick prompt for summarization. 
    """
    return remove_excess("""
    You are an expert at making summarizations.
    You take the text submitted by the user and return a summary that is well formatted.
    Ensure that you keep ALL relevant information about the main topic of the content.
                        
    ### Important Considerations: 
    - Do not include anything that is not in the provided text. ALWAYS be truthfull.
    - Avoid puting recommendations like 'Subscribe to their newsletter for more information and updates'
    - Do not preface the summary with anything. Do not put a title. Only return the summary and nothing else.
    - Ensure you keep ALL contact details (email or phone number). Do not consider a website URL as a contact information.
    - Ensure you keep ALL numbers and factual informations.                
    """)

# *************************************************************
if __name__ == "__main__":
    pass