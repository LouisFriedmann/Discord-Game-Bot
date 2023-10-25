import discord
import responses
import games

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message, username=message.author)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

# Create objects for games and
tic = games.TicTacToe(name="TicTacToe")
hang = games.Hangman(name="Hangman")
rps = games.RockPaperScissors(name="RockPaperScissors")
bin = games.Bingo(name="Bingo")
bin_timer = games.BingoTimer()
es = games.EmergencyStop()

def run_discord_bot():
    TOKEN = "MTA1ODQzMDgxMTE1OTkyODg1Mg.G3dhbo.p3BWkGZxDY3qac4N64Lk4UhIv1UprZIeopc-IM"
    the_intents = discord.Intents.default()
    the_intents.message_content = True
    client = discord.Client(intents=the_intents)
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        print(f"Message.content: {message.content}")
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: {user_message} in {channel}")

        # CHECK FOR EMERGENCY STOP
        if not es.emergency_stop:
            if user_message == "!stop":
                es.emergency_stop = True

            elif user_message[0] == '?':
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)
    client.run(TOKEN)