import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import random
import os

SAVE_FILE = "dragonborn_save.json"

class DragonbornRPG:
    def __init__(self, root):
        self.root = root
        self.root.title("Dragonborn RPG")
        self.root.geometry("800x600")

        self.character = None

        self.main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="DRAGONBORN RPG",
            font=("Times New Roman", 30, "bold"),
            fg="red"
        )
        title.pack(pady=40)

        tk.Button(
            self.root,
            text="Create Character",
            width=25,
            command=self.create_character
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Choose Character",
            width=25,
            command=self.load_character
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Start New Game",
            width=25,
            command=self.start_game
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Save Character",
            width=25,
            command=self.save_character
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Exit",
            width=25,
            command=self.root.quit
        ).pack(pady=10)

    def create_character(self):
        name = simpledialog.askstring("Character", "Enter character name:")

        if not name:
            return

        classes = ["Warrior", "Mage", "Rogue"]

        choice = simpledialog.askinteger(
            "Class",
            "Choose Class:\n1. Warrior\n2. Mage\n3. Rogue"
        )

        if not choice or choice not in [1, 2, 3]:
            return

        char_class = classes[choice - 1]

        self.character = {
            "name": name,
            "race": "Dragonborn",
            "class": char_class,
            "level": 1,
            "health": 100,
            "strength": 15,
            "gold": 50
        }

        messagebox.showinfo(
            "Success",
            f"{name} the Dragonborn {char_class} created!"
        )

    def save_character(self):
        if not self.character:
            messagebox.showwarning("Error", "No character to save.")
            return

        with open(SAVE_FILE, "w") as file:
            json.dump(self.character, file)

        messagebox.showinfo("Saved", "Character saved successfully!")

    def load_character(self):
        if not os.path.exists(SAVE_FILE):
            messagebox.showerror("Error", "No saved character found.")
            return

        with open(SAVE_FILE, "r") as file:
            self.character = json.load(file)

        messagebox.showinfo(
            "Loaded",
            f"{self.character['name']} loaded successfully!"
        )

    def start_game(self):
        if not self.character:
            messagebox.showwarning(
                "No Character",
                "Create or load a character first."
            )
            return

        self.game_screen()

    def game_screen(self):
        self.clear_screen()

        self.info_label = tk.Label(
            self.root,
            text=self.character_info(),
            font=("Arial", 14),
            justify="left"
        )
        self.info_label.pack(pady=20)

        self.story_label = tk.Label(
            self.root,
            text=(
                f"{self.character['name']} enters the Kingdom "
                "of Dragons..."
            ),
            font=("Arial", 12)
        )
        self.story_label.pack(pady=15)

        tk.Button(
            self.root,
            text="Fight Monster",
            width=20,
            command=self.fight_monster
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Search Treasure",
            width=20,
            command=self.search_treasure
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Rest",
            width=20,
            command=self.rest
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Save Game",
            width=20,
            command=self.save_character
        ).pack(pady=10)

        tk.Button(
            self.root,
            text="Main Menu",
            width=20,
            command=self.main_menu
        ).pack(pady=10)

    def character_info(self):
        return (
            f"Name: {self.character['name']}\n"
            f"Race: {self.character['race']}\n"
            f"Class: {self.character['class']}\n"
            f"Level: {self.character['level']}\n"
            f"Health: {self.character['health']}\n"
            f"Strength: {self.character['strength']}\n"
            f"Gold: {self.character['gold']}"
        )

    def update_screen(self):
        self.info_label.config(text=self.character_info())

    def fight_monster(self):
        monster_hp = random.randint(15, 50)
        damage = random.randint(5, 20)

        if self.character["strength"] > random.randint(1, 20):
            reward = random.randint(20, 60)

            self.character["gold"] += reward
            self.character["level"] += 1
            self.character["strength"] += 2

            self.story_label.config(
                text=f"You defeated a monster and earned {reward} gold!"
            )

        else:
            self.character["health"] -= damage

            self.story_label.config(
                text=f"The monster hit you for {damage} damage!"
            )

            if self.character["health"] <= 0:
                messagebox.showinfo(
                    "Game Over",
                    "You have fallen in battle."
                )
                self.main_menu()
                return

        self.update_screen()

    def search_treasure(self):
        treasure = random.randint(10, 100)

        self.character["gold"] += treasure

        self.story_label.config(
            text=f"You found {treasure} gold in a treasure chest!"
        )

        self.update_screen()

    def rest(self):
        healed = random.randint(10, 30)

        self.character["health"] += healed

        if self.character["health"] > 100:
            self.character["health"] = 100

        self.story_label.config(
            text=f"You rested and recovered {healed} health."
        )

        self.update_screen()


root = tk.Tk()
game = DragonbornRPG(root)
root.mainloop()