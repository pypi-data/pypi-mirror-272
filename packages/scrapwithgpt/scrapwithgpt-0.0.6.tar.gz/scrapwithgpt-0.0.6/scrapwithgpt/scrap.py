#   Main function to scrap the page according to the criteria specified.

from .config import MAX_TOKEN_OUTPUT_DEFAULT_HUGE, MAX_TOKEN_OUTPUT_GPT3, MAX_TOKEN_GPT4_RESULT, MAX_TOKEN_WINDOW_GPT35_TURBO
from .prompts import gen_prompt_filter, gen_prompt_result, gen_role_summarizer
from .web import crawl_website, fetch_content_url, clean_url_to_filename
from .oai import ask_question_gpt, calculate_token, ask_question_gpt4
from .utils import get_now, log_issue


from typing import Optional
import json
import os

def smartscrap(url:str, desired_output:str=None, example_output:str=None, filtering_criteria:str=None, summarization:bool=True, full_website:bool=True, verbose:bool=None) -> Optional[str]:
    """
    Main function to scrap a website.

    Args:
        - url (str): The website to scrap
        - desired_output (str): A json like structure with the keys representing the information you want to find
        - filtering_criteria (str): A set of criteria the content must respect for the program to continue
        - summarization (bool): If you want also to output the summary of the website. True by default.

    Returns:
        - The content or None if issue. The content will also be put in a file named "gptscrapper_url.txt" in the current dir. 

    Note:    
    full_website is True by default. We scrap the full website up to 30 pages by default. Put it to False if you want to scrap ONLY the page.
    Change the crawl_website params to scrap more (or less) pages
    """
    try:
        final_content, summary = "", ""
        if full_website:
            if verbose: print(f"👷‍♂️ Crawling the full website {url}. Please be patient...")
            content = str(crawl_website(url))
            
        else:
            if verbose: print(f"👷‍♂️ Crawling the page {url}.")    
            content = fetch_content_url(url)
        if filtering_criteria:
            if verbose: print(f"👷‍♂️ Checking if content matches criteria")
            role_filter = gen_prompt_filter(filtering_criteria)
            buffer_tok = MAX_TOKEN_WINDOW_GPT35_TURBO - calculate_token(role_filter) - calculate_token(content)
            if buffer_tok < MAX_TOKEN_OUTPUT_GPT3-100: # Adding -100 as security
                print(f"The website content is too large for a single prompt - remains only {buffer_tok} - TBD // TODO for Henry next version - chunking strat - END")
                return ""
            else:
                buffer_tok = max(min(buffer_tok, MAX_TOKEN_OUTPUT_GPT3-100), MAX_TOKEN_OUTPUT_DEFAULT_HUGE) # basically between 3K and 4K
            answer_from_filtergpt = ask_question_gpt(content, role_filter, max_tokens= buffer_tok, verbose=False)
            if not answer_from_filtergpt:
                if verbose: print("Couldn't check the Criteria - END")
                return
            elif "false" in answer_from_filtergpt[:10].lower(): 
                if verbose: print(f"The website is NOT relevant according to the Criteria. Response: {answer_from_filtergpt} - END")
                return
        if summarization:
            if verbose: print(f"👷‍♂️ Generating a summary")   
            summary = ask_question_gpt(content, gen_role_summarizer(), max_tokens=MAX_TOKEN_OUTPUT_DEFAULT_HUGE,  verbose=False)
        
        if verbose: print(f"👷‍♂️ Using GPT 4 to  the requested data")  
        result = ask_question_gpt4(content, gen_prompt_result(desired_output, example_output), max_tokens=MAX_TOKEN_GPT4_RESULT,  verbose=False)
        if result:
            title = f"scrapwithgpt_{clean_url_to_filename(url)}.txt"
            if os.path.exists(title):
                title = f"scrapwithgpt_{clean_url_to_filename(url)}_{get_now(True)}.txt" # To avoid overwriting
            if summary:
                final_content = f"### SUMMARY of {url}:\n" + summary.replace(".", ".\n") + "\n\n" 
            final_content += f"### RESULT for {url}:\n" + result
            with open(title, "w") as file:
                file.write(final_content)
            if verbose: print(f"✅ Done - The content is in {title}")
        else:
            print("Failed to get the result data - END")
        return final_content
    except Exception as e:
        log_issue(e, smartscrap, f"TBD - add the params here")

# *************************************************************

if __name__ == "__main__":
    pass
    # How to use
    # test_url = "https://www.27v.vc"
    #smartscrap(test_url, desired_output=JSON_OUTPUT_VC, example_output=JSON_EXAMPLE_VC, filtering_criteria=DEFAULT_FILTERING_CRITERIA, verbose=True)
