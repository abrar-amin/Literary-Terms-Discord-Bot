import Question
import discord
import json
import jsonSave
import vocabWords
class QuestionManager:
    def __init__(self,client):
        self.client = client
        self.Questions = {}

    async def startGame(self, channelRef , channelID,message):
        if not channelID in self.Questions:
            genre = message[6:].strip()
            self.Questions[channelID] = Question.Question(self,self.client, channelRef, channelID,genre)
            await self.Questions[channelID].askNewQuestion()
        else:
            await channelRef.send("A Game is in Progress in this Channel.")
    async def stopGame(self, channelID):
        if channelID in self.Questions:
            if(self.Questions[channelID].active == True):
                self.Questions[channelID].active = False
                await self.Questions[channelID].result()
                playerData = self.Questions[channelID].points
                jsonSave.saveData(playerData)
                self.Questions.pop(channelID)
        else:
            print("Possible error; Game has been deleted twice.")
    
    async def checkAnswer(self, answer, channelID):
        if channelID in self.Questions:
            await self.Questions[channelID].checkAnswer(answer)
    
    async def skip(self,channelID):
        if(channelID in self.Questions):
            await self.Questions[channelID].skipQuestion()

    async def help(self,message):
        embedVar = discord.Embed(title="List of Commands", description="", color=0xc9aa88)
        embedVar.add_field(name=".start <genre>", value="Starts Vocab Game\n  .start - All Vocabulary Terms \n  .start poetic - Only Poetic Terms \n  .start drama - Only Dramatic Terms \n  .start syntax - Only Syntactical Terms \n  .start grammatical - Only Grammatical Terms",  inline=False)
        embedVar.add_field(name=".stop", value="Stops Vocab Game", inline=False)
        embedVar.add_field(name=".skip", value="Skips Current Vocab Word (Adds Skipped Word to Missed Words)", inline=False)
        embedVar.add_field(name=".leaderboard", value="View the top players across all servers.", inline=False)
        embedVar.add_field(name=".search <word>", value="Find the definition of any IB Literary Term.", inline=False)

        await message.channel.send(embed=embedVar)

    async def viewLeaderboard(self,client,message):
        with open("playerData.json", "r") as playerDataFile:
            playerData = json.load(playerDataFile)
            sorted_keys = sorted(playerData, key=playerData.get)
            leaderboard = "👑"
            for userID in reversed(sorted_keys):
                user = await client.fetch_user(userID)
                userName = user.name
                leaderboard+= f"{userName}" + ": " + "**" +  str(playerData[userID]) + " Point(s)**" + '\n'

            embedVar = discord.Embed(title="Results 📈", description="", color=0xcc20a8)
            embedVar.add_field(name="Global Leaderboard 🏆", value = leaderboard, inline=False)
            await message.channel.send(embed=embedVar)

    async def searchTerm(self, message, term):
        embedVar = discord.Embed(title="Definition of Vocabulary Term 📖", description="", color=0xA020F0)

        if term.upper() in vocabWords.vocabWords:

            embedVar.add_field(name=term.title() , value=vocabWords.vocabWords[term.upper()], inline=False)
            await message.channel.send(embed=embedVar)
        elif term.title() in vocabWords.vocabWords:
            embedVar.add_field(name=term.title() , value=vocabWords.vocabWords[term.title()], inline=False)
            await message.channel.send(embed=embedVar)
        
        else:
            await message.channel.send("Could not find term.")


    
