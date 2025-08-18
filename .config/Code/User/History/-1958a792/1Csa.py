# immersive id="fairy_godmother_quest_code" type="code" title="The Fairy Godmother's Quest"
import tkinter as tk
from tkinter import messagebox
import random
import time # For delays in game logic

def __init__(self, master):
        self.master = master
        master.title("The Fairy Godmother's Quest")
        master.geometry("800x600") # Set initial window size
        master.resizable(False, False) # Make window non-resizable for simplicity

        self.current_game_index = 0
        self.story_parts = [
            """
            Part 1: The Young Fairy's First Lesson
            Long ago, before she was known as the Fairy Godmother, she was but a young fairy, eager to help, but lacking true understanding. Her first task was simple: to bring joy to a lonely little sprite by helping it inflate balloons for a party. She quickly learned that true kindness wasn't about grand gestures, but about patience and knowing when to stop, when to simply give what was needed without seeking more. Greed, she found, led only to burst dreams. This simple act of patience unlocked her first spark of lasting magic.
            """,
            """
            Part 2: The Empathy of the Mending Spool
            Her journey continued, and she soon encountered a creature whose delicate wing was torn, leaving it grounded and heartbroken. Others rushed by, seeing only a small problem. But the young fairy felt a deep pang of empathy. She realized that true magic wasn't about flashy spells, but about the gentle, caring acts that made someone feel whole again. With careful hands, she mended the tear, and as she did, the warmth of compassion infused her, strengthening her nascent powers. She learned that healing others, even in small ways, healed a part of herself.
            """,
            """
            Part 3: The Compassion of the Whispering Winds
            Finally, she met a tiny, overlooked sprite, lost and filled with silent despair. Its whispers were so faint, so easily drowned out by the world's clamor, that no one else seemed to notice. The young fairy, now attuned to the subtle currents of kindness, learned to listen with her heart, seeing beyond the obvious. This act of profound compassion gave her the ability to perceive the true, unspoken needs of those who felt invisible. It was then that her magic fully blossomed, rooted in the understanding that the most powerful kindness is extended to those who are unseen and unheard.
            """,
            """
            The Grand Finale: A Destiny of Kindness
            With her magic fully harnessed through patience, empathy, and deep compassion, the fairy godmother looked out into the world. Her gaze fell upon Cinderella, a soul constantly overlooked, burdened, and in desperate need of a helping hand. In Cinderella, she saw all the lessons she had learned embodied: a quiet despair, a need for healing, and a longing to be seen. Knowing her purpose, the Fairy Godmother smiled. Her magic wasn't just about wishes; it was about empowering kindness, one act at a time. And so, her destiny to help Cinderella, and countless others, was sealed.
            """
        ]

        self.setup_ui()
        self.display_story_part(0) # Start with the introduction

    def setup_ui(self):
        # Frame for story text
        self.story_frame = tk.Frame(self.master, bg="#e0f7fa", padx=20, pady=20)
        self.story_frame.pack(fill="both", expand=True)

        self.story_label = tk.Label(self.story_frame, text="", wraplength=700,
                                    font=("Arial", 14), bg="#e0f7fa", justify="left")
        self.story_label.pack(pady=10)

        self.start_game_button = tk.Button(self.story_frame, text="Start Game",
                                           command=self.start_current_game,
                                           font=("Arial", 12), bg="#4CAF50", fg="white",
                                           activebackground="#45a049", relief="raised", bd=3)
        self.start_game_button.pack(pady=20)

        # Frame for games (initially hidden)
        self.game_frame = tk.Frame(self.master, bg="#f0f8ff")
        # self.game_frame.pack(fill="both", expand=True) # Don't pack initially

    def display_story_part(self, part_index):
        if part_index < len(self.story_parts):
            self.story_label.config(text=self.story_parts[part_index])
            self.start_game_button.config(text=f"Start Game {part_index + 1}" if part_index < 3 else "See Final Story")
            self.start_game_button.pack(pady=20) # Ensure button is visible
            self.game_frame.pack_forget() # Hide game frame
            self.story_frame.pack(fill="both", expand=True) # Show story frame
        else:
            messagebox.showinfo("Quest Complete!", "You have unlocked the full story of the Fairy Godmother!")
            self.master.destroy() # Close the application

    def start_current_game(self):
        self.story_frame.pack_forget() # Hide story frame
        self.game_frame.pack(fill="both", expand=True) # Show game frame

        # Clear previous game content
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        if self.current_game_index == 0:
            self.balloon_game = BalloonGame(self.game_frame, self.game_completed)
        elif self.current_game_index == 1:
            self.mending_spool_game = MendingSpoolGame(self.game_frame, self.game_completed)
        elif self.current_game_index == 2:
            self.whispering_winds_game = WhisperingWindsGame(self.game_frame, self.game_completed)
        else:
            self.display_story_part(self.current_game_index) # Display final story part

    def game_completed(self, success):
        # This callback is called by each game when it finishes
        if success:
            messagebox.showinfo("Game Complete!", "You succeeded! Unlocking the next part of the story...")
            self.current_game_index += 1
            self.display_story_part(self.current_game_index)
        else:
            messagebox.showerror("Game Failed!", "You didn't quite make it. Try again!")
            # For simplicity, we'll let them retry the same game
            self.start_current_game()


class BalloonGame:
    def __init__(self, master_frame, on_complete_callback):
        self.master_frame = master_frame
        self.on_complete_callback = on_complete_callback
        self.total_score = 0
        self.attempts_left = 3
        self.current_score = 0
        self.burst_point = 0
        self.game_active = False # To prevent rapid clicks during reset

        self.setup_ui()
        self.start_new_attempt()

    def setup_ui(self):
        game_title = tk.Label(self.master_frame, text="Balloon Game: Patience & Humility",
                              font=("Arial", 18, "bold"), bg="#f0f8ff")
        game_title.pack(pady=10)

        self.canvas = tk.Canvas(self.master_frame, width=400, height=300, bg="#add8e6", bd=2, relief="solid")
        self.canvas.pack(pady=10)
        self.balloon = self.canvas.create_oval(150, 150, 250, 250, fill="red", outline="darkred", width=2)
        self.balloon_text = self.canvas.create_text(200, 200, text="0", font=("Arial", 24, "bold"), fill="white")

        self.score_label = tk.Label(self.master_frame, text="Current: 0 | Total: 0 | Attempts Left: 3",
                                    font=("Arial", 12), bg="#f0f8ff")
        self.score_label.pack(pady=5)

        button_frame = tk.Frame(self.master_frame, bg="#f0f8ff")
        button_frame.pack(pady=10)

        self.inflate_button = tk.Button(button_frame, text="Inflate 🎈", command=self.inflate_balloon,
                                        font=("Arial", 14), bg="#87CEEB", fg="white",
                                        activebackground="#6495ED", relief="raised", bd=3)
        self.inflate_button.pack(side="left", padx=10)

        self.collect_button = tk.Button(button_frame, text="Collect Score ✅", command=self.collect_score,
                                       font=("Arial", 14), bg="#FFA500", fg="white",
                                       activebackground="#FF8C00", relief="raised", bd=3)
        self.collect_button.pack(side="left", padx=10)

        self.message_label = tk.Label(self.master_frame, text="", font=("Arial", 12, "italic"), fg="blue", bg="#f0f8ff")
        self.message_label.pack(pady=5)

    def start_new_attempt(self):
        self.game_active = True
        self.current_score = 0
        self.burst_point = random.randint(7, 25) # Burst between 7 and 25 clicks
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
        # Make the balloon grow visually
        size_factor = 1 + (self.current_score * 0.05) # Grows by 5% per click
        x1, y1, x2, y2 = 150, 150, 250, 250 # Base coordinates
        
        # Calculate new coordinates centered
        center_x = (x1 + x2) / 2
        center_y = (y1 + y2) / 2
        new_width = (x2 - x1) * size_factor
        new_height = (y2 - y1) * size_factor

        new_x1 = center_x - (new_width / 2)
        new_y1 = center_y - (new_height / 2)
        new_x2 = center_x + (new_width / 2)
        new_y2 = center_y + (new_height / 2)

        self.canvas.coords(self.balloon, new_x1, new_y1, new_x2, new_y2)

    def burst_balloon(self):
        self.game_active = False
        self.message_label.config(text="POPP! The balloon burst! 💥", fg="red")
        self.canvas.itemconfig(self.balloon, fill="gray", outline="darkgray") # Make it look 'burst'
        self.canvas.itemconfig(self.balloon_text, text="X")
        self.inflate_button.config(state="disabled")
        self.collect_button.config(state="disabled")
        
        # Reset score for this attempt
        self.current_score = 0 
        self.attempts_left -= 1
        self.update_score_display()

        if self.attempts_left > 0:
            self.master_frame.after(1500, self.start_new_attempt) # Wait 1.5s then start new attempt
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
            self.master_frame.after(1500, self.start_new_attempt) # Wait 1.5s then start new attempt
        else:
            self.end_game()

    def update_score_display(self):
        self.score_label.config(text=f"Current: {self.current_score} | Total: {self.total_score} | Attempts Left: {self.attempts_left}")

    def end_game(self):
        if self.total_score >= 30:
            self.on_complete_callback(True) # Success
        else:
            self.on_complete_callback(False) # Failure


class MendingSpoolGame:
    def __init__(self, master_frame, on_complete_callback):
        self.master_frame = master_frame
        self.on_complete_callback = on_complete_callback
        self.mended_count = 0
        self.required_mends = 3 # Number of tears to mend
        self.drawing = False
        self.last_x, self.last_y = None, None
        
        self.setup_ui()
        self.draw_torn_item()

    def setup_ui(self):
        game_title = tk.Label(self.master_frame, text="Mending Spool: Empathy & Care",
                              font=("Arial", 18, "bold"), bg="#f0f8ff")
        game_title.pack(pady=10)

        self.canvas = tk.Canvas(self.master_frame, width=500, height=350, bg="#fdfd96", bd=2, relief="solid")
        self.canvas.pack(pady=10)

        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        self.mend_label = tk.Label(self.master_frame, text=f"Mended: {self.mended_count} / {self.required_mends}",
                                   font=("Arial", 12), bg="#f0f8ff")
        self.mend_label.pack(pady=5)

        self.message_label = tk.Label(self.master_frame, text="Click and drag to mend the tears!",
                                      font=("Arial", 12, "italic"), fg="blue", bg="#f0f8ff")
        self.message_label.pack(pady=5)

    def draw_torn_item(self):
        self.canvas.delete("all") # Clear canvas for new item
        
        # Draw a simple "torn" shape, e.g., a heart with a gap
        self.canvas.create_arc(100, 50, 400, 250, start=0, extent=180, fill="#FFC0CB", outline="red", width=3, style="arc")
        self.canvas.create_arc(100, 50, 400, 250, start=180, extent=180, fill="#FFC0CB", outline="red", width=3, style="arc")
        
        # Create a "tear" gap
        self.tear_coords = [
            (200, 200, 250, 250), # Example tear 1
            (300, 100, 350, 150), # Example tear 2
            (150, 150, 200, 200)  # Example tear 3
        ]
        
        for i, (x1, y1, x2, y2) in enumerate(self.tear_coords):
            # Draw a dashed line to indicate the tear
            self.canvas.create_line(x1, y1, x2, y2, fill="darkred", width=2, dash=(4, 2), tags=f"tear_{i}")
            # Store the tear as 'unmended'
            self.canvas.data[f"tear_{i}_mended"] = False

        self.message_label.config(text="Click and drag to mend the tears!")
        self.mended_count = 0
        self.update_mend_display()

    def start_draw(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw_line(self, event):
        if self.drawing:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    fill="green", width=3, capstyle=tk.ROUND, smooth=True)
            self.last_x, self.last_y = event.x, event.y

            # Simple check: if drawing over a tear area, mark it as mended
            for i, (tx1, ty1, tx2, ty2) in enumerate(self.tear_coords):
                if not self.canvas.data[f"tear_{i}_mended"]:
                    # Check if the current drawing point is near the tear
                    if tx1 <= event.x <= tx2 and ty1 <= event.y <= ty2:
                        self.canvas.data[f"tear_{i}_mended"] = True
                        self.mended_count += 1
                        self.update_mend_display()
                        self.message_label.config(text="A tear mended!", fg="forestgreen")
                        # Remove the dashed line once mended
                        self.canvas.delete(f"tear_{i}")
                        if self.mended_count >= self.required_mends:
                            self.master_frame.after(500, self.end_game) # Short delay before ending

    def end_draw(self, event):
        self.drawing = False
        self.last_x, self.last_y = None, None

    def update_mend_display(self):
        self.mend_label.config(text=f"Mended: {self.mended_count} / {self.required_mends}")

    def end_game(self):
        self.message_label.config(text="All tears mended! Great job!", fg="purple")
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.master_frame.after(1000, lambda: self.on_complete_callback(True))


class WhisperingWindsGame:
    def __init__(self, master_frame, on_complete_callback):
        self.master_frame = master_frame
        self.on_complete_callback = on_complete_callback
        self.round_num = 0
        self.correct_clicks = 0
        self.required_correct = 5 # Number of correct clicks to win
        self.items = []
        self.highlighted_item_index = -1
        self.game_active = False

        self.setup_ui()
        self.start_round()

    def setup_ui(self):
        game_title = tk.Label(self.master_frame, text="Whispering Winds: Compassion & Attentiveness",
                              font=("Arial", 18, "bold"), bg="#f0f8ff")
        game_title.pack(pady=10)

        self.canvas = tk.Canvas(self.master_frame, width=500, height=350, bg="#e6ffe6", bd=2, relief="solid")
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.check_click)

        self.score_label = tk.Label(self.master_frame, text=f"Correct: {self.correct_clicks} / {self.required_correct}",
                                    font=("Arial", 12), bg="#f0f8ff")
        self.score_label.pack(pady=5)

        self.message_label = tk.Label(self.master_frame, text="Watch for the whisper!",
                                      font=("Arial", 12, "italic"), fg="blue", bg="#f0f8ff")
        self.message_label.pack(pady=5)

        # Create items (using text/emojis for simplicity)
        item_positions = [(100, 100), (400, 100), (250, 200), (100, 300), (400, 300)]
        item_emojis = ["🌸", "🍄", "🦋", "✨", "🌿"]
        
        for i, (x, y) in enumerate(item_positions):
            item_id = self.canvas.create_text(x, y, text=item_emojis[i], font=("Arial", 48), tags=f"item_{i}")
            self.items.append(item_id)
            self.canvas.addtag_withtag(f"item_{i}", item_id) # Add a tag for easy identification

    def start_round(self):
        self.game_active = False # Temporarily disable clicks during highlighting
        self.round_num += 1
        self.message_label.config(text="Listen closely for the whisper...", fg="blue")
        
        # Reset previous highlight
        if self.highlighted_item_index != -1:
            self.canvas.itemconfig(self.items[self.highlighted_item_index], fill="black") # Reset color

        # Choose a random item to highlight
        self.highlighted_item_index = random.randrange(len(self.items))
        
        # Highlight it after a short delay
        highlight_duration = max(500, 1500 - (self.round_num * 100)) # Get faster over rounds
        
        self.master_frame.after(1000, lambda: self.highlight_item(self.highlighted_item_index, highlight_duration))

    def highlight_item(self, index, duration):
        # Change color to highlight
        self.canvas.itemconfig(self.items[index], fill="gold")
        
        # Revert color after duration
        self.master_frame.after(duration, lambda: self.canvas.itemconfig(self.items[index], fill="black"))
        
        # Enable clicks after highlight has finished
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
        
        # Find which of our specific items was clicked
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
                self.master_frame.after(1000, self.start_round) # Start next round
        else:
            self.message_label.config(text="Oops! That wasn't it. Try again!", fg="red")
            self.master_frame.after(1000, self.start_round) # Start next round

        self.set_game_active(False) # Disable clicks until next round starts

    def update_score_display(self):
        self.score_label.config(text=f"Correct: {self.correct_clicks} / {self.required_correct}")

    def end_game(self):
        self.message_label.config(text="You've mastered attentiveness!", fg="purple")
        self.canvas.unbind("<Button-1>")
        self.master_frame.after(1000, lambda: self.on_complete_callback(True))


# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = FairyGodmotherQuest(root)
    