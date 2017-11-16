#!/usr/bin/env python3
from .__import import *
from .config_handler import *
from .report_output import *

class GUIMode(Enum):
    normal = 0
    login = 1

class GUI(tk.Frame):
    """GUI
    Wrapper of Tkinter
    """

    def __init__(self, title = "GUI", mode = GUIMode.normal, parent=None, login = False, tab_dict=None):
        """__init__

        title : str
            Window Title

        mode : GUIMode(Enum)
            Named option (nin words) instead of manually typing integer into the field

        parent : tkinter Widget
            Intended to use for passing the parent to login dialog

        login : bool 
            The condition whether this constructor should invoke a modal login dialog as child

        tab_dict : OrderedDict
            Ordered Dictionary from the config that stores each tab's layout
        """
        
        info("initializing new GUI window")
        debug(debug_outer_stack_frame()) # debug: dump caller's info

        self.displayed_username = '' 
        self.mode = GUIMode(mode)

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

        if mode == GUIMode.login: # if "this should be a login dialog"
            self.loginModeSpecific_init()
        else:
            self.tab_dict = tab_dict
            self.mainUI()

        self.moveToTop()
        # events starts to be handled after this following function call
        self.root.mainloop()

    def initialize(self, title):
        """GUI initialization"""
        self.root.title(title)
        self.app_name = title

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
        vals = [escapeSQLi(x.get()) for x in self.login_txtVar]
        info("user: %s, pass: %s" % tuple(vals))#( user, pw))
        rs = queryData("staff", "CONCAT(firstName, ' ', lastName)", "username = '%s' AND password = '%s'" % tuple(vals))
        #if all(x == "admin" for x in vals): #[user, pw]):
        debug(rs)
        if len(rs[1]) == 1: #[user, pw]):
            self.parent.displayed_username = rs[1][0][0]
            self.root.destroy()
        return

    def mainUI(self):
        """
        mainUI

        Helper function that handles the initialization of children widgets of the Main UI 
        """
        self.maximize()
        self.logobar = self.LogoBar(self.root, self.app_name, self.displayed_username)
        self.notebook = ttk.Notebook(self.root)#, padding=(0,0,0,0))

        # be careful this is to delay the pack() and DO NOT call any update before pack()
        # otherwise grid() and pack() will bargain with each other for optimal solution 
        # and the program will hang until they're done
        self.notebook.grid(row=1, column=0, sticky="nsew")

        self.tabs = {}

        frame_w = scalei(self.width, 0.9)
        debug("frame_w: %r", frame_w)
        for tab_name, tab_data in self.tab_dict.items():
            self.tabs[tab_name] = ttk.Frame(self.notebook, width=frame_w)
            self.tabs[tab_name].pack()
            self.notebook.add(self.tabs[tab_name], text=tab_name)#, sticky="nesw")
            if tab_data['table'] != "":
                ListView(self.tabs[tab_name], frame_w, self.height, 50, **tab_data).pack(expand=False)
            else:
                report_output(self.tabs[tab_name])
            
        debug("self.tabs: %r", self.tabs)
        self.notebook.pack(fill="both", expand=True)

    def maximize(self):
        """maximize window"""
        root = self.root
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        self.width, self.height = w, h
        root.geometry("%dx%d+0+0" % (w, h))

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.resizable(False, False)

    class LogoBar(tk.Frame):
        """
        The Gradient Bar on top
        """
        def __init__(self, root, app_name, displayed_username):
            """
            __init__


            Parameters
            ----------------
            root : tkinter widget
                Parent of this wiget

            app_name : str
                String to be displayed on the Left Hand Side of the Bar

            displayed_username : str
                Displayed name of logged in user
            """
            root.update()
            width = root.winfo_width()
            self.width = width
            self.height = int(root.winfo_height() * 0.075)
            tk.Frame.__init__(self, root, height=self.height)
            cfg_filename = os.path.dirname(os.path.abspath(__file__)) + '/../color_config.ini'
            info(cfg_filename)
            config = config_dict(cfg_filename)
            grad_name = 'purple_paradise'
            colors = list(hex2tuple(config[grad_name]['color%d' % (i + 1)]) for i in range(2))
            info(colors)
            canvas = self.GradientCanvas(self, *colors, self.height, horizontal=(config[grad_name]['mode'] == 'h'))
            #canvas = self.GradientCanvas(self, (0, 198, 251), (0,91,234), self.height, True)
            tk.Label(canvas, text=app_name)
            #lbls = [tk.Label(canvas, text=s, fg="white", bg="green") for s in (app_name, displayed_username)]
            lbls = [tk.Label(canvas, text=s, fg="white", bg="systemTransparent", font=("Helvetica", 20)) for s in (app_name, displayed_username)]
            xpos = [self.width * ratio for ratio in [0.02, 0.85]]
            for lbl, x in zip(lbls, xpos):
                lbl.place(x=x, y=(self.height - 26) // 2)
                
#            root.wm_attributes('-transparentcolor', "green")
            self.pack(fill=tk.X)


        class GradientCanvas(tk.Canvas):
            """
            GradientCanvas
            Extends tkinter.Canvas

            The Gradient background, supporting widget of LogoBar
            """
            def __init__(self, root, color1, color2, height, horizontal=False, bd=0, relief="sunken"):
                """__init__

                Parameters
                ----------
                root : tkinter container / Tk()
                    parent of this object

                color1 : 3-tuple containing rgb value
                    first color

                color2 : 3-tuple containing rgb value
                    second color

                bd : int 
                    (inherited) 

                relief: str
                    (inherited)

                """
                tk.Canvas.__init__(self, root, bd=bd, relief=relief, height=height, highlightthickness=0)

                self.root = root
                self.color1 = color1
                self.color2 = color2
                self.colors = [color1, color2]
                self.height = height
                self.horizontal = horizontal
                self.bind("<Configure>", self.draw_gradient)
                self.draw_gradient()
                #self.grid(row=0, column=0, sticky="nsew")
                #self.pack(fill="both", expand=True)
                self.pack(fill=tk.X)#, expand=True)

            def draw_gradient(self, event=None):
                """
                draw_gradient
                The actual function that helps generate the gradient line by line.

                event: event
                    (inherited)
                """
                self.delete("gradient")
                width = self.winfo_width()
                height = self.height

                if self.horizontal:
                    limit = height
                    colors = self.colors
                    ratios = list(map(lambda comp: float(comp[1] - comp[0])/limit, zip(*colors)))
                    
                    for i in range(limit):
                        ncolors = list(map(lambda tup: int(tup[0] + (tup[1] * i)), zip(colors[0], ratios)))
                        #debug("ncolors: %r" % ncolors)
                        #color = "#%4.4x%4.4x%4.4x" % tuple(ncolors)
                        color = "#%02x%02x%02x" % tuple(ncolors)
                        #debug("color: %r" % color)
                        self.create_line((0, i, width, i + 1), tags=("gradient",), fill=color)
                    self.lower("gradient")
                else:
                    limit = width
                    colors = self.colors
                    ratios = list(map(lambda comp: float(comp[1] - comp[0])/limit, zip(*colors)))
                    
                    for i in range(limit):
                        ncolors = list(map(lambda tup: int(tup[0] + (tup[1] * i)), zip(colors[0], ratios)))
                        #debug("ncolors: %r" % ncolors)
                        #color = "#%4.4x%4.4x%4.4x" % tuple(ncolors)
                        color = "#%02x%02x%02x" % tuple(ncolors)
                        #debug("color: %r" % color)
                        self.create_line((i, 0, i + 1, height), tags=("gradient",), fill=color)
                    self.lower("gradient")

            

    def moveToTop(self):
        """
        moveToTop

        Helper function that moves the GUI window to top of another applications
        """
        self.root.lift()
        self.root.attributes('-topmost', 1)
        self.root.after_idle(self.root.attributes,'-topmost',False)

    def centerWindow(self):
        """
        centerWindow

        Helper function that positions the window to the center.
        """
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
        """
        terminate

        Aliasing sys.exit() to terminate the whole program
        """
        sys.exit()

