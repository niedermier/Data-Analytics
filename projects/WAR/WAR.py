import pandas as pd

def findHOF(myVal):
    if (myVal.find('+') != -1):
        return 1
    else:
        return 0
    
def findName(myVal):
    temp = myVal.split("(")
    return temp[0].rstrip()

def findSeasons(myVal):
    temp = myVal.split("(")
    temp1 = temp[1].split(",")
    if (temp1[0].find(')') == -1):
        return temp1[0]
    else:
        temp2 = temp[1].split(")")
        return temp2[0]
    
def findAge(myVal):
    temp = myVal.split(",")
    if len(temp) > 1:
        temp1 = temp[1]
        temp2 = temp1.split("(")
        temp3 = temp2[0].replace(")", "")        
        return temp3
    else:
        return ''
    
def calcWARLeft(WAR, projectedWAR):
    return projectedWAR - WAR

def calcWARPerSeason(WAR, Seasons):
    return WAR / int(Seasons)

def calc_RelatedToHOF(theMean, theStd, Value):
    if (Value > (theMean + theStd + theStd)):
        return "All Time Great"
    if (Value > (theMean + theStd)):
        return "Very Strong"
    if (Value >= theMean):
        return "Strong"
    if (Value < theMean and Value > (theMean - theStd)):
        return "Ok"
    return "Bad"
    
def calcWAR(WAR, Seasons, Age):
    ratePerSeason = int(WAR) / int(Seasons)
    if (int(Seasons) < 18):
        if (int(Age) <=26):
            earlyCareer = ratePerSeason * (int(Seasons)) 
            midCareer = ratePerSeason * 5 * 1.01
            midLateCareer = ratePerSeason * .85 * 4
            laterCareer = ratePerSeason * .75 * (38 - int(Age))        
        elif (int(Age)>26 and int(Age) < 31):
            earlyCareer = 0
            midCareer = ratePerSeason * int(Seasons)
            midLateCareer = ratePerSeason * .85 * 5
            laterCareer = ratePerSeason * .75 * (38 - int(Age))
        elif (int(Age)>=31):
            earlyCareer = 0
            midCareer = 0
            midLateCareer = ratePerSeason * int(Seasons)
            laterCareer = ratePerSeason * .75 * (38 - int(Age))
    else:
        earlyCareer = 0
        midCareer = 0 
        midLateCareer = 0
        laterCareer = WAR
        
    return earlyCareer + midCareer + midLateCareer + laterCareer

myData = pd.read_excel('WAR.xlsx')

myData['HOF'] = myData.apply(lambda row: findHOF(row['Name_WAR']),axis=1)
myData['FullName'] = myData.apply(lambda row: findName(row['Name_WAR']),axis=1)
myData['Seasons'] = myData.apply(lambda row: findSeasons(row['Name_WAR']),axis=1)
myData['Age'] = myData.apply(lambda row: findAge(row['Name_WAR']),axis=1)
myData['WARPerSeason'] = myData.apply(lambda row: calcWARPerSeason(row['WAR'],row['Seasons']),axis=1)
myDisplay = myData.sort_values(by=['WARPerSeason'], ascending=False)
myDisplay = myDisplay[['FullName', 'Seasons', 'Age', 'WAR','WARPerSeason','HOF']]


myHOF = myData[myData.HOF == 1]
myHOF = myHOF.sort_values(by=['WARPerSeason'], ascending=True)

HOF_Mean_War_Per_Season = myHOF.WARPerSeason.mean()
HOF_Std_War_Per_Season = myHOF.loc[:,"WARPerSeason"].std()
myData['WARPerYear_ComparedToHOF'] = myData.apply(lambda row: calc_RelatedToHOF(HOF_Mean_War_Per_Season, HOF_Std_War_Per_Season, row['WARPerSeason']),axis=1)
HOF_Mean_WAR = myHOF.WAR.mean()
HOF_Std_WAR = myHOF.loc[:,"WAR"].std()
myData['WAR_ComparedToHOF'] = myData.apply(lambda row: calc_RelatedToHOF(HOF_Mean_WAR, HOF_Std_WAR, row['WAR']),axis=1)

print(myHOF.WARPerSeason.describe())

#--curious players not in HOF
myCurious = myData[myData.HOF == 0]
myCurious = myCurious[['FullName', 'Seasons', 'Age', 'WAR','WARPerSeason']] 
#myCurious = myData[myData.Age is not '']
myCurious = myCurious[myCurious.WAR >= 60]
myCurious = myCurious.sort_values(by=['WARPerSeason'], ascending=False)
#print(myCurious.head(100))

#--bad HOF choices
badHOF = myData[myData.HOF == 1]
#badHOF = badHOF[badHOF.WarPerSeason < 60]
badHOF = badHOF.sort_values(by=['WAR'], ascending=True)
badHOF = badHOF[['FullName', 'Seasons', 'Age', 'WAR','WARPerSeason']] 
#print(badHOF.head(10))

#--active players
myActivePlayers = myData[myData.Age!= '']
myActivePlayers['ProjectedWAR'] = myActivePlayers.apply(lambda row: calcWAR(row['WAR'],row['Seasons'],row['Age']),axis=1)
myActivePlayers['WARRemaining'] = myActivePlayers.apply(lambda row: calcWARLeft(row['WAR'],row['ProjectedWAR']),axis=1)
myActivePlayers = myActivePlayers.sort_values(by=['WARPerSeason'], ascending=False)
#myActivePlayers = myActivePlayers.sort_values(by=['WARRemaining'], ascending=True)
OnTrackForHOF = myActivePlayers[myActivePlayers.ProjectedWAR >= 20]
OnTrackForHOF = OnTrackForHOF[['FullName', 'WAR','WARPerSeason','WARPerYear_ComparedToHOF','WAR_ComparedToHOF']] 
print(OnTrackForHOF.head(70))

myData.to_excel('myWAR-Output.xlsx')