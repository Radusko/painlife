import tkinter as tk
import numpy as np
from tkinter import filedialog as fd
win = tk.Tk()

WIDTH=500
HEIGHT=500
vs=10
abs=vs
cells = np.zeros((WIDTH//vs,HEIGHT//vs),dtype=int)
cells_new = np.zeros((WIDTH//vs,HEIGHT//vs),dtype=int)
cells_not = np.zeros((WIDTH//vs, HEIGHT//vs), dtype=int)


def slider_change(e):
    global vs

    print(w.get())
    #vymaz canvas a prekresli mriesku z touto hodnotou
    canvas.delete("all")
    vs=w.get()
    create_stage()
    redraw_cells()


def create_cells(e):
    global cells
    tx=e.x//vs
    ty=e.y//vs
    nx=(tx)*vs
    ny=(ty)*vs
    temp=(canvas.create_oval(nx, ny, nx+vs, ny+vs, fill="red"))
    canvas.create_oval(nx, ny, nx+vs, ny+vs, fill="red")
    cells[tx,ty]=1
    print(getnei(tx,ty))
    #print(cells)

def getnei(x,y):
    total=0
    if x > 0:
        total += cells[x - 1, y]
    if x > 0 and y > 0:
        total += cells[x - 1, y - 1]
    if y > 0:
        total += cells[x, y - 1]
    if x > 0 and y < (HEIGHT // abs - 1):
        total += cells[x - 1, y + 1]
    if x < (WIDTH // abs - 1):
        total += cells[x + 1, y]
    if x < (WIDTH // abs - 1) and y < (HEIGHT // abs - 1):
        total += cells[x + 1, y + 1]
    if y < (HEIGHT // abs - 1):
        total += cells[x, y + 1]
    if x < (WIDTH // abs - 1) and y > 0:
        total += cells[x + 1, y - 1]
    return total

def recalcul():
    global cells,cells_new
    for y in range(HEIGHT//abs):
        for x in range(WIDTH//abs):
            temp=getnei(x,y)
            if (temp == 2 and cells[x, y] == 1) or (temp == 3 and cells[x, y] == 1):
                cells_new[x, y] = 1
            elif temp == 3 and cells[x, y] == 0:
                cells_new[x, y] = 1
            elif temp<2 or temp>3:
                cells_new[x, y] = 0
    cells=cells_new.copy()
    canvas.delete("all")
    create_stage()
    redraw_cells()

def redraw_cells():
    for x in range(WIDTH//vs):
        for y in range(HEIGHT//vs):
            if cells[x,y]==1:
                canvas.create_oval(x*vs,y*vs,(x+1)*vs,(y+1)*vs,fill="red")



def create_stage():
    global cells_new,cells_not
    for x in range(WIDTH//vs):
        canvas.create_line(x*vs,0,x*vs,HEIGHT)
    for y in range(HEIGHT//vs):
        canvas.create_line(0,y*vs,WIDTH,y*vs)
    cells_new=cells_not

def openfile():
    global cells, cells_new
    load = []
    filename = fd.askopenfilename()
    f = open(filename,"r")
    cells_new = cells_not.copy()
    for i in f:
        for j in i.split():
            load.append(j)
    counter = 0
    for i in load:
        for j in i:
            counter += 1
    if counter < 2500:
        for i in range(len(load)):
            for j in range(len(load[i])):
                if load[i][j] == "1":
                    cells_new[i, j] = 1
                else:
                    cells_new[i, j] = 0
        cells = cells_new.copy()
        canvas.delete("all")
        create_stage()
        redraw_cells()
    else:
        print("Moc velky subor sefko")

def loop():
    if button2.config('text')[-1] == 'hadam to pojde same':
        recalcul()
        win.after(100, loop)

def zivotik():
    if button2.config('text')[-1] == 'omg ono sa to hybe':
        button2.config(text='hadam to pojde same')
        loop()
    else:
        button2.config(text='omg ono sa to hybe')




canvas = tk.Canvas(width=WIDTH,height=HEIGHT,bg="grey")
canvas.pack()

w = tk.Scale(win, from_=10, to=50, orient="horizontal", command=slider_change, length=500)
w.pack()

button=tk.Button(win,text="next gen",command=recalcul)
button.pack(side=tk.LEFT)

button1=tk.Button(win,text="otvor subores",command=openfile)
button1.pack(side=tk.RIGHT)

button2=tk.Button(win,text="same to pojde hadam",command=zivotik)
button2.pack(side=tk.BOTTOM)

create_stage()
canvas.bind("<Button-1>",create_cells)
win.mainloop()