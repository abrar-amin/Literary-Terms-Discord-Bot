import json



def saveData(playersPoints):
    with open("playerData.json","r+") as playerDataFile:
        playerData = json.load(playerDataFile)
        for player in playersPoints:
            if player in playerData:
                playerData[player] = playerData[player] + int(playersPoints[player])
            else:
                playerData[player] = playersPoints[player]

        playerDataFile.seek(0)  # rewind
        json.dump(playerData, playerDataFile)
        playerDataFile.truncate()

