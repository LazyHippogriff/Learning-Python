#This program will scrape data of the stocks given in the input file from https://www1.nseindia.com/products/content/equities/equities/eq_security.htm and dump the data into redis database.

import bs4
import requests
import sys
from bs4 import BeautifulSoup
from redis import Redis
from datetime import timedelta, datetime, date

start_date = date.today()
end_date = date.today()

def getEndDate(start_date, end_date):
    #print ("Inside getEndDate")
    if int((end_date - start_date).days) < 150:
#        print ("Returning " + end_date.strftime("%d-%m-%Y")) 
        return end_date
    else:
#        print ("Returning " + (start_date + timedelta(150)).strftime("%d-%m-%Y")) 
        return start_date + timedelta(150)

def correctInvalidValues(val):
    if val == "-":
        return 0
    else:
        return val

#No argument is given.
if len(sys.argv)==1:
    print "Case 1: Getting stock data from 1 month back"
    start_date = (date.today()-timedelta(30))
    end_date = (date.today()-timedelta(1))

#Start year is given.
elif len(sys.argv)==2:
    print "Case 2: Getting stock data from " + sys.argv[1] + " till today"
    input_date = "01-01-" + sys.argv[1]
    start_date = datetime.strptime(input_date, "%d-%m-%Y")
    end_date = (datetime.today()-timedelta(1))

#Both dates are given.
elif len(sys.argv)==3:
    print "Case 3: Getting stock data from " + sys.argv[1] + " till " + sys.argv[2]
    start_date = datetime.strptime(sys.argv[1], "%d-%m-%Y")
    end_date = datetime.strptime(sys.argv[2], "%d-%m-%Y")

else:
    print "Case 1: To get stock data from 1 month back-->python " + sys.argv[0]
    print "Case 2: To get stock data starting from a particular year till now-->python " + sys.argv[0] + " [Starting Year]"
    print "e.g. python " +sys.argv[0] + " 2017"
    print "Case 3: To get stock data between 2 given dates-->python " + sys.argv[0] + " [startDate] [EndDate]"
    print "e.g. python " +sys.argv[0] + " 17-02-2017 15-03-2017"
    sys.exit()

r = Redis(host='localhost', port=6379, db=0)

header = []
header.append({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0)Gecko/20100101 Firefox/76.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'referer': 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm'
    })

header.append({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0)Gecko/20100101 Firefox/77.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'referer': 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm'
    })

temp_date = start_date
i=0;
while (True):
        i=i+1
	f = open("nifty50Symbols.txt", "r")
	print ("start date-->" + temp_date.strftime("%d-%m-%Y"))
	print ("end date-->" + getEndDate(temp_date,end_date).strftime("%d-%m-%Y"))

	if temp_date == end_date:
	    break

	for symbol in f:
    		symbol = symbol.rstrip()
                try_again = 1
                retry_attempt = 0
                success = 1
                while (try_again == 1):
                    url='https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=' + symbol + '&segmentLink=3&symbolCount=2&series=EQ&dateRange=+&fromDate=' + temp_date.strftime("%d-%m-%Y") + '&toDate=' + getEndDate(temp_date,end_date).strftime("%d-%m-%Y") + '&dataType=PRICEVOLUMEDELIVERABLE'
                    print (url + "\n")
                    check = 0
    		    response = requests.get(url, headers=header[i%2])
    		    response.encoding = 'ascii' 
    		    soup = BeautifulSoup(response.text,'lxml')
        	    key1 = symbol + "_openPrice"
                    hmap1 = {}
    
      	            key2 = symbol + "_highPrice"
                    hmap2 = {}
    
	            key3 = symbol + "_lowPrice"
                    hmap3 = {}

	            key4 = symbol + "_closePrice"
                    hmap4 = {}

	            key5 = symbol + "_vwap"
                    hmap5 = {}

	            key6 = symbol + "_totalTradedQty"
                    hmap6 = {}

	            key7 = symbol + "_turnover"
                    hmap7 = {}

	            key8 = symbol + "_nTrades"
                    hmap8 = {}

	            key9 = symbol + "_delQty"
                    hmap9 = {}

	            key10 = symbol + "_percentageDlvry"
                    hmap10 = {}

    		    for p in soup('tr')[1:]:
		            binValues = p.find_all('td')
			    date = binValues[2].text.encode('ascii','ignore')
                            val1 = binValues[4].text.encode('ascii','ignore')
                            val1 = correctInvalidValues(val1) 
                            val1 = float(str(val1).replace(',', '')) 
                            hmap1[date] = val1

                            val2 = binValues[5].text.encode('ascii','ignore')
                            val2 = correctInvalidValues(val2)
                            val2 = float(str(val2).replace(',', '')) 
                            hmap2[date] = val2

                            val3 = binValues[6].text.encode('ascii','ignore')
                            val3 = correctInvalidValues(val3) 
                            val3 = float(str(val3).replace(',', '')) 
                            hmap3[date] = val3
        
                            val4 = binValues[8].text.encode('ascii','ignore')
                            val4 = correctInvalidValues(val4) 
                            val4 = float(str(val4).replace(',', '')) 
                            hmap4[date] = val4
        
                            val5 = binValues[9].text.encode('ascii','ignore')
                            val5 = correctInvalidValues(val5) 
                            val5 = float(str(val5).replace(',', '')) 
                            hmap5[date] = val5
        
                            val6 = binValues[10].text.encode('ascii','ignore')
                            val6 = correctInvalidValues(val6) 
                            val6 = float(str(val6).replace(',', '')) 
                            hmap6[date] = val6
        
                            val7 = binValues[11].text.encode('ascii','ignore')
                            val7 = correctInvalidValues(val7) 
                            val7 = float(str(val7).replace(',', '')) 
                            hmap7[date] = val7
        
                	    val8 = binValues[12].text.encode('ascii','ignore')
                            val8 = correctInvalidValues(val8) 
                            val8 = float(str(val8).replace(',', '')) 
                            hmap8[date] = val8

                	    val9 = binValues[13].text.encode('ascii','ignore')
                            val9 = correctInvalidValues(val9) 
                            val9 = float(str(val9).replace(',', '')) 
                            hmap9[date] = val9
        
                	    val10 = binValues[14].text.encode('ascii','ignore')
                            val10 = correctInvalidValues(val10) 
                            val10 = float(str(val10).replace(',', '')) 
                            hmap10[date] = val10

                    if (len(hmap1) != 0 and len(hmap2) != 0 and len(hmap3) != 0 and len(hmap4) != 0 and len(hmap5) != 0 and len(hmap6) != 0 and len(hmap7) != 0 and len(hmap8) != 0 and len(hmap9) != 0 and len(hmap10) != 0) :
                        try_again = 0
                    else:
                        retry_attempt+=1
                        if (retry_attempt > 6):
                            try_again = 0
                            success = 0

                if (success == 1):
                    #print (key4)
                    #print (hmap4)
                    r.hmset(key1,hmap1)
                    r.hmset(key2,hmap2)
                    r.hmset(key3,hmap3)
                    r.hmset(key4,hmap4)
                    r.hmset(key5,hmap5)
                    r.hmset(key6,hmap6)
                    r.hmset(key7,hmap7)
                    r.hmset(key8,hmap8)
                    r.hmset(key9,hmap9)
                    r.hmset(key10,hmap10)
        temp_date = getEndDate(temp_date,end_date)
