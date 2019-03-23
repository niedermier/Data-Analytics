import pandas as pd

def parseName(NameIn):
    NameOut, Misc = NameIn.split('(')
    NameOut.replace("+","")
    NameOut = NameOut.rstrip()
    return NameOut

def parseYears(NameIn):
    Values = NameIn.split('(')
    temp = Values[1].split(',')
    YearsOut = temp[0]
    YearsOut.replace(")","")
    if YearsOut.endswith(')'):
        YearsOut = ''
    return YearsOut

def parseSeasons(NameIn):
    Values = NameIn.split('(')
    temp = Values[1].split(',')
    print(Values)
    YearsOut = temp[0]
    YearsOut.replace(")","")
    if YearsOut.endswith(')'):
        SeasonsOut = YearsOut.replace(")","")
    else:
        SeasonsOut = ''
    print(NameIn, '..........', YearsOut, '......',SeasonsOut)
    #YearsOut = YearsOut.rstrip()
    return SeasonsOut



#----------------------------------------
#           load WAR data
#----------------------------------------
df_WAR = pd.read_excel('data/CareerWAR.xlsx')
df_WAR['WARName']= df_WAR.apply(lambda x: parseName(x.NameAndYears), axis=1)
#df_WAR['WARYears']= df_WAR.apply(lambda x: parseYears(x.NameAndYears), axis=1)
#df_WAR['WARSeasons']= df_WAR.apply(lambda x: parseSeasons(x.NameAndYears), axis=1)

print(df_WAR.head(10))

#print(df_myHOF.head(5))
#df_myHOF.to_excel('data/myHOF.xlsx')