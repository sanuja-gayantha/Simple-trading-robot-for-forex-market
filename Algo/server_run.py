from datetime import datetime
import time
import datetime
import MetaTrader5 as mt5
import USD
import EUR
import AUD
import NZD
import JPY
import CHF
import GBP
import CAD
import sqlite3
import pytz
from datetime import datetime as dt



#-------------------------------------------------------------------------------------------------------------------------------------------
#executing logic
def executing_logic(input_tframe, input_date):

    curency_list = [(USD,"usd"), (EUR,"eur"), (AUD,"aud"), (NZD,"nzd"), (JPY,"jpy"), (CHF,"chf"), (GBP,"gbp"), (CAD,"cad")]
    overbought_currency = []
    oversold_currency = []

    j = 0
    while j<8:
        currencies = curency_list[j][0].main_loop(input_tframe, input_date)
        oblist = list(currencies.items())
        #print(oblist)
        #print(len(oblist))

        
        ############################ find overbought currencies ##############################
        i = 0
        count  = 0  
        while i < (len(oblist) - 2):
            #print(i, oblist[i])
            if ((oblist[i][1] < 0.1 and oblist[i+1][1] > 0.1) or (oblist[i][1] > -0.1 and oblist[i+1][1] < -0.1) 
                    or (oblist[i][1] > 0.1 and oblist[i+1][1] < 0.1) or (oblist[i][1] < -0.1 and oblist[i+1][1] > -0.1)):

                count += 1
                #print(i, (i+1), oblist[i][0], oblist[i+1][0], count)
                if(count % 2 == 0):
                    #print(oblist[i+1], count)
                    overbought_currency.append((oblist[i+1][0], curency_list[j][1]))

            i = i+1     
        #print(count)

        ############################ find over sold currencies ##############################
        positive_oblist = []
        for k in oblist:
            positive_oblist.append(abs(k[1]))

        if (max(positive_oblist) <= 0.05):
            #print(max(positive_oblist), curency_list[j][1])
            oversold_currency.append(curency_list[j][1])    

        j = j+1

    #print(overbought_currency)
    #print(oversold_currency)

    return overbought_currency, oversold_currency

      
def execute_logic(input_tframe, input_date):
    try:
        overbought_currency, oversold_currency =  executing_logic(input_tframe, input_date)
        #print(overbought_currency, oversold_currency)

        combine_pairs = []
        for i in oversold_currency:
            for j in overbought_currency:
                csymbol, corder_type = searching_pair(i, j[1])
                combine_pairs.append([csymbol.upper(), corder_type, j[0]])


        #print(combine_pairs)

        orders = "" #send orders-------------->

        #open orders
        if (len(combine_pairs) != 0):

                connection = sqlite3.connect("7Algo.db")
                cursor = connection.cursor()

                cursor.execute("CREATE TABLE if not exists REAL_OPEN_CLOSE_ORDERS (EXECUTE_DATE TEXT, SYMBOL TEXT, ORDER_TYPE TEXT, STFEXECUTE TEXT, POSITION TEXT, STFCLOSE TEXT, PRIMARY KEY(EXECUTE_DATE, SYMBOL , ORDER_TYPE , STFEXECUTE))")
        
                insert_query0 = """SELECT * FROM REAL_OPEN_CLOSE_ORDERS WHERE EXECUTE_DATE = ? AND SYMBOL = ? AND ORDER_TYPE = ? AND STFEXECUTE = ? AND POSITION = ?"""
                position = "open"
                for i in combine_pairs:
                    cursor.execute(insert_query0, (input_date, i[0], i[1], i[2], position))
                    records = cursor.fetchall()

                    if len(records) == 0:
                                insert_query1 = """INSERT INTO REAL_OPEN_CLOSE_ORDERS (EXECUTE_DATE, SYMBOL, ORDER_TYPE,  STFEXECUTE, POSITION, STFCLOSE) VALUES (?, ?, ?, ?, ?, ?);"""
                                insert_data = (input_date, i[0], i[1], i[2], "open", None)
                                cursor.execute(insert_query1, insert_data)                           

                                #create bytestream variable
                                orders += i[0]
                                orders += ","
                                orders +=  i[1]
                                orders += ","
                                orders += str(int(i[2])/60)
                                orders += ","                            
                                orders +=  "open"
                                orders += ","

                connection.commit()
                cursor.close()
                connection.close()

        #Close trades
        
        connection = sqlite3.connect("7Algo.db")
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE if not exists REAL_OPEN_CLOSE_ORDERS (EXECUTE_DATE TEXT, SYMBOL TEXT, ORDER_TYPE TEXT, STFEXECUTE TEXT, POSITION TEXT, STFCLOSE TEXT, PRIMARY KEY(EXECUTE_DATE, SYMBOL , ORDER_TYPE , STFEXECUTE))")
     
        insert_query2 = """SELECT * FROM REAL_OPEN_CLOSE_ORDERS WHERE EXECUTE_DATE = ? AND POSITION = ?"""
        position = "open"
        cursor.execute(insert_query2, (input_date, position))
        records = cursor.fetchall()

        for row in records:
            ctime = current_time(input_date, row[1])
            if ctime >= (int(row[3]) + (6*60)) : #check qequility 

                #create bytestream variable
                orders += row[1]
                orders += ","
                orders +=  row[2]
                orders += ","
                orders += str(ctime)
                orders += ","                            
                orders +=  "close"
                orders += ","

                data_update_query = """UPDATE REAL_OPEN_CLOSE_ORDERS SET POSITION = ?, STFCLOSE = ? WHERE EXECUTE_DATE = ? AND SYMBOL = ? AND STFEXECUTE = ? AND POSITION = ?"""
                
                new_position = "close"
                update_values = (new_position, ctime, input_date, row[1], row[3], position)
                cursor.execute(data_update_query, update_values)
                connection.commit()           

        connection.commit()   
        cursor.close()
        connection.close()
        
       
        if len(orders) > 0:
            print(orders)
        else:
            print("No new order to open!!!")    
        return orders

    except Exception as e:
        pass 



def searching_pair(os, ob):
    
    pair_list = ["usdjpy", "nzdjpy", "gbpjpy", "eurjpy", "chfjpy", "cadjpy", "audjpy",
                 "audusd", "nzdusd", "usdchf", "gbpusd", "eurusd", "usdcad",
                 "audnzd", "nzdchf", "gbpnzd", "eurnzd", "nzdcad",
                 "gbpaud", "gbpchf", "eurgbp", "gbpcad",
                 "euraud", "eurchf", "eurcad",
                 "audchf", "cadchf",
                 "audcad"]
    
    for i in pair_list:
        if(ob+os == i):
            return i, "sell" 
        elif (os+ob == i):
            return i, "buy"


def current_time(idate, isymbol):

    mt5.initialize()
    timezone = pytz.timezone("Etc/UTC")
    utc_from = datetime.datetime(idate.year, idate.month, idate.day, 00, 00, tzinfo=timezone)
    utc_to = datetime.datetime(idate.year, idate.month, idate.day, 23, 59, tzinfo=timezone)
    crates = mt5.copy_rates_range(isymbol.upper(), mt5.TIMEFRAME_H1, utc_from, utc_to)
    mt5.shutdown()

    if crates is not None:
        timep = dt.utcfromtimestamp(int(crates[-1][0])).strftime('%Y-%m-%d %H:%M')
        timep_object = dt.strptime(timep, '%Y-%m-%d %H:%M')
        timepn = ((timep_object.hour) * 60 + timep_object.minute)
        return timepn




'''
fdate = dt(2020, 5, 28) 
execute_logic(mt5.TIMEFRAME_H1, fdate)
#symbol = "EURUSD"
#timepn = current_time(fdate, symbol)    
#print(timepn)
'''