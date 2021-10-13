import pandas as pd
from nsepy import get_history
from datetime import date


def addPreviousCloseColumn(fa_dataframe, fa_nDays, columnName):
    df1 = fa_dataframe
    df1[columnName] = df1['Close']
    df1[columnName] = df1[columnName].shift(fa_nDays)
    return df1

def printTop3(fa_dataframe, columnName):
    print("Top 3 bullish")
    maxDataFrame = fa_dataframe.nlargest(3, columnName)
    for idx in maxDataFrame.index:
        ref = fa_dataframe.index.get_loc(idx)
        print(fa_dataframe.iloc[ref - 15: ref + 15])

    print("Top 3 bearish")
    minDataFrame = fa_dataframe.nsmallest(3, columnName)
    for idx in minDataFrame.index:
        ref = fa_dataframe.index.get_loc(idx)
        print(fa_dataframe.iloc[ref - 15: ref + 15])


def rollingReturns(symbolName, isIndex, startYear, startMonth, startDate, endYear, endMonth, endDate, nRollingDays):
    l_symbolData = get_history(symbol=symbolName,
                               index=isIndex,
                               start=date(startYear, startMonth, startDate),
                               end=date(endYear, endMonth, endDate)
                               )
    columnName = "previous_close_" + str(nRollingDays)
    l_symbolData = l_symbolData[~l_symbolData.index.duplicated(keep='first')]

    l_symbolData[columnName] = l_symbolData['Close'].shift(nRollingDays)

    l_symbolData= l_symbolData[l_symbolData[columnName].notna()]

    l_symbolData = l_symbolData.drop('Turnover', 1)
    l_symbolData = l_symbolData.drop('Open', 1)
    l_symbolData = l_symbolData.drop('High', 1)
    l_symbolData = l_symbolData.drop('Low', 1)
    l_symbolData = l_symbolData.drop('Volume', 1)

    if isIndex is not True:
        l_symbolData = l_symbolData.drop('Prev Close', 1)
        l_symbolData = l_symbolData.drop('%Deliverble', 1)
        l_symbolData = l_symbolData.drop('Last', 1)
        l_symbolData = l_symbolData.drop('VWAP', 1)
        l_symbolData = l_symbolData.drop('Symbol', 1)
        l_symbolData = l_symbolData.drop('Series', 1)
        l_symbolData = l_symbolData.drop('Trades', 1)
        l_symbolData = l_symbolData.drop('Deliverable Volume', 1)

    rollingReturnsColumnName = symbolName + "_" + str(nRollingDays) + "Days_Rolling_Returns%"
    l_symbolData[rollingReturnsColumnName] = ((l_symbolData["Close"] - l_symbolData[columnName])/l_symbolData[columnName])*100

    l_symbolData = l_symbolData.drop('Close', 1)
    l_symbolData = l_symbolData.drop(columnName, 1)

    return l_symbolData

nRollingDays=1
symbolName="NIFTY"
isIndex = True
columnName = symbolName + "_" + str(nRollingDays) + "Days_Rolling_Returns%"

rollingReturns = rollingReturns(symbolName,isIndex,2000,1,1,2021,12,31,nRollingDays)
print(rollingReturns.describe())
printTop3(rollingReturns,columnName)

'''
       NIFTY_1Days_Rolling_Returns%
count                   5419.000000
mean                       0.055323
std                        1.439857
min                      -12.980464
25%                       -0.600735
50%                        0.096696
75%                        0.768370
max                       17.744066
Top 3 bullish
            NIFTY_1Days_Rolling_Returns%
Date                                    
2009-04-23                      2.804552
2009-04-24                      1.666326
2009-04-27                     -0.308841
2009-04-28                     -3.102305
2009-04-29                      3.319107
2009-05-04                      5.182861
2009-05-05                      0.216201
2009-05-06                     -1.006308
2009-05-07                      1.623426
2009-05-08                     -1.715573
2009-05-11                     -1.825614
2009-05-12                      3.558769
2009-05-13                     -1.245552
2009-05-14                     -1.149852
2009-05-15                      2.176182
2009-05-18                     17.744066
2009-05-19                     -0.108717
2009-05-20                     -1.114983
2009-05-21                     -1.391003
2009-05-22                      0.655442
2009-05-25                     -0.022414
2009-05-26                     -2.851884
2009-05-27                      3.870819
2009-05-28                      1.427720
2009-05-29                      2.578912
2009-06-01                      1.819530
2009-06-02                     -0.102651
2009-06-03                      0.120435
2009-06-04                      0.925905
2009-06-05                      0.311635
            NIFTY_1Days_Rolling_Returns%
Date                                    
2020-03-13                      3.806510
2020-03-16                     -7.612102
2020-03-17                     -2.504512
2020-03-18                     -5.556454
2020-03-19                     -2.424783
2020-03-20                      5.832915
2020-03-23                    -12.980464
2020-03-24                      2.507145
2020-03-25                      6.624749
2020-03-26                      3.890428
2020-03-27                      0.217556
2020-03-30                     -4.378049
2020-03-31                      3.823767
2020-04-01                     -4.000465
2020-04-03                     -2.059657
2020-04-07                      8.763205
2020-04-08                     -0.494188
2020-04-09                      4.150879
2020-04-13                     -1.295559
2020-04-15                     -0.762187
2020-04-16                      0.756277
2020-04-17                      3.046326
2020-04-20                     -0.052877
2020-04-21                     -3.027473
2020-04-22                      2.291946
2020-04-23                      1.377989
2020-04-24                     -1.712494
2020-04-27                      1.397142
2020-04-28                      1.062237
2020-04-29                      1.838310
            NIFTY_1Days_Rolling_Returns%
Date                                    
2004-04-27                     -3.973685
2004-04-28                     -0.038520
2004-04-29                     -0.418375
2004-04-30                     -0.710357
2004-05-03                     -1.636880
2004-05-04                      1.494311
2004-05-05                      0.936925
2004-05-06                      1.265263
2004-05-07                     -1.546814
2004-05-10                     -1.959046
2004-05-11                     -3.937030
2004-05-12                      0.685516
2004-05-13                      0.374028
2004-05-14                     -7.866084
2004-05-17                    -12.237740
2004-05-18                      8.295230
2004-05-19                      4.248811
2004-05-20                     -1.530759
2004-05-21                      1.059041
2004-05-24                      3.118190
2004-05-25                     -0.133636
2004-05-26                     -0.491691
2004-05-27                     -0.775582
2004-05-28                     -4.894730
2004-05-31                     -1.666943
2004-06-01                      1.637908
2004-06-02                      1.810465
2004-06-03                     -2.612038
2004-06-04                      1.739014
2004-06-07                      1.410164
Top 3 bearish
            NIFTY_1Days_Rolling_Returns%
Date                                    
2020-02-28                     -3.709609
2020-03-02                     -0.615975
2020-03-03                      1.531966
2020-03-04                     -0.462697
2020-03-05                      0.159986
2020-03-06                     -2.480699
2020-03-09                     -4.895604
2020-03-11                      0.066498
2020-03-12                     -8.301939
2020-03-13                      3.806510
2020-03-16                     -7.612102
2020-03-17                     -2.504512
2020-03-18                     -5.556454
2020-03-19                     -2.424783
2020-03-20                      5.832915
2020-03-23                    -12.980464
2020-03-24                      2.507145
2020-03-25                      6.624749
2020-03-26                      3.890428
2020-03-27                      0.217556
2020-03-30                     -4.378049
2020-03-31                      3.823767
2020-04-01                     -4.000465
2020-04-03                     -2.059657
2020-04-07                      8.763205
2020-04-08                     -0.494188
2020-04-09                      4.150879
2020-04-13                     -1.295559
2020-04-15                     -0.762187
2020-04-16                      0.756277
            NIFTY_1Days_Rolling_Returns%
Date                                    
2004-04-23                      0.153476
2004-04-27                     -3.973685
2004-04-28                     -0.038520
2004-04-29                     -0.418375
2004-04-30                     -0.710357
2004-05-03                     -1.636880
2004-05-04                      1.494311
2004-05-05                      0.936925
2004-05-06                      1.265263
2004-05-07                     -1.546814
2004-05-10                     -1.959046
2004-05-11                     -3.937030
2004-05-12                      0.685516
2004-05-13                      0.374028
2004-05-14                     -7.866084
2004-05-17                    -12.237740
2004-05-18                      8.295230
2004-05-19                      4.248811
2004-05-20                     -1.530759
2004-05-21                      1.059041
2004-05-24                      3.118190
2004-05-25                     -0.133636
2004-05-26                     -0.491691
2004-05-27                     -0.775582
2004-05-28                     -4.894730
2004-05-31                     -1.666943
2004-06-01                      1.637908
2004-06-02                      1.810465
2004-06-03                     -2.612038
2004-06-04                      1.739014
            NIFTY_1Days_Rolling_Returns%
Date                                    
2008-10-01                      0.753596
2008-10-03                     -3.352528
2008-10-06                     -5.655658
2008-10-07                      0.117979
2008-10-08                     -2.577220
2008-10-10                     -6.651203
2008-10-13                      6.425403
2008-10-14                      0.800699
2008-10-15                     -5.122703
2008-10-16                     -2.069854
2008-10-17                     -5.963050
2008-10-20                      1.575943
2008-10-21                      3.589727
2008-10-22                     -5.247457
2008-10-23                     -3.980229
2008-10-24                    -12.202912
2008-10-27                     -2.314241
2008-10-28                      6.354489
2008-10-29                      0.463756
2008-10-31                      6.990972
2008-11-03                      5.484128
2008-11-04                      3.227820
2008-11-05                     -4.683174
2008-11-06                     -3.415750
2008-11-07                      2.777730
2008-11-10                      5.894719
2008-11-11                     -6.657667
2008-11-12                     -3.069437
2008-11-14                     -1.337570
2008-11-17                     -0.384294

'''
