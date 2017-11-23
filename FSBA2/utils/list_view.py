from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import numbers
from collections import OrderedDict
from .debug import *
from .sorting import *
from .searching import *
from .odbc import *
from .table_utils import *

class ListView(Frame):
    """
    ListView

    Contain table-like widget and input fields that can query, insert, update and delete the table from database
    """

    def __init__(self, parent, width, height, padx, **kwargs):
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
        Frame.__init__(self, parent, width=width, height=height)
        self.root = parent # save the parent for accessing in whole class
        self.pack(expand=False, padx=padx) # display ListView
        width -= padx * 2
        self.tbl_args = kwargs

        filter_entry_frame = Frame(self)
        filter_entry_frame.pack(fill=X)#, expand=True)

        self.tbl = self.Table(self, width, height // 3, **kwargs)
        self.tbl.pack(fill=X)#, expand=True) # display the table on GUI
        self.filter_init(filter_entry_frame, self.tbl.update_filter)

        self.edit_pane = self.Fields(self, width, padx, **kwargs)
        
        self.tbl.set_click_cb(self.edit_pane.setValues)

        if kwargs['table'] == 'SalesOrder':
            debug("if kwargs['table'] == 'SalesOrder':")
            self.tbl2 = self.Table(self, width, height // 3, True, table="LineItem", columns="sequenceNumber, Product_id, price", condition="0")
            self.tbl2.pack(fill=X)
            self.edit_pane2 = self.Fields(self, width, padx, table="LineItem", columns="sequenceNumber, Product_id, price")
            #self.edit_pane2.pack()
            self.tbl2.set_click_cb(self.edit_pane2.setValues)
            self.tbl.set_click_cb(self.update_table_special)

    def update_table_special(self, idx):
        """
        event handler of sales order tab's table
        extends the original functionalities
        and add update on the table down there
        """
        self.edit_pane.setValues(idx)
        self.tbl2.special_set_idx(idx)

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
        filterInput_txt = StringVar()
        # set callback function when the content on the text field is edited (both adding characters at the end and backspace)
        filterInput_txt.trace("w", lambda *argv: self.handle_cb(callback, filterInput_txt))
        
        # init a text field with the text variable with callback
        e = Entry(frame, textvariable=filterInput_txt)
        # display the text field
        e.pack(side=RIGHT)

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


    class Table(Treeview):
        
        def __init__(self, parent, width, height, special=False, **kwargs):
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
            Treeview.__init__(self, parent)#, padding=(0,0,0,0))
            self.click_cb = None
            self.bind("<<TreeviewSelect>>", self.on_click)

            self.width = width
            self.special = special
            self.special_idx = -1

            self.pack()#fill="x", expand=True)
            self.root = parent

            self.kwargs = kwargs
            self.tmp()
            # self.cols, self.rows = queryData(**kwargs)
            # self.visibility = [True] * len(self.rows)

            # # ascending list, a sequence represents the key / index referencing self.rows
            # self.order = list(range(len(self.rows)))
            # self.config_columns()
            # self.init_rows()

        def tmp(self):
            """
            special table querying for sales order tab
            """
            if self.special and self.special_idx != -1:        
                if 'condition' in self.kwargs:
                    del self.kwargs['condition']
                result_set = queryData(condition="sales_id = '%d'" % self.special_idx, **self.kwargs)
            else:
                result_set = queryData(**self.kwargs)
            if result_set == ([], []):
                warning("result_set == ([], [])")
                return
            self.cols, self.rows = result_set

            self.visibility = [True] * len(self.rows)

            # ascending list, a sequence represents the key / index referencing self.rows
            self.order = list(range(len(self.rows)))
            self.config_columns()
            self.init_rows()

        def special_set_idx(self, idx):
            self.special_idx = self.root.tbl.rows[idx][0]
            self.refresh()


        def set_click_cb(self, f):
            assert(f is not None and callable(f))
            self.click_cb = f

        def getitem_idx(self):
            item = self.selection()
            if item == '':
                warning("this should not happen")
                return
            item_idx = self.order[int(self.index(item))]
            debug("item_idx: %d", item_idx)
            return item_idx

        def deleteRow(self):
            item_idx = self.getitem_idx()
            debug("delete item_idx: %d, %r", item_idx, self.rows[item_idx])
            row_id = self.rows[item_idx][0]

            result = askquestion("Delete", "Are You Sure?", icon='warning')
            if result == 'yes':
                debug("table: %r", self.kwargs['table'])
                errmsg = []
                rc = deleteData(self.kwargs['table'], condition="id = '%d'" % row_id, errmsg=errmsg)
                if errmsg != []:
                    showerror("ERROR", errmsg[0])
                else:
                    debug("deleted")
                self.refresh()
            else:
                debug("not deleted")

        def saveRecord(self, pair):
            item_idx = self.getitem_idx()
            row_id = self.rows[item_idx][0]
            debug("update: %s, col_and_val: %s, with id = %d", self.kwargs['table'], pair, row_id)
            errmsg = []
            updateData(self.kwargs['table'], pair, "id = '%d'" % row_id, errmsg)
            if errmsg != []:
                showerror("ERROR", errmsg[0])
            self.refresh()


        def on_click(self, event):
            item = self.selection()
            # nothing is selected
            if item == '':
                return

            item_idx = self.order[int(self.index(item))]
            debug("item_idx: %d, %r", item_idx, self.rows[item_idx])
            if self.click_cb is not None:
                assert callable(self.click_cb)
                debug("calling self.click_cb")
                self.click_cb(item_idx)
                pass

        def refresh(self):
            debug("refresh")
            self.delete(*self.get_children())
            self.tmp()

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
            self.column("#0", width = 0, stretch=False)
            for i, col in enumerate(self.cols):
                self.heading("#" + str(i), text=col, command=lambda col=i: self.sortTable(col))
                self.column("#" + str(i), minwidth=0, width=col_len[i], stretch=False)

        def init_rows(self):
            """init_rows"""
            self.rows_identifier = []
            for i, _row in enumerate(self.rows):
                zerothCol, *row = _row
                self.rows_identifier.append(self.insert('', 'end', iid=i+1, text=zerothCol, values=tuple(row))) # escape the #0
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
        
    class Fields(Frame):
        """Fields"""
        def __init__(self, parent, width, padx, **kwargs):
            """
            __init__


            Parameters
            ----------------
            parent : tkinter widget
                Parent widget of this widget
            result_set : 2-tuple of lists
                query result from database, with format (column_description[], column_names[], rows[][])
            """
            Frame.__init__(self, parent)
            self.pack(padx=padx)
            self.root = parent
            self.width = width - padx * 2
            debug("width: %d", width)

            result_set = queryData(**kwargs)

            if result_set == ([], []):
                warning("result_set == ([], [])")
                return
            self.tbl_handle = self.root.tbl
            self.kwargs = kwargs
            self.rs = result_set
            self.cols, self.rows = self.rs

            # for field modification
            self.mode = "new"
            self.modified_idx = []
            self.manual_mode = False
            
            btnFrame = Frame(self)
            btnFrame.pack(fill=X)#, expand=True)
            self.btns = OrderedDict()
            btn_names = ["New", "Save", "Confirm", "Delete", "Refresh"]
            btn_default_activate = [1,0,0,0,1]
            for i, btn_name in enumerate(btn_names):
                #                                                                 lazy
                self.btns[btn_name] = Button(btnFrame, text=btn_name, command=getattr(self, "cmd_" + btn_name))
                if btn_default_activate[i] == False:
                    self.btns[btn_name]['state'] = "disabled"
                self.btns[btn_name].pack(side=LEFT)
                pass

            entryFrame = Frame(self)
            entryFrame.pack(fill=X)#, expand=True)
            #self.entries = [Entry(self) for i in  range(len(self.cols))]
            self.labels = []
            self.entries = []
            self.entries_sv = []
            MAX_COL = 4
            for i, col_name in enumerate(self.cols):
                entryFrame.columnconfigure(i, weight=1, minsize=int(width / MAX_COL), pad=100)
                self.labels.append(Label(entryFrame, text=col_name, justify=LEFT, anchor=W))
                self.entries_sv.append(StringVar())
                self.entries_sv[-1].trace("w", lambda name, index, mode, sv=self.entries_sv[-1], entry_idx=i: self.modified(sv, entry_idx))
                self.entries.append(Entry(entryFrame, textvariable=self.entries_sv[-1]))
                self.labels[-1].grid(column=i % MAX_COL, row=3*(i // MAX_COL), sticky=W)
                self.entries[-1].grid(column=i % MAX_COL, row=3*(i // MAX_COL) + 1, sticky=W)

        def modified(self, sv, idx):
            if self.manual_mode == True:
                return 
            debug("modified")
            if idx not in self.modified_idx:
                self.modified_idx.append(idx)
            if self.mode == "edit":
                self.btns['Save']['state'] = 'normal'
            elif self.mode == "new":
                self.btns['Confirm']['state'] = 'normal'
            else:
                warning("unhandled self.mode: %r", self.mode)

        def cmd_New(self):
            debug("new clicked")
            self.clear()
            self.tbl_handle.selection_set('')
            self.btns['Save']['state'] = 'disabled'
            self.btns['Delete']['state'] = 'disabled'
            self.modified_idx = []
            self.mode = "new"

        def cmd_Save(self):
            debug("save clicked")
            columns, values = self.col_and_val()
            pair = ", ".join(["%s = '%s'" % (columns[i], values[i]) for i in range(len(columns))])
            debug(pair)
            self.tbl_handle.saveRecord(pair)


        def cmd_Confirm(self):
            debug("confirm clicked")
            col_list, val_list = self.col_and_val()
            columns = ", ".join(col_list)
            values = ", ".join(["'"+x+"'" for x in val_list])
            debug("columns: %r", columns)
            debug("values: %r", values)
            debug(self.kwargs['table'])
            rc = insertData(self.kwargs['table'], columns, values)
            debug("rc: %d", rc)
            self.tbl_handle.refresh()

        def col_and_val(self):
            """
            return the tuple of column and values modified by their column indices
            """
            columns = [self.cols[i] for i in self.modified_idx]
            debug(columns)
            values = [self.entries_sv[i].get() for i in self.modified_idx]
            debug(values)
            return (columns, values)

        def cmd_Delete(self):
            debug("delete clicked")
            self.tbl_handle.deleteRow()
            self.clear()


        def cmd_Refresh(self):
            debug("refresh clicked")
            self.tbl_handle.refresh()
            self.clear()


        def setValues(self, idx):
            """
            call back for the table to update the fields on selection
            """
            debug("index: %d", idx)
            self.btns['Delete']['state'] = 'normal'
            self.clear()
            self.manual_mode = True
            for i, entry in enumerate(self.entries):
                entry.insert(0, self.tbl_handle.rows[idx][i])
            self.mode = "edit"
            self.manual_mode = False

        def clear(self):
            self.manual_mode = True
            for entry in self.entries:
                entry.delete(0, END)
            self.manual_mode = False

