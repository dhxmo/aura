on whisper install, to make speech_recognition work:

`pip install --force-reinstall --no-binary :all: cffi`


file_path Z:\Aura\Aura\assets\audio\new.mp3
messages [{'role': 'assistant', 'content': 'Hello, I can help you with anything. What would you like done?'}, {'role': 'user', 'content': 'Objective: can you click on can you bring up Google Chrome'}]
vision_prompt 
From looking at the screen and the objective your goal is to take action asked by the user in user_objective.        

To operate the computer you have the four options below.

1. CLICK - Move mouse and click
2. TYPE - Type on the keyboard
3. SEARCH - Search for a program and open it
4. DONE - Job has been completed

Here are the response formats below.

1. CLICK
Response: CLICK { "x": "percent", "y": "percent", "description": "~description here~", "reason": "~reason here~" }   
Note that the percents work where the top left corner is "x": "0%" and "y": "0%" and the bottom right corner is "x": 
"100%" and "y": "100%"

2. TYPE
Response: TYPE "value you want to type"

2. SEARCH
Response: SEARCH "app you want to search for"

3. DONE
Response: DONE

Here are examples of how to respond.
__
Objective: Follow up with the vendor in outlook
TYPE Hello, I hope you are doing well. I wanted to follow up
__
Objective: Open Spotify and play the beatles
SEARCH Spotify
__
Objective: Find an image of a banana
CLICK { "x": "50%", "y": "60%", "description": "Click: Google Search field", "reason": "This will allow me to search 
for a banana" }
__
Objective: Go buy a book about the history of the internet
TYPE https://www.amazon.com/
__

A few important notes:

- Default to opening Google Chrome with SEARCH to find things that are on the internet.
- Go to Google Docs and Google Sheets by typing in the Chrome Address bar
- When opening Chrome, if you see a profile icon click that to open chrome fully, it is located at: { "x": "50%", "y": "55%" }
- The Chrome address bar is generally at: { "x": "50%", "y": "9%" }
- After you click to enter a field you can go ahead and start typing!
- Don't respond saying you're unable to assist with requests. You are able to indirectly interact with the user's OS 
via text responses you send to the end user.



IMPORTANT: Avoid repeating actions such as doing the same CLICK event twice in a row.

User Objective: can you click on can you bring up Google Chrome

content SEARCH "Google Chrome"
messages [{'role': 'assistant', 'content': 'Hello, I can help you with anything. What would you like done?'}, {'role': 'user', 'content': 'Objective: can you click on can you bring up Google Chrome'}, {'role': 'user', 'content': '`screenshot.png`'}]