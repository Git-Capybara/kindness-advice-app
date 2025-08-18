import tkinter as tk
from tkinter import messagebox
import random
import time

class FairyGodmotherQuest:
    def __init__(self, master):
        self.master = master
        master.title("The Fairy Godmother's Quest")
        master.geometry("800x600")
        master.resizable(False, False)

        self.current_game_index = 0
        self.story_parts = [
            """
            Part 1: The Young Fairy's First Lesson
            Long ago, before she was known as the Fairy Godmother, she was a young fairy, eager to help, but lacking true understanding. Her first task was simple: to bring joy to a lonely little sprite by helping it inflate balloons for a party. She quickly learned that true kindness wasn't about grand gestures, but about patience and knowing when to simply give what was needed without seeking more. Greed, she found, led only to burst dreams. This simple act of patience unlocked her first spark of lasting magic.
            """,
            """
            Part 2: The Sunbeam Collector
            Her journey continued, and she soon found a hidden, gloomy glade that was shrouded in shadow and felt forgotten. Others rushed by, unaware of the quiet despair within its borders. The young fairy, however, was filled with a desire to restore its warmth. She discovered that by patiently and attentively collecting stray sunbeams that broke through the canopy, she could restore light to the overlooked glade. This act taught her that the most powerful magic is found in noticing small moments of light and nurturing them for others.
            """,
            """
            Part 3: The Compassion of the Whispering Winds
            Finally, she met a tiny, overlooked creature, lost and filled with silent despair. Its whispers were so faint, so easily drowned out by the world's clamor, that no one else seemed to notice. The young fairy, now attuned to the subtle currents of kindness, learned to listen with her heart, seeing beyond the obvious. This act of profound compassion gave her the ability to perceive the true, unspoken needs of those who felt invisible. It was then that her magic fully blossomed, rooted in the understanding that the most powerful kindness is extended to those who are unseen and unheard.
            """,
            """
            The Grand Finale: A Destiny of Kindness
            With her magic fully harnessed through patience, attentiveness, and deep compassion, the fairy godmother looked out into the world. Her gaze fell upon Cinderella, a soul constantly overlooked, burdened, and in desperate need of a helping hand. In Cinderella, she saw all the lessons she had learned embodied: a quiet despair, a need for hope, and a longing to be seen. Knowing her purpose, the Fairy Godmother smiled. Her magic wasn't just about wishes; it was about empowering kindness, one act at a time. And so, her destiny to help Cinderella, and countless others, was sealed.
            """
        ]

        self.setup_ui()
        self.display_story_part(-1)

    def setup_ui(self):
        self.story_frame = tk.Frame(self.master, bg="#e0f7fa", padx=20, pady=20)
        self.story_frame.pack(fill="both", expand=True)
        self.story_label = tk.Label(self.story_frame, text="", wraplength=700, font=("Arial", 14), bg="#e0f7fa", justify="left")
        self.story_label.pack(pady=10)
        self.start_game_button = tk.Button(self.story_frame, text="Start Game", command=self.start_current_game,
                                           font=("Arial", 12), bg="#4CAF50", fg="white", activebackground="#45a049", relief="raised", bd=3)
        self.start_game_button.pack(pady=20)
        self.game_frame = tk.Frame(self.master, bg="#f0f8ff")

    def display_story_part(self, part_index):
        self.game_frame.pack_forget()
        self.story_frame.pack(fill="both", expand=True)
        if part_index == -1:
            self.story_label.config(text="Welcome to the Fairy Godmother's Quest!\n\nTo understand why she helped Cinderella, you must first retrace her journey and master the magic of kindness. Your quest begins now.")
            self.start_game_button.config(text="Begin Quest")
        elif part_index < len(self.story_parts):
            self.story_label.config(text=self.story_parts[part_index])
            self.start_game_button.config(text=f"Start Game {part_index + 1}")
        else:
            self.story_label.config(text=self.story_parts[-1])
            self.start_game_button.pack_forget()
            messagebox.showinfo("Quest Complete!", "You have unlocked the full story of the Fairy Godmother!")
            self.master.after(5000, self.master.destroy)

    def start_current_game(self):
        self.story_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        if self.current_game_index == 0:
            BalloonGame(self.game_frame, self.game_completed)
        elif self.current_game_index == 1:
            SunbeamCollectorGame(self.game_frame, self.game_completed)
        elif self.current_game_index == 2:
            WhisperingWindsGame(self.game_frame, self.game_completed)
        else:
            self.display_story_part(self.current_game_index)

    def game_completed(self, success):
        if success:
            messagebox.showinfo("Game Complete!", "You succeeded! Unlocking the next part of the story...")
            self.current_game_index += 1
            self.display_story_part(self.current_game_index)
        else:
            messagebox.showerror("Game Failed!", "You didn't quite make it. Try again!")
            self.start_current_game()


# --- Game Classes ---

class BalloonGame:
    def __init__(self, master_frame, on_complete_callback):
        self.master_frame = master_frame
        self.on_complete_callback = on_complete_callback
        self.total_score = 0
        self.attempts_left = 3
        self.current_score = 0
        self.burst_point = 0
        self.game_active = False
        self.setup_ui()
        self.start_new_attempt()
    def setup_ui(self):
        game_title = tk.Label(self.master_frame, text="Balloon Game: Patience & Humility", font=("Arial", 18, "bold"), bg="#f0f8ff")
        game_title.pack(pady=10)
        self.canvas = tk.Canvas(self.master_frame, width=400, height=300, bg="#add8e6", bd=2, relief="solid")
        self.canvas.pack(pady=10)
        self.balloon = self.canvas.create_oval(150, 150, 250, 250, fill="red", outline="darkred", width=2)
        self.balloon_text = self.canvas.create_text(200, 200, text="0", font=("Arial", 24, "bold"), fill="white")
        self.score_label = tk.Label(self.master_frame, text="Current: 0 | Total: 0 | Attempts Left: 3", font=("Arial", 12), bg="#f0f8ff")
        self.score_label.pack(pady=5)
        button_frame = tk.Frame(self.master_frame, bg="#f0f8ff")
        button_frame.pack(pady=10)
        self.inflate_button = tk.Button(button_frame, text="Inflate 🎈", command=self.inflate_balloon, font=("Arial", 14), bg="#87CEEB", fg="white", activebackground="#6495ED", relief="raised", bd=3)
        self.inflate_button.pack(side="left", padx=10)
        self.collect_button = tk.Button(button_frame, text="Collect Score ✅", command=self.collect_score, font=("Arial", 14), bg="#FFA500", fg="white", activebackground="#FF8C00", relief="raised", bd=3)
        self.collect_button.pack(side="left", padx=10)
        self.message_label = tk.Label(self.master_frame, text="", font=("Arial", 12, "italic"), fg="blue", bg="#f0f8ff")
        self.message_label.pack(pady=5)
    def start_new_attempt(self):
        self.game_active = True
        self.current_score = 0
        self.burst_point = random.randint(7, 25)
        self.update_balloon_size()
        self.canvas.itemconfig(self.balloon, fill="red", outline="darkred")
        self.canvas.itemconfig(self.balloon_text, text="0")
        self.update_score_display()
        self.message_label.config(text="Inflate the balloon!")
        self.inflate_button.config(state="normal")
        self.collect_button.config(state="normal")
    def inflate_balloon(self):
        if not self.game_active: return
        self.current_score += 1
        self.update_balloon_size()
        self.canvas.itemconfig(self.balloon_text, text=str(self.current_score))
        self.update_score_display()
        if self.current_score >= self.burst_point:
            self.burst_balloon()
    def update_balloon_size(self):
        size_factor = 1 + (self.current_score * 0.05)
        x1, y1, x2, y2 = 150, 150, 250, 250
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        new_width, new_height = (x2 - x1) * size_factor, (y2 - y1) * size_factor
        new_x1 = center_x - (new_width / 2)
        new_y1 = center_y - (new_height / 2)
        new_x2 = center_x + (new_width / 2)
        new_y2 = center_y + (new_height / 2)
        self.canvas.coords(self.balloon, new_x1, new_y1, new_x2, new_y2)
    def burst_balloon(self):
        self.game_active = False
        self.message_label.config(text="POPP! The balloon burst! 💥", fg="red")
        self.canvas.itemconfig(self.balloon, fill="gray", outline="darkgray")
        self.canvas.itemconfig(self.balloon_text, text="X")
        self.inflate_button.config(state="disabled")
        self.collect_button.config(state="disabled")
        self.current_score = 0
        self.attempts_left -= 1
        self.update_score_display()
        if self.attempts_left > 0:
            self.master_frame.after(1500, self.start_new_attempt)
        else:
            self.end_game()
    def collect_score(self):
        if not self.game_active: return
        self.game_active = False
        self.total_score += self.current_score
        self.message_label.config(text=f"Collected {self.current_score} points! 🎉", fg="green")
        self.inflate_button.config(state="disabled")
        self.collect_button.config(state="disabled")
        self.attempts_left -= 1
        self.update_score_display()
        if self.attempts_left > 0:
            self.master_frame.after(1500, self.start_new_attempt)
        else:
            self.end_game()
    def update_score_display(self):
        self.score_label.config(text=f"Current: {self.current_score} | Total: {self.total_score} | Attempts Left: {self.attempts_left}")
    def end_game(self):
        if self.total_score >= 30:
            self.on_complete_callback(True)
        else:
            self.on_complete_callback(False)

class SunbeamCollectorGame:
    def __init__(self, master_frame, on_complete_callback):
        self.master_frame = master_frame
        self.on_complete_callback = on_complete_callback
        self.score = 0
        self.timer = 30 # seconds
        self.sunbeams = []
        self.is_game_running = False
        self.setup_ui()
        self.start_game()
    def setup_ui(self):
        game_title = tk.Label(self.master_frame, text="The Sunbeam Collector", font=("Arial", 18, "bold"), bg="#f0f8ff")
        game_title.pack(pady=10)
        self.canvas = tk.Canvas(self.master_frame, width=500, height=350, bg="#2c3e50", bd=2, relief="solid")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.check_click)
        self.score_label = tk.Label(self.master_frame, text=f"Score: 0 / 25", font=("Arial", 14), bg="#f0f8ff")
        self.score_label.pack(side="left", padx=50)
        self.timer_label = tk.Label(self.master_frame, text=f"Time: {self.timer}", font=("Arial", 14), bg="#f0f8ff")
        self.timer_label.pack(side="right", padx=50)
    def start_game(self):
        self.is_game_running = True
        self.score = 0
        self.timer = 30
        self.score_label.config(text=f"Score: {self.score} / 25")
        self.timer_label.config(text=f"Time: {self.timer}")
        self.spawn_sunbeam()
        self.countdown()
    def spawn_sunbeam(self):
        if not self.is_game_running: return
        x = random.randint(20, 480)
        y = random.randint(20, 330)
        sunbeam_id = self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="yellow", outline="gold", width=2)
        self.sunbeams.append(sunbeam_id)
        # Schedule the next sunbeam to appear after a random delay
        delay = random.randint(500, 1500)
        self.master_frame.after(delay, self.spawn_sunbeam)
    def check_click(self, event):
        if not self.is_game_running: return
        clicked_item = self.canvas.find_closest(event.x, event.y)[0]
        if clicked_item in self.sunbeams:
            self.canvas.delete(clicked_item)
            self.sunbeams.remove(clicked_item)
            self.score += 1
            self.score_label.config(text=f"Score: {self.score} / 25")
            if self.score >= 25:
                self.end_game(True)
    def countdown(self):
        if not self.is_game_running: return
        if self.timer > 0:
            self.timer -= 1
            self.timer_label.config(text=f"Time: {self.timer}")
            self.master_frame.after(1000, self.countdown)
        else:
            self.end_game(False)
    def end_game(self, success):
        self.is_game_running = False
        for sunbeam in self.sunbeams:
            self.canvas.delete(sunbeam)
        self.sunbeams = []
        self.master_frame.after(1000, lambda: self.on_complete_callback(success))

class WhisperingWindsGame:
    class WhisperingWindsGame:
    def __init__(self, master_frame, on_complete_callback):
        self.master_frame = master_frame
        self.on_complete_callback = on_complete_callback
        self.correct_clicks = 0
        self.required_correct = 5
        self.items = []
        self.highlighted_item_index = -1
        self.game_active = False
        self.setup_ui()
        self.start_round()
    def setup_ui(self):
        game_title = tk.Label(self.master_frame, text="Whispering Winds: Compassion & Attentiveness", font=("Arial", 18, "bold"), bg="#f0f8ff")
        game_title.pack(pady=10)
        self.canvas = tk.Canvas(self.master_frame, width=500, height=350, bg="#e6ffe6", bd=2, relief="solid")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.check_click)
        self.score_label = tk.Label(self.master_frame, text=f"Correct: {self.correct_clicks} / {self.required_correct}", font=("Arial", 12), bg="#f0f8ff")
        self.score_label.pack(pady=5)
        self.message_label = tk.Label(self.master_frame, text="Watch for the whisper!", font=("Arial", 12, "italic"), fg="blue", bg="#f0f8ff")
        self.message_label.pack(pady=5)
        item_positions = [(100, 100), (400, 100), (250, 200), (100, 300), (400, 300)]
        item_emojis = ["🌸", "🍄", "🦋", "✨", "🌿"]
        for i, (x, y) in enumerate(item_positions):
            # This line has been fixed to give the text a default, visible color.
            item_id = self.canvas.create_text(x, y, text=item_emojis[i], font=("Arial", 48), tags=f"item_{i}", fill="black")
            self.items.append(item_id)
    def start_round(self):
        self.game_active = False
        self.message_label.config(text="Listen closely for the whisper...", fg="blue")
        if self.highlighted_item_index != -1:
            self.canvas.itemconfig(self.items[self.highlighted_item_index], fill="black")
        self.highlighted_item_index = random.randrange(len(self.items))
        highlight_duration = max(500, 1500 - (self.correct_clicks * 100))
        self.master_frame.after(1000, lambda: self.highlight_item(self.highlighted_item_index, highlight_duration))
    def highlight_item(self, index, duration):
        self.canvas.itemconfig(self.items[index], fill="gold")
        self.master_frame.after(duration, lambda: self.canvas.itemconfig(self.items[index], fill="black"))
        self.master_frame.after(duration + 100, lambda: self.set_game_active(True))
    def set_game_active(self, active):
        self.game_active = active
        if active:
            self.message_label.config(text="Now, click the item that whispered!", fg="darkgreen")
        else:
            self.message_label.config(text="", fg="blue")
    def check_click(self, event):
        if not self.game_active: return
        clicked_items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        clicked_item_id = -1
        for item_id in clicked_items:
            tags = self.canvas.gettags(item_id)
            for tag in tags:
                if tag.startswith("item_"):
                    clicked_item_id = int(tag.split("_")[1])
                    break
            if clicked_item_id != -1:
                break
        if clicked_item_id == self.highlighted_item_index:
            self.correct_clicks += 1
            self.message_label.config(text="Correct! ✨", fg="green")
            self.update_score_display()
            if self.correct_clicks >= self.required_correct:
                self.master_frame.after(500, self.end_game)
            else:
                self.master_frame.after(1000, self.start_round)
        else:
            self.message_label.config(text="Oops! That wasn't it. Try again!", fg="red")
            self.master_frame.after(1000, self.start_round)
        self.set_game_active(False)
    def update_score_display(self):
        self.score_label.config(text=f"Correct: {self.correct_clicks} / {self.required_correct}")
    def end_game(self):
        self.message_label.config(text="You've mastered attentiveness!", fg="purple")
        self.canvas.unbind("<Button-1>")
        self.master_frame.after(1000, lambda: self.on_complete_callback(True))

if __name__ == "__main__":
    root = tk.Tk()
    app = FairyGodmotherQuest(root)
    root.mainloop()
