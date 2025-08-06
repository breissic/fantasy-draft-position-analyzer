import customtkinter as ctk

# colors
APP_BG_COLOR = "#242424"
FRAME_BG_COLOR = "#2D2D2D"
BUTTON_COLOR = "#1F6AA5"
TEXT_COLOR = "#E0E0E0"
ENTRY_BG_COLOR = "#343638"
SUCCESS_COLOR = "#2FA572"

class DraftApp(ctk.CTk):
    """
    Main GUI class
    """
    def __init__(self):
        super().__init__()

        # base config
        self.title("Fantasy Football AI Draft Assistant")
        self.geometry("940x690")
        ctk.set_appearance_mode("dark")

        # layout config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # widgets
        self._create_setup_frame()
        self._create_draft_controls_frame()
        self._create_results_frame()

    def _create_setup_frame(self):
        """
        Create frame for pre-draft settings config (league rules/settings)
        """
        setup_frame = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR)
        setup_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        setup_frame.grid_columnconfigure(1, weight=1)
        setup_frame.grid_columnconfigure(5, weight=1)

        # roster
        roster_label = ctk.CTkLabel(setup_frame, text="Roster Settings:", text_color=TEXT_COLOR)
        roster_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.roster_entry = ctk.CTkEntry(setup_frame, placeholder_text="e.g., 1QB, 2RB, 2WR, 1TE, 1FLEX, 1D/ST, 1K, 7BE", width=350)
        self.roster_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # scoring
        scoring_label = ctk.CTkLabel(setup_frame, text="Scoring Format:", text_color=TEXT_COLOR)
        scoring_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.scoring_optionmenu = ctk.CTkOptionMenu(setup_frame, values=["Full PPR", "Half-PPR", "Standard/Non-PPR"])
        self.scoring_optionmenu.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        # league size
        size_label = ctk.CTkLabel(setup_frame, text="League Size:", text_color=TEXT_COLOR)
        size_label.grid(row=0, column=4, padx=(20, 10), pady=10, sticky="w")
        self.size_optionmenu = ctk.CTkOptionMenu(setup_frame, values=["8", "10", "12", "14", "16"])
        self.size_optionmenu.grid(row=0, column=5, padx=10, pady=10, sticky="ew")

    def _create_draft_controls_frame(self):
            """
            Creates the frame for in-draft actions.
            """
            controls_frame = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR)
            controls_frame.grid(row=1, column=0, padx=10, pady=0, sticky="ew")
            controls_frame.grid_columnconfigure(1, weight=1)

            # round display and controls
            self.round_label = ctk.CTkLabel(controls_frame, text="Current Round: 1", text_color=TEXT_COLOR)
            self.round_label.grid(row=0, column=0, padx=10, pady=10)
            self.next_round_button = ctk.CTkButton(controls_frame, text="Next Round", fg_color=BUTTON_COLOR)
            self.next_round_button.grid(row=0, column=2, padx=10, pady=10)

            # current roster display
            self.roster_display_label = ctk.CTkLabel(controls_frame, text="My Roster:", text_color=TEXT_COLOR)
            self.roster_display_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
            self.roster_value_label = ctk.CTkLabel(controls_frame, text="Empty", text_color=TEXT_COLOR, anchor="w")
            self.roster_value_label.grid(row=1, column=1, columnspan=4, padx=10, pady=10, sticky="ew")

            # position add buttons
            position_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
            position_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=5)
            self.add_qb_button = ctk.CTkButton(position_frame, text="Add QB", fg_color=BUTTON_COLOR, width=100)
            self.add_qb_button.pack(side="left", padx=5)
            self.add_rb_button = ctk.CTkButton(position_frame, text="Add RB", fg_color=BUTTON_COLOR, width=100)
            self.add_rb_button.pack(side="left", padx=5)
            self.add_wr_button = ctk.CTkButton(position_frame, text="Add WR", fg_color=BUTTON_COLOR, width=100)
            self.add_wr_button.pack(side="left", padx=5)
            self.add_te_button = ctk.CTkButton(position_frame, text="Add TE", fg_color=BUTTON_COLOR, width=100)
            self.add_te_button.pack(side="left", padx=5)
            self.add_k_button = ctk.CTkButton(position_frame, text="Add K", fg_color=BUTTON_COLOR, width=100)
            self.add_k_button.pack(side="left", padx=5)
            self.add_dst_button = ctk.CTkButton(position_frame, text="Add D/ST", fg_color=BUTTON_COLOR, width=100)
            self.add_dst_button.pack(side="left", padx=5)

            # get rec button
            self.recommendation_button = ctk.CTkButton(
                controls_frame, text="Get Draft Recommendation",
                fg_color=SUCCESS_COLOR, hover_color="#1E6948", height=40
            )
            self.recommendation_button.grid(row=3, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

    def _create_results_frame(self):
        """
        Creates the frame to display the AI's recommendation.
        """
        results_frame = ctk.CTkFrame(self, fg_color=FRAME_BG_COLOR)
        results_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        results_title_label = ctk.CTkLabel(results_frame, text="AI Recommendation", font=ctk.CTkFont(size=16, weight="bold"))
        results_title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.results_textbox = ctk.CTkTextbox(results_frame, state="disabled", text_color=TEXT_COLOR, font=ctk.CTkFont(size=14))
        self.results_textbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

if __name__ == '__main__':
    # to see how the gui looks
    app = DraftApp()
    app.mainloop()