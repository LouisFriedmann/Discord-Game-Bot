# Imports
import random

global names
names = []
# Games class
class Games:

    # Initializer
    def __init__(self, name):
        self.name = name
        self.names = []
        names.append(name)

# Player class
class Player:

    # Initializer
    def __init__(self, name):
        self.name = name

# TicTacToe Class
class TicTacToe(Games):

    # Initializer
    def __init__(self, name):
        super().__init__(name)
        self.board_updated = ""
        self.is_running = False
        self.is_size_entered = False
        self.p1 = Player(name="")
        self.p2 = Player(name="")
        self.p2_picked = False
        self.turn = ""
        self.moves = 0

    # Method makes a TicTacToe board
    def make_new_board(self, size):
        self.size = size
        self.is_size_entered = True
        the_board = ""
        for i in range(size):
            for j in range(size):
                the_board += "!#"
            the_board += "!\n"
        self.board_updated = the_board
        return self.board_updated

    # Method updates the board with a new piece at a location which is a tuple containing the row and the column
    def update_board(self, piece, location):
        EXTRA_COLUMNS = 2
        if self.valid_location(location):
            idx_to_replace = (self.size * 2 + EXTRA_COLUMNS) * (location[0] - 1) + (location[1] - 1) * 2 + 1
            board_updated_list = list(self.board_updated)
            board_updated_list[idx_to_replace] = piece
            self.board_updated = ''.join(board_updated_list)
            return self.board_updated

        return "Invalid location, enter another location"

    # Method determines if the location the piece is being placed is a valid location
    def valid_location(self, location):
        # Check if its a number first
        if not str(location[0]) in "1234567890" or not str(location[1]) in "1234567890":
            return False

        EXTRA_COLUMNS = 2
        idx_to_replace = (self.size * 2 + EXTRA_COLUMNS) * (int(location[0]) - 1) + (int(location[1]) - 1) * 2 + 1
        return int(location[0]) <= self.size and int(location[0]) >= 1 and int(location[1]) <= self.size and int(location[1]) >= 1 and self.board_updated[idx_to_replace] == '#'

    # Method determines if a player with a piece wins
    def winner(self, piece):

        rows_list = self.board_updated.split(sep="\n")
        rows_list.pop(len(rows_list) - 1)

        # Check rows
        rows_str = ("!" + piece)*self.size
        if rows_str in self.board_updated:
            return True

        # Check columns
        pieces_right = 0
        for r in range(self.size):
            for c in range(self.size):
                if rows_list[c][2 * r + 1] != piece:
                    break
                pieces_right += 1
            if pieces_right == self.size:
                return True
            pieces_right = 0

        # Check diagnols (last thing to check for)
        is_diag_win = False
        for i in range(len(rows_list)):
            if rows_list[len(rows_list) - i - 1][2 * i + 1] != piece:
                break
            if i == len(rows_list) - 1:
                is_diag_win = True
        for i in range(len(rows_list)):
            if rows_list[i][2 * i + 1] != piece:
                break
            if i == len(rows_list) - 1:
                is_diag_win = True

        return is_diag_win

    # Method resets the board
    def reset_board(self):
        self.is_running = False
        self.board_updated = ""
        self.is_size_entered = False
        self.turn = ""
        self.moves = 0
        self.p2_picked = False

# Hangman class
class Hangman(Games):

    # Initialize
    def __init__(self, name):
        super().__init__(name)
        self.tries = 7
        self.file = open('hangman.txt', 'r')
        self.file_list = self.file.readlines()
        self.board = ""
        self.is_running = False
        self.guesses = []

    # Method makes a random word
    def new_word(self):
        random_word_and_ln = self.file_list[random.randint(0, len(self.file_list))]
        self.random_word = random_word_and_ln[:len(random_word_and_ln) - 1]

    # Method makes the board and returns it
    def make_board(self):
        self.new_word()
        self.board += "#"*(len(self.random_word))
        return self.board

    # Method allows user to make a guess, then return the new board based on it and the number of tries left
    def guess(self, letter):
        if letter.lower() == letter and letter.upper() == letter or len(letter) != 1:
            return "Invalid, not a letter stupid!"

        elif letter.lower() in self.guesses:
            return f"{letter} was already guessed, try again"

        if letter.lower() in self.random_word:
            self.guesses.append(letter.lower())
            indeces_of_letter = []
            for i in range(len(self.random_word)):
                if self.random_word[i] == letter:
                    indeces_of_letter.append(i)

            for idx in indeces_of_letter:
                self.board = self.board[:idx] + letter + self.board[idx + 1:]

            # Check for win
            if self.wins():
                win_mes = f"{self.board}\nNice job, I doubted you, but you proved me wrong, respect!!!"
                self.reset()
                return win_mes

            return f"Nice job!\n{self.board}"

        else:
            self.tries -= 1

            self.guesses.append(letter.lower())
            # Check for losing
            if self.lose():
                lose_msg = f"{self.board}\nHaha, you lose, word was \"{self.random_word}\" try again.....NEVER!"
                self.reset()
                return lose_msg

            return f"Wrong, try again! You have {self.tries} tries left"


    # Method determines if user loses
    def lose(self):
        return self.tries == 0

    # Method determines if user wins
    def wins(self):
        return not "#" in self.board

    # Method resets hangman
    def reset(self):
        self.tries = 7
        self.board = ""
        self.is_running = False
        self.guesses = []

# Rock paper scissors
class RockPaperScissors(Games):

    # Initializer
    def __init__(self, name):
        super().__init__(name)
        self.choice = ""
        self.is_running = False
        self.score_entered = False
        self.score = 0
        self.p1_score = 0
        self.p2_score = 0

    # Get the score we are playing until and if the score is not valid, return that the score is not valid
    def get_score(self, score):
        score = str(score)
        numbers = "1234567890"
        is_symbol_in_score = False
        for character in score:
            if not character in numbers:
                is_symbol_in_score = True
                break
        self.score_entered = True
        if is_symbol_in_score or score[0] == "0" or int(score) <= 0:
            self.score = 5
            return "Invalid score, I guess we shall play to the default score, 5!"
        self.score = int(score)
        return ""

    # Method makes a choice for you randomly and returns the choice
    def make_choice(self):
        list = ["Rock", "Paper", "Scissors"]
        self.choice = list[random.randint(0, 2)]
        return self.choice

    # Method returns the outcome of the game and updates the scores accordingly, then tells the player what to do next
    def outcome(self, p1_choice, p2_choice):
        p1_choice = p1_choice.lower()
        p2_choice = p2_choice.lower()

        # Check to make sure choices are valid
        if (p1_choice != "rock" and p1_choice != "paper" and p1_choice != "scissors"):
            return "Please make a valid choice"
        if (p2_choice != "rock" and p2_choice != "paper" and p2_choice != "scissors"):
            return "Please make a valid choice"

        if p1_choice == p2_choice:
            return f"Tie, score you to bot is {self.p1_score} to {self.p2_score}!!!"
        elif p1_choice == "rock" and p2_choice == "scissors" or p1_choice == "scissors" and p2_choice == "paper" or p1_choice == "paper" and p2_choice == "rock":
            self.p1_score += 1
            # Check if player 1 won
            if self.p1_score >= self.score:
                self.reset()
                return f"You win, you got {self.score} points, type !rockpaperscissors to play again"
            return f"You win this round, score you to bot is {self.p1_score} to {self.p2_score}, type rock paper or scissors!"
        else:
            self.p2_score += 1
            # Check if player 2 won
            if self.p2_score >= self.score:
                self.reset()
                return f"Haha, you lose, I got {self.score} points, type !rockpaperscissors to play again"
            return f"Haha, I win this round, score you to bot is {self.p1_score} to {self.p2_score}, type rock, paper, or scissors!!!"

    # Method resets everything that needs to be reset for the game to function properly
    def reset(self):
        self.choice = ""
        self.is_running = False
        self.score_entered = False
        self.p1_score = 0
        self.p2_score = 0

# Bingo
class Bingo(Games):

    # Initializer
    def __init__(self, name):
        super().__init__(name)
        self.is_running = False
        self.player_list = []
        self.is_board_method_chosen = False
        self.symbols = ""
        self.crnt_symbol = ""
        self.players_playing = []

    # Method adds player to bingo, returns message if player is already playing, otherwise it returns that player is in
    def add_player(self, name):
        for player in self.players_playing:
            if player.name == name:
                return f"{player.name} is already playing"
        self.players_playing.append(BingoPlayer(name=name))
        return f"{name}, you are in!!!"

    # Method makes a board with random symbols and returns it
    def make_board_randomly(self):
        if not self.is_board_method_chosen:
            self.is_board_method_chosen = True
            board = " B I N G O\n"
            self.symbols = "1234567890@$%^&*()-=+-<>?/;:'|[]qwertyuiopalskdjfhgzxcvbnm"
            for i in range(5):
                for j in range(5):
                    rand_num = random.randint(0, len(self.symbols) - 1)
                    new_symbol = self.symbols[rand_num]
                    board += "!" + new_symbol
                    self.symbols = self.symbols[:self.symbols.index(new_symbol)] + self.symbols[
                                   self.symbols.index(new_symbol) + 1:]
                board += "!\n"
            return board

    # Method makes a board from an str of symbols and returns it
    def make_board_from_str(self, random_symbols_str):
        if len(random_symbols_str) < 25:
            raise Exception("string must be 25 or more characters long")

        if not self.is_board_method_chosen and not "#" in random_symbols_str and not "!" in random_symbols_str:
            self.is_board_method_chosen = True
            board = " B I N G O\n"
            self.symbols = random_symbols_str
            for i in range(5):
                for j in range(5):
                    rand_num = random.randint(0, len(self.symbols) - 1)
                    new_symbol = self.symbols[rand_num]
                    board += "!" + new_symbol
                    self.symbols = self.symbols[:self.symbols.index(new_symbol)] + self.symbols[
                                                self.symbols.index(new_symbol) + 1:]
                board += "!\n"
            return board


    # Method makes the players
    def make_players(self, names_list):
        for the_name in names_list:
            self.player_list.append(BingoPlayer(name=the_name))

    # Method draws a new symbol
    def draw_symbol(self, symbol):
        self.crnt_symbol = self.symbols[random.randint(0, len(self.symbols) - 1)]
        self.symbols.remove(self.crnt_symbol)

    # Method updates everyone's boards and returns list of all player's names whos boards were actually changed
    def update_boards(self):
        boards_changed_names = []
        for player in self.player_list:
            if self.crnt_symbol in self.symbols:
                player.board = player.board[:self.symbols.index(self.crnt_symbol)] + "#" + (
                player.board[self.symbols.index(self.crnt_symbol) + 1:])
                boards_changed_names.append(player.name)

        return boards_changed_names

    # Method determines if a player has won the game
    def is_winner(self, bingo_player):
        if not isinstance(bingo_player, BingoPlayer):
            raise TypeError("Player must be bingo player")
        return not "#" in bingo_player.board

    # Method resets the game
    def reset(self):
        self.is_running = False
        self.player_list = []
        self.is_board_method_chosen = False

# Bingo timer
import time
import pygame

class BingoTimer:

    # Default constructor
    def __init__(self):
        self.start_time = 0

    # Function starts the timer
    def start(self):
        self.start_time = time.time()

    # Function returns the elapsed time of the timer
    def elapsed_time(self):
        if self.start_time != 0:
            return time.time() - self.start_time
        else:
            return 0

    # Function resets the timer
    def reset(self):
        self.start_time = 0

# BingoPlayer class
class BingoPlayer(Player):

    # Initializer
    def __init__(self, name):
        super().__init__(name)
        self.board = ""

# Emergency Stop class
class EmergencyStop:
    def __init__(self):
        self.emergency_stop = False

