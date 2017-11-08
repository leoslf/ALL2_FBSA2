from random import *
from tkinter import *
from tkinter.ttk import *
import numbers
from .debug import *
from .sorting import *
from .odbc import *

class ListView(Frame):
    """
    ListView extends tkinter.Frame
    """

    def __init__(self, parent):
        """
        Constructor of ListView

        param:
            parent (tk.Tk): parent of the ListView Object, possibly directly passing the variable assigned from Tk()
                e.g. root = Tk()
                     ListView(root)
        """
        # super-class constructor
        Frame.__init__(self, parent)
        self.root = parent # save the parent for accessing in whole class
        self.pack() # display ListView

        self.table_init() # init table
        self.filter_init(self.tbl.update_filter)
        self.tbl.pack() # display the table on GUI

    def filter_init(self, callback):
        """
        initialize the text field for filter

        param:
            callback (function(str)): function to be called when the content of the text field is modified
        """
        # text variable
        filterInput_txt = StringVar()
        # set callback function when the content on the text field is edited (both adding characters at the end and backspace)
        filterInput_txt.trace("w", lambda *argv: self.handle_cb(callback, filterInput_txt))
        
        # init a text field with the text variable with callback
        e = Entry(self, textvariable=filterInput_txt)
        # display the text field
        e.pack()

    def handle_cb(self, f, v):
        """
        callback handler for text field modification
        
        param:
            f (function(str)): function to be called when the content of the text field is modified
            v (tkinter.StringVar): textvariable that contains the content of the text field
        """
        f(v.get()) # StringVar.get() retrieves the content in the text field

    def table_init(self):
        """
        initialize the table
        """
        self.tbl = self.Table(self, query(table="sales as s", join="deliveryLocations as d on d.id = s.deliveryLocation_id"))

    class Table(Treeview):
        
        def __init__(self, parent, result_set):
            """
            Constructor

            param:
                parent (tkinter.Frame): parent of widget
                result_set: (tuple: (column_description, rows)): query result from database
            """
            Treeview.__init__(self, parent)
            self.root = parent
            self.col_desc, _, self.rows = result_set
            self.visibility = [True] * len(self.rows)

            # ascending list, a sequence represents the key / index referencing self.rows
            self.order = list(range(len(self.rows)))
            self.config_columns()
            self.init_rows()

        def update_filter(self, txt):
            info(txt)
            if len(txt) < 1:
                self.visibility = [True] * len(self.rows)
            else:
                self.visibility = [False] * len(self.rows)
                for i in range(len(self.rows)):
                    for j in range(len(self.rows[i])):
                        if str(self.rows[i][j])[:len(txt)] == txt:
                            self.visibility[i] = True
                            break
            self.update_rows()


        def config_columns(self):
            self['columns'] = self['displaycolumns'] =  tuple(zip(*self.col_desc))[0]
            for i, col in enumerate(self['columns']):
                self.heading("#" + str(i), text=col, command=lambda col=i: self.sortTable(col))

        def init_rows(self):
            #pass
            self.rows_identifier = []
            for i, _row in enumerate(self.rows):
                zerothCol, *row = _row
                self.rows_identifier.append(self.insert('', 'end', iid=i+1, text=zerothCol, values=tuple(row)))
            info(self.rows_identifier)
            info(self.order)
        
        def update_rows(self):
            #for i, iid in enumerate(self.rows_identifier):
            #    info(iid)
            #    info(self.index(iid))
            #    self.move(iid, '', self.order[i] + 1)
            row = 0
            for i, row_idx in enumerate(self.order):
                if self.visibility[i]:
                    self.reattach(row_idx + 1, '', row)
                    row += 1
                else:
                    # hide the widget
                    self.detach(row_idx + 1)

        def sortTable(self, columnNo):
            info("column #%d pressed" % columnNo)
            #debug(list(zip(*self.rows))[columnNo])
            #qsort(self.order, lambda a, b: self.comparator(columnNo, a, b))
            bubblesort(self.order, lambda a, b: self.comparator(columnNo, a, b))
            info(self.order)
            self.update_rows()

        def comparator(self, col, a, b):
            a, b = self.rows[a][col], self.rows[b][col]
            #print((a, b))
            if a is None or b is None:
                return 0
            if str(a).isdigit() and str(b).isdigit() or isinstance(a, numbers.Number) and isinstance(b, numbers.Number):
                return float(a) - float(b)
            if isinstance(a, str) and isinstance(b, str):
                if a == b:
                    return 0
                elif a < b:
                    return -1
                else:
                    return 1
            if isinstance(a, str) and isinstance(b, numbers.Number):
                return 1
            return 0


def doNothing(*argv):
    info(argv)

