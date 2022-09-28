from tkinter import ACTIVE, DISABLED, END, Canvas, Frame, PhotoImage, Button, Text, Tk, Entry, Label
from tkinter.messagebox import showinfo, askyesno
from functools import partial


class main(Tk):
    def __init__(self):
        #Window Init Part
        Tk.__init__(self)
        self.class_init()
    
    def class_init(self):
        #Window Settings
        self.geometry("300x500")
        self.config(background="#272422")
        self.itemList = []
        self.active_list = []
        self.canBeAdded = True
        self.title = "Note+"
        self.attributes('-topmost',True)
        self.count = 0
        self.actual_count = 0   
        #Window Binds
        self.bind("<space>", self.adding)
        self.bind("<Delete>", self.removing)
        #Containers Creation
        self.topBar = Frame(self, bg="#1C1B1A", highlightthickness=0, width=300, height=40)
        self.mainFrame = Frame(self, highlightthickness=0, width=300, height=440, background="#272422")
        #Containers Creation (edition page)
        self.topBar_edit = Frame(self, bg="#1C1B1A", highlightthickness=0, width=300, height=40)
        self.mainFrame_edit = Frame(self, highlightthickness=0, width=300, height=460, background="#272422")
        #Top checker for button placement
        self.actual_top = self.topBar
        #Topbar Binds
        self.topBar.bind("<Double-Button-1>", self.minimize)
        self.topBar.bind("<ButtonPress-1>", self.mouse_down)
        self.topBar.bind("<B1-Motion>", self.mouse_drag)
        self.topBar.bind("<ButtonRelease-1>", self.mouse_up)
        #Topbar Binds (edition page)
        self.topBar_edit.bind("<Double-Button-1>", self.minimize)
        self.topBar_edit.bind("<ButtonPress-1>", self.mouse_down)
        self.topBar_edit.bind("<B1-Motion>", self.mouse_drag)
        self.topBar_edit.bind("<ButtonRelease-1>", self.mouse_up)
        #Images
        self.plus_image = PhotoImage(file="plus_image.png")
        self.minus_image = PhotoImage(file="minus_image.png")
        self.cross_image = PhotoImage(file="cross_image.png")
        self.validate_image = PhotoImage(file="validate_image.png")
        self.bin_image = PhotoImage(file="bin_image.png")
        self.arrow_back_image = PhotoImage(file="arrow_back_image.png")
        self.separator_image = PhotoImage(file="separator_image.png")
        self.edit_list_image = PhotoImage(file="list_image.png")
        #Buttons Creation
        self.plus_button = Button(self.topBar, image=self.plus_image, bg="#1C1B1A", foreground="#1C1B1A", relief="sunken", activebackground="#1C1B1A", borderwidth=0, command=self.add)
        self.minus_button = Button(self.topBar, image=self.minus_image, bg="#1C1B1A", foreground="#1C1B1A", relief="sunken", activebackground="#1C1B1A", borderwidth=0, command=self.place_remover)
        self.close_button = Button(self.topBar, image=self.cross_image, bg="#1C1B1A", foreground="#1C1B1A", relief="sunken", activebackground="#1C1B1A", borderwidth=0, command=self.close)
        #Buttons Creation (edition page)
        self.back_button = Button(self.topBar_edit, image=self.arrow_back_image, bg="#1C1B1A", foreground="#1C1B1A", relief="sunken", activebackground="#1C1B1A", activeforeground="#1C1B1A", borderwidth=0)
        self.separator = Label(self.topBar_edit, image=self.separator_image, bg="#1C1B1A", foreground="#1C1B1A", relief="flat")
        self.edit_user_text = Text(self.mainFrame_edit, width=280, borderwidth=0)
        self.edit_list = Button(self.topBar_edit, image=self.edit_list_image, bg="#1C1B1A", foreground="#1C1B1A", relief="sunken", activebackground="#1C1B1A", activeforeground="#1C1B1A", borderwidth=0)
        #Main Widgets Placement
        self.topBar.place(x=0, y=0)
        self.mainFrame.place(x=0, y=50)
        self.plus_button.place(x=5, y=7)
        self.minus_button.place(x=35, y=7)
        self.close_button.place(x=265, y=7)

    def mouse_down(self, event):
        global x, y
        x, y = event.x, event.y

    def mouse_up(self, event):
        global x, y
        x, y = None, None

    def mouse_drag(self, event):
        global x, y
        try:
            deltax = event.x - x
            deltay = event.y - y
            x0 = self.winfo_x() + deltax
            y0 = self.winfo_y() + deltay
            self.geometry("+%s+%s" % (x0, y0))
        except:
            pass

    def minimize(self, event):
        if self.winfo_height() == 500:
            self.geometry("300x40")
            if self.actual_top == self.topBar:
                active_note_str = "{} active note{}".format(str(self.count), "s" if self.count > 1 else "")
                self.active_note = Label(self.actual_top, text=active_note_str, bg="#1C1B1A", foreground="#FFFFFF", font=("Calibri", "12"))
                self.active_note.place(x=110, y=8)
        elif self.winfo_height() == 40:
            self.geometry("300x500")
            if self.actual_top == self.topBar:
                self.active_note.destroy()

    def saving_enter(self, entry, save_b, button, event):
        self.save(entry, save_b, button)

    def adding(self, event):
        self.add()

    def removing(self, event):
        self.place_remover()

    def clicking_entry(self, entry, event):
        if entry.get() == "Enter the name of your note":
            entry.delete(0, END)
            entry.config(foreground="#FFFFFF")

    def add(self):
        if self.winfo_height() == 40:
            self.geometry("300x500")
            self.active_note.destroy()
        if self.canBeAdded == True:
            self.canBeAdded = False
            self.itemList.append([Entry(self.mainFrame, borderwidth=0, font=("Calibri", "12"), foreground="#615E5D", bg="#44413F", width=24), Button(self.mainFrame, image=self.validate_image, foreground="#FFFFFF", background="#272422", relief="sunken", activebackground="#272422", activeforeground="#FFFFFF", borderwidth=0), Button(self.mainFrame, text=self.actual_count, foreground="#FFFFFF", background="#FFFFFF", relief="sunken", activebackground="#FFFFFF", activeforeground="#FFFFFF", borderwidth=0, disabledforeground="#FFFFFF", state=DISABLED)])
            self.itemList[self.count][1]["command"] = partial(self.save, self.itemList[self.count][0], self.itemList[self.count][1], self.itemList[self.count][2])
            self.itemList[self.count][2]["command"] = partial(self.open, self.itemList[self.count][0], self.itemList[self.count][2])
            self.bind("<Return>", partial(self.saving_enter, self.itemList[self.count][0], self.itemList[self.count][1], self.itemList[self.count][2]))
            self.y_value = 0
            for i in self.itemList:
                if i[0].winfo_exists(): 
                    if i[0].get() == "":
                        i[0].insert(0, "Enter the name of your note")
                    i[0].place(x=10, y=self.y_value)
                    i[0].bind("<ButtonPress-1>", partial(self.clicking_entry, i[0]))
                    i[1].place(x=220, y=self.y_value)
                    i[2].place(x=0, y=self.y_value+30, width=300, height=100)
                if len(i) > 4:
                    i[4].destroy()
                    i.pop(4)
                self.y_value += 140
        else:
            showinfo("Warning", "You have to save your active note first!")

    def save(self, entry, save_b, button):
        if self.canBeAdded == False or len(self.itemList) < 1:
            if entry.get() != "Enter the name of your note" and entry.get() != "":
                self.canBeAdded = True
                self.canBeRemoved = True
                button["state"] = ACTIVE
                save_b.destroy()
                self.itemList[self.count].append(Label(self.mainFrame, text=entry.get(), font=("Calibri", "12"), foreground="#FFFFFF", background="#272422"))
                self.itemList[self.count][3].place(x=10, y=self.y_value-140)
                entry.destroy()
                self.count += 1
                self.actual_count += 1
            else:
                showinfo("Warning", "You have to name your note!")
        else:
            showinfo("Warning", "You have no note to save!")

    def open(self, entry, button):
        edit()

    def insert_list(self):
        self.active_list.append([Frame(self.topBar_edit)])
        self.active_list[0].append((Button(self.active_list[0][0], text="testttt"), Label(self.active_list[0][0], text="fez")))
        for i in range(len(self.active_list[0])):
            self.active_list[0][i].place(x=50, y=8)

    def place_remover(self):
        if self.canBeAdded == True:
            if len(self.itemList) > 0:
                if self.winfo_height() == 40:
                    self.geometry("300x500")
                    self.active_note.destroy()
                if self.canBeRemoved == True:
                    self.canBeRemoved = False    
                    self.y_value = 0
                    for i in range(len(self.itemList)):
                        self.itemList[i].append(Button(self.mainFrame, image=self.bin_image, foreground="#FFFFFF", background="#272422", relief="sunken", activebackground="#272422", activeforeground="#FFFFFF", borderwidth=0, command=partial(self.remove, i)))
                        self.itemList[i][4].place(x=220, y=self.y_value)
                        self.y_value += 140
                else:
                    for j in self.itemList:
                        j[4].destroy()
                        j.pop(4)
                    self.canBeRemoved = True
            else:
                showinfo("Warning", "There is no note to delete!")
        else:
            showinfo("Warning", "You have to save your active note first!")

    def remove(self, widget):
        question = askyesno("Warning", "Do you really want to delete this note?")
        if question: 
            self.saved_label_value = []
            self.saved_button_value = []
            self.y_value = 0
            for i in range(len(self.itemList)):
                for j in range(len(self.itemList[i])):
                    if j == 2:
                        self.saved_button_value.append(self.itemList[i][j].cget("text"))
                    elif j == 3:
                        self.saved_label_value.append(self.itemList[i][j].cget("text"))
                    self.itemList[i][j].destroy()
            self.itemList.pop(widget)
            self.saved_label_value.pop(widget)
            self.saved_button_value.pop(widget)
            for l in range(len(self.itemList)):
                self.itemList[l].pop(4)
                self.itemList[l][2] = Button(self.mainFrame, text=self.saved_button_value[l], foreground="#FFFFFF", background="#FFFFFF", relief="sunken", activebackground="#FFFFFF", activeforeground="#FFFFFF", borderwidth=0, disabledforeground="#FFFFFF")
                self.itemList[l][3] = Label(self.mainFrame, text=self.saved_label_value[l], font=("Calibri", "12"), foreground="#FFFFFF", background="#272422")
                self.itemList[l][2]["command"] = partial(self.open, self.itemList[l][0], self.itemList[l][2])
                self.itemList[l][2].place(x=0, y=self.y_value+30, width=300, height=100)
                self.itemList[l][3].place(x=10, y=self.y_value)
                self.y_value += 140
            self.count -= 1
            if len(self.itemList) > 0:
                self.canBeRemoved = True
                self.place_remover()

    def close(self):
        self.quit()

class edit(main):
    def __init__(self):
        root.actual_top = root.topBar_edit
        root.unbind('<Return>')
        self.class_init_edit()
    
    def class_init_edit(self):
        root.topBar_edit.place(x=0, y=0) 
        root.mainFrame_edit.place(x=0, y=40)   
        root.separator.place(x=30, y=8)
        root.back_button.place(x=8, y=8)
        root.back_button["command"] = self.back
        root.edit_list.place(x=50, y=8)
        root.edit_list["command"] = root.insert_list
        root.edit_user_text.place(x=10, y=10, width=280, height=440)

    def back(self):
        root.class_init()

root = main()
root.overrideredirect(True)

root.mainloop()
