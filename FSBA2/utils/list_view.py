import tkinter as tk
import tkinter.ttk as ttk
import numbers
from collections import OrderedDict
from .debug import *
from .sorting import *
from .searching import *
from .odbc import *
from .table_utils import *

class ListView(tk.Frame):
    """
    ListView

    Contain table-like widget and input fields that can query, insert, update and delete the table from database
    """

    def __init__(self, parent, width, height, **kwargs):
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
        debug("width: %d, height: %d" % (width, height))


        # super-class constructor
        tk.Frame.__init__(self, parent, width=width, height=height)
        self.root = parent # save the parent for accessing in whole class
        self.pack() # display ListView

        self.tbl_args = kwargs
        self.rs = queryData(**kwargs)


        filter_entry_frame = tk.Frame(self)
        filter_entry_frame.pack(fill=tk.X, expand=True)

        self.tbl = self.Table(self, width, height // 3, self.rs)
        self.tbl.pack(fill=tk.X, expand=True) # display the table on GUI
        self.filter_init(filter_entry_frame, self.tbl.update_filter)


        self.edit_pane = self.Fields(self, width, self.rs)
        self.edit_pane.pack(fill="both", expand=True)
        
        self.tbl.set_click_cb(self.edit_pane.setValues)

    def filter_init(self, frame, callback):
        """
        filter_init
        
        initialize the text field for filter


        Parameters
        ----------------
        callback : f(str) -> None
            filter function to be called when the content of the text field is modified
        """
        # text variable
        filterInput_txt = tk.StringVar()
        # set callback function when the content on the text field is edited (both adding characters at the end and backspace)
        filterInput_txt.trace("w", lambda *argv: self.handle_cb(callback, filterInput_txt))
        
        # init a text field with the text variable with callback
        e = tk.Entry(frame, textvariable=filterInput_txt)
        # display the text field
        e.pack(side=tk.RIGHT)

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


    class Table(ttk.Treeview):
        
        def __init__(self, parent, width, height, result_set):
            """
            Constructor

            Parameters
            ----------------
            parent
                parent (tkinter.Frame): parent of widget
            result_set : 2-tuple of lists
                query result from database

            """
            # TODO
            ttk.Treeview.__init__(self, parent)#, padding=(0,0,0,0))
            self.click_cb = None
            self.bind("<<TreeviewSelect>>", self.on_click)

            self.width = width

            self.pack(fill="x", expand=True)
            self.root = parent
            if result_set == ([], []):
                warning("result_set == ([], [])")
                return

            self.cols, self.rows = result_set
            self.visibility = [True] * len(self.rows)

            # ascending list, a sequence represents the key / index referencing self.rows
            self.order = list(range(len(self.rows)))
            self.config_columns()
            self.init_rows()

        def set_click_cb(self, f):
            assert(f is not None and callable(f))
            self.click_cb = f
            

        def on_click(self, event):
            item = self.selection()
            item_idx = self.order[int(self.index(item))]
            debug("item_idx: %d, %r", item_idx, self.rows[item_idx])
            if self.click_cb is not None:
                assert callable(self.click_cb)
                debug("calling self.click_cb")
                self.click_cb(item_idx)
                pass

        def update_filter(self, txt):
            """
            update_filter

            Parameters
            ----------------
            txt : str
                Filter criterion
            """
            info("filter input: %r" % txt)

            if len(txt) < 1:
                # no filter
                self.visibility = [True] * len(self.rows)
            else:
                self.visibility = linearsearch_table(self.rows, txt, lambda a, b: default_cmp(str(a)[:len(b)],b))
                #self.visibility = [False] * len(self.rows)
                #for i in range(len(self.rows)):
                #    for j in range(len(self.rows[i])):
                #        if str(self.rows[i][j])[:len(txt)] == txt:
                #            self.visibility[i] = True
                #            break # the row is valid already

            self.update_rows()


        def config_columns(self):
            """config_columns"""
            self['columns'] = self['displaycolumns'] = self.cols
            debug(self['columns'])
            col_len = max_col(self['columns'], self.rows)
            debug("col_len: %r", col_len)
            total_len = sum(col_len)
            col_len = [l* int(self.width / total_len) for l in col_len]
            debug("new col_len: %r", col_len)
            for i, col in enumerate(self['columns']):
                self.column("#" + str(i), width=col_len[i], stretch=False)
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
            self.order = msort(self.order, lambda a, b: self.comparator(columnNo, a, b))
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
        
    class Fields(tk.Frame):
        """Fields"""
        def __init__(self, parent, width, result_set):
            """
            __init__


            Parameters
            ----------------
            parent : tkinter widget
                Parent widget of this widget
            result_set : 2-tuple of lists
                query result from database, with format (column_description[], column_names[], rows[][])
            """
            tk.Frame.__init__(self, parent)
            self.root = parent
            self.width = width
            debug("width: %d", width)

            if result_set == ([], []):
                warning("result_set == ([], [])")
                return
            
            self.rs = result_set
            self.cols, self.rows = self.rs

            btnFrame = tk.Frame(self)
            btnFrame.pack(fill=tk.X, expand=True)
            self.btns = OrderedDict()
            btn_names = ["New", "Save", "Confirm", "Delete", "Refresh"]
            for i, btn_name in enumerate(btn_names):
                #                                                                 lazy
                self.btns[btn_name] = tk.Button(btnFrame, text=btn_name, command=getattr(self, "cmd_" + btn_name))
                self.btns[btn_name].pack(side=tk.LEFT)
                pass

            entryFrame = tk.Frame(self)
            entryFrame.pack(fill=tk.X, expand=True)
            #self.entries = [tk.Entry(self) for i in  range(len(self.cols))]
            self.labels = []
            self.entries = []
            MAX_COL = 4
            for i, col_name in enumerate(self.cols):
                entryFrame.columnconfigure(i, weight=1, minsize=int(width / MAX_COL), pad=100)
                self.labels.append(tk.Label(entryFrame, text=col_name, justify=tk.LEFT, anchor=tk.W))
                self.entries.append(tk.Entry(entryFrame))
                self.labels[-1].grid(column=i % MAX_COL, row=3*(i // MAX_COL), sticky=tk.W)
                self.entries[-1].grid(column=i % MAX_COL, row=3*(i // MAX_COL) + 1, sticky=tk.W)

        def cmd_New(self):
            pass

        def cmd_Save(self):
            pass

        def cmd_Confirm(self):
            pass

        def cmd_Delete(self):
            pass

        def cmd_Refresh(self):
            pass


        def setValues(self, idx):
            debug("index: %d", idx)
            self.clear()
            for i, entry in enumerate(self.entries):
                entry.insert(0, self.rows[idx][i])

        def clear(self):
            for entry in self.entries:
                entry.delete(0, tk.END)

