import tkinter as tk
from tkinter import messagebox
import random

class FairyGodmotherQuest:
    def __init__(self, master):
        self.master = master
        master.title("The Fairy Godmother's Quest")
        master.geometry("800x600")
        master.resizable(False, False)
        self.current_game_index = -1
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
            Part 3: The Empathy Challenge
            Finally, she met a tiny, overlooked creature, lost and filled with silent despair. Its needs were so quiet, so easily drowned out by the world's clamor, that no one else seemed to notice. The young fairy, now attuned to the subtle currents of kindness, learned to listen with her heart, seeing beyond the obvious. This act of profound compassion gave her the ability to perceive the true, unspoken needs of those who felt invisible. It was then that her magic fully blossomed, rooted in the understanding that the most powerful kindness is extended to those who are unseen and unheard.
            """,
            """
            The Grand Finale: A Destiny of Kindness
            With her magic fully harnessed through patience, attentiveness, and deep compassion, the fairy godmother looked out into the world. Her gaze fell upon Cinderella, a soul constantly overlooked, burdened, and in desperate need of a helping hand. In Cinderella, she saw all the lessons she had learned embodied: a quiet despair, a need for hope, and a longing to be seen. Knowing her purpose, the Fairy Godmother smiled. Her magic wasn't just about wishes; it was about empowering kindness, one act at a time. And so, her destiny to help Cinderella, and countless others, was sealed.
            """
        ]
        self.setup_ui()
        self.display_story_part(self.current_game_index)
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
            self.start_game_button.config(text="Begin Quest", command=lambda: self.display_story_part(0))
            self.start_game_button.pack(pady=20)
        elif part_index < len(self.story_parts) - 1:
            self.story_label.config(text=self.story_parts[part_index])
            self.start_game_button.config(text=f"Start Game {part_index + 1}", command=lambda: self.start_game(part_index))
            self.start_game_button.pack(pady=20)
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
            EmpathyChallengeGame(self.game_frame, self.game_completed)
        else:
            self.display_story_part(self.current_game_index)
    def start_game(self, game_index):
        self.story_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        if game_index == 0:
            BalloonGame(self.game_frame, self.game_completed)
        elif game_index == 1:
            SunbeamCollectorGame(self.game_frame, self.game_completed)
        elif game_index == 2:
            EmpathyChallengeGame(self.game_frame, self.game_completed)
    def game_completed(self, success):
        if success:
            messagebox.showinfo("Game Complete!", "You succeeded! Unlocking the next part of the story...")
            self.current_game_index += 1
            self.display_story_part(self.current_game_index)
        else:
            messagebox.showerror("Game Failed!", "You didn't quite make it. Try again!")
            self.start_game(self.current_game_index)

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
        self.timer = 30
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

class EmpathyChallengeGame:
    def __init__(self, master_frame, on_complete_callback):
        self.master_frame = master_frame
        self.on_complete_callback = on_complete_callback
        self.correct_answers = 0
        self.questions_answered = 0
        self.total_questions = 5
        self.questions = [
            {"prompt": "A tiny sprite is sitting alone, looking sad. When you ask what's wrong, it says, 'Nothing.'",
             "options": ["Leave it alone, as it said it's fine.",
                         "Offer a distracting toy to cheer it up.",
                         "Sit quietly nearby, showing you're there if it needs you."],
             "correct": 2},
            {"prompt": "A creature is trying to carry a heavy basket of berries but keeps dropping them. It seems embarrassed.",
             "options": ["Laugh and say, 'You're so clumsy!'",
                         "Take the basket and carry it yourself without asking.",
                         "Walk beside the creature and help it pick up the berries, offering a gentle word of encouragement."],
             "correct": 2},
            {"prompt": "A grumpy troll snaps at you for getting too close to its bridge, but you notice its flowers are wilting.",
             "options": ["Get angry back and tell the troll to be nicer.",
                         "Silently and magically fix the flowers without the troll's knowledge.",
                         "Ask the troll if it needs a hand with its flowers, showing kindness despite its grumpiness."],
             "correct": 2},
            {"prompt": "A small bird is struggling to build its nest, with its materials repeatedly falling to the ground. It looks exhausted.",
             "options": ["Point out that it's doing a poor job.",
                         "Gather a handful of strong twigs and present them to the bird, letting it take over.",
                         "Tell a passing squirrel to help the bird, delegating the task."],
             "correct": 1},
            {"prompt": "A little river fairy is trying to make a beautiful melody, but the wind is too loud, and its music is lost. It looks dejected.",
             "options": ["Tell it the wind is a natural force and it should be quiet.",
                         "Create a small, magical dome to block the wind so the fairy's music can be heard.",
                         "Tell the fairy its music is not good enough for others to hear anyway."],
             "correct": 1}
        ]
        random.shuffle(self.questions)
        self.setup_ui()
        self.start_new_question()

    def setup_ui(self):
        game_title = tk.Label(self.master_frame, text="The Empathy Challenge", font=("Arial", 18, "bold"), bg="#f0f8ff")
        game_title.pack(pady=10)
        self.prompt_label = tk.Label(self.master_frame, text="", wraplength=700, font=("Arial", 14), bg="#f0f8ff", justify="left")
        self.prompt_label.pack(pady=20)
        self.button_frame = tk.Frame(self.master_frame, bg="#f0f8ff")
        self.button_frame.pack(pady=10)
        self.buttons = []
        for i in range(3):
            btn = tk.Button(self.button_frame, text="", font=("Arial", 12), command=lambda i=i: self.check_answer(i),
                            bg="#e0e0e0", activebackground="#c0c0c0", relief="raised", bd=3, wraplength=200)
            btn.pack(side="left", padx=10, pady=5, ipadx=10, ipady=5)
            self.buttons.append(btn)
        self.status_label = tk.Label(self.master_frame, text="", font=("Arial", 12), bg="#f0f8ff")
        self.status_label.pack(pady=10)

    def start_new_question(self):
        if self.questions_answered >= self.total_questions:
            self.end_game()
            return
        
        question_data = self.questions[self.questions_answered]
        self.prompt_label.config(text=question_data["prompt"])
        
        for i in range(3):
            self.buttons[i].config(text=question_data["options"][i], state="normal", bg="#e0e0e0")

    def check_answer(self, choice_index):
        current_question = self.questions[self.questions_answered]
        if choice_index == current_question["correct"]:
            self.correct_answers += 1
            self.status_label.config(text="Correct! You showed true empathy. ✨", fg="green")
            self.master_frame.after(1500, self.next_question)
        else:
            self.status_label.config(text="That's not the most empathetic choice. Try again!", fg="red")
            self.master_frame.after(1500, self.reset_question)
        
        for btn in self.buttons:
            btn.config(state="disabled")

    def next_question(self):
        self.questions_answered += 1
        self.status_label.config(text="")
        if self.questions_answered < self.total_questions:
            self.start_new_question()
        else:
            self.end_game()

    def reset_question(self):
        self.status_label.config(text="")
        for btn in self.buttons:
            btn.config(state="normal")

    def end_game(self):
        success = self.correct_answers >= self.total_questions
        message = "You passed the Empathy Challenge! Your kindness shines brightly." if success else "You didn't quite pass the challenge. Take a moment to reflect and try again!"
        messagebox.showinfo("Challenge Complete", message)
        self.on_complete_callback(success)
