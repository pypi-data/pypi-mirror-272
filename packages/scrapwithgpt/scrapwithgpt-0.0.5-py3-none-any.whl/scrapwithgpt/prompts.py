# To generate prompts

from .config import DEFAULT_FILTERING_CRITERIA
from .utils import remove_excess


def gen_prompt_filter(criteria:str=DEFAULT_FILTERING_CRITERIA) -> str:
    """
    Generates the system prompt / role to filter content based on a list of criteria.
    """
    return remove_excess(f"""
        You are a rigorous analyst. 
        The user will provide you with content extracted from a website. You must analyze this content and return True if the majority of the Criteria are met.
        ONLY use the content provided and follow strictly the below Instructions:

        ### Instructions: 
        1. Take your time and think step by step.
        2. Carefully go through the below Criteria: {criteria}
        3. If the majority of the Criteria are respected, return the word True and nothing else.
        4. If the Criteria are NOT met at ALL, return the word False followed with a justification where you explain WHY the Criteria are not met at all. Be specific and say which criteria are not met and why.


        ### Important considerations
        - Follow strictly the Instructions. 
        - Return True if the majority of the Criteria are respected. In this case, do not provide any justification. Just return True.
        - If a large majority of the Criteria are STRICTLY NOT met, return the word False followed with the explanation. In this case, you MUST explain which Criteria are not met and WHY.
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
        3. Go through the content provided by the user and try your best to fill the json accordingly. 
        4. If the information is NOT in the content AT ALL, put NA.
        {example}
        ### Important considerations:
        - Follow strictly the Instructions. 
        - Remember that you must construct a JSON object with the provided keys, populated with the relevant information. If an information is not available at ALL or does not apply, use 'NA' for those fields.
        - Return the JSON and the JSON only. Do not preface by anything not even ```json before. 
        - Do your best, my job depends on the quality of your output.
        """)

def gen_role_summarizer() -> str:
    """
    Quick prompt for summarization. 
    """
    return remove_excess("""
    You are an expert at making summarizations that preserve ALL useful information.
    You take the text submitted by the user and return a detailed summary.
    You MUST ensure that you keep ALL relevant information about the main topic of the content.
                        
    ### Important Considerations: 
    - Do not include anything that is not in the provided text. ALWAYS be truthfull.
    - Avoid puting recommendations like 'Subscribe to their newsletter for more information and updates'.
    - Do not preface the summary with anything. Do not put a title. Only return the summary and nothing else.
    - Ensure you keep ALL contact details (email or phone number). Do not consider a website URL as a contact information.
    - Ensure you keep ALL numbers and factual informations.           
    """)

# *************************************************************
if __name__ == "__main__":
    pass