# Hey Buddy

Hey Buddy is a simple multi-turn Q&A chatbot built with Streamlit, LangChain, and Google Gemini. It keeps the conversation visible in the browser and uses earlier messages as context for each new question.

## Architecture

The application is deliberately split into two small modules:

```text
                 ┌───────────────────┐
                 │       User        │
                 └─────────┬─────────┘
                           │ Question
                           v
              ┌────────────────────────┐
              │ Streamlit UI (app.py)  │
              │ • Chat input/output    │
              │ • Session history      │
              └─────────┬──────────────┘
                        │ Question + history
                        v
          ┌──────────────────────────────┐
          │ Chat Service                 │
          │ (chat_service.py)            │
          │ • Builds prompt              │
          │ • Loads API configuration    │
          └──────────────┬───────────────┘
                         │
                         v
          ┌──────────────────────────────┐
          │ LangChain + Google Gemini    │
          └──────────────┬───────────────┘
                         │ AI response
                         v
                 ┌───────────────────┐
                 │   Response to User│
                 └───────────────────┘
```

- `app.py` manages the Streamlit page, chat input, message display, session history, and user-facing errors.
- `chat_service.py` loads configuration, converts the Streamlit history into LangChain messages, creates the prompt, and requests a response from Gemini.
- `.env` holds local secrets and configuration. It is excluded from version control.

## Setup

1. Create and activate a Python virtual environment.

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   MODEL_NAME=gemini-3.5-flash
   ```

   `MODEL_NAME` is optional; if omitted, the application uses `gemini-3.5-flash`.

4. Start the application:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL shown by Streamlit in your browser.

## Design decisions

- **Separation of concerns:** The user interface and model integration are kept separate so each can be changed or tested independently.
- **Multi-turn context:** Streamlit session state stores prior user and assistant messages. The service turns them into LangChain `HumanMessage` and `AIMessage` objects before each request.
- **Prompt composition:** A system instruction sets the assistant's helpful, friendly behavior while a `MessagesPlaceholder` supplies the relevant conversation history.
- **Configuration through environment variables:** API credentials are never hard-coded. `python-dotenv` loads local settings from `.env`.
- **Friendly failures:** A missing API key produces an actionable message; unexpected provider failures return a short retry prompt without exposing internal details.

## Sample chatbot interaction

```text
You: What is photosynthesis?

Hey Buddy: Photosynthesis is the process plants, algae, and some bacteria use
to turn light energy, water, and carbon dioxide into glucose, releasing oxygen.

You: Why is the oxygen important?

Hey Buddy: It is important because many living organisms, including humans,
use oxygen for cellular respiration to release energy from food.
```

## Requirements

- Python 3.10 or newer
- A Google Gemini API key
- Dependencies listed in `requirements.txt`
