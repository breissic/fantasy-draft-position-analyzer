import customtkinter as ctk
from gui import DraftApp
from llm_handler import get_draft_recommendation
import json

class App(DraftApp):
    """
    App class to handle logic + state
    UI Setup from DraftApp class in gui.py
    """

    def __init__(self):
        # ui from parent class
        super().__init__()

        # state
        self.current_round = 1
        self.current_roster = []

        # callback connection
        self.next_round_button.configure(command=self.next_round_callback)
        self.recommendation_button.configure(command=self.get_recommendation_callback)

        self.add_qb_button.configure(command=lambda: self.add_to_roster("QB"))
        self.add_rb_button.configure(command=lambda: self.add_to_roster("RB"))
        self.add_wr_button.configure(command=lambda: self.add_to_roster("WR"))
        self.add_te_button.configure(command=lambda: self.add_to_roster("TE"))
        self.add_k_button.configure(command=lambda: self.add_to_roster("K"))
        self.add_dst_button.configure(command=lambda: self.add_to_roster("D/ST"))

    def next_round_callback(self):
        """
        increment round counter
        """

        self.current_round += 1
        self.round_label.configure(text=f"Current Round: {self.current_round}")
        print(f"Advanced to round {self.current_round}")
    
    def add_to_roster(self, position):
        """
        add a position to the roster list
        """
        self.current_roster.append(position)
        self.current_roster.sort()
        self.roster_value_label.configure(text=", ".join(self.current_roster))
        # debug
        print(f"Added {position} to roster. Roster is now: {self.current_roster}")

    def get_recommendation_callback(self):
        """
        gather all data, call AI, display result
        """
        # gather data from widgets
        roster_settings = self.roster_entry.get()
        scoring_format = self.scoring_optionmenu.get()
        league_size = self.size_optionmenu.get()

        # check settings are in
        if not roster_settings:
            self.display_error("Please enter the Roster Settings")
            return

        print("--- Sending Request to AI ---")
        print(f"Roster Settings: {roster_settings}")
        print(f"Scoring Format: {scoring_format}")
        print(f"League Size: {league_size}")
        print(f"Current Round: {self.current_round}")
        print(f"Current Roster: {self.current_roster}")

        # show loading in results field
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("1.0", "Getting recommendation from the AI...")
        self.results_textbox.configure(state="disabled")
        self.update_idletasks()

        # call llm handler
        try:
            response_data = get_draft_recommendation(
                roster_settings=roster_settings,
                scoring_format=scoring_format,
                league_size=league_size,
                current_round=self.current_round,
                current_roster=", ".join(self.current_roster)
            )
            self.display_results(response_data) # display the rec
        except Exception as e:
            self.display_error(f"An error occurred: {e}")
            print(f"Error during API call: {e}")

    def display_results(self, data):
        """
        format ai json into pretty text
        """
        # ready the textbox
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")

        # build the string
        output_string = ""
        output_string += f"Overall Reasoning:\n{data.get('reasoning', 'N/A')}\n\n"
        output_string += "Ranked Recommendations:\n"
        output_string += "-------------------------\n"

        for rec in data.get('recommendations', []):
            output_string += f"  - Priority {rec.get('priority', '?')}: {rec.get('position', 'N/A')}\n"
            output_string += f"    Justification: {rec.get('justification', 'N/A')}\n\n"
        
        self.results_textbox.insert("1.0", output_string)
        # turn the textbox back off
        self.results_textbox.configure(state="disabled")

    def display_error(self, message):
        """
        damn it
        """
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("1.0", f"ERROR:\n\n{message}")
        self.results_textbox.configure(state="disabled")

if __name__ == '__main__':
    app = App()
    app.mainloop()