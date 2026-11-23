# AI Service Desk Chat

A Python and Streamlit app for Module 03. Support chat offers first-line IT guidance.
Ticket triage returns a JSON object with a category, a summary, and one next step.
Both modes use the Gemini API and support session chat history, custom instructions,
and a temperature setting.

## Upload to GitHub

1. Extract the ZIP in the Chromebook Files app.
2. Open your `ai-service-desk-chat` repository. Choose **Add file → Upload files**.
3. Upload `app.py`, `service_desk.py`, `requirements.txt`, and `SETUP.md` together
   at the repository root. Commit the upload. Your existing README can stay in place.

## Deploy to Streamlit Community Cloud

1. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/api-keys).
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub.
   Create an app for `kwabenaagyei21/ai-service-desk-chat`, branch `main`, main file
   `app.py`.
3. Open **Advanced settings** and add this line to **Secrets**, using your own key.

   ```toml
   GEMINI_API_KEY = "paste-your-key-here"
   ```

4. Deploy the app. Save the resulting `.streamlit.app` address for the Module 03 submission.
   Keep the key in the hosting secrets.

## Verify the live app

- In **Ticket triage**, submit “Six employees cannot connect to office Wi-Fi this morning.”
  The result should be JSON with category `incident`, a summary, and a next step.
- Try “Please install approved spreadsheet software on my laptop.” The expected category
  is `service_request`.
- In **Support chat**, ask for first checks on an office Wi-Fi outage, then ask “Which
  should I try first?” Check that the follow-up uses the earlier context.
- Add custom instructions such as “Use two short bullet points” in **Support chat**.
  Submit a new question and check the response. Confirm token usage appears in the
  sidebar, then verify **Clear chat** removes messages.

## Cost and error handling

The app sends at most eight previous messages and requests up to 512 output tokens.
It shows the provider-reported input and total token counts when available. To limit
demo traffic, the app accepts up to 50 API attempts per UTC day per running server
process. A server restart resets this counter. Provider quotas still apply. The app
shows a readable error for API failures, blocked or empty replies, and invalid ticket JSON.

## Run locally

Install the dependencies with `python -m pip install -r requirements.txt`, set the
`GEMINI_API_KEY` environment variable, then run `python -m streamlit run app.py`.
