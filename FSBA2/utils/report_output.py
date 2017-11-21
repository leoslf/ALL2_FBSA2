import dicttoxml
import csv
from collections import OrderedDict
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from .debug import *
from .odbc import *

class report_output(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Button(self, text="Output Business Report: csv", command=self.output_csv).pack()
        Button(self, text="Output Business Report: xml", command=self.output_xml).pack()
        self.pack()

    def output_csv(self, *argv):
        debug("btnclick")
        cols, out_dict_list = self.getDict()
        with open('business_report.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cols)

            writer.writeheader()
            for r in out_dict_list:
                writer.writerow(r)

    def output_xml(self, *argv):
        debug("btnclick")
        cols, out_dict_list = self.getDict()
        with open('business_report.xml', 'w') as xmlfile:
            xml=dicttoxml.dicttoxml(out_dict_list)
            xmlfile.write(xml.decode('utf-8'))
            

    def getDict(self):
        rs = queryData("SalesOrder as o",\
                        """
                        o.id as sales_id, o.Customer_id, o.PrintStatus_id, o.OrderStatus_id, o.date, o.date_created, o.last_updated, o.price, o.source, o.PaymentMethod_id,
                        l.Product_id, p.name, p.Category, l.sequenceNumber, l.price as 'product_price', 
                        o.created_by, e.emailAddr, e.firstName, e.lastName, e.role, e.status""",
                        join="LineItem as l on l.Sales_id = o.id INNER JOIN Product as p ON p.id = l.Product_id INNER JOIN Staff as e on o.created_by = e.id")
        cols, rows = rs
        debug(cols)
        debug(rows)
        out_dict_list = list(OrderedDict(zip(cols, r)) for r in rows)
        debug(out_dict_list)
        return (cols, out_dict_list)

