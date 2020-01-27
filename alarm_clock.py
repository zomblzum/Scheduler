import json
import time
from tkinter import *
from tkinter import colorchooser
import random
 
shedule_filename = 'shedule.json'

class Ball:
    def __init__(self):
        self.xpos = random.randint(0, 254)
        self.ypos = random.randint(0, 310)
        self.xspeed = random.randint(1, 6)
        self.yspeed = random.randint(1, 6)

class AlarmWindow:
    def __init__(self, text):
        self.tk = Tk()
        self.tk.title("Sheduler")
        self.tk.attributes("-fullscreen", True)
        self.tk.bind("<Escape>", self.close)

        self.canvas = Canvas(self.tk)
        self.canvas.pack(fill="both",expand=True)

        self.lbl = Label(self.canvas, text=text,font=("Arial Bold", 50), bd=2, relief=RIDGE)  
        self.lbl.pack(expand=True)

        self.balls_count = 100
        self.ball_size = 15

        self.balls = []
        self.bs = []      
        for _ in range(self.balls_count):
            ball = Ball()
            color = '#' + '{:06x}'.format(random_color())
            self.balls.append(ball)
            self.bs.append(self.canvas.create_oval(ball.xpos - self.ball_size, ball.ypos - self.ball_size, ball.xpos + self.ball_size, ball.ypos + self.ball_size, fill=color))
        self.run()

    def run(self):
        for b, ball in zip(self.bs, self.balls):
            self.canvas.move(b, ball.xspeed, ball.yspeed)
            pos = self.canvas.coords(b)
            if pos[3] >= self.tk.winfo_screenheight() or pos[1] <= 0:
                ball.yspeed = - ball.yspeed
            if pos[2] >= self.tk.winfo_screenwidth() or pos[0] <= 0:
                ball.xspeed = - ball.xspeed
        self.canvas.after(10, self.run)

    def close(self, event=None):
        self.tk.destroy()

def read_json_file(filename):
    with open('shedule.json', encoding='utf8') as f:
        return json.load(f)['events']

def find_item_in_dictionary(dictionary, value):
    for k, v in dictionary.items():
        if v == value:
            return k

def random_color():
    return random.randint(0,0x1000000)

def get_current_time():
    return time.strftime("%H:%M")

def run_alarm(text):
    window = AlarmWindow(text)
    window.tk.mainloop()

def run_sheduler():
    last_alarm = 0

    while True:
        events = read_json_file(shedule_filename)  
        current_time = get_current_time()
        
        if current_time in events.values() and last_alarm != current_time:
            last_alarm = current_time
            run_alarm(find_item_in_dictionary(events,current_time))

        time.sleep(1)

if __name__ == "__main__":
    run_sheduler()


    

    

