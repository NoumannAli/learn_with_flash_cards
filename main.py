# -------------------------------------------------- IMPORTS ------------------------------------------ #
from tkinter import *
import pandas as pd
import random

# -----------------------------------------------    CONSTANT    -------------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"


# -----------------------------------------------   DICTIONARIES -------------------------------------- #
current_card = {}
to_learn = {}
# ----------------------------------------------   GENERATE WORDS -------------------------------------- #
try:
    data = pd.read_csv("data/words_to_know.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")



# --------------------------------------------- MANAGE CARDS ------------------------------------------ #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(background_card_image, image=front_card_image)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_title, text="French", fill="black")
    canvas.itemconfig(canvas_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(background_card_image, image=back_card_image)
    canvas.itemconfig(canvas_title, text="English", fill="white")
    canvas.itemconfig(canvas_word, text=current_card["English"], fill="white")


def to_know():
    to_learn.remove(current_card)
    words_to_know = pd.DataFrame(to_learn)
    words_to_know.to_csv("data/words_to_know.csv", index= False)
    next_card()


# ------------------------------------------------ UI SETUP -------------------------------------------- #

window = Tk()

window.title("Flash Cards")

flip_timer = window.after(3000, flip_card)

window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

front_card_image = PhotoImage(file="images/card_front.png")

back_card_image = PhotoImage(file="images/card_back.png")

background_card_image = canvas.create_image(400, 263, image=front_card_image)
canvas_title = canvas.create_text(400, 190, text="", font=("ariel", 40, "italic"))
canvas_word = canvas.create_text(400, 263, text="", font=("ariel", 60, "bold"))

canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")

cross_button = Button(image=cross_image, highlightthickness=0, command=next_card)
cross_button.grid(column=0, row=1)

correct_image = PhotoImage(file="images/right.png")

correct_button = Button(image=correct_image, highlightthickness=0, command=to_know)
correct_button.grid(column=1, row=1)

next_card()

window.mainloop()
