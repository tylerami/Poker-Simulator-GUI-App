from random import shuffle
from tkinter import *
from PIL import ImageTk, Image


class Card:
    def __init__(self, v, s):
        self.suitsFull = ("Hearts", "Clubs", "Spades", "Diamonds")
        self.values = (None, None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace")
        self.v = v
        self.s = s

    def __str__(self):
        return self.values[self.v] + " of " + self.suitsFull[self.s]


class Deck:
    def __init__(self):
        self.hand = []
        self.cards = []
        self.table = []
        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i, j))
        shuffle(self.cards)

    def dc_remove(self, v, s):
        found = False
        for q in range(len(self.cards) - 1):
            if self.cards[q].v == v and self.cards[q].s == s:
                del self.cards[q]
                found = True
        return found

    def hand_display(self):
        if len(self.hand) == 0:
            return "YOUR CARDS:"
        elif len(self.hand) == 1:
            return "YOUR CARDS:\n" + str(self.hand[0])
        elif len(self.hand) == 2:
            return "YOUR CARDS:\n" + str(self.hand[0]) + "\n" + str(self.hand[1])

    def tc_add(self, card):
        self.table.append(card)

    def hand_add(self, card):
        self.hand.append(card)

    def tc_remove(self):
        hand_ind = len(self.hand) - 1
        table_ind = len(self.table) - 1
        if len(self.hand) == 0:
            pass
        elif len(self.table) == 0:
            self.cards.append(self.hand.pop())
            print(str(self.cards[len(self.cards) - 1]))
        else:
            self.cards.append(self.table.pop())
        display_text.set(deck.hand_display() + "\n\n\n" + deck.tc_display())
        if len(self.hand) == 0:
            var.set("Input first card:")
        elif len(self.hand) == 1:
            var.set("Input second card:")
        elif len(self.table) == 0:
            var.set("Input first flop card:")
        elif len(self.table) == 1:
            var.set("Input second flop card:")
        elif len(self.table) == 2:
            var.set("Input third flop card:")
        elif len(self.table) == 3:
            var.set("Input first river card:")
        elif len(self.table) == 4:
            var.set("Input second river card:")
            
    def reset(self):
        self.hand = []
        self.cards = []
        self.table = []
        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i, j))
        shuffle(self.cards)

    def tc_display(self):
        txt = "TABLE CARDS:\n"
        for card in self.table:
            txt = txt + str(card) + "\n"
        return txt

    def sim(self):
        global nop
        example_hand = Hand(None, None)
        rand1 = False
        rand2 = False
        if len(self.table) == 3:
            rand1 = True
            rand2 = True
        elif len(self.table) == 4:
            rand2 = True
        best1 = 0
        best2 = 0
        best3 = 0
        best4 = 0
        for k in range(500):
            shuffle(self.cards)
            if rand1:
                riv1 = self.cards[25]
            else:
                riv1 = self.table[3]
            if rand2:
                riv2 = self.cards[30]
            else:
                riv2 = self.table[4]
            hands = []
            j = 0
            better_hands = 0
            for i in range(nop):
                hands.append(Hand(self.cards[j], self.cards[j + 1]))
                j += 2
            for x in range(nop):
                if best_hand(self.hand[0], self.hand[1], self.table[0], self.table[1], self.table[2], riv1, riv2) == \
                        best_hand(hands[x].c1,
                                  hands[x].c2,
                                  self.table[0], self.table[1], self.table[2], riv1, riv2):
                    if self.hand[0].v + self.hand[1].v < hands[x].c1.v + hands[x].c2.v:
                        better_hands += 1
                elif best_hand(self.hand[0], self.hand[1], self.table[0], self.table[1], self.table[2], riv1, riv2) < \
                        best_hand(hands[x].c1,
                                  hands[x].c2,
                                  self.table[0], self.table[1], self.table[2], riv1, riv2):
                    better_hands += 1
                    example_hand.c1 = hands[x].c1
                    example_hand.c2 = hands[x].c2
            if better_hands == 0:
                best1 += 1
            elif better_hands == 1:
                best2 += 1
            elif better_hands == 2:
                best3 += 1
            elif better_hands == 3:
                best4 += 1
        n = float(best1) / float(500) * 100
        b = float(best2) / float(500) * 100
        c = float(best3) / float(500) * 100
        d = float(best4) / float(500) * 100
        n = round(n, 5)
        b = round(b, 5)
        c = round(c, 5)
        d = round(d, 5)
        op = "Best hand: " + str(n) + "%\nSecond best hand: " + str(b) + "%\nThird best hand: " + str(c) + \
             "%\nFourth best hand: " + str(d) + "%\n"
        if len(self.table) == 4 or len(self.table) == 5:
            op = op + "Better Hand Example:\n" + str(example_hand.c1) + "\n" + str(example_hand.c2)
        return op


class Hand:
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2


def eval_hand(c1, c2, f1, f2, f3):
    straight = False
    flush = False
    value = 0
    cards = [c1, c2, f1, f2, f3]
    for i in range(len(cards)):
        for j in range(len(cards)):
            if j == i == 4:
                break
            elif j == i:
                pass
            elif cards[i].v == cards[j].v:
                value += 5
    cards_values = [c1.v, c2.v, f1.v, f2.v, f3.v]
    cards_values.sort()
    if cards_values[4] == 14 and cards_values[0] == 2 and cards_values[1] == 3 and cards_values[2] == 4 and \
            cards_values[3] == 5:
        straight = True
        value = 35
    elif cards_values[0] == cards_values[1] - 1 == cards_values[2] - 2 == cards_values[3] - 3 == cards_values[4] - 4:
        straight = True
        value = 35
    cards_suits = [c1.s, c2.s, f1.s, f2.s, f3.s]
    if c1.s == c2.s == f1.s == f2.s == f3.s:
        flush = True
        value = 38
    if straight and flush:
        value = 90
    return value


def best_hand(c1, c2, f1, f2, f3, r1, r2):
    a = eval_hand(c1, c2, f1, f2, f3)
    b = eval_hand(r1, c2, f1, f2, f3)
    c = eval_hand(c1, r1, f1, f2, f3)
    d = eval_hand(c1, c2, r1, f2, f3)
    e = eval_hand(c1, c2, f1, r1, f3)
    f = eval_hand(c1, c2, f1, f2, r1)
    g = eval_hand(r2, c2, f1, f2, f3)
    h = eval_hand(c1, r2, f1, f2, f3)
    i = eval_hand(c1, c2, r2, f2, f3)
    j = eval_hand(c1, c2, f1, r2, f3)
    k = eval_hand(c1, c2, f1, f2, r2)
    l = eval_hand(c1, r1, r2, f2, f3)
    m = eval_hand(c1, c2, r1, r2, f3)
    n = eval_hand(c1, c2, f1, r1, r2)
    o = eval_hand(c1, r1, f1, r2, f3)
    p = eval_hand(c1, r1, f1, f2, r2)
    q = eval_hand(r1, c2, r2, f2, f3)
    r = eval_hand(r1, c2, f1, r2, f3)
    s = eval_hand(r1, c2, f1, f2, r2)
    t = eval_hand(c1, c2, r1, f2, r2)
    input_values = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t]
    input_values.sort()
    return input_values[19]


def input_nop():
    global nop_buttons
    for i in range(8):
        xval = 620
        yval = 240
        if i < 4:
            xval += i * 120
        else:
            yval += 220
            xval += (i - 4) * 120
        nop_buttons[i].place(x=xval, y=yval, height=200, width=100)


def set_nop(num):
    global nop
    global nop_buttons
    nop = num
    for d in range(8):
        nop_buttons[d].place_forget()
    var.set("Input first card:")
    input_value()


def set_suit(s):
    global suit
    suit = s
    for h in range(4):
        suit_buttons[h].place_forget()
    found = deck.dc_remove(val, suit)
    if found:
        if len(deck.hand) < 2:
            deck.hand_add(Card(val, suit))
            display_text.set(deck.hand_display() + "\n\n\n" + deck.tc_display())
            run()
        else:
            deck.tc_add(Card(val, suit))
            display_text.set(deck.hand_display() + "\n\n\n" + deck.tc_display())
            run()
    else:
        var.set("Card not found. Try again:")
        input_value()


def set_value(v):
    global val
    val = v
    for g in range(13):
        value_buttons[g].place_forget()
    input_suit()


def input_value():
    global value_buttons
    for n in range(13):
        if n < 5:
            yval = 220
            xval = 600 + n * 100
        elif 5 <= n < 9:
            yval = 400
            xval = 660 + (n - 5) * 100
        else:
            yval = 580
            xval = 660 + (n - 9) * 100
        value_buttons[n].place(x=xval, y=yval, height=150, width=80)


def input_suit():
    global suit_buttons
    for a in range(4):
        if a < 2:
            xval = 600 + a * 280
            yval = 220
        else:
            xval = 600 + (a - 2) * 280
            yval = 520
        suit_buttons[a].place(x=xval, y=yval, width=230, height=250)


def next_card():
    result_label.place_forget()
    if len(deck.cards) == 0:
        var.set("Input first card:")
        input_value()
    if len(deck.cards) == 1:
        var.set("Input second card:")
        input_value()
    if len(deck.table) == 0:
        var.set("Input first flop card:")
        input_value()
    elif len(deck.table) == 1:
        var.set("Input second flop card:")
        input_value()
    elif len(deck.table) == 2:
        var.set("Input third flop card:")
        input_value()
    elif len(deck.table) == 3:
        var.set("Input first river card:")
        input_value()
    elif len(deck.table) == 4:
        var.set("Input second river card:")
        input_value()
    elif len(deck.table) == 4:
        var.set("Input second river card:")
        input_value()
    elif len(deck.table) == 5:
        var.set("Input Number of Opponents:")
        deck.reset()
        input_nop()
        display_text.set(deck.hand_display() + "\n\n\n" + deck.tc_display())
        nc_button.place_forget()
        nc.set("Input Next Card")


def run():
    if len(deck.hand) == 0:
        var.set("Input first card:")
        input_value()
    elif len(deck.hand) == 1:
        var.set("Input second card:")
        input_value()
    elif len(deck.table) < 1:
        var.set("Input first flop card:")
        input_value()
    elif len(deck.table) < 2:
        var.set("Input second flop card:")
        input_value()
    elif len(deck.table) < 3:
        var.set("Input third flop card:")
        input_value()
    elif len(deck.table) == 3:
        var.set("WIN PROBABILITY:")
        result_label.place(x=650, y=300)
        result.set(deck.sim())
        nc_button.place(x=300, y=700)
    elif len(deck.table) == 4:
        var.set("WIN PROBABILITY:")
        result_label.place(x=650, y=300)
        result.set(deck.sim())
    elif len(deck.table) == 5:
        var.set("WIN PROBABILITY:")
        result_label.place(x=650, y=300)
        nc.set("New Hand")
        result.set(deck.sim())


deck = Deck()
val = 0
suit = 0
nop = 0
window = Tk()
window.title("Poker Odds Calculator by Tyler Amirault")
window.geometry("1200x800")
bg = Label(window, bg="#1F2833")
bg.place(relwidth=1, relheight=1, x=0, y=0)
shadow = Label(window, bg="#45A29E", text="POKER ODDS CALCULATOR", fg="#66FCF1", font="Proxima 40 bold",
               justify=CENTER, padx=235, pady=15)
shadow.place(x=0, y=5)
title = Label(window, text="POKER ODDS CALCULATOR", bg="#0B0C10", fg="white", font="Proxima 40 bold", padx=225, pady=10)
title.place(x=8, y=10)

hearts = PhotoImage(file="assets/h.png")
spades = PhotoImage(file="assets/s.png")
diamonds = PhotoImage(file="assets/d.png")
clubs = PhotoImage(file="assets/c.png")

var = StringVar()
direction = Label(window, textvariable=var, font="Proxima 25 bold", fg="#66FCF1", bg="#0B0C10", justify=CENTER, pady=10,
                  padx=10)
direction.place(x=600, y=150)

result = StringVar()
result.set("")
result_label = Label(window, textvariable=result, bg="#C5C6C7", fg="#0B0C10", font="Proxima 25 bold ", justify=CENTER,
                     padx=20, pady=20)

suit_buttons = [Button(window, image=hearts, bg="#C5C6C7", command=lambda: set_suit(0)),
                Button(window, image=clubs, bg="#C5C6C7", command=lambda: set_suit(1)),
                Button(window, image=spades, bg="#C5C6C7", command=lambda: set_suit(2)),
                Button(window, image=diamonds, bg="#C5C6C7", command=lambda: set_suit(3))]
nop_buttons = []
value_buttons = []
for b in range(13):
    if b == 12:
        text = "A"
    elif b == 11:
        text = "K"
    elif b == 10:
        text = "Q"
    elif b == 9:
        text = "J"
    else:
        text = str(b + 2)
    value_buttons.append(Button(window, text=text, fg="#1F2833", bg="#C5C6C7", font="Proxima 40 bold",
                                command=lambda n=b: set_value(n + 2)))

for i in range(8):
    nop_buttons.append(Button(window, text=str(i + 2), font="Proxima 40 bold", fg="#1F2833", bg="#C5C6C7", command=
                       lambda n=i: set_nop(n + 2), relief=GROOVE))

display_text = StringVar()
# display_text.set("\n                                                    \n\n\n\n\n\n\n\n\n\n\n\n\n\n")
display = Label(window, textvariable=display_text, bg="#0B0C10", fg="white", font="Proxima 20 bold", justify=CENTER,
                pady=20, padx=20)
display.place(x=60, y=200)
display_text.set(deck.hand_display() + "\n\n\n" + deck.tc_display())

nc = StringVar()
nc.set("Input Next Card")

nc_button = Button(window, textvariable=nc, fg="#1F2833", bg="#C5C6C7", command=next_card, font="Proxima 20 bold",
                   padx=5, pady=5)
back_button = Button(window, text="Undo Last Entry", fg="#0B0C10", bg="#C5C6C7", padx=5, pady=5, font="Proxima 20 bold",
                     command=lambda: deck.tc_remove())
back_button.place(x=50, y=700)

var.set("Enter number of opponents:")
input_nop()
window.mainloop()
