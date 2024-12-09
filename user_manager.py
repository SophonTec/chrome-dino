import json
import os
from datetime import datetime

class UserManager:
    def __init__(self):
        self.users_file = "users.json"
        self.scores_file = "scores.json"
        self.last_login_file = "last_login.json"
        self.current_user = None
        self._load_data()
        self.last_login = self._load_last_login()

    def _load_data(self):
        # Create files if they don't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.scores_file):
            with open(self.scores_file, 'w') as f:
                json.dump({}, f)

        # Load existing data
        with open(self.users_file, 'r') as f:
            self.users = json.load(f)
        
        try:
            with open(self.scores_file, 'r') as f:
                self.scores = json.load(f)
        except:
            self.scores = {}

    def register_user(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        
        self.users[username] = password
        self.scores[username] = []  # Initialize empty scores list for new user
        
        # Save both users and scores
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
        with open(self.scores_file, 'w') as f:
            json.dump(self.scores, f, indent=4)
            
        return True, "Registration successful"

    def _load_last_login(self):
        if not os.path.exists(self.last_login_file):
            return {"username": "", "password": ""}
        try:
            with open(self.last_login_file, 'r') as f:
                return json.load(f)
        except:
            return {"username": "", "password": ""}

    def _save_last_login(self, username, password):
        with open(self.last_login_file, 'w') as f:
            json.dump({"username": username, "password": password}, f)

    def login_user(self, username, password):
        if username not in self.users:
            return False, "Username not found"
        
        if self.users[username] != password:
            return False, "Incorrect password"
        
        self.current_user = username
        self._save_last_login(username, password)  # Save credentials on successful login
        return True, "Login successful"

    def add_score(self, score):
        if not self.current_user:
            return
        
        print(f"Adding score {score} for user {self.current_user}")  # Debug print
        
        # Initialize scores list for user if it doesn't exist
        if self.current_user not in self.scores:
            self.scores[self.current_user] = []
            
        # Add new score
        self.scores[self.current_user].append(score)
        
        # Sort user's scores in descending order
        self.scores[self.current_user].sort(reverse=True)
        
        # Save updated scores immediately
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.scores, f, indent=4)
            print(f"Scores saved successfully: {self.scores}")  # Debug print
        except Exception as e:
            print(f"Error saving scores: {e}")  # Debug print

    def get_top_scores(self, limit=5):
        # Collect all scores from all users
        all_scores = []
        for username, user_scores in self.scores.items():
            for score in user_scores:
                all_scores.append({
                    "username": username,
                    "score": score
                })
        
        # Sort by score (descending)
        all_scores.sort(key=lambda x: x["score"], reverse=True)
        return all_scores[:limit]

    def get_user_best_score(self, username):
        if username not in self.scores or not self.scores[username]:
            return 0
        return max(score_entry["score"] for score_entry in self.scores[username])

    def get_user_scores(self, username, limit=5):
        if username not in self.scores:
            return []
        
        # Return the top scores for the user
        return self.scores[username][:limit]

    def logout(self):
        self.current_user = None