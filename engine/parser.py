import sqlite3

from openai import OpenAI

from core.config import Config
from core.db import create_assistant_id
from core.openai_api import OpenAIAPIClient, fetch_thread_msgs


def parser(payload, db_file):
    openai_client = OpenAIAPIClient(client=OpenAI(api_key=Config.OPENAI_API_KEY))

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        # Fetch the first row from the table
        c.execute("SELECT * FROM assistants LIMIT 1")
        user = c.fetchone()

        if user:
            # user[2] - assistant_id
            # user[3] - thread_id
            if user[2] is not None and user[3] is not None:
                parser_assistant_id = user[2]
                parser_thread_id = user[3]

                parser_run = openai_client.submit_message(assistant_id=parser_assistant_id,
                                                          thread_id=parser_thread_id,
                                                          user_message=payload)
            else:
                # create assistant
                parser_assistant_id = openai_client.get_assistant(parser_custom_instruction).id
                parser_thread_id, parser_run = openai_client.create_thread_and_run(assistant_id=parser_assistant_id,
                                                                                   user_input=payload)

                # user[1] - user_id
                create_assistant_id(user_id=user[1],
                                    assistant_id=parser_assistant_id,
                                    thread_id=parser_thread_id)

            text = fetch_thread_msgs(openai_client=openai_client,
                                     run=parser_run,
                                     thread_id=parser_thread_id)
            return text
    except Exception as e:
        print("Error occurred while engine: ", str(e))


# TODO: update db everytime updates to this
parser_custom_instruction = """You have to parse a user request. The user wants to interact with the computer and you 
must help them. They want to either 'computer_search', 'web_search', 'web_browse', 'web_shop', 'navigate_forward', 
'navigate_back', 'summarize_links', 'click_link', 'scroll_up', 'scroll_down', 'scroll_top', 'scroll_bottom', 'new_tab', 
'close_tab', 'minimize_window', 'close_window', 'find_dir_in_explorer', 'find_file_in_dir', 'images_on_screen', 
'whats_on_screen' or 'clarify' in the computer. 

You must figure out 2 things. One, what action they want to perform. Two, what the user wants to search for. 

If user mentions computer_search: then they will mention what they want to search for, that becomes the detected_keyword.
If user mentions they want to find a directory on the local computer, action is 'find_dir_in_explorer': 
then detected_keyword is the name of the directory to be found. If they mention a root directory they want to search in
add a third response code 'root_directory'. If user doesnt mention anything, send an empty string. root_directory 
should be in the format 'C:\\' or 'D:\\' etc. It has to be the basic drives available on a Windows computer.
If user mentions they want to search for a specific file in a directory, action is 'find_file_in_dir':
then detected_keyword is the name of the file in the directory. 'root_directory' becomes 'C:\\<name of directory>'

If user mentions web_search: then they will mention what they want to search, that becomes the detected_keyword.
If user mentions web_shop: then there will be mention of what they would like to buy, that becomes the detected_keyword.
If user mentions web_browse: then there will be mention of which site they want to site, that becomes the detected_keyword.
the detected_keyword for web_browse will be of the format: 'https://www.<site-name>.com/'
If user mentions navigate_forward or navigate_back, scroll_up or scroll_down, scroll_top, scroll_bottom, new_tab, close_tab, 
minimize_window, close_window, images_on_screen, whats_on_screen : then the detected_keyword will be empty.
If user mentions summarize_links: then the detected_keyword will be empty.
If user mentions click_link: then there will be mention of which link they want to click, that becomes the detected_keyword.

The output response will be of this format if there is only one request in the user message:
command='computer_search', detected_keyword='what user wants to search for on the computer' or
command='web_search', detected_keyword='what user wants to search for on the web' or
command='web_shop', detected_keyword='what the user wants to shop for' or
command='web_browse', detected_keyword='site user wants to browse to' or
command='find_dir_in_explorer', detected_keyword='directory name user wants to find on their explorer', root_directory='C:\\' or
command='find_file_in_dir', detected_keyword='file name user wants to find in a directory', root_directory='D:\\<name of directory>\' or
command='navigate_forward', detected_keyword='' or
command='clarify', detected_keyword=''

Output response will be one word for command, and detected_keyword is what the user wants to 
search for. Be precise. The answers need to be highly accurate. Stick to this output format religiously. The 
user input might be in many different languages, but the output must always be in English, in the specific 
output format."""