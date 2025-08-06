from google import genai
from google.genai import types
import json
import os
from config import GEMINI_API_KEY

# setup
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
                file=file_path
            )
            context_file_references.append(uploaded_file)
    print("Context file upload complete")

# main function
def get_draft_recommendation(roster_settings, scoring_format, league_size, current_round, current_roster):
    
    # model we are sending requests to
    model_name = "gemini-2.5-pro" 

    # define generation config to tune output and format
    # THIS IS THE CORRECTED STRUCTURE BASED ON THE OFFICIAL DOCUMENTATION
    generation_config = types.GenerateContentConfig(
        temperature=0.2,
        response_mime_type="application/json",
        system_instruction="""
        You are an elite fantasy football draft analyst AI. Your sole purpose is to provide draft recommendations based on the provided strategic frameworks, league rules, roster settings, and current draft status.
        You will analyze all provided context files and adhere strictly to their principles.
        Your output MUST be a valid JSON object following the structure shown in the example.
        IMPORTANT: The context files contain citation numbers that appear as plain numbers in sentences. For example: "...making them inefficient investments of high draft capital.20", 20 is the citation number. You MUST ignore these numbers completely and never include them in your response. However, relevant numbers that are a part of the actual context information should still be fully considered.
        Do not return overly verbose reasoning, keep it to a concise sentence for each position.
        Common abbreviations:
        QB = quarterback
        RB = running back
        WR = wide receiver
        TE = tight end
        K = Kicker
        D/ST = Defense/Special Teams
        FLEX/SUPERFLEX = Flex/Superflex
        BE = Bench
        """
    )
    
    # few-shot example
    example_user_input = """
    **League Configuration & Draft Status:**
    * Roster Settings: 1QB, 2RB, 2WR, 1TE, 1FLEX, 1K, 6Bench
    * Scoring Format: Half-PPR
    * League Size: 12 Teams
    * Current Round: 3
    * My Current Roster: 1 QB, 1 RB
    """

    example_model_output = {
        "recommendations": [
            {"position": "RB", "priority": 1, "justification": "Completes a 'Robust RB' build by securing a second foundational player at a scarce position, creating a significant weekly advantage."},
            {"position": "WR", "priority": 2, "justification": "Builds roster flexibility. The WR position is deep, but securing a high-upside player here maintains balance."},
            {"position": "TE", "priority": 3, "justification": "Addresses a starting position. While less urgent than RB/WR, a TE pick here can exploit a potential tier drop at the position."}
        ],
        "reasoning": "The primary need is a second RB to complete a strong starting corps. This aligns with a 'Robust RB' strategy, which is powerful given the current roster construction."
    }

    # build dynamic user prompt (the actual request)
    actual_user_prompt = f"""
    **League Configuration & Draft Status:**
    * Roster Settings: {roster_settings}
    * Scoring Format: {scoring_format}
    * League Size: {league_size} Teams
    * Current Round: {current_round}
    * My Current Roster: {current_roster}
    ---
    Based on all the strategic documents provided and the current draft status, provide your JSON response now.
    """

    # full prompt construction
    # The system instruction is now in the config object, so it is NOT included here.
    final_prompt = [
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
        config=generation_config
    )

    return json.loads(response.text)
