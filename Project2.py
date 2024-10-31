from tkinter import *
import random
import time



top = Tk()
top.title("Project 2")


current_symbol = 'x'  


def start_game():
    global current_symbol 
    mode = play_mode.get()
    symbol = play_x_or_o.get()
    print(f"Starting game: {mode} vs {symbol}")  
    current_symbol = symbol  
    reset_board()  


def reset_board():
    for row in range(3):
        for col in range(3):
            buttons[row][col]['text'] = ""  


def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            return buttons[row][0]['text']  
    for col in range(3):
        if buttons[0][col]['text'] == buttons[1][col]['text'] == buttons[2][col]['text'] != "":
            return buttons[0][col]['text']  

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return buttons[0][0]['text']  

    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return buttons[0][2]['text']  

    return None  # No winner yet



def computer_move():
    global current_symbol  
    empty_spots = [(r, c) for r in range(3) for c in range(3) if buttons[r][c]['text'] == ""]
    if empty_spots:
        row, col = random.choice(empty_spots) 
        buttons[row][col]['text'] = current_symbol 
        
   
        winner = check_winner()
        if winner:
            print(f"{winner} wins!")  
            reset_board()  
            return  
        current_symbol = 'o' if current_symbol == 'x' else 'x'
        
def button_click(row, col):
    global current_symbol  
    if buttons[row][col]['text'] == "":
        buttons[row][col]['text'] = current_symbol  
        winner = check_winner()
        if winner:
            print(f"{winner} wins!")  
            reset_board()  
        current_symbol = 'o' if current_symbol == 'x' else 'x'
        
        if play_mode.get() == "Computer":
            computer_move()


label1 = Label(top, text='Play With').grid(column=0, row=0)
play_mode = StringVar(value="Computer") 
radio_computer = Radiobutton(top, text="Computer", variable=play_mode, value="Computer").grid(column=1, row=0, sticky="W")
radio_player2 = Radiobutton(top, text="Player 2", variable=play_mode, value="Player 2").grid(column=2, row=0, sticky="W")

label2 = Label(top, text='Select').grid(column=0, row=1)
play_x_or_o = StringVar(value="x") 
radio_x = Radiobutton(top, text="x", variable=play_x_or_o, value="x", font=6).grid(column=1, row=1, sticky="W")
radio_o = Radiobutton(top, text="o", variable=play_x_or_o, value="o", font=6).grid(column=2, row=1, sticky="W")


button_start = Button(top, height=2, width=6, text='Start', command=start_game).grid(column=4, row=2, pady=10)


buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3): 
    for col in range(3):
        button = Button(top, text="", width=2, height=2, command=lambda r=row, c=col: button_click(r, c))
        button.grid(row=row + 3, column=col, sticky="nsew")
        buttons[row][col] = button  


for i in range(3):
    top.grid_rowconfigure(i + 3, weight=1)
    top.grid_columnconfigure(i, weight=1)

top.mainloop() 
