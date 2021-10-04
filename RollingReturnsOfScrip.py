from nsepy import get_history
from datetime import date

def addPreviousCloseColumn(fa_dataframe, fa_nDays, columnName):
    df1 = fa_dataframe
    df1[columnName] = df1['Close']
    df1[columnName] = df1[columnName].shift(fa_nDays)
    return df1

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

niftyRollingReturns = rollingReturns("NIFTY",True,2000,1,1,2021,8,31,30)
relianceRollingReturns = rollingReturns("ASIANPAINT",False,2000,1,1,2021,8,31,30)

print(niftyRollingReturns.describe())
print(niftyRollingReturns.nlargest(3, 'NIFTY_30Days_Rolling_Returns%'))
print(niftyRollingReturns.nsmallest(3, 'NIFTY_30Days_Rolling_Returns%'))

print(relianceRollingReturns.describe())
print(relianceRollingReturns.nlargest(3, 'ASIANPAINT_30Days_Rolling_Returns%'))
print(relianceRollingReturns.nsmallest(3, 'ASIANPAINT_30Days_Rolling_Returns%'))



'''
Output
       NIFTY_30Days_Rolling_Returns%
count                    5360.000000
mean                        1.657004
std                         8.404172
min                       -41.276064
25%                        -2.899790
50%                         2.169115
75%                         6.597464
max                        45.004449
            NIFTY_30Days_Rolling_Returns%
Date                                     
2009-05-19                      45.004449
2009-05-20                      41.356196
2009-05-18                      39.068406
            NIFTY_30Days_Rolling_Returns%
Date                                     
2008-10-24                     -41.276064
2008-10-27                     -41.164953
2020-03-23                     -37.302016
       ASIANPAINT_30Days_Rolling_Returns%
count                         5360.000000
mean                             2.376215
std                             11.452175
min                            -92.291981
25%                             -2.169749
50%                              2.941246
75%                              8.550549
max                             39.832072
            ASIANPAINT_30Days_Rolling_Returns%
Date                                          
2009-05-21                           39.832072
2009-05-27                           38.688171
2009-05-26                           35.108494
            ASIANPAINT_30Days_Rolling_Returns%
Date                                          
2013-09-03                          -92.291981
2013-09-04                          -92.014336
2013-09-02                          -91.897336

'''
