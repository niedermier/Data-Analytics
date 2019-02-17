import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

def calc_percentOfVotes(ballots,votes):
    return int(round(votes/ballots*100))

def calc_AllStarStart(startingPos):
    if startingPos > 0:
        return 1
    else:
        return 0

def calc_AllStarGames(year):
    if year > 0:
        return 1   
    else:
        return 0  

#def roundup(x):
    #--round up to the nearest 10
#    return int(math.ceil(x / 10.0)) * 10

def round_down(num):
    #--round down to the nearest 10
    divisor = 10
    return num - (num%divisor)

#----------------------------------------
#           load HOF data
#----------------------------------------
df_HallOfFame = pd.read_excel('data/HallOfFame.xlsx')
df_HallOfFame = df_HallOfFame[df_HallOfFame.category == 'Player']
#df_HallOfFame = df_HallOfFame[df_HallOfFame.inducted == 'Y']
#df_HallOfFame = df_HallOfFame[df_HallOfFame.votedBy == 'BBWAA']
df_HallOfFame['ElectionDecade'] = df_HallOfFame.apply(lambda x: round_down(x.yearid), axis=1)

#--inducted
#df_HallOfFame_INDUCTED = df_HallOfFame_ALL[df_HallOfFame_ALL.inducted == 'Y']
#df_HallOfFame_INDUCTED = df_HallOfFame_INDUCTED[df_HallOfFame_INDUCTED.votedBy == 'BBWAA']

#-not inducted
#df_No_HallOfFame = df_HallOfFame_ALL[df_HallOfFame_ALL.inducted != 'Y']

#--combined list - inducted and not inducted
#df_Dups = df_No_HallOfFame.merge(df_HallOfFame_INDUCTED, on=['playerID'])
#print(df_Dups.head(15)) 


#----------------------------------------
#           load people
#----------------------------------------
df_People = pd.read_excel('data/People.xlsx')


#----------------------------------------
#           load batting
#----------------------------------------
df_Batting = pd.read_excel('data/Batting.xlsx')
df_Batting_agg = df_Batting.groupby(['playerID']).agg({'R':'sum','H':'sum','HR':'sum','RBI':'sum','SB':'sum','2B':'sum','3B':'sum','BB':'sum','IBB':'sum','AB':'sum'}).reset_index()

#---------------------------------------
#           merge HOF and people 
#---------------------------------------
df_myHOF = df_HallOfFame.merge(df_People, on=["playerID"], how='left')

#---------------------------------------
#           merge HOF and batting
#---------------------------------------
df_myHOF = df_myHOF.merge(df_Batting_agg, on=["playerID"])



#---------------------------------------
#           eliminate pitchers
#---------------------------------------
df_Pitching = pd.read_excel('data/Pitching.xlsx')
df_Pitching['isPitcher'] = df_Pitching.apply(lambda _: '', axis=1)
df_Pitching['isPitcher'] =  True
myPitchColumns = ['playerID', 'isPitcher', 'G']
df_Pitching = df_Pitching[myPitchColumns].copy()
df_Pitching = df_Pitching[df_Pitching.G > 10]
del df_Pitching['G']
df_myHOF = df_myHOF.merge(df_Pitching, on=["playerID"], how='left')
df_myHOF = df_myHOF[df_myHOF.isPitcher != True]
del df_myHOF['isPitcher']

#---------------------------------------
#           merge All Star starts/games
#---------------------------------------
df_AllStarFull = pd.read_excel('data/AllstarFull.xlsx')
df_AllStarFull['AllStarStarts'] = df_AllStarFull.apply(lambda x: calc_AllStarStart(x.startingPos), axis=1) 
df_AllStarStarts = df_AllStarFull.groupby(['playerID']).agg({'AllStarStarts':'sum'}).reset_index()
df_myHOF = df_myHOF.merge(df_AllStarStarts, on=["playerID"], how='left')
df_AllStarFull['AllStarGames'] = df_AllStarFull.apply(lambda x: calc_AllStarGames(x.yearID), axis=1) 
df_AllStarGames = df_AllStarFull.groupby(['playerID']).agg({'AllStarGames':'sum'}).reset_index()
df_myHOF = df_myHOF.merge(df_AllStarGames, on=["playerID"], how='left')

#---------------------------------------
#           merge Awards
#---------------------------------------
df_Awards = pd.read_excel('data/AwardsPlayers.xlsx')
#--Gold Glove
df_GoldGlove =  df_Awards[df_Awards.awardID == 'Gold Glove']
df_GoldGlove = df_GoldGlove.groupby(['playerID']).size().reset_index()
df_GoldGlove = df_GoldGlove.rename(columns={df_GoldGlove.columns[1]: 'GoldGlove'})
df_myHOF = df_myHOF.merge(df_GoldGlove, on=["playerID"], how='left')
#--TSN All Star
df_TSNAllStar =  df_Awards[df_Awards.awardID == 'TSN All-Star']
df_TSNAllStar = df_TSNAllStar.groupby(['playerID']).size().reset_index()
df_TSNAllStar = df_TSNAllStar.rename(columns={df_TSNAllStar.columns[1]: 'TSNAllStar'})
df_myHOF = df_myHOF.merge(df_TSNAllStar, on=["playerID"], how='left')
#--Most Valuable Player
df_MVP =  df_Awards[df_Awards.awardID == 'Most Valuable Player']
df_MVP = df_MVP.groupby(['playerID']).size().reset_index()
df_MVP = df_MVP.rename(columns={df_MVP.columns[1]: 'MVP'})
df_myHOF = df_myHOF.merge(df_MVP, on=["playerID"], how='left')
#--Silver Slugger
df_SilverSlugger =  df_Awards[df_Awards.awardID == 'Silver Slugger']
df_SilverSlugger = df_SilverSlugger.groupby(['playerID']).size().reset_index()
df_SilverSlugger = df_SilverSlugger.rename(columns={df_SilverSlugger.columns[1]: 'SilverSlugger'})
df_myHOF = df_myHOF.merge(df_SilverSlugger, on=["playerID"], how='left')

#---------------------------------------
# eliminate unneeded columns & set data types
#---------------------------------------
myHOFColumns = ['playerID', 'nameFirst','nameLast'
                ,'ElectionDecade','yearid','ballots','needed','votes',
                'R','H','HR','RBI','SB','2B','3B','BB','IBB','AB',
                'AllStarStarts','AllStarGames',
                'GoldGlove', 'TSNAllStar','MVP','SilverSlugger',
                'inducted']

df_myHOF = df_myHOF[myHOFColumns].copy()
#df_myHOF['yearid'] = df_myHOF.yearid.astype(int)
#df_myHOF['ballots'] = df_myHOF.ballots.astype(int)
#df_myHOF['needed'] = df_myHOF.needed.astype(int)
#df_myHOF['votes'] = df_myHOF.votes.astype(int)
#df_myHOF['GoldGloves'] = df_myHOF.GoldGlove.astype(int)
#df_myHOF['AllStarStarts'] = df_myHOF.AllStarStarts.astype(int)
#df_myHOF['AllStarGames'] = df_myHOF.AllStarGames.astype(int)
#print(df_myHOF.dtypes)

#---------------------------------------
#       set percent of votes
#---------------------------------------
#df_myHOF['percentOfVotes'] = df_myHOF.apply(lambda x: calc_percentOfVotes(x.ballots, x.votes), axis=1) 


#---------------------------------------
#           limit dataset
#---------------------------------------
df_myHOF = df_myHOF[df_myHOF.yearid >= 1975]

df_Decade = df_myHOF.groupby(['ElectionDecade']).agg({'R':'sum','H':'sum','HR':'sum','RBI':'sum','SB':'sum','2B':'sum','3B':'sum','BB':'sum','IBB':'sum','AB':'sum'}).reset_index()
sns.boxplot(x="ElectionDecade", y="R", palette=["m", "g"], data=df_myHOF, hue="inducted")
plt.figure()
sns.boxplot(x="ElectionDecade", y="HR", data=df_myHOF, hue="inducted")
sns.despine(offset=10, trim=True)
plt.figure()
sns.boxplot(x="ElectionDecade", y="AllStarGames", data=df_myHOF, hue="inducted")
sns.despine(offset=1, trim=True)
plt.figure()
sns.boxplot(x="ElectionDecade", y="AllStarStarts", data=df_myHOF, hue="inducted")
sns.despine(offset=1, trim=True)
plt.figure()
#sns.set(color_codes=True)
#g = sns.lmplot(x="yearid", y="H", hue="inducted", data=df_myHOF, markers=["X", "o"])
g = sns.lmplot(x="yearid", y="H",hue="inducted", data=df_myHOF, markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})
plt.figure()
g = sns.lmplot(x="yearid", y="HR",hue="inducted", data=df_myHOF, markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})
plt.figure()
g = sns.lmplot(x="yearid", y="RBI",hue="inducted", data=df_myHOF, markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})
plt.figure()
g = sns.lmplot(x="yearid", y="AllStarStarts",hue="inducted", data=df_myHOF,markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})
plt.figure()
g = sns.lmplot(x="yearid", y="AllStarGames",hue="inducted", data=df_myHOF, markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})
plt.figure()
g = sns.lmplot(x="yearid", y="GoldGlove",hue="inducted", data=df_myHOF, markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})
plt.figure()
g = sns.lmplot(x="yearid", y="MVP",hue="inducted", data=df_myHOF, markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})
plt.figure()
g = sns.lmplot(x="yearid", y="SilverSlugger",hue="inducted", data=df_myHOF, markers=["X", "o"], palette={"Y": "#0A9803", "N": "#EEE688"})





#sns.boxplot(x="H",data=df_myHOF)
print('H:\n',df_myHOF.H.describe())
print('HR:\n',df_myHOF.HR.describe())
print('RBI:\n',df_myHOF.RBI.describe())
print('AllStarStarts:\n',df_myHOF.AllStarStarts.describe())
print('AllStarGames:\n',df_myHOF.AllStarGames.describe())
print('GoldGlove:\n',df_myHOF.GoldGlove.describe())
print('MVP:\n',df_myHOF.MVP.describe())
print('SilverSlugger:\n',df_myHOF.SilverSlugger.describe())
print('AB:\n',df_myHOF.AB.describe())
#df_myHOF.corr().to_excel('data/myHOFCorr.xlsx')

print(df_myHOF.head(5))
df_Decade.to_excel('data/myHOF.xlsx')




print('----- ALL DONE -----')

