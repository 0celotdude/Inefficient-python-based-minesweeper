from tkinter import *
from random import *

window = Tk()

# add preset difficulty levels?

mineimagedata = "iVBORw0KGgoAAAANSUhEUgAAAA0AAAANCAYAAABy6+R8AAAAYElEQVQoU52S0Q4AIARF+f+P1lLMhJSH2uoedIWQBwEARtfh4Ra2IBHN3cdMrkl8pQiQBKq1EANEi0PMn/MNVS2F3h6VihFw17oYiy/MCbEPBZW6J/N4mpMVt36Ez55CA37IFw0KsTaYAAAAAElFTkSuQmCC"
mineimagephoto = PhotoImage(data = mineimagedata)
window.iconphoto(True, mineimagephoto)

global buttons

global pastsizex
global pastsizey
global pastmines

global marked
marked = []
global clickedbuttons
clickedbuttons = []
global selectedmines
selectedmines = []

global winstate
winstate = False
global firstclick
firstclick = True
global gameactive
gameactive = False

global mingridsize
mingridsize = 5
global maxgridsize
maxgridsize = 10

global widgetoffset

global debug
debug = False

global devwindow

global custommaxgridsize
custommaxgridsize = 16

global cheats
cheats = [("xrayenabled", False)] # ("{name}", {value}),

global logbutton
global revealminesbutton
global extrasizebutton

global sortedmineslabel

window.title("Minesweeper")
window.geometry("500x500")
window.minsize(240,135)

def devmode():
    global debug
    global devwindow
    global logbutton
    global revealminesbutton
    global extrasizebutton
    try:
        if devwindow.winfo_ismapped() == True:
            pass
    except:
        debug = True
        print("Debug mode enabled")
        print("MAY REDUCE PERFORMANCE")
        devwindow = Toplevel()
        devwindow.title("Developer Console")
        devwindow.geometry("270x50")
        devwindow.minsize(270,120) # +20 per extra button
        devwindow.maxsize(270,120)
        logbutton = Button(devwindow, text = "Logs", relief = "sunken", borderwidth = 3, command = lambda: debugtoggle())
        logbutton.pack(fill = X, padx = 10, pady = 5)
        revealminesbutton = Button(devwindow, text = "Xray", state = "disabled", relief = "raised", borderwidth = 3) # gets its command after first click
        revealminesbutton.pack(fill = X, padx = 10, pady = 5)
        extrasizebutton = Button(devwindow, text = "Extra sizes", state = "normal", relief = "raised", borderwidth = 3, command = lambda: customsize())
        extrasizebutton.pack(fill = X, padx = 10, pady = 5)
    
def debugtoggle():
    global debug
    global logbutton
    if debug != False:
        logbutton.config(relief = "raised")
        print("Logs disabled")
        debug = False
    else:
        logbutton.config(relief = "sunken")
        print("Logs enabled")
        debug = True

def sizesettings():
    global pastsizex
    global pastsizey
    global mingridsize
    global maxgridsize
    clearwindow() # only does anything when playing again
    sizexslidertext = Label(window, text = "Horizontal Size").pack(pady=(10,0))
    sizexslider = Scale(window, orient = "horizontal", from_ = mingridsize, to = maxgridsize, cursor = "sb_h_double_arrow")
    sizexslider.pack()
    try:
        sizexslider.set(pastsizex)
    except:
        pass
    sizeyslidertext = Label(window, text = "Vertical Size").pack(pady=(40,0))
    sizeyslider = Scale(window, orient = "horizontal", from_ = mingridsize, to = maxgridsize, cursor = "sb_h_double_arrow")
    sizeyslider.pack()
    try:
        sizeyslider.set(pastsizey)
    except:
        pass
    tominessettingsbutton = Button(window, text = "NEXT", command = lambda: minessettings(sizexslider, sizeyslider)).pack()
    randombutton = Button(window, text = "🎲", font = ("Arial", 30), borderwidth = 0, cursor = "exchange", command = lambda: randomsettings()).pack(pady = 10)
    devbutton = Button(window, text = "🛠", cursor = "gumby", borderwidth = 0, command = lambda: devmode(), height = 2, width = 4).pack(side = "bottom", anchor = "w")

def minessettings(sizexslider, sizeyslider):
    global pastsizex
    global pastsizey
    global pastmines
    sizex = sizexslider.get()
    sizey = sizeyslider.get()
    try:
        if sizex != pastsizex or sizey != pastsizey:
            pastmines = 0
    except:
        pass
    try:
        global extrasizebutton
        extrasizebutton.config(state = "disabled")
    except:
        pass
    pastsizex = sizex
    pastsizey = sizey
    clearwindow()
    sizet = sizex * sizey
    minesslidertext = Label(window, text = "Number Of Mines In " + str(sizet) + " Tiles").pack()
    minesslider = Scale(window, orient = "horizontal", from_ = max(8,((sizex-4)*(sizey-4))), to = (((sizex-2)*(sizey-2))-4), cursor = "sb_h_double_arrow")
    minesslider.pack()
    try:
        minesslider.set(pastmines)
    except NameError:
        pass
    startbutton = Button(window, text = "START", command = lambda: grid(sizex, sizey, sizet, minesslider)).pack()
    devbutton = Button(window, cursor = "gumby", borderwidth = 0, command = lambda: devmode(), height = 2, width = 4).pack(side = "bottom", anchor = "w")

def randomsettings():
    global pastsizex
    global pastsizey
    global pastmines
    global mingridsize
    global maxgridsize
    sizex = max(randrange(mingridsize,maxgridsize),(randrange((mingridsize+1),maxgridsize)+1))
    sizey = max(randrange(mingridsize,maxgridsize),(randrange((mingridsize+1),maxgridsize)+1))
    if sizex > 7 and sizey > 7:
        mines = randrange(16,((sizex-3)*(sizey-3))) 
    else:
        mines = randrange(6,((sizex-2)*(sizey-2)))
    sizet = sizex * sizey
    pastsizex = sizex
    pastsizey = sizey
    grid(sizex, sizey, sizet, mines)

def minesgenerator(sizet, mines, firstarea):
    global debug
    global selectedmines
    while len(selectedmines) < (mines):
        newmine = (randrange(0,sizet)) # the use of randrange() instead of randint() is because the array of buttons starts at 0,0 and sizet starts at 1 and range is exclusive of the ceiling
        if newmine not in selectedmines and newmine not in firstarea:
            selectedmines.append(newmine)
            if debug == True:
                print("Mine",len(selectedmines),"set for position",selectedmines[-1]) ##debug

def click(pos, mines, x, y, sizex, sizey, sizet, button, buttons, auto):
    global marked
    if pos in marked:
        pass
    else:
        global clickedbuttons
        global selectedmines
        global winstate # winstate only works when NO mines are hit, if a mine is hit and dosen't cause a loss it counts towards winstate
        global debug
        global firstclick
        global revealminesbutton
        nearbyminescount = 0
        neighbors = []
        offsets = [(-1, -1),(0, -1),(1, -1),(-1, 0),(1, 0),(-1, 1),(0, 1),(1, 1)]
        offsetsincl = [(-1, -1),(0, -1),(1, -1),(-1, 0),(0, 0),(1, 0),(-1, 1),(0, 1),(1, 1)]
        if firstclick == True:
            firstarea = []
            for dx, dy in offsetsincl:
                nx, ny = x + dx, y + dy
                if 0 <= nx < sizex and 0 <= ny < sizey:
                    firstarea.append(pos + dx + dy * sizex)
            if debug == True: # debug
                print("Staring area:",firstarea)
            minesgenerator(sizet, mines, firstarea)
            try:
                revealminesbutton.config(command = lambda: Xray(selectedmines, buttons), state = "normal")
                sortmines(selectedmines)
            except:
                pass
        if debug == True:
            if auto == False:
                print("Button",str(pos),"clicked")    
            else:
                print("Button",str(pos),"automatically clicked")     
        if pos not in clickedbuttons:
            clickedbuttons.append(pos)
            if pos in selectedmines:
                if debug == True:
                    print("Mine",str(pos),"hit. Loose condition met")
                loose()
            else:
                button.config(relief = "flat", state = "disabled")
                if debug == True: # debug
                    print("Mines ("+str(len(selectedmines))+"): "+str(selectedmines),"in a",sizex,"by",sizey,"grid")
                    print("Coords: "+str(x)+"x,"+str(y)+"y")
                    nearbymines = []
                for dx, dy in offsets: # detects the neighbors
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < sizex and 0 <= ny < sizey:
                        neighbors.append(pos + dx + dy * sizex)
                        if neighbors[-1] in selectedmines:
                            nearbyminescount += 1
                            if debug == True: # debug
                                nearbymines.append(neighbors[-1])
                        if debug == True: # debug
                            if nearbyminescount == 1:
                                print("In neighbors:",neighbors,"1 is a mine",nearbymines)
                            elif nearbyminescount != 0:
                                print("In neighbors:",neighbors,nearbyminescount,"are mines",nearbymines)
                            else:
                                print("In neighbors:",neighbors,nearbyminescount,"are mines")
                if debug == True: # debug
                    if nearbyminescount == 1:
                        print(pos,"("+str(x)+","+str(y)+") has 1 nearby mine",nearbymines)
                    elif nearbyminescount !=0:
                        print(pos,"("+str(x)+","+str(y)+") has",str(nearbyminescount),"nearby mines",nearbymines)
                    else:
                        print(pos,"("+str(x)+","+str(y)+") has 0 nearby mines")
                if nearbyminescount > 0:
                    button.config(text = nearbyminescount)
                elif nearbyminescount == 0:
                    button.config(text = " ")
                if sizet-len(clickedbuttons) == len(selectedmines): # winstate checker
                    winstate = True
                    if debug == True:
                        print("Winstate met")
                    win()
                elif nearbyminescount == 0: # explorer
                    explorerneighbors = neighbors
                    for j in explorerneighbors[:]:
                        if j in selectedmines:
                            explorerneighbors.remove(j)
                        try:
                            if j in clickedbuttons:
                                explorerneighbors.remove(j)
                            if j in marked and firstclick == False:
                                explorerneighbors.remove(j)
                        except:
                            pass
                    firstclick = False
                    if debug == True: # debug
                        print("Non-mine, non-flagged neighbors:",str(explorerneighbors))
                    if explorerneighbors == []:
                        pass
                    for newpos in explorerneighbors:
                        if newpos not in clickedbuttons:
                            if debug == True: # debug
                                print("newpos = "+str(newpos))
                            x = int(newpos)
                            y = 0
                            while x >= sizex and winstate == False:
                                x-=sizex
                                y+=1
                                if debug == True: # debug
                                    print("y = "+str(y)+"x = "+str(x)+" k = "+str(newpos))
                            if debug == True:
                                print("Next button to be clicked is at y = "+str(y)+"x = "+str(x)+" pos = "+str(newpos))
                            button = buttons[newpos]
                            click(newpos, selectedmines, x, y, sizex, sizey,sizet, button, buttons, True)
                        else:
                            pass
                
def mark(event): #the tkinter buttons' widget names' numbers' get offset by previous buttons, widgetoffset is used to dynamically counter it
    global marked
    global clickedbuttons
    global selectedmines
    global widgetoffset
    global debug
    global cheats
    if ((int(str(event.widget).replace(".!button","")))-widgetoffset) not in marked and event.widget.cget("state") != "disabled":
        marked.append((int(str(event.widget).replace(".!button","")))-widgetoffset)
        if ((int(str(event.widget).replace(".!button","")))-widgetoffset) in selectedmines and next(value for name, value in cheats if name == "xrayenabled") == True:
            event.widget.config(image = "")
        event.widget.config(text = "🚩", relief = "ridge")
        if debug == True:
            print("Button pressed:",str(event.widget))
            print("Button pos:",((int(str(event.widget).replace(".!button","")))-widgetoffset))
            print("Marked tiles:",str(marked))
    elif event.widget.cget("state") != "disabled":
        event.widget.config(text = "X", relief = "groove")
        marked.remove((int(str(event.widget).replace(".!button","")))-widgetoffset)
        if debug == True:
            print(((int(str(event.widget).replace(".!button","")))-widgetoffset), "removed from marked tiles")
            print("Marked tiles:",str(marked))

def grid(sizex, sizey, sizet, minesslider):
    global debug
    global widgetoffset
    try:
        global extrasizebutton
        extrasizebutton.config(state = "disabled")
    except:
        pass
    global cheats
    global pastmines
    global gameactive
    gameactive = True
    global buttons
    buttons = []
    try:
        mines = minesslider.get()
        pastmines = mines
    except:
        mines = minesslider
        pastmines = mines
    if debug == True:
        print(sizex,"by",sizey,"grid with",str(mines),"mines")
    clearwindow()
    row = 1     # grid rows
    used = 0    # grid overflows to column
    window.grid_rowconfigure(index = 0, weight = 1)
    window.grid_columnconfigure(index = 0, weight = 1)
    window.grid_rowconfigure(index = sizey+1, weight = 1)
    window.grid_columnconfigure(index = sizex+1, weight = 1)
    for i in range(sizet):
        button = Button(window, text = "X", font = ("Arial", 20, "bold"), background = "#e8ecec", foreground = "#222e3c", relief = "groove", borderwidth = 5, width=1, height=1)    # images?
        if i == 0:
            widgetoffset = int(str(button).replace(".!button",""))
        button.bind("<Return>", mark)
        button.bind("<Button-2>", mark)
        button.bind("<Button-3>", mark)
        x=i
        y=0
        if used >= sizex:
            row+=1
            used = 0
        if i >= sizex*row:
            x-=sizex*row
            y+=1*row
            used+=1
        window.grid_rowconfigure(index = y+1, weight = 4)
        window.grid_columnconfigure(index = x+1, weight = 4)
        button.grid(column = x+1, row = y+1, sticky = "NSEW")
        buttons.append(button)
        button.config(command = lambda pos = i, x = x, y = y, button = button: click(pos, mines, x, y, sizex, sizey, sizet, button, buttons, False))
        if debug == True: # debug
            print(str(len(buttons)) + "/" + str(sizet),"buttons generated")
    window.padx = 50
    window.pady = 50
    window.grid_propagate(False)

def loose():
    global gameactive
    gameactive == False
    clearwindow()
    disabledevbuttons()
    wintext = Label(window, text = "YOU LOOSE!", font = ("Arial", 50, "bold")).pack(pady = (50,20))
    playagainbutton = Button(window, text = "Play Again", font = ("Arial", 25), relief = "groove", borderwidth = 2, command = lambda: restart()).pack()

def win():
    global gameactive
    gameactive == False
    clearwindow()
    disabledevbuttons()
    wintext = Label(window, text = "YOU WIN!", font = ("Arial", 50, "bold")).pack(pady = (50,20))
    playagainbutton = Button(window, text = "Play Again", font = ("Arial", 25), relief = "groove", borderwidth = 2, command = lambda: restart()).pack()
    
def resize(e):
    global gameactive
    global buttons
    try:
        if gameactive == True:
            if e.width >= e.height:
                for tiles in buttons:
                    tiles.config(font = ("Arial", int(e.height/3), "bold"))
            else:
                for tiles in buttons:
                    tiles.config(font = ("Arial", int(e.width/3), "bold"))
    except:
        pass

def Xray(selectedmines, buttons):
    global cheats
    global clickedbuttons
    global revealminesbutton
    try:
        if next(value for name, value in cheats if name == "xrayenabled") == True:
            cheats = [(name, False if name == "xrayenabled" else value) for name, value in cheats]
            print("Xray disabled")
            revealminesbutton.config(relief = "raised")
            iteration = 0
            for iteration, tiles in enumerate(buttons, start = 0):
                if iteration in selectedmines and iteration not in clickedbuttons:
                    tiles.config(image = "")
        else:
            cheats = [(name, True if name == "xrayenabled" else value) for name, value in cheats]
            print("Xray enabled")
            revealminesbutton.config(relief = "sunken")
            for iteration, tiles in enumerate(buttons, start = 0):
                if iteration in selectedmines and iteration not in clickedbuttons:
                        tiles.config(image = mineimagephoto)
    except NameError:
        pass

def sortmines(selectedmines):
    global sortedmineslabel
    try:
        sortedmines = str(sorted(selectedmines))
        sortedmines = sortedmines.replace("[","")
        sortedmines = sortedmines.replace("]","")
        devwindow.minsize(270,120+40(((len(selectedmines)//12)+1)*15)) # 40*buttons + 40 (text + spacing) (+12 (list of mines) +3 (line spacing))
        devwindow.maxsize(270,120+40(((len(selectedmines)//12)+1)*15))
        sortedmineslabel = Label(devwindow, text = "Mines ("+str(len(selectedmines))+"):\n"+ sortedmines, wraplength = 245)
        sortedmineslabel.pack(fill = BOTH, expand = True)
    except:
        pass

def customsize():
    print("Disables logs for lag")
    global debug
    global logbutton
    global custommaxgridsize
    global extrasizebutton
    debug = False # prevents lag due to prints taking up valuable time on main thread
    logbutton.config(relief = "raised")
    extrasizebutton.config(relief = "sunken", state = "disabled")
    clearwindow()
    customsizexslidertext = Label(window, text = "Horizontal Size").pack(pady=(10,0))
    customsizexslider = Scale(window, orient = "horizontal", from_ = 4, to = custommaxgridsize, cursor = "sb_h_double_arrow")
    customsizexslider.pack()
    customsizeyslidertext = Label(window, text = "Vertical Size").pack(pady=(40,0))
    customsizeyslider = Scale(window, orient = "horizontal", from_ = 4, to = custommaxgridsize, cursor = "sb_h_double_arrow")
    customsizeyslider.pack()
    tominessettingsbutton = Button(window, text = "NEXT", command = lambda: custommines(customsizexslider, customsizeyslider)).pack()

def custommines(customsizexslider, customsizeyslider):
    sizex = customsizexslider.get()
    sizey = customsizeyslider.get()
    sizet = sizex * sizey
    clearwindow()
    customminesslidertext = Label(window, text = "Number Of Mines In " + str(sizet) + " Tiles").pack()
    customminesslider = Scale(window, orient = "horizontal", from_ = 1, to = sizet-9, cursor = "sb_h_double_arrow")
    customminesslider.pack()
    customstartbutton = Button(window, text = "START", command = lambda: grid(sizex, sizey, sizet, customminesslider.get())).pack()

def disabledevbuttons():
    try:
        global revealminesbutton
        revealminesbutton.config(state = "disabled", relief = "raised")
        global logbutton
        logbutton.config(state = "disabled", relief = "raised")
    except:
        pass

def restart():
    global firstclick
    global debug
    global winstate
    global custommaxgridsize
    global clickedbuttons
    global selectedmines
    global marked
    global devwindow
    global cheats
    for t in range(custommaxgridsize+2):
        window.grid_rowconfigure(index = t, weight = 0)
        window.grid_columnconfigure(index = t, weight = 0)
    winstate = False
    firstclick = True
    clickedbuttons = []
    selectedmines = []
    marked = []
    if debug == True:
        print("New game")
        debug = False
    try:
        devwindow.destroy()
        devwindow = None
    except:
        pass
    try:
        cheats = [(name, False if name == "xrayenabled" else value) for name, value in cheats]
    except:
        pass
    sizesettings()

def clearwindow():
    for item in window.winfo_children():
        try:
            if item is not devwindow:
                item.destroy()
        except: # if devwindow isnt existing, after close its still targetable
            item.destroy()

window.bind("<Configure>", resize)

sizesettings()

window.mainloop()