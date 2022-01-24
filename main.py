import os
import datetime
import getpass
import ctypes
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from PIL import ImageTk, Image # pillow

# ievācam vides informāciju
working_dir = os.getcwd()

os.chdir(working_dir)
username = os.getlogin()
domain = os.environ['userdomain']
user = getpass.getuser()
#passwd = getpass.getpass()

progName = f"ExpoRemoteJobs: [ {domain}/{username} ][ {working_dir} ]"

# definējam bilžu atrašanās direktoriju
img_path = f"{working_dir}\\lib\\images"

# definējam programmas loga ikonas attēlošanu
myappid = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class CreateToolTip:
    '''
    It creates a tooltip for a given widget as the mouse goes on it.

    see:

    http://stackoverflow.com/questions/3221956/
           what-is-the-simplest-way-to-make-tooltips-
           in-tkinter/36221216#36221216

    http://www.daniweb.com/programming/software-development/
           code/484591/a-tooltip-class-for-tkinter

    - Originally written by vegaseat on 2014.09.09.

    - Modified to include a delay time by Victor Zaccardo on 2016.03.25.

    - Modified
        - to correct extreme right and extreme bottom behavior,
        - to stay inside the screen whenever the tooltip might go out on
          the top but still the screen is higher than the tooltip,
        - to use the more flexible mouse positioning,
        - to add customizable background color, padding, waittime and
          wraplength on creation
      by Alberto Vassena on 2016.11.05.

      Tested on Ubuntu 16.04/16.10, running Python 3.5.2

    TODO: themes styles support
    '''

    def __init__(self, widget,
                 *,
                 bg='#FFFFEA',
                 pad=(5, 3, 5, 3),
                 text='widget info',
                 waittime=400,
                 wraplength=250):

        self.waittime = waittime  # in miliseconds, originally 500
        self.wraplength = wraplength  # in pixels, originally 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.onEnter)
        self.widget.bind("<Leave>", self.onLeave)
        self.widget.bind("<ButtonPress>", self.onLeave)
        self.bg = bg
        self.pad = pad
        self.id = None
        self.tw = None

    def onEnter(self, event=None):
        self.schedule()

    def onLeave(self, event=None):
        self.unschedule()
        self.hide()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show)

    def unschedule(self):
        id_ = self.id
        self.id = None
        if id_:
            self.widget.after_cancel(id_)

    def show(self):
        def tip_pos_calculator(widget, label,
                               *,
                               tip_delta=(10, 5), pad=(5, 3, 5, 3)):

            w = widget

            s_width, s_height = w.winfo_screenwidth(), w.winfo_screenheight()

            width, height = (pad[0] + label.winfo_reqwidth() + pad[2],
                             pad[1] + label.winfo_reqheight() + pad[3])

            mouse_x, mouse_y = w.winfo_pointerxy()

            x1, y1 = mouse_x + tip_delta[0], mouse_y + tip_delta[1]
            x2, y2 = x1 + width, y1 + height

            x_delta = x2 - s_width
            if x_delta < 0:
                x_delta = 0
            y_delta = y2 - s_height
            if y_delta < 0:
                y_delta = 0

            offscreen = (x_delta, y_delta) != (0, 0)

            if offscreen:

                if x_delta:
                    x1 = mouse_x - tip_delta[0] - width

                if y_delta:
                    y1 = mouse_y - tip_delta[1] - height

            offscreen_again = y1 < 0  # out on the top

            if offscreen_again:
                # No further checks will be done.

                # TIP:
                # A further mod might automagically augment the
                # wraplength when the tooltip is too high to be
                # kept inside the screen.
                y1 = 0

            return x1, y1

        bg = self.bg
        pad = self.pad
        widget = self.widget

        # creates a toplevel window
        self.tw = tk.Toplevel(widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)

        win = tk.Frame(self.tw,
                       background=bg,
                       borderwidth=0)
        label = tk.Label(win,
                         text=self.text,
                         justify=tk.LEFT,
                         background=bg,
                         relief=tk.SOLID,
                         borderwidth=0,
                         wraplength=self.wraplength)

        label.grid(padx=(pad[0], pad[2]),
                   pady=(pad[1], pad[3]),
                   sticky=tk.NSEW)
        win.grid()

        x, y = tip_pos_calculator(widget, label)

        self.tw.wm_geometry("+%d+%d" % (x, y))

    def hide(self):
        tw = self.tw
        if tw:
            tw.destroy()
        self.tw = None


# veidojam galvenā loga objektu
root = tk.Tk()
root.geometry('960x720+10+20')
root.minsize(810, 600)
root.title(progName)
# ieslēdzam mērogošanu
root.resizable(True, True)
# iestatam loga ikonu
logo_file = f"{img_path}\\erj-logo.ico"
root.iconbitmap(logo_file)

# izveidojam fontu instances
LabelFont = font.Font(
    family='Berlin Sans FB', name='vsLabelFont', size=12, weight='normal')
TextFont = font.Font(
    family='Tahoma', name='vsTextFont', size=10, weight='normal')
FixedFont = font.Font(
    family='Courier', name='vsFixedFont', size=10, weight='normal')
ToolTipFont = font.Font(
    family='Berlin Sans FB', name='vsToolTipFont', size=9, weight='normal')
# Bahnschrift

# izveidojam DEMO datoru sarakstu
computerList = list()
i = 0
while i < 100:
    if i <= 9:
        number = f"0{i}"
    else:
        number = str(i)
    computerList.append(f"nb035{number}.ltb.lan")
    i += 1

computerNames = tuple(computerList)
compNames = tk.StringVar(value=computerNames)

main_frame = ttk.Frame(root, padding=(5, 5, 5, 2))

# veidojam datoru ievadīšanas zonu
entry = tk.Entry(main_frame, borderwidth=1, bd=1, font=TextFont)

# veidojam datoru listi
computerListLabel = tk.Label(main_frame,
                             text="Computer names", font=LabelFont)
computerListBox = tk.Listbox(main_frame, listvariable=compNames,
                             width=20, height=20, background="#E8E8E4", font=TextFont)
computerListScrollbarV = ttk.Scrollbar(main_frame,
                                       orient=tk.VERTICAL, command=computerListBox.yview)

# veidojam rezultātu zonu
resultsTableLabel = tk.Label(main_frame, text="Results", font=LabelFont)
resultsTable = tk.Text(main_frame, height=20, wrap="none",
                       background="#E8E8E4", font=FixedFont)
resultsTableScrollbarV = ttk.Scrollbar(main_frame,
                                       orient=tk.VERTICAL, command=resultsTable.yview)
resultsTableScrollbarH = ttk.Scrollbar(main_frame,
                                       orient=tk.HORIZONTAL, command=resultsTable.xview)

# veidojam žurnalēšanas pierakstu zonu
logMessagesLabel = tk.Label(main_frame, text="Messages", font=LabelFont)
logMessages = tk.Text(main_frame, height=7, wrap="none",
                      background="#F8EDEB", font=FixedFont)
logMessagesScrollbarV = ttk.Scrollbar(main_frame,
                                      orient=tk.VERTICAL, command=logMessages.yview)
logMessagesScrollbarH = ttk.Scrollbar(main_frame,
                                      orient=tk.HORIZONTAL, command=logMessages.xview)


def add_computer():
    pass


def del_computer():
    pass


def browse_computer():
    pass


def check_computer():
    pass


def update_computer():
    pass


def eventLog_computer():
    pass


def asset_computer():
    pass


def install_computer():
    pass


def uninstall_computer():
    pass


def wakeOnLan_computer():
    pass


def reboot_computer():
    pass


def stop_computer():
    pass


def help_computer():
    pass


def shutdown_computer():
    """
    Beidzam darbu
    """
    root.destroy()


# definējam AddComputer pogu
addCompIcoPath = Image.open(f"{img_path}\\add.ico")
addCompIcon = ImageTk.PhotoImage(addCompIcoPath.resize((32, 32)))
addComp_button = tk.Button(main_frame, image=addCompIcon, width=48,
                           heigh=48, command=add_computer)
addComp_button_ttp = CreateToolTip(
    addComp_button, text="[Add]: Pievienojam ierakstu datoru sarakstā.")

# definējam DeleteComputer pogu
delCompIcoPath = Image.open(f"{img_path}\\delete.ico")
delCompIcon = ImageTk.PhotoImage(delCompIcoPath.resize((32, 32)))
delComp_button = tk.Button(main_frame, image=delCompIcon, width=48,
                           heigh=48, command=del_computer)
delComp_button_ttp = CreateToolTip(
    delComp_button, text="[Delete]: Notīram ierakstu.")

# definējam Browse pogu
browseCompIcoPath = Image.open(f"{img_path}\\browse.ico")
browseCompIcon = ImageTk.PhotoImage(browseCompIcoPath.resize((32, 32)))
browseComp_button = tk.Button(main_frame, image=browseCompIcon, width=48,
                              heigh=48, command=browse_computer)
browseComp_button_ttp = CreateToolTip(
    browseComp_button, text="[Browse]: Ielasām datoru sarakstu no datnes.")

# definējam Ckeck pogu
checkIcoPath = Image.open(f"{img_path}\\check.ico")
checkIcon = ImageTk.PhotoImage(checkIcoPath.resize((32, 32)))
check_button = tk.Button(main_frame, image=checkIcon, width=48,
                         heigh=48, command=check_computer)
check_button_ttp = CreateToolTip(
    check_button, text="[Check]: Pārbaudam Windows jauninājumu statusu.")

# definējam Update pogu
updateIcoPath = Image.open(f"{img_path}\\update.ico")
updateIcon = ImageTk.PhotoImage(updateIcoPath.resize((32, 32)))
update_button = tk.Button(main_frame, image=updateIcon, width=48,
                          heigh=48, command=update_computer)
update_button_ttp = CreateToolTip(
    update_button, text="[Upgrade]: Uzstādam Windows jauninājumus.")

# definējam EventLog pogu
eventLogIcoPath = Image.open(f"{img_path}\\eventLog.ico")
eventLogIcon = ImageTk.PhotoImage(eventLogIcoPath.resize((32, 32)))
eventLog_button = tk.Button(main_frame, image=eventLogIcon, width=48,
                            heigh=48, command=eventLog_computer)
eventLog_button_ttp = CreateToolTip(
    eventLog_button, text="[Event]: Apskatāmies Windows jauninājumu uzstādīšanas statusu attālinātā datora notikumu žurnālā.")

# definējam Asset pogu
assetIcoPath = Image.open(f"{img_path}\\asset.ico")
assetIcon = ImageTk.PhotoImage(assetIcoPath.resize((32, 32)))
asset_button = tk.Button(main_frame, image=assetIcon, width=48,
                         heigh=48, command=asset_computer)
asset_button_ttp = CreateToolTip(
    asset_button, text="[Asset]: Apskatīt uz datora uzstādītās programmatūras sarakstu un datora tehniskos parametrus.")

# definējam Install pogu
installIcoPath = Image.open(f"{img_path}\\install.ico")
installIcon = ImageTk.PhotoImage(installIcoPath.resize((32, 32)))
install_button = tk.Button(main_frame, image=installIcon, width=48,
                           heigh=48, command=install_computer)
install_button_ttp = CreateToolTip(
    install_button, text="[Install]: Uzstādam norādīto programmatūru.")

# definējam Uninstall pogu
uninstallIcoPath = Image.open(f"{img_path}\\uninstall.ico")
uninstallIcon = ImageTk.PhotoImage(uninstallIcoPath.resize((32, 32)))
uninstall_button = tk.Button(main_frame, image=uninstallIcon, width=48,
                             heigh=48, command=uninstall_computer)
install_button_ttp = CreateToolTip(
    uninstall_button, text="[Uninstall]: Novācam norādīto programmatūru. Programmatūru identificējošais numurs (Identifying number) atrodams Assets atskaitē.")

# definējam WakOnLan pogu
wakeOnLanIcoPath = Image.open(f"{img_path}\\wakeOnLan.ico")
wakeOnLanIcon = ImageTk.PhotoImage(wakeOnLanIcoPath.resize((32, 32)))
wakeOnLan_button = tk.Button(main_frame, image=wakeOnLanIcon, width=48,
                             heigh=48, command=wakeOnLan_computer)
install_button_ttp = CreateToolTip(
    wakeOnLan_button, text="[WakeOnLan]: Attālināti pamodinam izslēgtu datoru (datora IP un MAC adresei jābūt reģistrētai programmas datu bāzē).")

# definējam Reboot pogu
rebootIcoPath = Image.open(f"{img_path}\\reboot.ico")
rebootIcon = ImageTk.PhotoImage(rebootIcoPath.resize((32, 32)))
reboot_button = tk.Button(main_frame, image=rebootIcon, width=48,
                          heigh=48, command=reboot_computer)
reboot_button_ttp = CreateToolTip(
    reboot_button, text="[Reboot]: Attālināti pārsāknējam datoru.")

# definējam Stop pogu
stopIcoPath = Image.open(f"{img_path}\\stop.ico")
stopIcon = ImageTk.PhotoImage(stopIcoPath.resize((32, 32)))
stop_button = tk.Button(main_frame, image=stopIcon, width=48,
                        heigh=48, command=stop_computer)
stop_button_ttp = CreateToolTip(stop_button,
                                text="[Stop]: Attālināti izslēdzam datoru.")

# definējam Help pogu
helpIcoPath = Image.open(f"{img_path}\\help.ico")
helpIcon = ImageTk.PhotoImage(helpIcoPath.resize((32, 32)))
help_button = tk.Button(main_frame, image=helpIcon, width=48,
                        heigh=48, command=help_computer)
help_button_ttp = CreateToolTip(help_button,
                                text="[Help]: Palīdzība.")

# definējam Exit pogu
exitIcoPath = Image.open(f"{img_path}\\shutdown.ico")
exitIcon = ImageTk.PhotoImage(exitIcoPath.resize((32, 32)))
exit_button = tk.Button(main_frame, image=exitIcon, width=48,
                        heigh=48, command=shutdown_computer)
exit_button_ttp = CreateToolTip(exit_button,
                                text="[Quit]: Aizveram programmu.")

# definējam atdalošās strīpas
statusSeparatorV1 = ttk.Separator(main_frame, orient='vertical')
statusSeparatorV2 = ttk.Separator(main_frame, orient='vertical')
statusSeparatorV3 = ttk.Separator(main_frame, orient='vertical')
statusSeparatorV4 = ttk.Separator(main_frame, orient='vertical')
entrySeparatorH1 = ttk.Separator(main_frame, orient='vertical')
entrySeparatorH2 = ttk.Separator(main_frame, orient='vertical')
statusSeparatorH3 = ttk.Separator(main_frame, orient='vertical')

# definējam statusa joslu
status = ttk.Label(
    main_frame, text="Te tiks attēlots uzdevumu izpildes progress vai statuss", anchor='e')

# izvietojam objektus ekrānā
c = 0 # kolonas
r = 0 # rindas
main_frame.grid(column=c, row=r, sticky=('n', 'w', 'e', 's'))
addComp_button.grid(column=c, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
delComp_button.grid(column=c + 1, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
browseComp_button.grid(column=c + 2, row=r, columnspan=2,
                       padx=(5, 0), pady=(5, 0), sticky='w')

statusSeparatorV1.grid(column=c + 4, row=r, rowspan=3, sticky=('n', 's'))

check_button.grid(column=c + 5, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
update_button.grid(column=c + 6, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
eventLog_button.grid(column=c + 7, row=r, padx=(5, 0), pady=(5, 0), sticky='w')

statusSeparatorV2.grid(column=c + 8, row=r, rowspan=2, sticky=('n', 's'))

asset_button.grid(column=c + 9, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
install_button.grid(column=c + 10, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
uninstall_button.grid(column=c + 11, row=r, padx=(5, 0), pady=(5, 0), sticky='w')

statusSeparatorV3.grid(column=c + 12, row=r, rowspan=2, sticky=('n', 's'))

wakeOnLan_button.grid(column=c + 13, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
reboot_button.grid(column=c + 14, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
stop_button.grid(column=c + 15, row=r, padx=(5, 0), pady=(5, 0), sticky='w')
statusSeparatorV4.grid(column=c + 16, row=r, rowspan=2, sticky=('n', 's'))

help_button.grid(column=c + 20, row=r, sticky='e')
exit_button.grid(column=c + 21, row=r, sticky='e')

entrySeparatorH1.grid(column=c, row=r + 1, columnspan=30, sticky=('w', 'e'))
entry.grid(column=c, row=r + 2, columnspan=4, pady=5, sticky=('w', 'e'))
entrySeparatorH2.grid(column=c, row=r + 3, columnspan=30, sticky=('w', 'e'))

computerListLabel.grid(column=c, row=r + 4, columnspan=3, sticky='w')
computerListBox.grid(column=c, row=r + 5, columnspan=3,
                     sticky=('n', 'w', 'e', 's'))
computerListScrollbarV.grid(column=c + 3, row=r + 5, sticky=('n', 's'))
computerListBox["yscrollcommand"] = computerListScrollbarV.set

resultsTableLabel.grid(column=c + 4, row=r + 4, columnspan=17, sticky='w')
resultsTable.grid(column=c + 4, row=r + 5, columnspan=22, sticky=('n', 'w', 'e', 's'))
resultsTableScrollbarV.grid(column=c + 25, row=r + 5, sticky=('n', 's'))
resultsTable["yscrollcommand"] = resultsTableScrollbarV.set
resultsTableScrollbarH.grid(column=c + 4, row=r + 6, columnspan=22, sticky=('w', 'e'))
resultsTable["xscrollcommand"] = resultsTableScrollbarH.set

logMessagesLabel.grid(column=c, row=r + 6, columnspan=17, sticky='w')
logMessages.grid(column=c, row=r + 7, columnspan=22, sticky=('n', 'w', 'e', 's'))
logMessagesScrollbarV.grid(column=c + 25, row=r + 7, sticky=('n', 's'))
logMessages["yscrollcommand"] = logMessagesScrollbarV.set
logMessagesScrollbarH.grid(column=c, row=r + 8, columnspan=22, sticky=('w', 'e'))
logMessages["xscrollcommand"] = logMessagesScrollbarH.set

statusSeparatorH3.grid(column=c, row=r + 20, columnspan=22,
                       sticky=('n', 'w', 'e', 's'))
status.grid(column=c, row=r + 21, columnspan=22, sticky=('w', 'e'))

# iestatam mērogošanu
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(18, weight=1)
main_frame.grid_rowconfigure(5, weight=1)
main_frame.grid_rowconfigure(7, weight=1)


for i in range(0, len(computerNames), 2):
    computerListBox.itemconfigure(i, background="#F8EDEB")

for child in main_frame.winfo_children():
    child.grid_configure(padx=1, pady=1)

computerListBox.selection_set(0)
entry.focus()


if __name__ == '__main__':
    # Aizpildam logMessages un resultsTable ar DEMO tekstu
    i = 0
    while i < 100:
        position = logMessages.index("end")
        logMessages.insert(
            position, "2022.01.10 22:01 | INFO | [Get-Data] Uzsākam darbu un sākotnējā informācija savākta.\n")
        logMessages.insert(
            str(float(position)+1), "2022.01.10 22:01 | INFO | [Get-Data] informācijas kompilācija veiksmīga.\n")
        logMessages.insert(
            str(float(position)+2), "2022.01.10 22:02 | SEND | [Get-Data] uzsākam datu ievākšanas procesu\n")
        logMessages.insert(
            str(float(position)+3), "2022.01.10 22:02 | WAIT | [Get-Data] gaidām rezultātu...\n")
        logMessages.insert(
            str(float(position)+4), "2022.01.10 22:08 | SUCC | [Get-Data] process pabeigts, rezultāts apkopots.\n")
        i += 1

    text = font.names()
    for line in text:
        position = resultsTable.index("end")
        resultsTable.insert(
            position, f"{line}\n"
        )

    # slēdzam laukus uz rediģēšanu
    logMessages["state"] = "disabled"
    resultsTable["state"] = "disabled"

    root.mainloop()
