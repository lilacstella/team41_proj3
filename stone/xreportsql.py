import json
import psycopg2
from datetime import date

def get_xreport():
    connection = None
    try:
        connection = psycopg2.connect(user="csce315331_team_41_master",
                                      password="goldfishwithnuts",
                                      host="csce-315-db.engr.tamu.edu",
                                      database="csce315331_team_41")
        cursor = connection.cursor()
        todaysdate = date.today()
        todaystr = todaysdate.strftime("%Y-%m-%d")

        xreportquery = ("select c.menuitem, c.countitem as quantity, ROUND(c.countitem * price, 2) as totalsales  from menu_t m inner join "
                    + "(select menuitem, count(menuitem) as countitem from orderitem_t i inner join(select ordernumber from order_history where date(orderedat)  = '"
                    + todaystr + "')h on h.ordernumber = i.ordernumber  group by menuitem) c on m.menuitem = c.menuitem")
        cursor.execute(xreportquery)
        xreporttable = cursor.fetchall()

        xreportdict = {}
        saleslist = []
        for row in xreporttable:
            salesdata = {"itemname" : row[0], "numbersold" : row[1], "sales": str(row[2])}
            saleslist.append(salesdata)
        xreportdict["salesdata"] = saleslist

        xreportpaymenttype = "select paymentform, sum(total) as totalsales from order_history where date(orderedat) = '" + todaystr +  "' group by paymentform;"
        cursor.execute(xreportpaymenttype)
        xreportpayment = cursor.fetchall()
        paymentlist = []
        total = 0
        for row in xreportpayment:
            total += row[1]
            paymentdata = {"paymenttype" : row[0], "sales": str(row[1])}
            paymentlist.append(paymentdata)
        xreportdict["paymentdata"] = paymentlist
        xreportdict["total"] = str(total)

        print(xreportdict)
        return xreportdict
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")