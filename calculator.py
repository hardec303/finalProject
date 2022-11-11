import time
from tkinter import *
import sqlite3
from tkinter import ttk, messagebox
import tkinter as tk
import os  # os is a module that allows us to interact with the operating system
import pyglet  # pyglet is a module that allows us to use different fonts in python
from PIL import Image, ImageTk
from tkfontawesome import icon_to_image

try:
    import main
except:
    pass

dir_path = os.path.dirname(os.path.realpath(__file__))  # dir_path is the path of the current directory
pyglet.font.add_file(
    os.path.join(dir_path, 'files', 'pacifico-font', 'pacifico-v17-latin-regular.ttf'))  # add font to pyglet
pyglet.font.add_file(
    os.path.join(dir_path, 'files', 'merriweather-font', 'merriweather-v28-latin-regular.ttf'))  # add font to pyglet

con = sqlite3.connect('crm.db')
cur = con.cursor()

global i, n, Monthly_payment


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text='widget info', h_side="right", v_side="bottom", padx=10, pady=30, underline=False):
        self.waittime = 300  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.underline = underline
        self.h_side = h_side
        self.v_side = v_side
        self.padx = padx
        self.pady = pady
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        if self.underline:
            # self.widget.config(underline=True)
            f = font.Font(self.widget, self.widget.cget("font"))
            f.configure(underline=True)
            self.widget.configure(font=f)
        self.schedule()

    def leave(self, event=None):
        if self.underline:
            # self.widget.config(underline=True)
            f = font.Font(self.widget, self.widget.cget("font"))
            f.configure(underline=False)
            self.widget.configure(font=f)
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        if self.h_side == "right":
            x += self.widget.winfo_rootx() + self.padx
        elif self.h_side == "left":
            x += self.widget.winfo_rootx() - self.padx
        if self.v_side == "top":
            y += self.widget.winfo_rooty() - self.pady
        elif self.v_side == "bottom":
            y += self.widget.winfo_rooty() + self.pady

        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='center', anchor="center", font=("Merriweather", 9),
                      background="white", bg="white", activebackground="#ffffff", relief='solid', borderwidth=1,
                      wraplength=self.wraplength)
        label.pack(ipadx=4, anchor=tk.CENTER)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class ScrolledWindow(Frame):

    def __init__(self, parent, canv_w=400, canv_h=400, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # creating a scrollbars
        self.yscrlbr = ttk.Scrollbar(self.parent, orient='vertical')
        self.yscrlbr.pack(side="right", fill="y")
        # creating a canvas
        self.canv = tk.Canvas(self.parent, yscrollincrement=8.5, width=660, relief='flat')
        # placing a canvas into frame
        self.canv.pack(fill=BOTH, expand=True)
        # associating scrollbar commands to canvas scrolling
        self.yscrlbr.config(command=self.canv.yview)

        # creating a frame to insert to canvas
        self.scrollwindow = ttk.Frame(self.parent)

        self.canv.create_window(0, 0, window=self.scrollwindow, anchor='nw', width=660)

        self.canv.config(yscrollcommand=self.yscrlbr.set,
                         scrollregion=(0, 0, 100, 100))

        self.yscrlbr.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        self.canv.config(scrollregion='0 0 %s %s' % size)
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.config(width=self.scrollwindow.winfo_reqwidth())
        if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.config(height=self.scrollwindow.winfo_reqheight())

    def jump_to_widget_top(self, widget):
        if self.scrollwindow.winfo_height() > self.canv.winfo_height():
            pos = widget.winfo_rooty() - self.scrollwindow.winfo_rooty()
            height = self.scrollwindow.winfo_height()
            if widget.winfo_rooty() < self.canv.winfo_height():
                _70_percent = height * 0.7
                _90_percent = height * 0.9
                _95_percent = height * 0.95
                i = 1
                while i < height:
                    try:
                        self.canv.yview_moveto(pos / round(i))
                    except:
                        pass

                    if height - i < 10:
                        i += height - i
                    else:
                        i += 10
                    if i + 70 < height and i > _70_percent:
                        i += 70
                    if i + 90 < height and i > _90_percent:
                        i += 90
                    if i + 120 < height and i > _95_percent:
                        i += 120
                    try:
                        self.canv.update()
                    except:
                        pass
                    time.sleep(0.000001)
            else:
                r = widget.winfo_rooty() - self.scrollwindow.winfo_height()
                i = ((self.scrollwindow.winfo_rooty() - r) / widget.winfo_height()) / 10
                j = r / (self.scrollwindow.winfo_rooty() * 2)
                _70_percent = j * 0.7
                _90_percent = j * 0.9
                _95_percent = j * 0.95
                while i < j:
                    try:
                        self.canv.yview_moveto(i)
                    except:
                        pass
                    if i > _70_percent:
                        i += 0.001
                    elif i > _90_percent:
                        i += 0.0004
                    else:
                        i += 0.04
                    try:
                        self.canv.update()
                    except:
                        pass
                    time.sleep(0.00005)


class calc(Toplevel):
    def __init__(self):

        Toplevel.__init__(self)
        self.style = ttk.Style()
        self.window = self
        self.home_price = StringVar()
        self.down_payment = StringVar()
        self.amortization = StringVar()
        self.interest_rate = StringVar()
        self.payment_frequency = StringVar()
        self.additional_payment = StringVar()
        self.annual_household_income = StringVar()
        self.down_payment2 = StringVar()
        self.loans_other_debits = StringVar()
        self.credit_cards = StringVar()
        self.monthly_condo_fees = StringVar()
        self.taxable_income = StringVar()
        self.title("CRM System")
        self.geometry("700x550")
        self.resizable(False, False)
        # self.update()
        self.iconbitmap(os.path.join(dir_path, 'files', 'calculator.ico'))
        x_cordinate = int((self.winfo_screenwidth() / 2) - (self.winfo_width() / 2))
        y_cordinate = int((self.winfo_screenheight() / 2) - (self.winfo_height() / 2))
        self.geometry("+{}+{}".format(x_cordinate, y_cordinate))

        # self._root_frame = Frame(self, bg="white")
        # self._root_frame.pack(fill=BOTH, expand=True)

        self.notebook = ttk.Notebook(self, style="new.TNotebook")
        self.style.configure("new.TNotebook", background="white")
        self.tab_1 = Frame(self.notebook, background="white", width=700)
        self.tab_2 = Frame(self.notebook, background="white")
        self.tab_3 = Frame(self.notebook, background="white")

        self.notebook.add(self.tab_1, text="Mortgage Payment Calculator")
        self.notebook.add(self.tab_2, text="Mortgage Affordability Calculator")
        self.notebook.add(self.tab_3, text="Personal Tax Calculator")
        self.notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # ============================ Tab 2 (Mortgage Payment Calculator) ========================

        self.Tab1_sw = ScrolledWindow(self.tab_1)
        self.Tab1_sw.pack(fill=BOTH, expand=True)
        self.Tab1_scrollable = self.Tab1_sw.scrollwindow

        self.top_frame = Frame(self.Tab1_scrollable, bg="white", width=700)
        self.top_frame.pack(fill=X, expand=True, anchor=CENTER)

        self.Heading_text = Label(self.top_frame, text="Monthly Payment", font=("Merriweather", 17, "bold"), bg="white",
                                  fg="black")
        self.Heading_text.pack(pady=(5, 10))

        self.Amount_text = Label(self.top_frame, text="$ 0", font=("Merriweather", 16), bg="#1a894b", fg="white")
        self.Amount_text.pack(expand=True, fill=X, pady=(0, 10), ipady=12, padx=(0, 0))

        back_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(dir_path, 'files', "back.png")))
        self.Back_btn = Button(self.top_frame, image=back_btn_img, bd=0, highlightthickness=0, height=36, width=36,
                               relief=FLAT, background="#ffffff", bg="#ffffff", activebackground="#ffffff",
                               command=self.destroy, cursor="hand2")
        self.Back_btn.image = back_btn_img
        self.Back_btn.place(x=5, y=5)
        CreateToolTip(self.Back_btn, text="Go Back To Main Menu", h_side="right", v_side="bottom", padx=-8, pady=42)

        # self.hidden = Label(self.top_frame, text="", font=("Merriweather", 0), bg="white", fg="black")
        # self.hidden.pack(padx=0,expand=True)

        self.bottom_frame = Frame(self.Tab1_scrollable, bg="white")
        self.bottom_frame.pack(fill=BOTH, expand=True)

        self.total_cost_Label = Label(self.bottom_frame, text="Total Cost of Loan", font=("Arial", 12), bg="white",
                                      fg="black")
        self.total_cost_Label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.bottom_frame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=0, column=1)
        self.total_cost_Amount = Label(self.bottom_frame, text="$ 0", font=("Arial", 12), bg="white", fg="black")
        self.total_cost_Amount.grid(row=0, column=2, sticky="W")

        self.total_interest_Label = Label(self.bottom_frame, text="Total Interest Paid", font=("Arial", 13), bg="white",
                                          fg="black")
        self.total_interest_Label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.bottom_frame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=1, column=1)
        self.total_interest_Amount = Label(self.bottom_frame, text="$ 0", font=("Arial", 13), bg="white", fg="black")
        self.total_interest_Amount.grid(row=1, column=2, sticky="W")

        self.mortgage_insurance_Label = Label(self.bottom_frame, text="Mortgage Insurance", font=("Arial", 13),
                                              bg="white", fg="black")
        self.mortgage_insurance_Label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.bottom_frame, text=":", font=("Arial", 13, "bold"), bg="white", fg="black").grid(row=2, column=1)
        self.mortgage_insurance_Amount = Label(self.bottom_frame, text="N/A", font=("Arial", 13), bg="white",
                                               fg="black")
        self.mortgage_insurance_Amount.grid(row=2, column=2, sticky="W")

        self.home_price_Label = Label(self.bottom_frame, text="Home Price", font=("Arial", 14), bg="white", fg="black")
        self.home_price_Label.grid(row=3, column=0, padx=(10, 0), pady=(12, 3), sticky="W")

        self.check_decimal_num_reg = self.window.register(self._check_decimal_num)
        self.home_price_Input = ttk.Entry(self.bottom_frame, style="Home_price.TEntry", font=("Arial", 14),
                                          textvariable=self.home_price, validate="key",
                                          validatecommand=(self.check_decimal_num_reg, '%P'))
        # self.style.configure("Home_price.TEntry", foreground="black", background="#8c66ff", selectbackground="#007fff", selectforeground="white")
        self.home_price_Input.grid(row=4, column=0, columnspan=1, padx=(10, 0))

        self.down_payment_Label = Label(self.bottom_frame, text="Down Payment ($)", font=("Arial", 14), bg="white",
                                        fg="black")
        self.down_payment_Label.grid(row=5, column=0, padx=(10, 0), pady=(12, 3), sticky="W")

        self.down_payment_Input = ttk.Entry(self.bottom_frame, style="Down_payment.TEntry", font=("Arial", 14),
                                            textvariable=self.down_payment, validate="key",
                                            validatecommand=(self.check_decimal_num_reg, '%P'))
        # self.style.configure("Down_payment.TEntry", foreground="black", background="#8c66ff", selectbackground="#007fff", selectforeground="white")
        self.down_payment_Input.grid(row=6, column=0, columnspan=1, padx=(10, 0))

        self.amortization_Label = Label(self.bottom_frame, text="Amortization", font=("Arial", 14), bg="white",
                                        fg="black")
        self.amortization_Label.grid(row=7, column=0, padx=(10, 0), pady=(12, 3), sticky="W")

        amortization_option_list = ["", "Options...", "1 year", "2 years", "3 years", "4 years", "5 years", "7 years",
                                    "10 years", "15 years", "20 years", "25 years", "30 years"]
        self.amortization.set(amortization_option_list[1])
        self.amortization_option_menu = ttk.OptionMenu(self.bottom_frame, self.amortization,
                                                       style="Amortization.TMenubutton", *amortization_option_list)
        self.style.configure("Amortization.TMenubutton", foreground="black", background="#8c66ff",
                             selectbackground="#007fff", selectforeground="white", font=("Merriweather", 11), width=20)
        self.amortization_option_menu.grid(row=8, column=0, columnspan=1, padx=(10, 0), sticky="W")

        self.interest_rate_Label = Label(self.bottom_frame, text="Interest Rate (%)", font=("Arial", 14), bg="white",
                                         fg="black")
        self.interest_rate_Label.grid(row=9, column=0, padx=(10, 0), pady=(12, 3), sticky="W")

        self.interest_rate_Input = ttk.Entry(self.bottom_frame, style="Interest_rate.TEntry", font=("Arial", 14),
                                             textvariable=self.interest_rate, validate="key",
                                             validatecommand=(self.check_decimal_num_reg, '%P'))
        # self.style.configure("Interest_rate.TEntry", foreground="black", background="#8c66ff", selectbackground="#007fff", selectforeground="white")
        self.interest_rate_Input.grid(row=10, column=0, columnspan=1, padx=(10, 0))

        self.payment_frequency_Label = Label(self.bottom_frame, text="Payment Frequency", font=("Arial", 14),
                                             bg="white", fg="black")
        self.payment_frequency_Label.grid(row=11, column=0, padx=(10, 0), pady=(12, 3), sticky="W")

        payment_frequency_option_list = ["", "Options...", "Monthly", "Semi-Monthly", "Weekly"]
        self.payment_frequency.set(payment_frequency_option_list[1])
        self.payment_frequency_option_menu = ttk.OptionMenu(self.bottom_frame, self.payment_frequency,
                                                            style="Payment_Frequency.TMenubutton",
                                                            *payment_frequency_option_list)
        self.style.configure("Payment_Frequency.TMenubutton", foreground="black", background="#8c66ff",
                             selectbackground="#007fff", selectforeground="white", font=("Merriweather", 11), width=20)
        self.payment_frequency_option_menu.grid(row=12, column=0, columnspan=1, padx=(10, 0), sticky="W")

        self.Tab1_MiddleButtonFrame = Frame(self.Tab1_scrollable)
        self.Tab1_MiddleButtonFrame.pack(fill=BOTH, expand=True)

        self.PaymentCalculateButton = ttk.Button(self.Tab1_MiddleButtonFrame, text="Calculate",
                                                 style="Calculate.Accent.TButton", cursor="hand2",
                                                 command=self.PaymentCalculate)
        self.style.configure("Calculate.Accent.TButton", foreground="white", background="#8c66ff",
                             font=("Merriweather", 12))
        self.PaymentCalculateButton.pack(pady=30)

        # ============================ Tab 2 (Mortgage Affordability Calculator) ========================

        self.Tab2_sw = ScrolledWindow(self.tab_2)
        self.Tab2_sw.pack(fill=BOTH, expand=True)
        self.Tab2_scrollable = self.Tab2_sw.scrollwindow
        self.Tab2_sw.configure(border=0, borderwidth=0, background="white")

        self.Tab2_topFrame = Frame(self.Tab2_scrollable, bg="white")
        self.Tab2_topFrame.pack(fill=X, expand=True)
        self.Tab2_topFrame.columnconfigure(index=0, weight=1)
        self.Tab2_topFrame.columnconfigure(index=1, weight=1)

        self.Heading_text2 = Label(self.Tab2_topFrame, text="Mortgage Affordability Calculator",
                                   font=("Merriweather", 17, "bold"), bg="white", fg="black")
        self.Heading_text2.pack(pady=(5, 12))

        back_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(dir_path, 'files', "back.png")))
        self.Back_btn = Button(self.Tab2_topFrame, image=back_btn_img, bd=0, highlightthickness=0, height=36, width=36,
                               relief=FLAT, background="#ffffff", bg="#ffffff", activebackground="#ffffff",
                               command=self.destroy, cursor="hand2")
        self.Back_btn.image = back_btn_img
        self.Back_btn.place(x=5, y=5)
        CreateToolTip(self.Back_btn, text="Go Back To Main Menu", h_side="right", v_side="bottom", padx=-8, pady=42)

        self.Tab2_middleFrame = Frame(self.Tab2_scrollable, bg="white")
        self.Tab2_middleFrame.pack(fill=BOTH, expand=True)

        self.Tab2_middleFrame.columnconfigure(index=0, weight=1)
        self.Tab2_middleFrame.columnconfigure(index=1, weight=1)
        self.Tab2_middleFrame.columnconfigure(index=3, weight=1)
        self.Tab2_middleFrame.columnconfigure(index=4, weight=1)

        self.annual_household_income_Label = Label(self.Tab2_middleFrame, text="Total gross annual household income",
                                                   font=("Arial", 14), bg="white", fg="black")
        self.annual_household_income_Label.grid(row=0, column=0, padx=(10, 0), pady=(12, 3), sticky="W")

        # self.check_decimal_num_reg = self.window.register(self._check_decimal_num)
        self.annual_household_income_Input = ttk.Entry(self.Tab2_middleFrame, style="annual_household_income.TEntry",
                                                       font=("Arial", 14), textvariable=self.annual_household_income,
                                                       validate="key",
                                                       validatecommand=(self.check_decimal_num_reg, '%P'))
        self.annual_household_income_Input.grid(row=1, column=0, columnspan=2, padx=(10, 0), sticky="W")

        self.down_payment_Label2 = Label(self.Tab2_middleFrame, text="Down Payment ($)", font=("Arial", 14), bg="white",
                                         fg="black")
        self.down_payment_Label2.grid(row=2, column=0, columnspan=2, padx=(10, 0), pady=(12, 3), sticky="W")

        self.down_payment_Input2 = ttk.Entry(self.Tab2_middleFrame, style="Down_payment.TEntry", font=("Arial", 14),
                                             textvariable=self.down_payment2)
        self.down_payment_Input2.config(validate="key", validatecommand=(self.check_decimal_num_reg, '%P'))
        self.down_payment_Input2.grid(row=3, column=0, columnspan=2, padx=(10, 0), sticky="W")

        self.loans_Label = Label(self.Tab2_middleFrame, text="Loans & other debts (per month)", font=("Arial", 14),
                                 bg="white", fg="black")
        self.loans_Label.grid(row=4, column=0, padx=(10, 0), columnspan=2, pady=(12, 3), sticky="W")

        self.loans_other_debits_Input = ttk.Entry(self.Tab2_middleFrame, style="loans.TEntry", font=("Arial", 14),
                                                  textvariable=self.loans_other_debits, validate="key",
                                                  validatecommand=(self.check_decimal_num_reg, '%P'))
        self.loans_other_debits_Input.grid(row=5, column=0, columnspan=2, padx=(10, 0), sticky="W")

        self.credit_cards_Label = Label(self.Tab2_middleFrame, text="Credit cards & lines of credit (total owing)",
                                        font=("Arial", 14), bg="white", fg="black")
        self.credit_cards_Label.grid(row=6, column=0, columnspan=2, padx=(10, 0), pady=(12, 3), sticky="W")

        self.credit_cards_Input = ttk.Entry(self.Tab2_middleFrame, style="credit.TEntry", font=("Arial", 14),
                                            textvariable=self.credit_cards, validate="key",
                                            validatecommand=(self.check_decimal_num_reg, '%P'))
        self.credit_cards_Input.grid(row=7, column=0, columnspan=2, padx=(10, 0), sticky="W")

        self.monthly_condo_fees_Label = Label(self.Tab2_middleFrame, text="Monthly condo fees (if applicable)",
                                              font=("Arial", 14), bg="white", fg="black")
        self.monthly_condo_fees_Label.grid(row=8, column=0, columnspan=2, padx=(10, 0), pady=(12, 3), sticky="W")

        self.monthly_condo_fees_Input = ttk.Entry(self.Tab2_middleFrame, style="monthly_condo.TEntry",
                                                  font=("Arial", 14), textvariable=self.monthly_condo_fees,
                                                  validate="key", validatecommand=(self.check_decimal_num_reg, '%P'))
        self.monthly_condo_fees_Input.grid(row=9, column=0, columnspan=2, padx=(10, 0), pady=(0, 30), sticky="W")

        self.Tab2_MiddleButtonFrame = Frame(self.Tab2_scrollable)
        self.Tab2_MiddleButtonFrame.pack(fill=BOTH, expand=True)

        self.AffordabilityCalculateButton = ttk.Button(self.Tab2_MiddleButtonFrame, text="Calculate",
                                                       style="Calculate.Accent.TButton", cursor="hand2",
                                                       command=self.AffordabilityCalculate)
        self.style.configure("Calculate.Accent.TButton", font=("Merriweather", 12))
        self.AffordabilityCalculateButton.pack(pady=(0, 30))

        self.Tab2_bottomFrame = ttk.LabelFrame(self.Tab2_scrollable, style="estimate_result.TLabelframe",
                                               text="Your affordability estimate")
        self.style.configure("estimate_result.TLabelframe.Label", font=("Arial", 14), fg="black")
        # self.style.configure("estimate_result.TLabelframe", bg="#e9f2eb")
        self.Tab2_bottomFrame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.Tab2_bottomFrame.columnconfigure(index=0, weight=1)
        self.Tab2_bottomFrame.columnconfigure(index=1, weight=1)
        self.Tab2_bottomFrame.columnconfigure(index=3, weight=1)
        self.Tab2_bottomFrame.columnconfigure(index=4, weight=1)

        self.home_img = icon_to_image("home", fill="#1a894b", scale_to_width=52)
        self.home_icon_Label = tk.Label(self.Tab2_bottomFrame, image=self.home_img, anchor=CENTER)
        self.home_icon_Label.image = self.home_img
        self.home_icon_Label.grid(row=1, column=0, columnspan=2, padx=0, pady=(14, 3), sticky="nesw")
        self.maximum_purchase_price_Label = Label(self.Tab2_bottomFrame, text="   Maximum purchase price   ",
                                                  font=("Merriweather", 12, "bold"), fg="black")
        self.maximum_purchase_price_Label.grid(row=2, column=0, columnspan=2, padx=0, pady=(3, 3), sticky="nesw")
        self.maximum_purchase_price_amount_Label = Label(self.Tab2_bottomFrame, text="$ 0", font=("Arial", 19),
                                                         fg="black")
        self.maximum_purchase_price_amount_Label.grid(row=3, column=0, columnspan=2, padx=0, pady=(3, 14),
                                                      sticky="nesw")

        self.separator = ttk.Separator(self.Tab2_bottomFrame, orient="vertical")
        self.separator.grid(row=1, column=2, rowspan=3, padx=0, pady=(3, 10), sticky="nesw")

        self.money_img = icon_to_image("money-check-alt", fill="#1a894b", scale_to_width=52)
        self.money_icon_Label = tk.Label(self.Tab2_bottomFrame, image=self.money_img, anchor=CENTER)
        self.money_icon_Label.image = self.money_img
        self.money_icon_Label.grid(row=1, column=3, columnspan=2, padx=0, pady=(14, 3), sticky="nesw")
        self.monthly_mortgage_payment_Label = Label(self.Tab2_bottomFrame, text="Monthly mortgage payment",
                                                    font=("Merriweather", 12, "bold"), fg="black")
        self.monthly_mortgage_payment_Label.grid(row=2, column=3, columnspan=2, padx=0, pady=(3, 3), sticky="nesw")
        self.monthly_mortgage_payment_amount_Label = Label(self.Tab2_bottomFrame, text="$ 0", font=("Arial", 19),
                                                           fg="black")
        self.monthly_mortgage_payment_amount_Label.grid(row=3, column=3, columnspan=2, padx=0, pady=(3, 14),
                                                        sticky="nesw")

        # ============================ Tab 3 (Personal Tax Calculator) ========================

        self.Tab3_sw = ScrolledWindow(self.tab_3)
        self.Tab3_sw.pack(fill=BOTH, expand=True)
        self.Tab3_scrollable = self.Tab3_sw.scrollwindow
        self.Tab3_sw.configure(border=0, borderwidth=0, background="white")

        self.Tab3_topFrame = Frame(self.Tab3_scrollable, bg="white")
        self.Tab3_topFrame.pack(fill=X, expand=True)

        self.Heading_text3 = Label(self.Tab3_topFrame, text="Personal Tax Calculator",
                                   font=("Merriweather", 17, "bold"), bg="white", fg="black")
        self.Heading_text3.pack(pady=(5, 4))

        back_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(dir_path, 'files', "back.png")))
        self.Back_btn = Button(self.Tab3_topFrame, image=back_btn_img, bd=0, highlightthickness=0, height=36, width=36,
                               relief=FLAT, background="#ffffff", bg="#ffffff", activebackground="#ffffff",
                               command=self.destroy, cursor="hand2")
        self.Back_btn.image = back_btn_img
        self.Back_btn.place(x=5, y=5)
        CreateToolTip(self.Back_btn, text="Go Back To Main Menu", h_side="right", v_side="bottom", padx=-8, pady=42)

        self.Tab3_middleFrame = Frame(self.Tab3_scrollable, bg="white")
        self.Tab3_middleFrame.pack(fill=BOTH, expand=True)

        self.taxable_income_Label = Label(self.Tab3_middleFrame, text="Taxable Income", font=("Arial", 14), bg="white",
                                          fg="black")
        self.taxable_income_Label.grid(row=1, column=0, padx=(10, 0), pady=(10, 3), sticky="W")

        # self.check_decimal_num_reg = self.window.register(self._check_decimal_num)
        self.taxable_income_Input = ttk.Entry(self.Tab3_middleFrame, style="taxable_income.TEntry", font=("Arial", 14),
                                              textvariable=self.taxable_income, validate="key",
                                              validatecommand=(self.check_decimal_num_reg, '%P'))
        self.taxable_income_Input.grid(row=2, column=0, columnspan=2, padx=(10, 0), sticky="W")

        self.Tab3_MiddleButtonFrame = Frame(self.Tab3_scrollable)
        self.Tab3_MiddleButtonFrame.pack(fill=BOTH, expand=True)

        self.TaxCalculateButton = ttk.Button(self.Tab3_MiddleButtonFrame, text="Calculate",
                                             style="TaxCalculate.Accent.TButton", cursor="hand2",
                                             command=self.TaxCalculate)
        self.style.configure("TaxCalculate.Accent.TButton", foreground="white", background="#8c66ff",
                             font=("Merriweather", 12))
        self.TaxCalculateButton.pack(pady=(30, 30))

        self.Tab3_bottomFrame = Frame(self.Tab3_scrollable)
        # self.style.configure("result.TLabelframe.Label", font=("Arial", 14))
        # self.style.configure("estimate_result.TLabelframe", bg="#e9f2eb")
        self.Tab3_bottomFrame.pack(fill=BOTH, expand=True)

        self.tax_payable_Label = Label(self.Tab3_bottomFrame, text="Tax Payable", font=("Arial", 12), bg="white",
                                       fg="black")
        self.tax_payable_Label.grid(row=0, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.Tab3_bottomFrame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=0, column=1,
                                                                                                        padx=5)
        self.tax_payable_Amount = Label(self.Tab3_bottomFrame, text="$ 0", font=("Arial", 12), bg="white", fg="black")
        self.tax_payable_Amount.grid(row=0, column=2, sticky="W")

        self.after_tax_income_Label = Label(self.Tab3_bottomFrame, text="After-Tax Income", font=("Arial", 12),
                                            bg="white", fg="black")
        self.after_tax_income_Label.grid(row=1, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.Tab3_bottomFrame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=1, column=1,
                                                                                                        padx=5)
        self.after_tax_income_Amount = Label(self.Tab3_bottomFrame, text="$ 0", font=("Arial", 12), bg="white",
                                             fg="black")
        self.after_tax_income_Amount.grid(row=1, column=2, sticky="W")

        self.average_tax_rate_Label = Label(self.Tab3_bottomFrame, text="Average Tax Rate", font=("Arial", 12),
                                            bg="white", fg="black")
        self.average_tax_rate_Label.grid(row=2, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.Tab3_bottomFrame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=2, column=1,
                                                                                                        padx=5)
        self.average_tax_rate_percent = Label(self.Tab3_bottomFrame, text="0.00 %", font=("Arial", 12), bg="white",
                                              fg="black")
        self.average_tax_rate_percent.grid(row=2, column=2, sticky="W")

        self.marginal_tax_rate_Label = Label(self.Tab3_bottomFrame, text="Marginal Tax Rate", font=("Arial", 12),
                                             bg="white", fg="black")
        self.marginal_tax_rate_Label.grid(row=3, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.Tab3_bottomFrame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=3, column=1,
                                                                                                        padx=5)
        self.marginal_tax_rate_percent = Label(self.Tab3_bottomFrame, text="0.00 %", font=("Arial", 12), bg="white",
                                               fg="black")
        self.marginal_tax_rate_percent.grid(row=3, column=2, sticky="W")

        self.marginal_rate_capital_Label = Label(self.Tab3_bottomFrame, text="Marginal Rate on Capital Gains",
                                                 font=("Arial", 12), bg="white", fg="black")
        self.marginal_rate_capital_Label.grid(row=4, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.Tab3_bottomFrame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=4, column=1,
                                                                                                        padx=5)
        self.marginal_rate_capital_percent = Label(self.Tab3_bottomFrame, text="0.00 %", font=("Arial", 12), bg="white",
                                                   fg="black")
        self.marginal_rate_capital_percent.grid(row=4, column=2, sticky="W")

        self.marginal_rate_eligible_dividends_Label = Label(self.Tab3_bottomFrame,
                                                            text="Marginal Rate on Eligible Dividends",
                                                            font=("Arial", 12), bg="white", fg="black")
        self.marginal_rate_eligible_dividends_Label.grid(row=5, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.Tab3_bottomFrame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=5, column=1,
                                                                                                        padx=5)
        self.marginal_rate_eligible_dividends_percent = Label(self.Tab3_bottomFrame, text="0.00 %", font=("Arial", 12),
                                                              bg="white", fg="black")
        self.marginal_rate_eligible_dividends_percent.grid(row=5, column=2, sticky="W")

        self.marginal_rate_ineligible_dividends_Label = Label(self.Tab3_bottomFrame,
                                                              text="Marginal Rate on Ineligible Dividends",
                                                              font=("Arial", 12), bg="white", fg="black")
        self.marginal_rate_ineligible_dividends_Label.grid(row=6, column=0, padx=(10, 0), pady=5, sticky="W")
        Label(self.Tab3_bottomFrame, text=":", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=6, column=1,
                                                                                                        padx=5)
        self.marginal_rate_ineligible_dividends_percent = Label(self.Tab3_bottomFrame, text="0.00 %",
                                                                font=("Arial", 12), bg="white", fg="black")
        self.marginal_rate_ineligible_dividends_percent.grid(row=6, column=2, sticky="W")

    def PaymentCalculate(self):
        if self.home_price.get() == "" or self.down_payment.get() == "" or self.amortization.get() == "Options..." or self.interest_rate.get() == "" or self.payment_frequency.get() == "Options...":
            messagebox.showerror("Error !!!", "     All fields are required...\n     Please check and try again...",
                                 parent=self)
        else:
            home_price = float(self.home_price.get())
            down_payment = float(self.down_payment.get())
            amortization = float(self.amortization.get().split(" ")[0])
            interest_rate = float(self.interest_rate.get())
            payment_frequency = self.payment_frequency.get()

            pv = home_price - down_payment

            if payment_frequency == 'Monthly':
                i = (interest_rate / 100) / 12
                n = amortization * 12
                self.Heading_text.configure(text='Monthly Payment')
            elif payment_frequency == 'Semi-Monthly':
                i = (interest_rate / 100) / 24
                n = amortization * 24
                self.Heading_text.configure(text='Semi-Monthly Payment')
            elif payment_frequency == 'Weekly':
                i = (interest_rate / 100) / 52
                n = amortization * 52
                self.Heading_text.configure(text='Weekly Payment')
            else:
                pass
            k = round((1 + i) ** n, 2)
            Monthly_Payment = round((pv * i * k / (k - 1)) // 1)
            total_cost_of_loan = Monthly_Payment * n
            total_interest_paid = total_cost_of_loan - pv

            self.total_cost_Amount.configure(text='$ ' + "{:,}".format(total_cost_of_loan))
            self.total_interest_Amount.configure(text='$ ' + "{:,}".format(total_interest_paid))
            self.Amount_text.configure(text='$ ' + "{:,}".format(Monthly_Payment))
            self.Tab1_sw.jump_to_widget_top(self.Heading_text)

        return Monthly_Payment

    def AffordabilityCalculate(self):
        if self.annual_household_income.get() == "" or self.down_payment2.get() == "" or self.loans_other_debits.get() == "" or self.credit_cards.get() == "":
            messagebox.showerror("Error !!!", "     All fields are required...\n     Please check and try again...",
                                 parent=self)
        else:
            annual_household_income = float(self.annual_household_income.get())
            down_payment2 = float(self.down_payment2.get())
            loans_other_debits = float(self.loans_other_debits.get())
            credit_cards = float(self.credit_cards.get())
            monthly_condo_fees = float(self.monthly_condo_fees.get()) if self.monthly_condo_fees.get() != "" else 0

            total_debits = loans_other_debits + credit_cards + monthly_condo_fees
            monthly_income = annual_household_income / 12
            if (total_debits + 500) >= (monthly_income * 0.44):
                messagebox.showwarning("Message ",
                                       "Sorry, you will not be able to afford the \nmortgage due to high debts...",
                                       parent=self)
            else:
                pmt = (monthly_income * 0.44) - total_debits - 500
                i = round(0.0525 / 12, 6)
                n = 12 * 30
                k = round((1 + i) ** n, 2)
                k_minus_1 = round((k - 1), 2)
                pmt_into_k_minus_1 = round(pmt * k_minus_1, 1)
                i_into_k = round((i * k), 3)
                pv = pmt_into_k_minus_1 / i_into_k
                affordable_home_price = pv + down_payment2

                self.monthly_mortgage_payment_amount_Label.configure(text='$' + "{:,}".format(round(pmt, 2)))
                self.maximum_purchase_price_amount_Label.configure(
                    text='$' + "{:,}".format(round(affordable_home_price, 2)))
                self.Tab2_sw.jump_to_widget_top(self.monthly_mortgage_payment_amount_Label)

        return pmt, int(pv), int(affordable_home_price)


    def TaxCalculate(self):
        if self.taxable_income.get() == "":
            messagebox.showerror("Error!", "     Enter taxable income.",
                                 parent=self)
        else:
            taxable_income = float(self.taxable_income.get())
            federal_tax = self._calculate_federal_tax(taxable_income)
            provincial_tax = self._calculate_provincial_tax(taxable_income)
            marginal_tax_rate, marginal_rate_eligible_dividends, marginal_rate_ineligible_dividends, marginal_rate_capital_gain = self._get_percentages(
                taxable_income)

            if taxable_income <= 34929:
                tax_credits = 481 - ((taxable_income - 21418) * 0.0356)
                tax_payable = (federal_tax + provincial_tax) - tax_credits
            else:
                tax_payable = federal_tax + provincial_tax
            after_tax_income = taxable_income - tax_payable
            average_tax_rate = (tax_payable / taxable_income) * 100

            self.tax_payable_Amount.configure(text='$ ' + "{:,}".format(round(tax_payable, 2)))
            self.after_tax_income_Amount.configure(text='$ ' + "{:,}".format(round(after_tax_income, 2)))
            self.average_tax_rate_percent.configure(text=str(round(average_tax_rate, 2)) + ' %')

            self.marginal_tax_rate_percent.configure(text=str(marginal_tax_rate) + ' %')
            self.marginal_rate_capital_percent.configure(text=str(marginal_rate_capital_gain) + ' %')
            self.marginal_rate_eligible_dividends_percent.configure(text=str(marginal_rate_eligible_dividends) + ' %')
            self.marginal_rate_ineligible_dividends_percent.configure(
                text=str(marginal_rate_ineligible_dividends) + ' %')

            return round(tax_payable, 2)

    def _calculate_federal_tax(self, taxable_income):
        federal_tax = 0
        if taxable_income <= 14398:
            federal_tax = 0
        elif 14399 <= taxable_income <= 50197:
            taxable_income -= 14399
            federal_tax = taxable_income * 0.15
        elif 50198 <= taxable_income <= 100392:
            taxable_income -= 50198
            federal_tax = (taxable_income * 0.205) + ((50197 - 14399) * 0.15)
        elif 100393 <= taxable_income <= 155625:
            taxable_income -= 100393
            federal_tax = (taxable_income * 0.26) + ((50197 - 14399) * 0.15) + ((100392 - 50198) * 0.205)
        elif 155626 <= taxable_income <= 221708:
            taxable_income -= 155626
            federal_tax = (taxable_income * 0.29) + ((50197 - 14399) * 0.15) + ((100392 - 50198) * 0.205) + (
                    (155625 - 100393) * 0.26)
        elif taxable_income >= 221709:
            taxable_income -= 221709
            federal_tax = (taxable_income * 0.33) + ((50197 - 14399) * 0.15) + ((100392 - 50198) * 0.205) + (
                    (155625 - 100393) * 0.26) + ((221708 - 155626) * 0.29)
        return federal_tax

    def _calculate_provincial_tax(self, taxable_income):
        provincial_tax = 0
        if taxable_income <= 11302:
            provincial_tax = 0
        elif 11303 <= taxable_income <= 43070:
            taxable_income -= 11303
            provincial_tax = taxable_income * 0.0506
        elif 43071 <= taxable_income <= 86141:
            taxable_income -= 43071
            provincial_tax = (taxable_income * 0.077) + ((43070 - 11303) * 0.0506)
        elif 86142 <= taxable_income <= 98901:
            taxable_income -= 86142
            provincial_tax = (taxable_income * 0.105) + ((43070 - 11303) * 0.0506) + ((86141 - 43071) * 0.077)
        elif 98902 <= taxable_income <= 120094:
            taxable_income -= 98902
            provincial_tax = (taxable_income * 0.1229) + ((43070 - 11303) * 0.0506) + ((86141 - 43071) * 0.077) + (
                    (98901 - 86142) * 0.105)
        elif 120095 <= taxable_income <= 162832:
            taxable_income -= 120095
            provincial_tax = (taxable_income * 0.147) + ((43070 - 11303) * 0.0506) + ((86141 - 43071) * 0.077) + (
                    (98901 - 86142) * 0.105) + ((120094 - 98902) * 0.1229)
        elif 162833 <= taxable_income <= 227091:
            taxable_income -= 162833
            provincial_tax = (taxable_income * 0.168) + ((43070 - 11303) * 0.0506) + ((86141 - 43071) * 0.077) + (
                    (98901 - 86142) * 0.105) + ((120094 - 98902) * 0.1229) + ((162832 - 120095) * 0.147)
        elif taxable_income >= 227092:
            taxable_income -= 227092
            provincial_tax = (taxable_income * 0.205) + ((43070 - 11303) * 0.0506) + ((86141 - 43071) * 0.077) + (
                    (98901 - 86142) * 0.105) + ((120094 - 98902) * 0.1229) + ((162832 - 120095) * 0.147) + (
                                     (227091 - 162833) * 0.168)
        return round(provincial_tax, 2)

    def _get_percentages(self, taxable_income):
        marginal_tax_rate = 0.00
        marginal_rate_capital_gain = 0.00
        marginal_rate_eligible_dividends = 0.00
        marginal_rate_ineligible_dividends = 0.00
        if taxable_income <= 14398:
            marginal_tax_rate = 0.00
            marginal_rate_capital_gain = 0.00
            marginal_rate_eligible_dividends = 0.00
            marginal_rate_ineligible_dividends = 0.00
        elif 14399 <= taxable_income <= 21006:
            marginal_tax_rate = 15.00
            marginal_rate_eligible_dividends = 0.00
            marginal_rate_ineligible_dividends = 6.87
            marginal_rate_capital_gain = 7.50
        elif 21007 <= taxable_income <= 21867:
            marginal_tax_rate = 20.06
            marginal_rate_eligible_dividends = 0.00
            marginal_rate_ineligible_dividends = 10.43
            marginal_rate_capital_gain = 10.03
        elif 21868 <= taxable_income <= 35659:
            marginal_tax_rate = 23.62
            marginal_rate_eligible_dividends = 0.00
            marginal_rate_ineligible_dividends = 14.53
            marginal_rate_capital_gain = 11.81
        elif 35660 <= taxable_income <= 43070:
            marginal_tax_rate = 20.06
            marginal_rate_eligible_dividends = 0.00
            marginal_rate_ineligible_dividends = 10.43
            marginal_rate_capital_gain = 10.03
        elif 43071 <= taxable_income <= 50197:
            marginal_tax_rate = 22.70
            marginal_rate_eligible_dividends = 0.00
            marginal_rate_ineligible_dividends = 13.47
            marginal_rate_capital_gain = 11.35
        elif 50198 <= taxable_income <= 86141:
            marginal_tax_rate = 28.20
            marginal_rate_eligible_dividends = 7.56
            marginal_rate_ineligible_dividends = 19.80
            marginal_rate_capital_gain = 14.10
        elif 86142 <= taxable_income <= 98901:
            marginal_tax_rate = 31.00
            marginal_rate_eligible_dividends = 7.56
            marginal_rate_ineligible_dividends = 23.02
            marginal_rate_capital_gain = 15.50
        elif 98902 <= taxable_income <= 100392:
            marginal_tax_rate = 32.79
            marginal_rate_eligible_dividends = 7.96
            marginal_rate_ineligible_dividends = 25.07
            marginal_rate_capital_gain = 16.40
        elif 100393 <= taxable_income <= 120094:
            marginal_tax_rate = 38.29
            marginal_rate_eligible_dividends = 15.55
            marginal_rate_ineligible_dividends = 31.40
            marginal_rate_capital_gain = 19.15
        elif 120095 <= taxable_income <= 155625:
            marginal_tax_rate = 40.70
            marginal_rate_eligible_dividends = 18.88
            marginal_rate_ineligible_dividends = 34.17
            marginal_rate_capital_gain = 20.35
        elif 155626 <= taxable_income <= 162832:
            marginal_tax_rate = 44.08
            marginal_rate_eligible_dividends = 23.54
            marginal_rate_ineligible_dividends = 38.06
            marginal_rate_capital_gain = 22.04
        elif 162833 <= taxable_income <= 221708:
            marginal_tax_rate = 46.18
            marginal_rate_eligible_dividends = 26.44
            marginal_rate_ineligible_dividends = 40.47
            marginal_rate_capital_gain = 23.09
        elif 221709 <= taxable_income <= 227091:
            marginal_tax_rate = 49.80
            marginal_rate_eligible_dividends = 31.44
            marginal_rate_ineligible_dividends = 44.64
            marginal_rate_capital_gain = 24.90
        elif taxable_income >= 227092:
            marginal_tax_rate = 53.50
            marginal_rate_eligible_dividends = 36.54
            marginal_rate_ineligible_dividends = 48.89
            marginal_rate_capital_gain = 26.75
        return marginal_tax_rate, marginal_rate_eligible_dividends, marginal_rate_ineligible_dividends, marginal_rate_capital_gain

    def _check_decimal_num(self, input):
        if len(input) > 0:
            if input[-1] == " ":
                return False
        try:
            if input.strip() != "":
                input = input.strip()
                input = float(input)
                integer, decimal = str(input).split(".")
                if len(decimal) > 2: return False
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    try:
        main.main()
    except:
        pass
