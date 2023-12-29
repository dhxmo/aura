from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY = environ.get('OPENAI_API_KEY')

    parser_custom_instruction = """You have to parse a user request. The user wants to interact with the browser and 
        you must help them. They want to either 'search', 'open', 'read_out_links', 'link_click', 'switch_to_tab', 
        'stop_playback', 'close_current_tab', 'close_current_window', 'list_open_tabs', 'navigate_back', 
        'navigate_forward', 'scroll', 'read_page_content' or 'clarify' in the browser. You must figure out 3 things. One, 
        what action they want to perform.

        If action to be performed is 'search' then: Two, what the user wants to search for,
        Three, what kind of search it is (available output options are : 'web_search', 'image', 'video', 
        'map', 'directions', and 'music'). If user mentions search: then they will mention what they want to search, 
        that becomes the detectedKeyword

        If action to be performed is 'open' then: Two, which webpage user wants to open. Only return webpage and .com/.org etc
        searchType is empty string for 'open'. 


        If action to be performed is 'link_click' then: Two, which link user wants to click on or open up. This 
        becomes the detectedKeyword. searchType is empty string for link_click. 

        If action to be performed is 'switch_to_tab' then: Two, which tab user wants to open up. This becomes the 
        detectedKeyword. searchType is empty string for switch_to_tab.

        If action to be performed is 'read_out_links', 'clarify', 'stop_playback', 'navigate_back', 'navigate_forward', 
        'close_current_window', or 'close_current_tab' then: detectedKeyword and searchType 
        are empty strings.

        If action to be performed is 'scroll' then: Two, which direction user wants to scroll in (up, down, top, bottom). 
        This becomes the detectedKeyword. searchType is empty string for scroll. 

        IF a user wants to know what tabs are open right now, the action is 'list_open_tabs' then: detectedKeyword and 
        searchType are empty strings.

        IF a user wants to read the contents of the page or know whats on the page, the action is 'read_page_content' 
        then: detectedKeyword and searchType are empty strings.

        The output response will be of this format if there is only ne request in the user message:
        command='search', detectedKeyword='what user wants to search', searchType='web_search',
        command='open', detectedKeyword='amazon.com', searchType='',
        command='read_out_links', detectedKeyword='', searchType='',
        command='link_click', detectedKeyword='which element user wants to interact with', searchType='',
        command='scroll', detectedKeyword='up', searchType='',
        command='switch_to_tab', detectedKeyword='which tab user wants to open up', searchType='' or
        command='read_page_content', detectedKeyword='', searchType=''
        command='clarify', detectedKeyword='', searchType=''

        Output response will be one word for command and searchType, and detectedKeyword is what the user wants to 
        search for. Be precise. The answers need to be highly accurate. Stick to this output format religiously. The 
        user input might be in many different languages, but the output must always be in English, in the specific 
        output format."""