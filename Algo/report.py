from PollyReports import *
from reportlab.pdfgen.canvas import Canvas
import sqlite3

def report():
    ldata = []
    data = {}
    dlist=[]

    try:
        connection = sqlite3.connect("7Algo.db")
        cursor = connection.cursor()
        insert_query = """SELECT * FROM EXECUTE_ORDERS """
        cursor.execute(insert_query)
        ldata = cursor.fetchall()
        cursor.close()
        connection.close()

    except Exception as e:
        print(e)

    date_list = []
    for count,row in enumerate(ldata):
        data["No"] = count+1
        data["Date"] = row[0]
        date_list.append(row[0])
        data["Symbol"] = row[1]
        data["Type"] = row[2]
        data["Exe_time"] = row[4]
        data["Open_value"] = str(row[5])
        data["Close_value"] = str(row[7])
        data["Close_time"] = row[6]
        data["Pips"] = row[8]
        dlist.append(data.copy())


    report_start_date = date_list[0]
    report_end_date = date_list[-1]
    rpt = Report(dlist)
    rpt.detailband = Band([
                    Element((10,0),  ("Helvetica", 10), key = "No"),
                    Element((33,0),  ("Helvetica", 10), key = "Date"),
                    Element((107,0), ("Helvetica", 10), key = "Symbol"),
                    Element((170,0), ("Helvetica", 10), key = "Type"),
                    Element((220,0), ("Helvetica", 10), key = "Exe_time"),
                    Element((275,0), ("Helvetica", 10), key = "Open_value"),
                    Element((345,0), ("Helvetica", 10), key = "Close_value"),
                    Element((415,0), ("Helvetica", 10), key = "Close_time"),
                    Element((470,0), ("Helvetica", 10), key = "Pips"),
                    ])

    rpt.pageheader = Band([
        Element((250, 0), ("Times-Bold", 20), 
            text = "Trade History Report", align = "center"),
        Element((170, 27), ("Times-Bold", 12), 
            text = report_start_date),
        Element((239, 27), ("Times-Bold", 12), 
            text = "To"),
        Element((265, 27), ("Times-Bold", 12), 
            text = report_end_date),

        Rule((7, 50), 7*72, thickness = 2),

        Element((10, 55), ("Times-Bold", 10), 
            text = "No"),
        Element((43, 55), ("Times-Bold", 10), 
            text = "Date"),
        Element((107, 55), ("Times-Bold", 10), 
            text = "Symbol"),
        Element((169, 55), ("Times-Bold", 10), 
            text = "Type"),
        Element((210, 55), ("Times-Bold", 10), 
            text = "Exe_time"),
        Element((270, 55), ("Times-Bold", 10), 
            text = "Open_value"),
        Element((340, 55), ("Times-Bold", 10), 
            text = "Close_value"),
        Element((405, 55), ("Times-Bold", 10), 
            text = "Close_time"),
        Element((469, 55), ("Times-Bold", 10), 
            text = "Pips"),

        Rule((7, 70), 7*72, thickness = 2),
    ])
    rpt.pagefooter = Band([
        Element((36, 16), ("Times-Bold", 10), 
            sysvar = "pagenumber", 
            format = lambda x: "Page %d" % x),
    ])


    rpt.reportfooter = Band([
        Rule((7, 4), 7*72, thickness = 2),
        Element((405, 10), ("Helvetica-Bold", 12),
            text = "Total pips"),
        SumElement((469, 10), ("Helvetica-Bold", 12), 
            key = "Pips"),
        Element((36, 17), ("Helvetica-Bold", 12), 
            text = ""),
    ])

    name = (report_start_date +" " +"to" +" " +report_end_date +".pdf")
    canvas = Canvas(name, (72*8.27, 72*11.69))
    rpt.generate(canvas)
    canvas.save()

