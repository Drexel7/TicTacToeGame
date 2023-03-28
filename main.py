from tkinter import *
import random
import sqlite3

# Conectarea la baza de date
conn = sqlite3.connect('game_results.db')
c = conn.cursor()

# Crearea unui tabel de a stoca rezultatele
c.execute('''CREATE TABLE IF NOT EXISTS game_results
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              winner TEXT,
              result TEXT)''')

def next_turn(row, column):
    global player

    if buttons[row][column]['text'] == "" and check_winner() is False:
        if player == players[0]:
            buttons[row][column]['text'] = player
            buttons[row][column].config(fg="red") # setare culoare X = rosu
            if check_winner() is False:
                player = players[1]
                label.config(text=(players[1]+" turn"))
            elif check_winner() is True:
                label.config(text=(players[0]+" wins"))
            elif check_winner() == "Draw":
                label.config(text="Draw!")
        else:
            buttons[row][column]['text'] = player
            buttons[row][column].config(fg="red") # Setare culoare O = rosu
            if check_winner() is False:
                player = players[0]
                label.config(text=(players[0]+" turn"))
            elif check_winner() is True:
                label.config(text=(players[1]+" wins"))
            elif check_winner() == "Draw":
                label.config(text="Draw!")

def check_winner():
    global player

    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            buttons[row][0].config(bg="green")
            buttons[row][1].config(bg="green")
            buttons[row][2].config(bg="green")
            winner = buttons[row][0]['text'] #castigator pe linie
            c.execute("INSERT INTO game_results (winner, result) VALUES (?, ?)", (winner, "win"))
            conn.commit()  #adaug rezultatul in baza de date
            label.config(text=(winner+" wins"))
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            buttons[0][column].config(bg="green")
            buttons[1][column].config(bg="green")
            buttons[2][column].config(bg="green")
            winner = buttons[0][column]['text'] #castigator pe coloana
            c.execute("INSERT INTO game_results (winner, result) VALUES (?, ?)", (winner, "win"))
            conn.commit() #
            label.config(text=(winner+" wins"))
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        winner = buttons[0][0]['text'] #castigator pe diagonala (colt stanga sus, dreapta jos)
        c.execute("INSERT INTO game_results (winner, result) VALUES (?, ?)", (winner, "win"))
        conn.commit()
        label.config(text=(winner+" wins"))
        return True

    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        winner = buttons[0][2]['text'] #castigator pe diagonala (colt dreapta sus, stanga jos)
        c.execute("INSERT INTO game_results (winner, result) VALUES (?, ?)", (winner, "win"))
        conn.commit()
        label.config(text=(winner+" wins"))
        return True

    elif empty_spaces() is False:
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="yellow")
        c.execute("INSERT INTO game_results (winner, result) VALUES (?, ?)", ("none", "tie"))
        conn.commit()
        label.config(text="Draw!")
        return "Draw"

    else:
        return False


def empty_spaces():

    spaces = 9

    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != "":
                spaces -= 1

    if spaces == 0:
        return False
    else:
        return True

def new_game():

    global player

    player = random.choice(players)

    label.config(text=player+" turn")

    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="",bg="#F0F0F0")


window = Tk()
window.title("X si 0")
players = ["X","0"]
player = random.choice(players)
buttons = [[0,0,0],
           [0,0,0],
           [0,0,0]]

label = Label(text=player + " turn", font=('Viner Hand ITC',40))
label.pack(side="top")

reset_button = Button(text="Restart", font=('Viner Hand ITC',20),command=new_game)
reset_button.pack(side="bottom")

frame = Frame(window)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="",font=('Viner Hand ITC',40), bg="white", width=4, height=1,
                                      command= lambda row=row, column=column: next_turn(row,column))
        buttons[row][column].grid(row=row,column=column)

window.mainloop()

