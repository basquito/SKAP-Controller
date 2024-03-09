import tkinter as tk
from tkinter import PhotoImage
import json
import os
from os import path
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class ScoreControllerApp:
    bundle_dir = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
    output_file = os.getcwd()
    #print(output_file)
    #print(bundle_dir)
    
    def __init__(self, root):
        self.root = root
        self.root.title("SKAP Controller")
        self.root.configure(bg='#2E2E2E')  # Dark background color
        self.create_json_file()
        self.gdrive = self.setup_google_drive()
        

        # Load the logo image and resize it to 16x16
        #bundle_dir = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
        #print(bundle_dir)
        path_to_icon = path.join(self.bundle_dir, "assets", "logo.png")
        img = PhotoImage(file= path_to_icon)
        root.iconphoto(False, img)
        
        path_to_logo = path.join(self.bundle_dir, "assets", "logo.png")
        original_logo = PhotoImage(file=path_to_logo)
        #original_logo = PhotoImage(file='assets\\logo.png')
        self.logo_image = original_logo.subsample(8, 8)  # Adjust the subsample values to resize

        # Create a label to display the logo at the top of the window
        tk.Label(self.root, image=self.logo_image, bg='#2E2E2E').grid(row=0, column=0, columnspan=7)

        self.teams = ["Team 1", "Team 2", "Answer", "Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5", "Correct Answer 1", "Correct Answer 2", "Correct Answer 3", "Correct Answer 4", "Correct Answer 5"]
        self.vars = {team: {"Name": tk.StringVar(), "Score": tk.IntVar(value=0) if team in ["Team 1", "Team 2"] else tk.StringVar()} for team in self.teams}
        self.update_text_var = tk.Text(self.root, height=1, width=40, bg='#2E2E2E', fg='white')
        self.update_text_var.grid(row=1, column=0, columnspan=7, padx=2, pady=2)

        self.init_gui()

    
    def setup_google_drive(self):
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")

        return GoogleDrive(gauth) 
    
    def update_google_drive(self, json_content):
        file_id = "1LGdP8KxCU8rTVYTS9mfswOAxWxuBlDmx"  # Replace with your actual file ID
        file1 = self.gdrive.CreateFile({'id': file_id})
        file1.Upload()
    

    def init_gui(self):
        tk.Label(self.root, text="Participants / Scoreboard", font=("Helvetica", 16, "bold"), pady=10, bg='#2E2E2E', fg='white').grid(row=2, column=0, columnspan=7)

        row_index = 3
        for team in self.teams:
            if team != "Answer":
                self.create_team_widgets(team, row_index)
                row_index += 1

                # Stop creating widgets after "Team 2"
                if team == "Team 2":
                    break

        # Spacer
        tk.Label(self.root, text="", bg='#2E2E2E').grid(row=row_index, column=0, columnspan=7)

        # Header for "IN THE BIBLE"
        row_index += 1
        tk.Label(self.root, text="IN THE BIBLE", font=("Helvetica", 16, "bold"), pady=10, bg='#2E2E2E', fg='white').grid(row=row_index, column=0, columnspan=7)
        row_index += 1

        # Team entry for "Answer"
        self.create_team_widgets("Answer", row_index)
        row_index += 1

        # Spacer
        tk.Label(self.root, text="", bg='#2E2E2E').grid(row=row_index, column=0, columnspan=7)

        # Header for "BONUS ROUND"
        row_index += 1
        tk.Label(self.root, text="BONUS ROUND", font=("Helvetica", 16, "bold"), pady=10, bg='#2E2E2E', fg='white').grid(row=row_index, column=0, columnspan=7)
        row_index += 1

        tk.Label(self.root, textvariable=self.update_text_var, bg='#2E2E2E', fg='white').grid(row=row_index, column=0, columnspan=7, padx=2, pady=2)

        for team in ["Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5"]:
            self.create_team_widgets(team, row_index)
            row_index += 1

        # Spacer
        tk.Label(self.root, text="", bg='#2E2E2E').grid(row=row_index, column=0, columnspan=7)

        # Header for "Correct Answer 1 to 5"
        row_index += 1
        tk.Label(self.root, text="Correct Answer 1 to 5", font=("Helvetica", 16, "bold"), pady=10, bg='#2E2E2E', fg='white').grid(row=row_index, column=0, columnspan=7)
        row_index += 1

        for team in ["Correct Answer 1", "Correct Answer 2", "Correct Answer 3", "Correct Answer 4", "Correct Answer 5"]:
            self.create_team_widgets(team, row_index, update_button_text="Show", hide_button_text="Hide")
            row_index += 1

    def create_team_widgets(self, team, row, update_button_text="Update", hide_button_text=None):
        tk.Label(self.root, text=team, bg='#2E2E2E', fg='white').grid(row=row, column=0, padx=2, pady=2)
        tk.Entry(self.root, textvariable=self.vars[team]["Name"], width=20, bg='#3E3E3E', fg='white').grid(row=row, column=1, padx=2, pady=2)
        tk.Button(self.root, text=update_button_text, command=lambda t=team: self.update_team(t), bg='#4CAF50', fg='white').grid(row=row, column=2, padx=2, pady=2)

        if team in ["Team 1", "Team 2"]:
            tk.Label(self.root, textvariable=self.vars[team]["Score"], bg='#2E2E2E', fg='white').grid(row=row, column=3, padx=2, pady=2)
            tk.Button(self.root, text="+", command=lambda t=team: self.update_score(t, 5), bg='#4CAF50', fg='white').grid(row=row, column=4, padx=2, pady=2)
            tk.Button(self.root, text="-", command=lambda t=team: self.update_score(t, -5), bg='#FF5733', fg='white').grid(row=row, column=5, padx=2, pady=2)

        if team.startswith("Correct Answer"):
            hide_button = tk.Button(self.root, text=hide_button_text, command=lambda t=team: self.hide_team(t), bg='#FF5733', fg='white')
            hide_button.grid(row=row, column=3, padx=2, pady=2)  # Move closer to the "Show" button

    def hide_team(self, team):
        self.clear_in_json(team)
        notification_text = f"Data for {team} cleared in scores.json"
        self.update_text_var.delete("1.0", tk.END)
        self.update_text_var.insert("1.0", notification_text)

    def clear_in_json(self, team):
        #bundle_dir = path.abspath(path.dirname(__file__))
        json_file_path = os.path.join(self.output_file, "scores.json")
        #print(json_file_path)
        try:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

            # Clear the data for the specified team
            for entry in data:
                if entry["Team"] == team:
                    entry["Name"] = ""
                    entry["Score"] = 0
                    break

            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

            print(f"Successfully cleared data for {team} in scores.json")

        except Exception as e:
            print(f"Error clearing data for {team} in scores.json: {e}")

    def create_json_file(self):
        #bundle_dir = path.abspath(path.dirname(__file__))
        json_file_path = os.path.join(self.output_file, "scores.json")

        try:
            if not os.path.exists(json_file_path):
                default_data = [
                    {"Team": "Team 1", "Name": "", "Score": 0},
                    {"Team": "Team 2", "Name": "", "Score": 0},
                    {"Team": "Answer", "Name": "", "Score": 0},
                    {"Team": "Answer 1", "Name": "", "Score": 0},
                    {"Team": "Answer 2", "Name": "", "Score": 0},
                    {"Team": "Answer 3", "Name": "", "Score": 0},
                    {"Team": "Answer 4", "Name": "", "Score": 0},
                    {"Team": "Answer 5", "Name": "", "Score": 0},
                    {"Team": "Correct Answer 1", "Name": "", "Score": 0},
                    {"Team": "Correct Answer 2", "Name": "", "Score": 0},
                    {"Team": "Correct Answer 3", "Name": "", "Score": 0},
                    {"Team": "Correct Answer 4", "Name": "", "Score": 0},
                    {"Team": "Correct Answer 5", "Name": "", "Score": 0},
                ]
                with open(json_file_path, "w") as json_file:
                    json.dump(default_data, json_file, indent=4)

        except Exception as e:
            print(f"Error creating scores.json: {e}")

    def update_team(self, team):
        name = self.vars[team]["Name"].get()
        self.write_to_json(team, name, self.vars[team]["Score"].get())
        notification_text = f"{name} updated. Score: {self.vars[team]['Score'].get()}"
        self.update_text_var.delete("1.0", tk.END)
        self.update_text_var.insert("1.0", notification_text)

    def update_score(self, team, delta):
        if team != "Answer":
            score_var = self.vars[team]["Score"]
            new_score = score_var.get() + delta
            # Ensure the score is a multiple of 5
            new_score = 5 * ((new_score + 4) // 5)
            score_var.set(new_score)
            self.write_to_json(team, self.vars[team]["Name"].get(), new_score)
            notification_text = f"{team} score updated to {new_score}"
            self.update_text_var.delete("1.0", tk.END)
            self.update_text_var.insert("1.0", notification_text)

    def write_to_json(self, team, name, score):
        #bundle_dir = path.abspath(path.dirname(__file__))
        json_file_path = os.path.join(self.output_file, "scores.json")

        try:
            with open(json_file_path, "r") as json_file:
                data = json.load(json_file)

            # Update the existing entry
            for entry in data:
                if entry["Team"] == team:
                    entry["Name"] = name
                    entry["Score"] = score
                    break

            with open(json_file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)
                
            self.update_google_drive(data)  # Update Google Drive

            print("Successfully updated scores.json")

        except Exception as e:
            print(f"Error writing to scores.json: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreControllerApp(root)
    root.mainloop()
