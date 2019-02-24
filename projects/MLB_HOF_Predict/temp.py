import pandas as pd
import math

#----------------------------------------
#           load HOF data
#----------------------------------------
df_HallOfFame_all = pd.read_excel('data/HallOfFame.xlsx')
df_HallOfFame_all = df_HallOfFame_all[df_HallOfFame_all.category == 'Player']
df_HallOfFame_all = df_HallOfFame_all[df_HallOfFame_all.votedBy == 'BBWAA']
df_HallOfFame_all['ElectionDecade'] = df_HallOfFame_all.apply(lambda x: round_down(x.yearid), axis=1)

#--inducted
df_HallOfFame_INDUCTED = df_HallOfFame_all[df_HallOfFame_all.inducted == 'Y']

#-not inducted
df_No_HallOfFame = df_HallOfFame_all[df_HallOfFame_all.inducted != 'Y']

#--combined list - inducted and not inducted
df_Dups = df_No_HallOfFame.merge(df_HallOfFame_INDUCTED, on=['playerID'], how='left')
#--remove inducted from non inducted df
df_No_HallOfFame = df_Dups[df_Dups.inducted_y != 'Y']

#--clean up the data
df_No_HallOfFame.rename(
    {'ElectionDecade_x': 'ElectionDecade',
     'inducted_x':'inducted',
     'ballots_x':'ballots',
     'needed_x':'needed',
     'votes_x':'votes',
     'yearid_x':'yearid',
     'playerID':'playerID',
    },
    axis=1 ,
    inplace=True
)

myColumns = ['ElectionDecade','inducted','ballots','needed','votes','yearid','playerID']
df_No_HallOfFame = df_No_HallOfFame[myColumns].copy()

df_HallOfFame_INDUCTED.rename(
    {'ElectionDecade_y': 'ElectionDecade',
     'inducted_y':'inducted',
     'ballots_y':'ballots',
     'needed_y':'needed',
     'votes_y':'votes',
     'yearid_y':'yearid',
     'playerID':'playerID',
    },
    axis=1 ,
    inplace=True
)

df_HallOfFame_INDUCTED = df_HallOfFame_INDUCTED[myColumns].copy()
df_myHOF = pd.concat([df_No_HallOfFame, df_HallOfFame_INDUCTED])


print(df_myHOF.head(5))
df_myHOF.to_excel('data/myHOF.xlsx')