from nsepy import get_history
from datetime import date

def rollingReturns(symbolName, isIndex, startYear, startMonth, startDate, endYear, endMonth, endDate, nRollingDays):
    l_symbolData = get_history(symbol=symbolName,
                            index=isIndex,
                            start=date(startYear, startMonth, startDate),
                       end=date(endYear, endMonth, endDate)
                       )
    columnName = "previous_close_" + str(nRollingDays)

    l_symbolData[columnName] = l_symbolData['Close'].shift(nRollingDays)
    l_symbolData= l_symbolData[l_symbolData[columnName].notna()]
    l_symbolData = l_symbolData.drop('Turnover', 1)
    l_symbolData = l_symbolData.drop('Open', 1)
    l_symbolData = l_symbolData.drop('High', 1)
    l_symbolData = l_symbolData.drop('Low', 1)
    l_symbolData = l_symbolData.drop('Volume', 1)

    rollingReturnsColumnName = str(nRollingDays) + "Days_Rolling_Returns%"
    l_symbolData[rollingReturnsColumnName] = ((l_symbolData["Close"] - l_symbolData[columnName])/l_symbolData[columnName])*100

    l_symbolData = l_symbolData.drop('Close', 1)
    l_symbolData = l_symbolData.drop(columnName, 1)

    return l_symbolData

print(rollingReturns("NIFTY",True,2000,1,1,2021,12,31,30).describe())
print(rollingReturns("RELIANCE",False,2000,1,1,2021,12,31,30).describe())



'''
Output

       30Days_Rolling_Returns%
count              5382.000000
mean                  1.686174
std                   8.399817
min                 -41.276064
25%                  -2.867361
50%                   2.206729
75%                   6.639907
max                  45.004449
'''
