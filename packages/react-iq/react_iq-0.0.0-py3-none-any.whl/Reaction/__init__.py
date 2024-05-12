from tkinter import *
import time 
import threading
import random as rd

class Firstwin:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x400")
        self.root.title("Test Your Reaction-Time")

        self.trailer = Label(self.root, text="Reaction Time Test ! ", font="Dungeon 35")
        self.trailer.pack(anchor="center", fill=BOTH, expand=True)

        self.start = Button(self.root, text="Start" , font = "Dungeon 15", bd=4, bg="lightgrey",relief=RAISED, command=self.React_win)
        self.start.pack(fill=BOTH, side=TOP)

    def React_win(self):
        self.root.destroy()  # Destroy the first window
        obj = Reaction()
        obj.open()

class Reaction:
    def __init__(self):
        self.win = Tk()
        self.win.geometry("600x400") 
        self.win.title("Reaction-Time Testor !!!")
        self.win.bind("<space>",self.fill_real )
        self.win.bind("<Return>",self.clicked)

        Label(self.win, text="Click SpaceBar To Start", font="elephant 30",bg="black",fg="white").pack(fill=BOTH,pady=10)
        self.frame = Frame(self.win, relief=RIDGE, bg="lightblue")
        self.frame.pack(pady=10)

        self.light_1 = Label(self.frame,bg="grey",height=3,width=5)
        self.light_1.grid(row=0,column=0,padx=15,pady=10)

        self.light_2 = Label(self.frame,bg="grey",height=3,width=5)
        self.light_2.grid(row=0,column=1,padx=15,pady=10)

        self.light_3 = Label(self.frame,bg="grey",height=3,width=5)
        self.light_3.grid(row=0,column=2,padx=15,pady=10)

        self.light_4 = Label(self.frame,bg="grey",height=3,width=5)
        self.light_4.grid(row=0,column=3,padx=15, pady=10)

        self.light_5 = Label(self.frame,bg="grey",height=3,width=5)
        self.light_5.grid(row=0,column=4,padx=15,pady=10)

        self.frame_1 = Frame(self.win, bg = "grey", relief = RIDGE)
        self.frame_1.pack(pady=10)

        self.score = Label(self.frame_1)
        self.score.grid(row=0,column=0,pady=10,padx=10) 

        self.guide = Button(self.win, text="Guide",font="Dungeon 20",bg="lightgrey",command=self.guide_window)
        self.guide.pack(side=RIGHT, anchor="sw")

        self.win.protocol("WM_DELETE_WINDOW", self.reopen)

    # def guide_window(self):
    #     self.guide_win = Toplevel(self.win)
    #     self.guide_win.geometry("600x500")
    #     self.guide_win.title("Guide")
    #     Label(self.guide_win,text="How To Use Reaction Time Tester: ", font="Elephant 20",bg="lightgrey").pack(fill=BOTH,side=TOP)
    #     texty = guide_description
    #     Label(self.guide_win,text=texty,font="consolas 10").pack()

    def guide_window(self):
        self.guide_win = Toplevel(self.win)
        self.guide_win.geometry("600x500")
        self.guide_win.title("Guide")
        
        # Styling
        self.guide_win.configure(bg="lightgrey")
        
        # Title
        Label(self.guide_win, text="🎮 Reaction Time Tester Guide 🎮", font=("Segoe UI Emoji", 20, "bold"), bg="lightgrey").pack(pady=10)

        guide_description = """🚦Welcome to Reaction Time Tester! 🚦\n\n
        To start testing your reaction time, follow these simple steps: \n\n

        1: Start test : By pressing the space bar. 🚀\n
        2: Watch the Lights: Keep your eyes on the screen as the lights start blinking one by one, 🚥just like the start sequence in a Formula One race! 🏎️\n
        3: Right after the last red light turns off, you need to press enter as quickly as possible cause the reaction time starts right after the last red light goes off. ⏱️\n
        4: View Your Results: Your reaction time will be displayed on the screen, 📊\nshowing you just how fast you reacted. 💨\n\n

        Ready to test your reflexes? Click the spacebar and see how quick you are! 🏁"""

        
        # Guide text
        guide_text = Text(self.guide_win, font=("Dungeon", 12), wrap=WORD, bg="lightgrey")
        guide_text.pack(fill=BOTH, expand=True, padx=20, pady=10)
        guide_text.insert(END, guide_description)
        guide_text.config(state=DISABLED)  # Make the text read-only





    def clicked(self,event):
        try:
            last_l = time.time()
            time_taken = (last_l-initial_l)*1000
            if time_taken >= 1800:
                pass
            else:
                self.score.config(text=f"Your Reaction Time is {int(time_taken)} milliseconds",font="consolas 16", bg="lightgreen")
        except Exception as e:
            print("Too fast !!!")
    def fill_real(self, event):
        threading.Thread(target=self.fill, daemon=True).start()

    def fill(self):
        try:
            self.light_1.config(bg="red",height=3,width=5)
            time.sleep(1)
            self.light_2.config(bg="red",height=3,width=5)
            time.sleep(1)
            self.light_3.config(bg="red",height=3,width=5)
            time.sleep(1)
            self.light_4.config(bg="red",height=3,width=5)
            time.sleep(1)
            self.light_5.config(bg="red",height=3 ,width=5)
            time.sleep(rd.uniform (1.10,1.60 ))
            self.light_1.config(bg="grey",height=3,width=5)
            self.light_2.config(bg="grey",height=3,width=5) 
            self.light_3.config(bg="grey",height=3,width=5)
            self.light_4.config(bg="grey",height=3,width=5)
            self.light_5.config(bg="grey",height=3,width=5)   
            global initial_l
            initial_l = time.time()
        except EXCEPTION as e:
            pass

    def open(self):
        self.win.mainloop()

    def reopen(self):
        self.root = Tk()
        self.root.geometry("600x400")
        self.win.destroy()
        obj = Firstwin(self.root)

         # Reopen the first window

if __name__ == "__main__":
    win = Tk()
    obj = Firstwin(win)
    win.mainloop()
