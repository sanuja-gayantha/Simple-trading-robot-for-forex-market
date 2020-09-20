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

    overbought_currency, oversold_currency =  executing_logic(input_tframe, input_date)
    #print(overbought_currency, oversold_currency)

    combine_pairs = []
    for i in oversold_currency:
        for j in overbought_currency:
            csymbol, corder_type = searching_pair(i, j[1])
            combine_pairs.append([csymbol, corder_type, j[0]])



    #print(combine_pairs)
    #Insert data into sqlite database
    for i in combine_pairs:
            insert_database(input_date, i[0], i[1], ((i[2]/60)+1), ((i[2]/60)+1), round(symbol_value(input_date, i[0], ((i[2]/60)+1)),5), None, None, None)




def insert_database(execute_date, symbol, order_type, tfexecute, stfexecute, open_value, stfclose, close_value, tpips):
    try:
        connection = sqlite3.connect("7Algo.db")
        cursor = connection.cursor()
        #print("Connected to SQLite")

        cursor.execute("CREATE TABLE if not exists EXECUTE_ORDERS (EXECUTE_DATE TEXT, SYMBOL TEXT, ORDER_TYPE TEXT, TFEXECUTE TEXT, STFEXECUTE TEXT, OPEN_VALUE REAL, STFCLOSE TEXT, CLOSE_VALUE REAL, TPIPS REAL, PRIMARY KEY(EXECUTE_DATE, STFEXECUTE , SYMBOL))")
        cursor.execute("CREATE TABLE if not exists ALL_ORDERS (EXECUTE_DATE TEXT, SYMBOL TEXT, ORDER_TYPE TEXT, TFEXECUTE TEXT, STFEXECUTE TEXT, OPEN_VALUE REAL, PRIMARY KEY(EXECUTE_DATE, STFEXECUTE , SYMBOL))")

        insert_query1 = """INSERT INTO EXECUTE_ORDERS
                            (EXECUTE_DATE, SYMBOL, ORDER_TYPE, TFEXECUTE, STFEXECUTE, OPEN_VALUE, STFCLOSE, CLOSE_VALUE, TPIPS) 
                             VALUES 
                            (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        insert_query2 = """INSERT INTO ALL_ORDERS
                            (EXECUTE_DATE, SYMBOL, ORDER_TYPE, TFEXECUTE, STFEXECUTE, OPEN_VALUE) 
                             VALUES 
                            (?, ?, ?, ?, ?, ?);"""

        All_data1 = (execute_date, symbol, order_type, tfexecute, stfexecute, open_value, stfclose, close_value, tpips)
        All_data2 = (execute_date, symbol, order_type, tfexecute, stfexecute, open_value)

        cursor.execute(insert_query1, All_data1)
        cursor.execute(insert_query2, All_data2)
        connection.commit()
        cursor.close()
        connection.close()

    except Exception as e:
        print(e)




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



def symbol_value(idate, isymbol, itime):

    if itime > 23:
        itime = itime - 23    

        wtdelta = datetime.timedelta(days = 1)
        wdate = wtdelta + idate
        day_of_week = datetime.date(wdate.year, wdate.month, wdate.day).weekday()
    
        if (0 != day_of_week): 
            tdelta = datetime.timedelta(days = 1)
        else: 
            tdelta = datetime.timedelta(days = 3)

        idate =  idate + tdelta #create real date


    #connect to metatrader 5
    mt5.initialize()
    # set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime.datetime(idate.year, idate.month, idate.day, 00, 00, tzinfo=timezone)
    utc_to = datetime.datetime(idate.year, idate.month, idate.day, 23, 59, tzinfo=timezone)
    crates = mt5.copy_rates_range(isymbol.upper(), mt5.TIMEFRAME_H1, utc_from, utc_to)
    mt5.shutdown()

    for i in crates:
        timep = dt.utcfromtimestamp(int(i[0])).strftime('%Y-%m-%d %H:%M')
        timep_object = dt.strptime(timep, '%Y-%m-%d %H:%M')
        if(timep_object.hour == itime-1):
            return i[4]   # return for sutable time




#-------------------------------------------------------------------------------------------------------------------------------------------
#closing logic

def trade_closing_logic(input_tframe, input_date):
    try:
        connection = sqlite3.connect("7Algo.db")
        cursor = connection.cursor()

        insert_query = """SELECT * FROM EXECUTE_ORDERS WHERE EXECUTE_DATE = ?"""

        cursor.execute(insert_query, (input_date,))
        records = cursor.fetchall()

        for row in records:
            #check equality symbol and order type
            #and calculate total pips values
            #update the values in to sqlite database
            close_value = round((symbol_value(input_date, row[1], (float(row[3]) + 6))), 5)
            
            if (row[2] == "buy"):
                cbs_values = (close_value - row[5])

            elif(row[2] == "sell"): 
                cbs_values = (row[5] - close_value)

            if (float(row[3]) + 6) > 23:
                itime = (float(row[3]) + 6) - 23
            else:
                itime = (float(row[3]) + 6)


            if(row[1] == "usdjpy" or row[1] == "nzdjpy" or row[1] == "gbpjpy" or row[1] == "eurjpy" or row[1] == "chfjpy"
                        or row[1] == "cadjpy" or row[1] == "audjpy"):

                tpips = round((cbs_values * 100),0)
                update_data(row[0], row[1], row[2], row[3], row[4], row[5], itime, close_value, tpips)

            else:
                tpips = round((cbs_values * 10000), 0)
                update_data(row[0], row[1], row[2], row[3], row[4], row[5], itime, close_value, tpips)


        cursor.close()
        connection.close()

    except Exception as e:
            print(e)
        

def update_data(execute_date, symbol, order_type, tfexecute, stfexecute, open_value, stfclose, close_value, tpips):
    try:

        connection = sqlite3.connect("7Algo.db")
        cursor = connection.cursor()
      
        #update data in to database
        data_insert_query = """UPDATE EXECUTE_ORDERS SET STFCLOSE =?, CLOSE_VALUE  =?,  TPIPS = ? WHERE EXECUTE_DATE = ? AND SYMBOL = ? AND TFEXECUTE = ?"""
        i_values = (stfclose, close_value, tpips, execute_date, symbol, tfexecute)
        cursor.execute(data_insert_query, i_values)
        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        print(e)   



#-------------------------------------------------------------------------------------------------------------------------------------------
#calling function 

def Algo(fdate): 

    execute_logic(mt5.TIMEFRAME_H1, fdate)
    trade_closing_logic(mt5.TIMEFRAME_H1, fdate) 

    
