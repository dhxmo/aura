# Aura

Aura is a voice-controlled Windows desktop assistant that uses speech recognition and OpenAI's GPT models to control web browsers, search computers, manage emails, and perform screen analysis. The system only supports Windows due to platform-specific dependencies (pywin32, pyautogui, Windows file paths).

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Fix cffi for speech_recognition (required)
pip install --force-reinstall --no-binary :all: cffi

# Run the application
python run.py
```

## Environment Setup

- Create a `.env` file with `OPENAI_API_KEY` set
- The app uses OpenAI's GPT-4 and GPT-4 Vision models
- Requires microphone access for speech recognition
- Tesseract OCR is optional (currently commented out in main flow)

## Architecture

### Core Flow: Speech → Parser → Runner → Intent

1. **Speech Recognition** (`aura/core/speech_recognition.py`)
   - Listens continuously for "activate"/"deactivate" keywords
   - Records 4-second audio chunks when active
   - Uses Google Speech Recognition API
   - Forwards recognized text to `init_aura()`

2. **Parser** (`aura/engine/parser.py`)
   - Uses OpenAI Assistant API with persistent threads (stored in SQLite)
   - Converts natural language to structured commands
   - Returns format: `command='action', detected_keyword='params', root_directory='path'`
   - Parser maintains conversational context via thread_id

3. **Runner** (`aura/engine/runner.py`)
   - Uses Python 3.10+ match/case pattern matching
   - Dispatches to appropriate intent handler based on `command`
   - Always calls `play_sound('ready.mp3')` after intent execution

4. **Intents** (`aura/intents/`)
   - Each intent is a separate module (browser_actions, email_actions, etc.)
   - All intents use `read_aloud()` for user feedback via pyttsx3
   - Browser intents receive `driver` (Selenium WebDriver instance)

### Key Design Patterns

#### Audio Feedback System
- `play_sound(filename)`: Plays MP3 from `aura/assets/audio/`
- `read_aloud(text)`: Uses global pyttsx3 engine initialized once (aura/core/utils.py:106)
- Sound cues: `ready.mp3`, `start.mp3`, `end.mp3`, `new.mp3`

#### Driver Management
- Single Chrome instance with stealth mode (selenium-stealth)
- Uses Chrome user data directory for persistence
- `driver_in_focus()`: Maximizes and activates browser window before actions
- Session storage saved/restored via background threads

#### OpenAI Integration
- **OpenAIAPIClient wrapper** (aura/core/openai_api.py): Manages Assistants API
- Two separate assistant threads stored in SQLite:
  - Parser assistant (command interpretation)
  - Email assistant (email tone rewriting)
- Vision API for screen analysis (gpt-4-vision-preview)

#### Database (SQLite)
- Single table `assistants` tracks user_id, assistant_id, thread_id
- Persistent threads allow context retention across sessions
- Helper functions: `init_db()`, `create_assistant_id()`, `create_email_assistant_id()`

### Threading Model

Three daemon threads started in `aura/main.py:start_worker_threads()`:
1. `save_session_storage`: Saves browser session every 5 seconds
2. `set_session_storage`: Restores session on page navigation
3. `worker_speech_recognition`: Continuous speech listening loop

### Available Commands (Intent Categories)

- **Computer**: `computer_search` (Windows search)
- **Web**: `web_search`, `web_browse`, `web_shop` (Amazon)
- **Browser**: `navigate_forward`, `navigate_back`, `summarize_links`, `click_link`, `submit_form`, `open_bookmark`
- **Screen**: `images_on_screen`, `whats_on_screen`, `amazon_product_summary` (uses Vision API)
- **Email** (Gmail): `compose_email`, `touch_up_email`, `attach_file_to_email`, `email_send`
- **Fallback**: `clarify`

### Helper Utilities

#### utils.py Key Functions
- `play_sound(filename)`: Audio playback from assets/audio/
- `read_aloud(res)`: TTS via global pyttsx3 engine
- `clean_up_intent(intent)`: Parses command string to dict
- `take_rolling_screenshot(driver, steps, is_amazon)`: Stitches scrolling screenshots
- `image_capture_n_parse(path, objective)`: Vision API + TTS response
- `get_screenshot_file()`: Returns path to aura/assets/screenshots/screenshot.png

#### driver_in_focus Pattern
All browser intents must call `driver_in_focus(driver)` first to:
1. Maximize window
2. Get window by title
3. Activate if not in focus
4. Sleep 0.2s for stability

## Coding Style & Abstractions

### Error Handling
- Try/except with `read_aloud()` for user-facing errors
- Print statements for debug errors
- Common pattern:
  ```python
  try:
      element = driver.find_element(By.CSS_SELECTOR, selector)
      element.click()
  except NoSuchElementException:
      read_aloud("Element not found")
  ```

### String Formatting
- Use `.format()` for dynamic messages: `"Web search complete for {}".format(keyword)`
- F-strings for debugging: `print(f"Recognized text: {text}")`

### Path Construction
- Always use `os.path.join()` for cross-directory paths
- `current_dir = os.getcwd()` for relative asset access
- Windows paths in parser instructions use `C:\\` format

### Config Pattern
- Centralized Config class (aura/core/config.py)
- Uses python-dotenv for environment variables
- Access via `Config.OPENAI_API_KEY`, `Config.db_file`

### File Organization
- `aura/core/`: Core functionality (speech, database, OpenAI client, config)
- `aura/engine/`: Processing layer (parser, runner, image parsing)
- `aura/intents/`: Action handlers (browser, email, search, screen)
- `aura/assets/`: Audio files, screenshots

## Important Notes

- Platform check in `init_aura()`: Only proceeds if `platform.system() == "Windows"`
- Speech recognition energy threshold: 3000 (hardcoded in AuraSpeechRecognition)
- Audio chunks: 4 seconds duration, 0 offset
- Parser uses GPT-4-1106-preview model
- Vision uses gpt-4-vision-preview with max_tokens=300
- Some features commented out: Tesseract install, PDF reading, directory search, bookmark deletion

## TODOs in Codebase
- Add Aura server check for paid users
- Prevent multiple sessions per email
- Update mechanism needed
- Close active Chrome sessions on startup
- Fix root_directory error in dir/file search
- Update DB when parser instructions change
