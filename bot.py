import discord
import QuestionManager
import logging
logging.basicConfig(filename= "Crash.txt", encoding='utf-8', level=logging.DEBUG) 

#Specific Sections to start .start poetic etc
#.skip



intents = discord.Intents.default()
intents.messages = True
intents.message_content = True



client = discord.Client(intents = intents)

QuestionManager = QuestionManager.QuestionManager(client)





@client.event
async def on_ready():
    print("bot ready")
    await client.change_presence(activity=discord.Game('Type .help for all commands | I am in ' + str(len(client.guilds)) + " servers!"))



@client.event
async def on_message(message):
    print(message.content)
    if(message.author != client.user ):
        if(message.content.startswith(".start")):
            await QuestionManager.startGame(message.channel, message.channel.id, message.content.lower())
        elif(message.content == ".stop"):
            await QuestionManager.stopGame(message.channel.id)
        
        elif(message.content == ".skip"):
            await QuestionManager.skip(message.channel.id)
        
        elif(message.content == ".help"):
            print(".helped")
            await QuestionManager.help(message)
        
        elif(message.content == ".leaderboard"):
            await QuestionManager.viewLeaderboard(client,message)
        elif message.content.startswith(".search"):
            term = message.content[7:].strip()
            await QuestionManager.searchTerm(message, term)
        else:
            await QuestionManager.checkAnswer(message,message.channel.id)
            
        
def main():
    client.run('You won't be stealing my authtoken :D')

if __name__ == "__main__":
    main()



        



        
   




