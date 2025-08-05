from google import genai
from google.genai import types
import json
import os
from config import GEMINI_API_KEY

# Setup
client = genai.Client()
context_file_references = []
context_directory = 'context'

if not context_file_references:
    print("Uploading context...")
    for filename in os.listdir(context_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(context_directory, filename)
            print(f"Uploading {file_path}...")
            uploaded_file = client.files.upload(
                path=file_path,
                display_name=filename
            )
            context_file_references.append(uploaded_file)
    print("Context file upload complete")

# main function
def get_draft_recommendation(roster_settings, scoring_format, league_size, current_round, current_roster):
    
    # model we are sending requests to
    model_name = "gemini-2.5-pro" 

    # define generation config to tune output and format
    generation_config = genai.GenerationConfig(
        temperature=0.2,
        response_mime_type="application/json"
    )

    # system instructions + few-shot example
    system_prompt = """
    You are an elite fantasy football draft analyst AI. Your sole purpose is to provide draft recommendations based on the provided strategic frameworks, league rules, and current draft status.
    You will analyze all provided context files and adhere strictly to their principles.
    Your output MUST be a valid JSON object following the structure shown in the example.
    """

    # afforementioned example
    example_user_input = """
    **League Configuration & Draft Status:**
    * Roster Settings: 1QB, 2RB, 2WR, 1TE, 1FLEX
    * Scoring Format: Half-PPR
    * League Size: 12 Teams
    * Current Round: 3
    * My Current Roster: 1 QB, 1 RB
    """

    example_model_output = {
        "recommendations": [
            {"position": "RB", "priority": 1, "justification": "Your roster has a clear need at RB and the value for top RBs drops significantly after this round."},
            {"position": "WR", "priority": 2, "justification": "A top-tier WR is still available and would be a strong value pick here."},
            {"position": "TE", "priority": 3, "justification": "While not a critical need, the last elite TE is on the board, presenting a scarcity advantage."}
        ],
        "reasoning": "The primary recommendation is RB due to positional scarcity and your current roster construction. The value over replacement for an RB in this round is extremely high."
    }

    # build dynamic user prompt (the actual request)
    actual_user_prompt = f"""
    **League Configuration & Draft Status:**
    * Roster Settings: {roster_settings}
    * Scoring Format: {scoring_format}
    * League Size: {league_size}
    * Current Round: {current_round}
    * My Current Roster: {current_roster}
    ---
    Based on all the strategic documents provided and the current draft status, provide your JSON response now.
    """

    # full prompt construction
    # system -> examples -> real request
    final_prompt = [
        system_prompt,
        *context_file_references,
        example_user_input,
        json.dumps(example_model_output),
        actual_user_prompt
    ]

    # api call
    print(f"Generating recommendation using model {model_name}")
    response = client.models.generate_content(
        model=model_name,
        contents=final_prompt,
        generation_config=generation_config
    )

    return json.loads(response.text)