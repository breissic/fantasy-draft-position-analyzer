# Fantasy Football AI Draft Assistant

This is a Python-based desktop application that serves as an AI-powered assistant for fantasy football drafts. It leverages the Google Gemini API to provide strategic recommendations for which *position* to draft next, based on a comprehensive set of modern fantasy football theories, your specific league settings, and your current roster construction.

The tool is designed to handle the high-level strategic thinking (roster construction, positional value) while leaving the specific player-level decisions to you.

---

## How It Works

The application operates on a few core components:

1.  **AI Engine (`llm_handler.py`):** This is the brain of the operation. It uses the `google-genai` library to communicate with the Gemini Pro model. On startup, it uploads a collection of strategy documents from the `context/` directory to give the AI its foundational knowledge.
2.  **Context Files (`context/`):** A series of `.txt` files, each containing a detailed breakdown of a specific fantasy football strategy (e.g., Value-Based Drafting, Zero RB, Positional Scarcity). These files are used to construct the AI's knowledge base for every request.
3.  **Graphical User Interface (`gui.py` & `app.py`):** Desktop application built with `customtkinter`. It provides a user-friendly interface to input league settings, track your draft progress, and receive recommendations from the AI.

The core logic involves sending a carefully constructed "few-shot" prompt to the AI, which includes the strategic context files, your league settings, the current round, your roster, and an example of the desired JSON output format. This ensures that the responses are not only strategically sound but also structured and reliable.

---

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

-   Python 3.9 or newer.
-   A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Clone the Repository

Clone this project to your local machine using Git:

```bash
git clone <your-repository-url>
cd fantasy-draft-position-analyzer
```

### 3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project-specific dependencies.

```bash
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (Git Bash or PowerShell):
source .venv/Scripts/activate
# On macOS/Linux:
# source .venv/bin/activate
```

### 4. Install Dependencies

With your virtual environment active, install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

This will install `google-genai`, `python-dotenv`, and `customtkinter`.

### 5. Set Up Your API Key

The application loads your API key from a `.env` file to keep it secure.

-   Create a new file named `.env` in the root directory of the project.
-   Add the following line to the file, replacing `YOUR_API_KEY_HERE` with your actual Gemini API key:

```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

The `.gitignore` file is already configured to prevent this file from being committed to version control.

---

## How to Use the Application

### 1. Launch the App

With your virtual environment still active, run the `app.py` file from the root directory:

```bash
python app.py
```

The application window should appear. The first time you run it, you will see messages in your terminal indicating that the context files are being uploaded.

### 2. Pre-Draft Configuration

Before the draft starts, fill out the top section of the UI:

-   **Roster Settings:** Enter your league's starting positions (e.g., `1QB, 2RB, 2WR, 1TE, 1FLEX`).
-   **Scoring Format:** Select `Full PPR`, `Half-PPR`, or `Standard` from the dropdown.
-   **League Size:** Select the number of teams in your league.

### 3. In-Draft Usage

On each of your turns:

1.  **Get Recommendation:** Click the large **"Get Draft Recommendation"** button. The app will send the current draft state to the AI and display the ranked positional recommendations in the results box.
2.  **Make Your Pick:** Based on the AI's advice and your own player knowledge, make your pick in your fantasy platform's draft room.
3.  **Update Your Roster:** Click the corresponding **"Add QB"**, **"Add RB"**, etc., button in the app to log your pick. Your roster display will update.
4.  **Advance the Round:** If your pick was the last of the round, click the **"Next Round"** button to advance the round counter.

Repeat this process for each of your picks.

---

## Customizing the AI's Strategy

You have full control over the AI's strategic knowledge base. You can modify its "brain" by editing the `.txt` files in the `context/` directory.

-   **To add a new strategy:** Create a new `.txt` file in the `context/` folder with your desired information.
-   **To modify an existing strategy:** Simply open and edit one of the existing `.txt` files.
-   **To remove a strategy:** Delete the corresponding `.txt` file from the folder.

**Important:** After making any changes to the context files, you must **restart the application**. The app only uploads the context files on startup.
