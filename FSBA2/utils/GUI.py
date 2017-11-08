#!/usr/bin/env python3
from .__import import *

class GUIMode(Enum):
    normal = 0
    login = 1

class GUI(tk.Frame):
    """GUI
    Wrapper of Tkinter
    """

    def __init__(self, title = "GUI", mode = GUIMode.normal, parent=None, login = False):
        """__init__

        :param title: Window Title
        :type title: str

        :param mode: (GUIMode enum -> named option (in words) instead of manually typing integer into the field
        :type mode: GUIMode(Enum)

        :param login: condition whether this constructor should invoke a modal login dialog as child
        :type login: bool

        """
        
        info("initializing new GUI window")
        debug(debug_outer_stack_frame()) # debug: dump caller's info

        if login == True:
            # Prompt a MODAL login dialog
            # ** Recursive call ** to this class, construct a modal dialog, i.e. it does NOT show the main dialog before a successful login
            self.loginDialog = GUI("Login", GUIMode.login, self)
            # loginDialog will continue if and only if the login is sucessful, it should terminate the program before returning ...

        if parent:
            self.parent = parent

        # the "root" of Tkinter
        self.root = tk.Tk()
        # calling super-class constructor
        tk.Frame.__init__(self, self.root)
        # goto the customized initialization (common, for either mode: normal or login) method, just trying to make the code clean and easy to understand
        self.initialize(title)
        self.app_name = title

        if mode == GUIMode.login: # if "this should be a login dialog"
            self.loginModeSpecific_init()
        else:
            self.mainUI()

        self.moveToTop()
        # events starts to be handled after this following function call
        self.root.mainloop()

    def initialize(self, title):
        """GUI initialization"""
        self.root.title(title)

    def loginModeSpecific_init(self):
        """loginModeSpecific_init"""
        # override the "X" button to directly terminate the program in login mode
        self.root.protocol('WM_DELETE_WINDOW', self.terminate)
        # center the window
        self.centerWindow()

        # declaring lists, for convenience on looping
        fields = []
        self.login_txtVar = [tk.StringVar() for i in range(2)] # [self.usernamesvalue, self.passwordsvalue]
        login_lbls = ["Username", "Password"]

        for i in range(2):
            # Text display
            tk.Label(self.root, 
                     text=login_lbls[i]).grid(row=i*2, column=0,\
                          columnspan=1, sticky='w')

            # text field for user-input, appending the new field into list fields for easier reference
            fields.append(tk.Entry(self.root, \
                                   textvariable=self.login_txtVar[i],\
                                   show="*" if i else ""))
            fields[-1].grid(row=i*2+1, column=0, sticky='w')

        # declare two buttons
        for (txt, (f, sticky)) in {"Login": (self.checkLogin, 'w'), "Cancel": (self.terminate, 'e')}.items():
            tk.Button(self.root, 
                      text=txt, command=f)\
                    .grid(row=4, column=0, sticky=sticky)


    def checkLogin(self):
        """Check whether the combination of username and input is valid for login"""
        #user = self.usernamesvalue.get()
        #pw = self.passwordsvalue.get()
        vals = [x.get() for x in self.login_txtVar]
        info("user: %s, pass: %s" % tuple(vals))#( user, pw))
        rs = query("staff", "CONCAT(firstName, ' ', lastName)", "username = '%s' AND password = '%s'" % tuple(vals))
        #if all(x == "admin" for x in vals): #[user, pw]):
        debug(rs)
        if len(rs[2]) == 1: #[user, pw]):
            self.parent.displayed_username = rs[2][0][0]
            self.root.destroy()
        return

    def mainUI(self):
        """mainUI"""
        self.maximize()
        #self.logoBar = self.GradientCanvas(self.root, "white", "black")
        #self.logoBar.grid(
        #self.logoBar.pack()
        self.LogoBar(self.root, self.app_name, self.displayed_username)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew")
        tab_txts = ['Accounts', 'Products', 'Sales Order', 'Service Order']
        self.tabs = {}
        for tab_txt in tab_txts:
            self.tabs[tab_txt] = ttk.Frame(self.notebook)
            self.notebook.add(self.tabs[tab_txt], text=tab_txt)
        debug(self.tabs)
        self.notebook.pack(fill="both", expand=True)
        self.salesOrderUI()

    def salesOrderUI(self):
        tbl = ListView(self.tabs['Sales Order'])
        tbl.pack()

    def maximize(self):
        """maximize"""
        root = self.root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

    class LogoBar(tk.Frame):
        def __init__(self, root, app_name, displayed_username):
            root.update()
            width = root.winfo_width()
            self.width = width
            self.height = int(root.winfo_height() * 0.075)
            tk.Frame.__init__(self, root, height=self.height)
            canvas = self.GradientCanvas(self, (68,68,68), (32,32,32), self.height)
            tk.Label(canvas, text=app_name)
            #lbls = [tk.Label(canvas, text=s, fg="white", bg="green") for s in (app_name, displayed_username)]
            lbls = [tk.Label(canvas, text=s, fg="white", bg="systemTransparent", font=("Helvetica", 20)) for s in (app_name, displayed_username)]
            xpos = [self.width * ratio for ratio in [0.02, 0.85]]
            for lbl, x in zip(lbls, xpos):
                lbl.place(x=x, y=(self.height - 26) // 2)
                
#            root.wm_attributes('-transparentcolor', "green")
            self.pack(fill=tk.X)


        class GradientCanvas(tk.Canvas):
            """GradientCanvas"""
            def __init__(self, root, color1, color2, height, bd=0, relief="sunken"):
                """__init__

                :param root: parent of this object
                :type root: tkinter container / Tk()

                :param color1: first color
                :type color1: str / 3-tuple containing rgb value

                :param color2: second color
                :type color2: str / 3-tuple containing rgb value

                :param borderwidth: (inherited) 
                :type borderwidth: int

                :param relief: (inherited)
                :type relief: str

                """
                tk.Canvas.__init__(self, root, bd=bd, relief=relief, height=height, highlightthickness=0)

                self.root = root
                self.color1 = color1
                self.color2 = color2
                self.colors = [color1, color2]
                self.height = height
                self.bind("<Configure>", self.draw_gradient)
                #self.grid(row=0, column=0, sticky="nsew")
                #self.pack(fill="both", expand=True)
                self.pack(fill=tk.X)#, expand=True)

            def draw_gradient(self, event=None):
                """draw_gradient

                :param event: (inherited)
                :type event: event

                """
                self.delete("gradient")
                width = self.winfo_width()
                height = self.height #self.winfo_height()
                limit = height
                #(r1,g1,b1) = self.winfo_rgb(self.color1)
                #(r2,g2,b2) = self.winfo_rgb(self.color2)
                #TODO colors = list(map(self.winfo_rgb, self.colors))
                colors = self.colors
                ratios = list(map(lambda comp: float(comp[1] - comp[0])/limit, zip(*colors)))
                
                for i in range(limit):
                    ncolors = list(map(lambda tup: int(tup[0] + (tup[1] * i)), zip(colors[0], ratios)))
                    color = "#%4.4x%4.4x%4.4x" % tuple(ncolors)
                    self.create_line(0, i, width, i, tags=("gradient",), fill=color)
                self.lower("gradient")
            

    def moveToTop(self):
        """moveToTop"""
        self.root.lift()
        self.root.attributes('-topmost', 1)
        self.root.after_idle(self.root.attributes,'-topmost',False)

    def centerWindow(self):
        """centerWindow"""
        root = self.root
        # Apparently a common hack to get the window size. Temporarily hide the
        # window to avoid update_idletasks() drawing the window in the wrong
        # position.
        root.withdraw()
        root.update_idletasks()  # Update "requested size" from geometry manager

        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        root.deiconify()

    def terminate(self):
        """terminate"""
        sys.exit()

