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

    def __init__(self, parent, **kwargs):
        """
        Constructor of ListView

        Parameters
        ----------
        parent : tkinter Componenets
            parent of the ListView Object, possibly directly passing the variable assigned from Tk()
            e.g. root = Tk()
            ListView(root)
        **kwargs :
            arguemnts of query()
        """
        # super-class constructor
        Frame.__init__(self, parent)
        self.root = parent # save the parent for accessing in whole class
        self.pack() # display ListView

        self.tbl_args = kwargs
        self.rs = query(**kwargs)

        self.tbl = self.Table(self, self.rs)

        self.filter_init(self.tbl.update_filter)

        self.tbl.pack() # display the table on GUI

        self.edit_pane = self.Fields(self, self.rs)


        self.edit_pane.pack()
        

    def filter_init(self, callback):
        """
        filter_init
        
        initialize the text field for filter


        Parameters
        ----------------
        callback : f(str) -> None
            filter function to be called when the content of the text field is modified
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
        handle_cb

        Callback handler for text field modification

        Parameters
        ----------------
        f : f(str) -> None
            filter function to be called when the content of the text field is modified
        v : tkinter.StringVar 
            textvariable that contains the content of the text field
        """
        f(v.get()) # StringVar.get() retrieves the content in the text field

    class Fields(Frame):
        """Fields"""
        def __init__(self, parent, result_set):
            """
            __init__


            Parameters
            ----------------
            parent : tkinter widget
                Parent widget of this widget
            result_set : 3-tuple of lists
                query result from database, with format (column_description[], column_names[], rows[][])
            """
            Frame.__init__(self, parent)
            self.root = parent

            if result_set == ([], [], []):
                warning("result_set == ([], [], [])")
                return
            else:
                self.rs = result_set

            self.entries = [tk.Entry(self) for i in  range(len(self.rs[0]))]
            for x in self.entries:
                x.pack()


    class Table(Treeview):
        
        def __init__(self, parent, result_set):
            """
            Constructor

            Parameters
            ----------------
            parent
                parent (tkinter.Frame): parent of widget
            result_set : 3-tuple of lists
                query result from database

            """
            Treeview.__init__(self, parent)
            self.root = parent
            if result_set == ([], [], []):
                warning("result_set == ([], [], [])")
                return

            self.col_desc, _, self.rows = result_set
            self.visibility = [True] * len(self.rows)

            # ascending list, a sequence represents the key / index referencing self.rows
            self.order = list(range(len(self.rows)))
            self.config_columns()
            self.init_rows()

        def update_filter(self, txt):
            """
            update_filter

            Parameters
            ----------------
            txt : str
                Filter criterion
            """
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
            """config_columns"""
            self['columns'] = self['displaycolumns'] =  tuple(zip(*self.col_desc))[0]
            for i, col in enumerate(self['columns']):
                self.heading("#" + str(i), text=col, command=lambda col=i: self.sortTable(col))

        def init_rows(self):
            """init_rows"""
            self.rows_identifier = []
            for i, _row in enumerate(self.rows):
                zerothCol, *row = _row
                self.rows_identifier.append(self.insert('', 'end', iid=i+1, text=zerothCol, values=tuple(row)))
            #info(self.rows_identifier)
            #info(self.order)
        
        def update_rows(self):
            """
            Update Rows

            Update the display of rows
            """
            row = 0
            for i, row_idx in enumerate(self.order):
                if self.visibility[i]:
                    self.reattach(row_idx + 1, '', row)
                    row += 1
                else:
                    # hide the widget
                    self.detach(row_idx + 1)

        def sortTable(self, columnNo):
            """
            sortTable


            Parameters
            ----------------
            columnNo : int
                Column number of the column required ascending sort
            """
            info("column #%d pressed" % columnNo)
            #debug(list(zip(*self.rows))[columnNo])
            #qsort(self.order, lambda a, b: self.comparator(columnNo, a, b))
            bubblesort(self.order, lambda a, b: self.comparator(columnNo, a, b))
            info(self.order)
            self.update_rows()

        def comparator(self, col, a, b):
            """
            comparator


            Parameters
            ----------------
            col : int
                The column number which is being sorted.
            a : int / float / str / None
                The first value of the pair to be compared.
            b : int / float / str / None
                The second value of the pair to be compared.

            Returns
            -----------------
            int
                The comparison result:
                < 0 if a < b
                0 if a == b
                > 0 if a > b

            """
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



