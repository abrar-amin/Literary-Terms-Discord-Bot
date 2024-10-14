from operator import truediv
import random
import time
import asyncio
import vocabWords
import discord

class Question:
    def __init__(self, manager, client, channel, channelID, genre):
        self.vocabWord = ""
        self.vocabDefinition = ""
        self.missedWords = []
        self.expiredAmount = 0
        self.answered = False

        if(genre in ["poetic", "syntax", "grammatical", "drama"]):
            self.vocabWords = vocabWords.GenredVocabWords[genre].copy()
            self.genre = genre + " Terms"
            self.genreHex = vocabWords.genreColors[genre] 


        else:
            self.genre = "All IB Literary Terms"
            self.genreHex = vocabWords.genreColors[self.genre] 
            self.vocabWords = vocabWords.GenredVocabWords[self.genre].copy()



        self.active = True
        self.client = client
        self.points = {}
        self.channel = channel
        self.manager = manager
        self.channelID= channelID
        self.usedWords = []


    
    
    async def checkAnswer(self,answer):
        if(self.active):
            if(answer.content.lower() == self.vocabWord.lower() and self.answered == False):
                self.answered = True
                await self.increasePoint(answer.author.id)
                self.usedWords.append(self.vocabWord)
                await self.channel.send(":medal: Correct!" + " " + answer.author.mention + " **+1 Point** (Total: " + str(self.points[str(answer.author.id)]) + ")")
                await answer.add_reaction("🥇")
                await asyncio.sleep(2)
                if(self.active):
                    if(len(self.vocabWords) == 0):
                        self.manager.stopGame(self.channelID)
                    self.vocabWords.remove(self.vocabWord)
                    await self.askNewQuestion()

            

    async def expireQuestion(self, duration, currentWord):
        await asyncio.sleep(duration)
        if(self.expiredAmount > 3 and currentWord == self.vocabWord):
            self.answered = True
            await self.channel.send("The Correct term is **" + self.vocabWord.title() + "**")
            await self.channel.send(random.choice(vocabWords.gifs))
            self.missedWords.append(self.vocabWord)

            await self.manager.stopGame(self.channelID)
        elif(self.active and self.answered == False and currentWord == self.vocabWord):
            self.usedWords.append(self.vocabWord)
            self.answered = True
            self.missedWords.append(self.vocabWord)
            self.expiredAmount += 1
            await self.channel.send("The Correct term is **" + self.vocabWord.title() + "**")
            await self.channel.send(random.choice(vocabWords.gifs))
            await asyncio.sleep(2)
            self.vocabWords.remove(self.vocabWord)
            if(len(self.vocabWords) == 0):
                await self.manager.stopGame(self.channelID)
            elif(self.active):
                await self.askNewQuestion()


    async def askNewQuestion(self):
        if(len(self.vocabWords) == 0):
            await self.manager.stopGame(self.channelID)
        else:
            self.vocabWord =  random.choice(list(self.vocabWords))
            self.vocabDefinition = vocabWords.vocabWords[self.vocabWord]
            self.answered = False

            embedVar = discord.Embed(title="Definition of Vocabulary Term 📖", description="", color=self.genreHex)
            embedVar.add_field(name= self.genre.upper() + " ", value=self.vocabDefinition, inline=False)
            await self.channel.send(embed=embedVar)
            await self.expireQuestion(15, self.vocabWord)
        
    
    async def increasePoint(self,userID):
        if not str(userID) in self.points:
            self.points[str(userID)] = 1
        else:
            self.points[str(userID)] = self.points[str(userID)]  + 1

    async def result(self):
        
        leaderboard = ""
        missedWords = ""
        sorted_keys = sorted(self.points, key=self.points.get)
        if(len(self.points) > 0):
            leaderboard+=":crown:"
        else:
            leaderboard = "‎"

        for userID in reversed(sorted_keys):
            leaderboard+= f"<@{userID}>" + ": " + "**" +  str(self.points[userID]) + " Point(s)**" + '\n'
        if(len(self.missedWords) > 0):
            for word in self.missedWords:
                missedWords+= '\n•' + "**" + word.title() + "**" 
        else:
            missedWords = "‎"

        
        embedVar = discord.Embed(title="Results 📈", description="", color=self.genreHex)
        embedVar.add_field(name="Leaderboard 🏆", value = leaderboard, inline=False)
        embedVar.add_field(name="Missed Words ❌", value= missedWords, inline=False)

        await self.channel.send(embed=embedVar)

    async def skipQuestion(self):
        if(len(self.vocabWords) == 0):
            await self.manager.stopGame(self.channelID)
        elif(self.answered == False):

            self.vocabWords.remove(self.vocabWord)

            self.answered = True
            self.missedWords.append(self.vocabWord)
        
            await self.askNewQuestion()

        
    



