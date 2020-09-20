from datetime import datetime
import time
import MetaTrader5 as mt5
import pytz
from pprint import pprint
import matplotlib.pyplot as plt
import math
import collections 
from collections import OrderedDict
from datetime import datetime as dt

'''
important-:
value1, value2 = return_values() #in the case where you return 2 values
values = return_values() # in the case values will contain a tuple

Etc/GMT is just a standard way of saying UTC, GMT, GMT0 or GMT+00:00.

start = time.time()
end = time.time()
print(end - start)
'''


class PN_values:
    try:
        def __init__(self, ctype, time_frame, sedate):
            self.ctype = ctype
            self.time_frame = time_frame
            self.pnvalues = {}
            if self.ctype == "CHFJPY" :
                self.boolvalue = 100
            else:
                self.boolvalue = 10000
            self.sedate = sedate

        def currency_main(self):
                #connect to metatrader 5
                mt5.initialize()
                # set time zone to UTC
                timezone = pytz.timezone("Etc/UTC")
                # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone
                utc_from = datetime(self.sedate.year, self.sedate.month, self.sedate.day, 00, 00, tzinfo=timezone)
                utc_to = datetime(self.sedate.year, self.sedate.month, self.sedate.day, 23, 59, tzinfo=timezone)
                crates = mt5.copy_rates_range(self.ctype, self.time_frame, utc_from, utc_to)
                #shut down connection to MetaTrader 5
                mt5.shutdown()

                self.pnvalues = {}

                if crates is not None:
                    for row_values in crates:
                        #print(row_values[0] ,row_values[4])
                        #get row_values[4] ,starting closing value
                        zero_value = float(crates[0][4])
                        timep = dt.utcfromtimestamp(int(row_values[0])).strftime('%Y-%m-%d %H:%M')
                        timep_object = dt.strptime(timep, '%Y-%m-%d %H:%M')
                        timepn = ((timep_object.hour) * 60 + timep_object.minute)
                        if timepn == 0:
                            pass

                        else:                                   
                            #valuestake positive / negative to dictonary 
                            if self.ctype == "AUDCHF" or self.ctype == "NZDCHF" or self.ctype == "USDCHF" or self.ctype ==  "GBPCHF" or self.ctype ==  "EURCHF" or self.ctype ==  "CADCHF":
                                #ged USD/EUR ratio pips value
                                # equation________
                                #if we consider (x,y) are the ratios of EUE/USD pair and pair is going up then;
                                # total up pip values in UDS/EUR pair = (y-x)/(x*y)

                                self.inverse  =  round((zero_value - row_values[4]), 6) / round((row_values[4] * zero_value), 6)

                            else:
                                self.inverse = (row_values[4] - zero_value)

                            self.pnvalues[timepn] = round(((self.inverse * self.boolvalue)  / timepn), 6)
                            #print(timepn , row_values[4], self.pnvalues[timepn])

                    return self.pnvalues

    except Exception as e:
        print(e,' ,Somethin went wrong "currency_main(time_frame)" in "currency" module')




def main_loop(time_framel, sedatel):
    i = 0
    #contain all dictonary values in list
    all_pnvalues_list = []

    #currency pair list
    currency_pair_list = ["AUDCHF", "NZDCHF", "CHFJPY", "USDCHF", "GBPCHF", "EURCHF", "CADCHF"]
    while i < 7:
        #create PN_values class object
        object_PN_values = PN_values(currency_pair_list[i], time_framel, sedatel)
        all_pnvalues_list.append(object_PN_values.currency_main())
        i += 1
    #print(all_pnvalues_list)

    # sum the values with same keys / visit this site for more detils --> https://www.geeksforgeeks.org/python-sum-list-of-dictionaries-with-same-key/
    counter = collections.Counter() 
    for d in all_pnvalues_list:  
        counter.update(d)         
    result = dict(counter)

    #print(result)

    #deviding all dictionary values by 7 to get average value foe "EUR"
    # EUR = ((eur_aud+ eur_nzd_pnvalues + eur_jpy_pnvalues + eur_chf_pnvalues + eur_gbp_pnvalues + eur_usd_pnvalues + eur_cad_pnvalues) / 7)
    
    for key in result:      
        #print(key)
        result[key] = result[key] / 7 

    #print(result)
    #add {0:0} dictonary value to result dictonary for better matplotlib chart
    result[0] = 0

    #sort dictonary for get {0:0} value to beginning /[0] index of the dictonary
    #"fresult" contain  the final values of EUR,....
    chf_fresult = OrderedDict(sorted(result.items()))
    #print(b)

    return chf_fresult

