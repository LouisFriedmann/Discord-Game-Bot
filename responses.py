import random
import bot
import games
import datetime
from datetime import date
from datetime import datetime

def handle_response(message, username) -> str:
    regular_name = str(username)[:str(username).index("#")]
    full_discord_name = str(username)
    p_message = message.lower()

    if p_message == '!hello':
        return f"Hey {regular_name}, I am game dev bot at your service!"

    if p_message == '!roll':
        return f"Your random number is {random.randint(1, 6)}"

    if p_message == '!encouragement':
        encouragement_file = open('encouragement.txt', 'r')
        enc_file_list = encouragement_file.readlines()
        the_line = enc_file_list[random.randrange(0, len(enc_file_list), 2)]
        words_of_enc = the_line[the_line.index("\""):]
        return f"Bro I gotchu, here's a quote of encouragement:\n{words_of_enc}"

    if p_message == '!game':
        game_file = open('games.txt', 'r')
        game_file_list = game_file.readlines()
        return f"You should play {game_file_list[random.randrange(0, len(game_file_list), 2)]}"

    # Games to play
    if p_message == "!play":
        games_list = ""
        for game in games.names:
            games_list += "!" + game + "\n"
        return f"What game would you like to play? Here is a list of them:\n{games_list}"

    # TicTacToe (NOT FULLY WORKING YET, NEEDS FIX)
    if p_message == "!tictactoe":
        bot.tic.p1.name = full_discord_name
        bot.tic.is_running = True
        if bot.tic.board_updated == "":
            return f"{bot.tic.p1.name}, what size board do you want? Size must be from 0 to 9"

    if bot.tic.is_running:
        if not bot.tic.is_size_entered and full_discord_name == bot.tic.p1.name:
            if not p_message in "1234567890":
                return "Invalid size, size must from 1 to 9!"
            size = int(p_message)
            if size > 9 or size <= 0:
                return "Invalid size, size must be from 1 to 9"
            return f"Here is your board!\n{bot.tic.make_new_board(size)}\nFirst person to type in chat is player 2, unless the word \"bot\" is typed in chat, then player 2 will be the bot"

        if p_message == "bot" and not bot.tic.p2_picked:
            bot.tic.p2.name = "bot"
            bot.tic.p2_picked = True
            bot.tic.turn = bot.tic.p1.name
            return "Time to play me, you are \"x\" and I am \"o\", prepare to lose!!!\nPick a location in the form row(seperator of any character length)column"

        if not bot.tic.p2_picked and full_discord_name != bot.tic.p1.name:
            bot.tic.p2.name = full_discord_name
            bot.tic.p2_picked = True
            bot.tic.turn = bot.tic.p1.name
            return f"{bot.tic.p1.name}, you are \"x\", {bot.tic.p2.name}, you are \"o\", {bot.tic.p1.name}, pick a location in the form row column"

        if bot.tic.turn == bot.tic.p1.name and bot.tic.p2_picked:
            if not bot.tic.valid_location((p_message[0], p_message[len(p_message) - 1])):
                return bot.tic.update_board("x", (p_message[0], p_message[len(p_message) - 1]))
            else:
                bot.tic.moves += 1
                player1_board = bot.tic.update_board("x", (int(p_message[0]), int(p_message[len(p_message) - 1])))

            # Check for tie
            if bot.tic.moves >= bot.tic.size**2 and not bot.tic.winner("x") and not bot.tic.winner("o"):
                bot.tic.reset_board()
                if bot.tic.p2.name == "bot":
                    return f"{player1_board}\nDang, we tied, type !tictactoe to play again"
                else:
                    return f"{player1_board}\nTie!!! Type !tictactoe to play again"

            bot.tic.turn = bot.tic.p2.name
            # Check if player 1 wins
            if bot.tic.winner("x"):
                bot.tic.reset_board()
                if bot.tic.p2.name == "bot":
                    return f"{player1_board}\nDang you win, you're good! Type !tictactoe to play again"
                else:
                    return f"{player1_board}\n{bot.tic.p1.name} wins, type !tictactoe to play again"

            # Otherwise, the game continues
            if bot.tic.p2.name != "bot":
                return f"{player1_board}\n{bot.tic.p2.name}, your turn, pick a location in the form row column"

        if bot.tic.turn == "bot" and bot.tic.p2_picked:
            rand_location = (random.randint(1, bot.tic.size), random.randint(1, bot.tic.size))
            while not bot.tic.valid_location(rand_location):
                rand_location = (random.randint(1, int(bot.tic.size)), random.randint(1, int(bot.tic.size)))
            bot.tic.turn = bot.tic.p1.name

            p2_board = bot.tic.update_board('o', rand_location)

            # Check for tie
            if bot.tic.moves >= bot.tic.size**2 and not bot.tic.winner("x") and not bot.tic.winner("o"):
                bot.tic.reset_board()
                return f"{p2_board}\nDang, we tied, type !tictactoe to play again"

            # Check for player 2 winner
            if bot.tic.winner("o"):
                bot.tic.reset_board()
                return f"{p2_board}\nHaha, you suck, I win!!!"

            bot.tic.moves += 1

            # If the game hasn't ended the game continues
            return f"{p2_board}\nYour turn again"

        if bot.tic.turn == bot.tic.p2.name and bot.tic.p2_picked:
            player2_board = ""
            if not bot.tic.valid_location((p_message[0], p_message[len(p_message) - 1])):
                return bot.tic.update_board("o", (p_message[0], p_message[len(p_message) - 1]))
            else:
                bot.tic.moves += 1
                player2_board = bot.tic.update_board("o", int(p_message[0]), int(p_message[len(p_message) - 1]))

            # Check for tie
            if bot.tic.moves >= bot.tic.size ** 2 and not bot.tic.winner("x") and not bot.tic.winner("o"):
                bot.tic.reset_board()
                return f"{player2_board}\nTie!!! Type !tictactoe to play again"

            bot.tic.turn = bot.tic.p1.name
            # Check if player 2 wins
            if bot.tic.winner("o"):
                bot.tic.reset_board()
                return f"{player2_board}\n{bot.tic.p1.name} wins, type !tictactoe to play again"

            # Otherwise, the game continues
            return f"{player2_board}\n{bot.tic.p1.name}, your turn, pick a location in the form row column"

    # Hangman
    if p_message == "!hangman":
        bot.hang.is_running = True
        return f"Ready to lose....\nGood!!! Here is your board\n{bot.hang.make_board()}"

    if bot.hang.is_running:
        return bot.hang.guess(p_message)

    # Datetime
    if p_message == "!year":
        return f"We are in {date.today().year}"

    if p_message == "!month":
        return f"We are in {datetime.now().strftime('%B')}"

    if p_message == "!day":
        return f"Today is {datetime.now().strftime('%A')}"

    # Rock paper scissors
    if p_message == "!rockpaperscissors":
        bot.rps.p1 = username
        bot.rps.is_running = True
        return "Ready to lose!!! Good!!! Type in what score we should play until"

    if bot.rps.is_running:
        # Get the score that the two players will play until
        if not bot.rps.score_entered:
            return bot.rps.get_score(p_message) + " Type in rock, paper, or scissors!"

        return bot.rps.outcome(p_message, bot.rps.make_choice())

    # Bingo
    minutes = 1
    bingo_leader = "Louis13#3771"
    if p_message == "!bingo":
        bot.bin.is_running = True
        bot.bin_timer.start()
        return f"Players will have {minutes} minutes to join bingo!!! To play, type \"Bingo\" in chat, your bingo leader is {bingo_leader}!!!"

    if bot.bin.is_running:
        print(not full_discord_name in bot.bin.players_playing)
        if bot.bin_timer.elapsed_time() <= minutes * 60 * 1000 and bot.bin_timer.elapsed_time() != 0 and not full_discord_name in bot.bin.players_playing:
            if p_message == "bingo":
                return bot.bin.add_player(name=full_discord_name)


