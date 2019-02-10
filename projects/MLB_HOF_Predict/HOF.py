import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    

#AllstarFull.xlsx
#AwardsPlayers.xlsx
#BattingPost.xlsx
#Fielding.xlsx
#FieldingOF.xlsx
#PitchingPost.xlsx
#Salaries.xlsx
#Schools.xlsx
#SeriesPost.xlsx
#Teams.xlsx
#TeamsFranchises.xlsx


#----------------------------------------
#           load HOF data
#----------------------------------------
df_HallOfFame = pd.read_excel('data/HallOfFame.xlsx')
df_HallOfFame = df_HallOfFame[df_HallOfFame.inducted == 'Y']
df_HallOfFame = df_HallOfFame[df_HallOfFame.category == 'Player']
df_HallOfFame = df_HallOfFame[df_HallOfFame.votedBy == 'BBWAA']
#print(df_HallOfFame.columns)

#----------------------------------------
#           load people
#----------------------------------------
df_People = pd.read_excel('data/People.xlsx')


#----------------------------------------
#           load batting
#----------------------------------------
df_Batting = pd.read_excel('data/Batting.xlsx')
df_Batting_agg = df_Batting.groupby(['playerID']).agg({'R':'sum','H':'sum','HR':'sum','RBI':'sum','SB':'sum','2B':'sum','3B':'sum','BB':'sum','IBB':'sum'}).reset_index()

#---------------------------------------
#           merge HOF and people 
#---------------------------------------
df_myHOF = df_People.merge(df_HallOfFame, on=["playerID"])

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
# eliminate unneeded columns & set data types
#---------------------------------------
myHOFColumns = ['playerID', 'nameFirst','nameLast'
                ,'yearid','ballots','needed','votes',
                'R','H','HR','RBI','SB','2B','3B','BB','IBB',
                'AllStarStarts','AllStarGames']

df_myHOF = df_myHOF[myHOFColumns].copy()
df_myHOF['yearid'] = df_myHOF.yearid.astype(int)
df_myHOF['ballots'] = df_myHOF.ballots.astype(int)
df_myHOF['needed'] = df_myHOF.needed.astype(int)
df_myHOF['votes'] = df_myHOF.votes.astype(int)
#df_myHOF['AllStarStarts'] = df_myHOF.AllStarStarts.astype(int)
#df_myHOF['AllStarGames'] = df_myHOF.AllStarGames.astype(int)
#print(df_myHOF.dtypes)

#---------------------------------------
#       set percent of votes
#---------------------------------------
#df['col_3'] = df.apply(lambda x: f(x.col_1, x.col_2), axis=1)
df_myHOF['percentOfVotes'] = df_myHOF.apply(lambda x: calc_percentOfVotes(x.ballots, x.votes), axis=1) 




#---------------------------------------
#           limit dataset
#---------------------------------------
df_myHOF = df_myHOF[df_myHOF.yearid >= 1965]


#sns.boxplot(x="H",data=df_myHOF)
print('H:\n',df_myHOF.H.describe())
print('HR:\n',df_myHOF.HR.describe())
print('RBI:\n',df_myHOF.RBI.describe())
print('AllStarStarts:\n',df_myHOF.AllStarStarts.describe())
print('AllStarGames:\n',df_myHOF.AllStarGames.describe())
df_myHOF.corr().to_excel('data/myHOFCorr.xlsx')

print(df_myHOF.head(5))
df_myHOF.to_excel('data/myHOF.xlsx')
print('----- ALL DONE -----')

