import dicttoxml
import csv
from collections import OrderedDict
from tkinter import *
from tkinter.ttk import *
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
        rs = queryData("SalesOrder")
        cols, rows = rs
        out_dict_list = list(OrderedDict(zip(cols, r)) for r in rows)
        debug(out_dict_list)
        return (cols, out_dict_list)

