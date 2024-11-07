import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import random
import os


class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.root.geometry("800x600")
        self.root.configure(bg="darkgreen")

        # Creating back images for cards
        self.create_back_card_image()

        # Initialize game state
        self.deck = self.shuffle_deck(self.gen_deck())
        self.player_hand = self.deal_cards(2)
        self.dealer_hand = self.deal_cards(2)
        self.show_dealer_full = False

        # GUI setting up
        self.player_frame = tk.Frame(self.root, bg="green")
        self.player_frame.pack(pady=20)
        self.dealer_frame = tk.Frame(self.root, bg="green")
        self.dealer_frame.pack(pady=20)
        self.player_value_label = tk.Label(self.root, text="Player Value: ?", font=("Helvetica", 16), bg="darkgreen", fg="white")
        self.player_value_label.pack()
        self.dealer_value_label = tk.Label(self.root, text="Dealer Shows: ?", font=("Helvetica", 16), bg="darkgreen", fg="white")
        self.dealer_value_label.pack()

        tk.Button(self.root, text="Hit", command=self.hit, font=("Helvetica", 14), width=10).pack(pady=10)
        tk.Button(self.root, text="Stand", command=self.stand, font=("Helvetica", 14), width=10).pack(pady=10)
        tk.Button(self.root, text="Reset", command=self.reset_game, font=("Helvetica", 14), width=10).pack(pady=10)

        self.update_display()

    def gen_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        return [(rank, suit) for suit in suits for rank in ranks]

    def shuffle_deck(self, deck):
        random.shuffle(deck)
        return deck

    def deal_cards(self, n=2):
        return [self.deck.pop() for _ in range(n)]

    def deck_value(self, deck):
        total_value = 0
        ace_count = 0
        for rank, suit in deck:
            if rank in ['jack', 'queen', 'king']:
                total_value += 10
            elif rank == 'ace':
                total_value += 11
                ace_count += 1
            else:
                total_value += int(rank)

            while total_value > 21 and ace_count > 0:
                total_value -= 10
                ace_count -= 1

        return total_value

    def load_card_image(self, rank, suit):
        if rank == "back":
            path = os.path.join("cards", "back_red.png")
        else:
            path = os.path.join("cards", f"{rank}_of_{suit}.png")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        image = Image.open(path).resize((100, 140))
        return ImageTk.PhotoImage(image)

    def update_display(self):
        # Update player's cards
        for widget in self.player_frame.winfo_children():
            widget.destroy()

        for rank, suit in self.player_hand:
            card_img = self.load_card_image(rank, suit)
            card_label = tk.Label(self.player_frame, image=card_img, bg="green")
            card_label.image = card_img
            card_label.pack(side="left", padx=5)

        # Update dealer's cards
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        for i, (rank, suit) in enumerate(self.dealer_hand):
            if i == 0 and not self.show_dealer_full:
                card_img = self.load_card_image("back", "red")  # Back of card
            else:
                card_img = self.load_card_image(rank, suit)

            card_label = tk.Label(self.dealer_frame, image=card_img, bg="green")
            card_label.image = card_img
            card_label.pack(side="left", padx=5)

        self.player_value_label['text'] = f"Player Value: {self.deck_value(self.player_hand)}"
        if self.show_dealer_full:
            self.dealer_value_label['text'] = f"Dealer Value: {self.deck_value(self.dealer_hand)}"
        else:
            self.dealer_value_label['text'] = "Dealer Shows: ?"

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.update_display()

        if self.deck_value(self.player_hand) > 21:
            messagebox.showinfo("Game Over", "You busted! Dealer wins.")
            self.reset_game()

    def stand(self):
        self.show_dealer_full = True

        while self.deck_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        self.update_display()
        self.determine_winner()

    def determine_winner(self):
        p_total = self.deck_value(self.player_hand)
        d_total = self.deck_value(self.dealer_hand)

        if d_total > 21 or p_total > d_total:
            messagebox.showinfo("You Win!", "Congratulations, you beat the dealer!")
        elif d_total > p_total:
            messagebox.showinfo("Game Over", "Dealer wins!")
        else:
            messagebox.showinfo("It's a Tie", "Nobody wins!")

        self.reset_game()

    def reset_game(self):
        self.deck = self.shuffle_deck(self.gen_deck())
        self.player_hand = self.deal_cards(2)
        self.dealer_hand = self.deal_cards(2)
        self.show_dealer_full = False
        self.update_display()

    def create_back_card_image(self):
        path = os.path.join("cards", "back_red.png")
        if not os.path.exists(path):
            os.makedirs("cards", exist_ok=True)
            width, height = 100, 140
            image = Image.new("RGB", (width, height), "red")
            draw = ImageDraw.Draw(image)
            draw.rectangle([5, 5, width - 5, height - 5], outline="white", width=5)
            draw.text((30, 60), "Card Back", fill="white")
            image.save(path)
            print(f"Created placeholder back card: {path}")


if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()

