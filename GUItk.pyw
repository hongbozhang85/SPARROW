#coding=utf-8
#!/usr/bin/python
'''
GUI(tkinter) of SPARROW
copyright Hong-Bo Zhang
Using tk_menuBar and Menubutton, obsolete since Tk 4.0
'''

from Tkinter import *
import re
import os
import tkFont
import tkFileDialog
import tkMessageBox
#from ttk import *
import DataClass
import OutputMolecules
import Reactions


##control paramters##
FullScreenOpt = 'N'
GeomWin = '800x500'
sideButImaSize = [215,111] # 111*4 = 444, so the width of root ~ 500
# bgImage 600x450
#####################

class Select(Frame):
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.label = Button(self, master,text="Filename:",command=self.filedialogpopup)#,relief='groove') 
        self.entry = Entry(self,master,width=40)  
        self.label.grid(row=0, column=0, sticky=N)  
        self.entry.grid(row=0, column=1, sticky=N)  
        self.pack()
    def filedialogpopup(self): 
        filename = tkFileDialog.askopenfilename(defaultextension='log',filetypes=[('log','*.log'),('out','*.out')])
        return filename

def MainWindow():
    global mainbodyFrame, root, bgImage
    mainbodyFrame.destroy()
    mainbodyFrame = Frame(root)#,bg='red')
    mainbodyFrame.pack(fill=BOTH,expand=1)
    #bgImage = PhotoImage(file='./icon/MolLarge.gif') # chang image
    Label(mainbodyFrame,image=bgImage,width=(winsizewid-sideButImaSize[1])).place(x=0,y=0,relwidth=1,relheight=1)#.pack(fill=X)
    Label(mainbodyFrame,text='Welcome to SPARROW',font=("Courier" ,10, "bold"),relief='flat',width=(winsizewid-sideButImaSize[1])).pack(fill=X) 
    MainHelpText = '''\nSystematical Python Assistant for Reaction Rate cOefficient Widget.
                     \n Click the "A Single Molecule" or "A Single PES" 
                     \non the left side. For "A Single PES" widget, a folder with the 
                     \nlog/out files of all the molecules on the PES should be placed  
                     \nunder ./Gaussian, where ./ is the directory of inifile with the
                     \nreaction information of the PES'''
    AuthorText = '''\nHong-Bo Zhang   hongbozhang@tsinghua.edu.cn'''
    #Label(mainbodyFrame).pack()
    Label(mainbodyFrame,text=MainHelpText,font=('Courier',10),anchor=W).pack()
    Label(mainbodyFrame,text=AuthorText,font=('Courier',10),anchor=W).pack()

def MainMenu():
    MainMenu_btn = Menubutton(menuFrame, text='Main', underline=0)
    MainMenu_btn.pack(side=LEFT, padx="2m")
    MainMenu_btn.menu = Menu(MainMenu_btn)
    MainMenu_btn.menu.add_command(label="Main Window", underline=0,command =MainWindow) 
    MainMenu_btn['menu'] = MainMenu_btn.menu
    return MainMenu_btn

def MolMenu():
    MolMenu_btn = Menubutton(menuFrame, text='Molecule', underline=0)
    MolMenu_btn.pack(side=LEFT, padx="2m")
    MolMenu_btn.menu = Menu(MolMenu_btn)
    MolMenu_btn.menu.add_command(label="KeyParams", underline=0)#,command = 
    MolMenu_btn.menu.add_command(label="LaTeX", underline=0) #,command =
    MolMenu_btn['menu'] = MolMenu_btn.menu
    return MolMenu_btn

def ReaMenu():
    ReaMenu_btn = Menubutton(menuFrame, text='Reaction', underline=0)
    ReaMenu_btn.pack(side=LEFT, padx="2m")
    ReaMenu_btn.menu = Menu(ReaMenu_btn)
    ReaMenu_btn.menu.add_command(label="KeyParams", underline=0)#,command =
    ReaMenu_btn.menu.add_command(label="LaTeX", underline=0) #,command =
    ReaMenu_btn.menu.add_separator()
    ReaMenu_btn.menu.add_command(label="Thermo", underline=0) #,command =
    ReaMenu_btn.menu.add_command(label="MESMER", underline=0) #,command =
    ReaMenu_btn.menu.add_command(label="MultiWell", underline=0) #,command =
    ReaMenu_btn.menu.add_separator()
    ReaMenu_btn.menu.add_command(label="Mathematica", underline=0) #,command =
    ReaMenu_btn.menu.add_separator()
    ReaMenu_btn.menu.add_command(label="MultiWellOnly", underline=0,command =InDeveloping) #
    ReaMenu_btn.menu.add_command(label="DensumOnly", underline=0,command =InDeveloping) #
    ReaMenu_btn['menu'] = ReaMenu_btn.menu
    return ReaMenu_btn

def SysMenu():
    SysMenu_btn = Menubutton(menuFrame, text='Systems', underline=0)
    SysMenu_btn.pack(side=LEFT, padx="2m")
    SysMenu_btn.menu = Menu(SysMenu_btn)
    SysMenu_btn.menu.add_command(label="KeyParams", underline=0,command =InDeveloping) #
    SysMenu_btn.menu.add_command(label="LaTeX", underline=0,command =InDeveloping) #
    SysMenu_btn.menu.add_separator()
    SysMenu_btn.menu.add_command(label="Thermo", underline=0,command =InDeveloping) #
    SysMenu_btn.menu.add_command(label="MESMER", underline=0,command =InDeveloping) #
    SysMenu_btn.menu.add_command(label="MultiWell", underline=0,command =InDeveloping) #
    SysMenu_btn.menu.add_separator()
    SysMenu_btn.menu.add_command(label="MultiWellOnly", underline=0,command =InDeveloping) #
    SysMenu_btn.menu.add_command(label="DensumOnly", underline=0,command =InDeveloping) #
    SysMenu_btn['menu'] = SysMenu_btn.menu
    return SysMenu_btn

def DocMenu():
    DocMenu_btn = Menubutton(menuFrame, text='Documentation', underline=0)
    DocMenu_btn.pack(side=LEFT, padx="2m")
    DocMenu_btn.menu = Menu(DocMenu_btn)
    DocMenu_btn.menu.add_command(label="LaTeX:Molecule", underline=0,command =InDeveloping) #
    DocMenu_btn.menu.add_command(label="LaTeX:Reaction", underline=0,command =InDeveloping) #
    DocMenu_btn.menu.add_command(label="LaTeX:Systems", underline=0,command =InDeveloping) #
    DocMenu_btn.menu.add_separator()
    DocMenu_btn.menu.add_command(label="JMol:Image", underline=0,command =InDeveloping) #
    DocMenu_btn.menu.add_command(label="JMol:Movie", underline=0,command =InDeveloping) #
    DocMenu_btn.menu.add_separator()
    DocMenu_btn.menu.add_command(label="docs?", underline=0,command =InDeveloping) #
    DocMenu_btn.menu.add_command(label="xls?", underline=0,command =InDeveloping) #
    DocMenu_btn['menu'] = DocMenu_btn.menu
    return DocMenu_btn

def HelMenu():
    HelMenu_btn = Menubutton(menuFrame, text='Help', underline=0)
    HelMenu_btn.pack(side=LEFT, padx="2m")
    HelMenu_btn.menu = Menu(HelMenu_btn)
    HelMenu_btn.menu.add_command(label="Help", underline=0,command =InDeveloping) #
    HelMenu_btn.menu.add_command(label="About", underline=0,command =InDeveloping) #
    HelMenu_btn['menu'] = HelMenu_btn.menu
    return HelMenu_btn

def QuiMenu():
    QuiMenu_btn = Menubutton(menuFrame, text='Quit', underline=0)
    QuiMenu_btn.pack(side=LEFT, padx="2m")
    QuiMenu_btn.menu = Menu(QuiMenu_btn)
    QuiMenu_btn.menu.add_command(label="Quit", underline=0,command = root.destroy)
    QuiMenu_btn['menu'] = QuiMenu_btn.menu
    return QuiMenu_btn

def InDeveloping():
    global mainbodyFrame, root, bgImage
    mainbodyFrame.destroy()
    mainbodyFrame = Frame(root)#,bg='red')
    mainbodyFrame.pack(fill=BOTH,expand=1)
    #bgImage = PhotoImage(file='./icon/MolLarge.gif') # chang image
    Label(mainbodyFrame,image=bgImage,width=(winsizewid-sideButImaSize[1])).place(x=0,y=0,relwidth=1,relheight=1)#.pack(fill=X)
    Label(mainbodyFrame,text='\nWelcome to SPARROW\n',font=("Courier" ,10, "bold"),relief='flat',width=(winsizewid-sideButImaSize[1])).pack(fill=X)
    Label(mainbodyFrame,text='In Developing',font=("Courier",20,"bold")).pack(expand=1)

def filedialogpopup1():
    global FilButEntry
    FilButEntry.delete(0,END)
    filename = tkFileDialog.askopenfilename(defaultextension='log',filetypes=[('log','*.log'),('out','*.out')])
    if filename:
        FilButEntry.insert(0,filename)

def filedialogpopup2():
    global FilButEntry
    FilButEntry.delete(0,END)
    filename = tkFileDialog.askopenfilename(defaultextension='ini',filetypes=[('ini','*.ini')])
    if filename:
        FilButEntry.insert(0,filename)

def MolMain():
    global FilButEntry,mainbodyFrame,var1,var2
    filename = FilButEntry.get()
    if filename == '':
        tkMessageBox.askokcancel(title='SPARROW: File error',message='Click Filename button and choose a file',default='ok')
    elif not os.path.isfile(filename):
        tkMessageBox.askokcancel(title='SPARROW: File error',message=filename+' does not exist',default='ok')
    else:
        path = os.path.dirname(filename)
        prefix = re.sub('\.(\w+)','',os.path.basename(filename))
        Mol = DataClass.MoleculeClass(path,prefix)
        Mol.ReadGaussian(0)
        if var1.get() == 'NO' and var2.get() =='NO':
            tkMessageBox.askokcancel(title='SPARROW: Checkbutton error',message='Choose KeyParams or/and LaTeX',default='ok')            
        if var1.get() == 'YES':
            OutputMolecules.WriteMolintoFile(Mol)
            temp1=Label(mainbodyFrame,text=filename+' has been read. '+prefix+'.params has(ve) been generated')
            #temp1.pack(side=TOP)
        if var2.get() == 'YES':
            OutputMolecules.WriteSupInfoLaTeX(Mol)
            temp2=Label(mainbodyFrame,text=filename+' has been read. '+prefix+'.tex has(ve) been generated')
            #temp2.pack(side=TOP)
    
    
def MolButCommand():
    global mainbodyFrame, root, bgImage,FilButEntry,var1,var2,bgImage
    mainbodyFrame.destroy()
    mainbodyFrame = Frame(root)#,bg='red')
    mainbodyFrame.pack(fill=BOTH,expand=1)
    #bgImage = PhotoImage(file='./icon/MolLarge.gif') # chang image
    Label(mainbodyFrame,image=bgImage,width=(winsizewid-sideButImaSize[1])).place(x=0,y=0,relwidth=1,relheight=1)#.pack(fill=X)
    Label(mainbodyFrame,text='Welcome to SPARROW',font=("Courier" ,10, "bold"),relief='flat',width=(winsizewid-sideButImaSize[1])).pack(fill=X) 
    MolHelpText = '\nThis widget is useful to read, extract and output\nall the key informations from a Gaussian log/out file.\n'
    #Label(mainbodyFrame).pack()
    Label(mainbodyFrame,text=MolHelpText,font=('Courier',10)).pack()
    Label(mainbodyFrame).pack()
    fileFrame = Frame(mainbodyFrame)
    fileFrame.pack(fill=X,expand=0)
    Button(fileFrame,text="Filename:",command=filedialogpopup1,relief='groove',width=15).grid(row=0, column=0, sticky=N) 
    FilButEntry = Entry(fileFrame,width=60)
    FilButEntry.grid(row=0, column=1, sticky=N) 
    #filename = tkFileDialog.askopenfilename(parent=mainbodyFrame,defaultextension='log',filetypes=[('log','*.log'),('out','*.out')])
    var1 = StringVar()
    var2 = StringVar()
    var1.set('YES')
    var2.set('YES')
    Label(mainbodyFrame).pack()
    Checkbutton(mainbodyFrame,state='normal',text="Key Parameters under /KeyParams",variable=var1,onvalue='YES',offvalue='NO').pack(anchor=W)
    Checkbutton(mainbodyFrame,text="LaTeX: tex, pdf, div and ps format under /SupInfo/LaTeX",variable=var2,onvalue='YES',offvalue='NO').pack(anchor=W)
    Label(mainbodyFrame).pack(side=BOTTOM)
    Label(mainbodyFrame).pack(side=BOTTOM)
    Button(mainbodyFrame,text='Ok',command=MolMain,relief='groove',width=15).pack(anchor = SE,side=BOTTOM)

def ReaMain():
    global FilButEntry,mainbodyFrame,var3
    filename = FilButEntry.get()
    if filename == '':
        tkMessageBox.askokcancel(title='SPARROW: File error',message='Click Filename button and choose a file',default='ok')
    elif not os.path.isfile(filename):
        tkMessageBox.askokcancel(title='SPARROW: File error',message=filename+' does not exist',default='ok')
    else:
        path = os.path.dirname(filename)
        prefix = re.sub('\.(\w+)','',os.path.basename(filename))
        logicbuffer = 'False'
##        for i in range(7):
##            if var3[i].get()=='YES':
##                templogic = 'True'
##            else:
##                templogic = 'False'
##            logicbuffer = (logicbuffer and templogic)
##        if logicbuffer == 'False':
##            tkMessageBox.askokcancel(title='SPARROW: Checkbutton error',message='Choose one or more options',default='ok')
        if var3[0].get()=='NO' and var3[1].get()=='NO' and var3[2].get()=='NO' and var3[3].get()=='NO' and var3[4].get()=='NO' and var3[5].get()=='NO' and var3[6].get()=='NO':
            tkMessageBox.askokcancel(title='SPARROW: Checkbutton error',message='Choose one or more options',default='ok')
        else:
            React = Reactions.ReactionsIniClass(filename)
            if var3[0].get()=='YES':
                React.OutputReactions()
            if var3[1].get()=='YES':
                React.WriteSupInfoLaTexReactions()
            if var3[2].get()=='YES':
                React.WriteMathematica()
            if var3[3].get()=='YES':
                React.WriteThermo()
            if var3[4].get()=='YES':
                React.WriteDensum()
            if var3[5].get()=='YES':
                React.WriteMultiWell()
            if var3[6].get()=='YES':
                React.WriteMESMER()
            Label(mainbodyFrame,text=filename+' finished.')

def ReaButCommand():
    global mainbodyFrame,root,bgImage,FilButEntry, var3,bgImage
    mainbodyFrame.destroy()
    mainbodyFrame = Frame(root)#,bg='red')
    mainbodyFrame.pack(fill=BOTH,expand=1)
    #bgImage = PhotoImage(file='./icon/MolLarge.gif') # chang image
    Label(mainbodyFrame,image=bgImage,width=(winsizewid-sideButImaSize[1])).place(x=0,y=0,relwidth=1,relheight=1)#.pack(fill=X)
    Label(mainbodyFrame,text='Welcome to SPARROW',font=("Courier" ,10, "bold"),relief='flat',width=(winsizewid-sideButImaSize[1])).pack(fill=X)
    ReaHelpText = 'For a give PES, this widget read and output key informations,\nincluding *.params and *.tex of all the molecules on the PES,\nand sequently generate the input file for PES.nb, Thermo(both Keq\nand CTST), Densum, MultiWell and MESMER'
    #Label(mainbodyFrame).pack()
    Label(mainbodyFrame,text=ReaHelpText,font=('Courier',10)).pack()
    Label(mainbodyFrame).pack()
    fileFrame = Frame(mainbodyFrame)
    fileFrame.pack(fill=X,expand=0)
    Button(fileFrame,text="Filename:",command=filedialogpopup2,relief='groove',width=15).grid(row=0, column=0, sticky=N) 
    FilButEntry = Entry(fileFrame,width=60)
    FilButEntry.grid(row=0, column=1, sticky=N)
    var3 = [StringVar() for i in range(7)]
    for i in range(7):
        var3[i].set('YES')
    Label(mainbodyFrame).pack()
    Checkbutton(mainbodyFrame,text="Key Parameters under /KeyParams",variable=var3[0],onvalue='YES',offvalue='NO').pack(anchor=W)
    Checkbutton(mainbodyFrame,text="LaTeX: tex, pdf, div and ps format under /SupInfo/LaTeX",variable=var3[1],onvalue='YES',offvalue='NO').pack(anchor=W)
    Checkbutton(mainbodyFrame,text="Mathematica: plotting PES under /PES",variable=var3[2],onvalue='YES',offvalue='NO').pack(anchor=W)
    Checkbutton(mainbodyFrame,text="Thermo: both Keq and CTST under /Thermo",variable=var3[3],onvalue='YES',offvalue='NO').pack(anchor=W)
    Checkbutton(mainbodyFrame,text="DENSUM: density of state and a batch under /MultiWell/Densum",variable=var3[4],onvalue='YES',offvalue='NO').pack(anchor=W)
    Checkbutton(mainbodyFrame,text="MultiWell: MultiWell input under /MultiWell",variable=var3[5],onvalue='YES',offvalue='NO').pack(anchor=W)
    Checkbutton(mainbodyFrame,text="MESMER: MESMER input under /MESMER",variable=var3[6],onvalue='YES',offvalue='NO').pack(anchor=W)
    Label(mainbodyFrame).pack(side=BOTTOM)
    Label(mainbodyFrame).pack(side=BOTTOM)
    Button(mainbodyFrame,text='Ok',command=ReaMain,relief='groove',width=15).pack(anchor = E,side=BOTTOM)
##    
#############################main###################

root = Tk()
# title and geometry
if FullScreenOpt == 'Y':
    root.geometry(str(root.winfo_screenwidth())+'x'+str(root.winfo_screenheight()))
    root.overrideredirect(1)
    titleFrame = Frame(root)#.pack(fill=X,expand=0)
    Label(titleFrame,text="SPARROW: Systematical Python Assistant for Reaction Rate cOefficient Widget").pack()
    titleFrame.pack(fill=X,expand=1)    
else:
    root.geometry(GeomWin)
    winsizewid = int(re.sub('x(\d+)','',re.sub('\'','',GeomWin)))
    winsizehei = int(re.sub('(\d+)x','',re.sub('\'','',GeomWin)))
    root.minsize(winsizewid,winsizehei) 
    root.maxsize(winsizewid,winsizehei)
    root.overrideredirect(0)
    root.title('SPARROW: Systematical Python Assistant for Reaction Rate cOefficient Widget')
root.attributes('-alpha',0.82)

# menubar
menuFrame = Frame(root)
menuFrame.pack(fill=X,expand=0,anchor=N)
  #Button(menuFrame,text='Main',command=MainWindow).pack()
menuFrame.tk_menuBar(MainMenu(),MolMenu(),ReaMenu(),SysMenu(),DocMenu(),HelMenu(),QuiMenu())

# side button
sideFrame = Frame(root)#,bg='red')
sideFrame.pack(fill=Y,expand=0,side=LEFT,anchor=W) # side=RIGHT
MolButtImg=PhotoImage(file="./icon/MolSmall.gif") # change image
MolButt = Button(sideFrame,text='A Single\nMolecule',font=tkFont.Font(font=("Courier", 20, "bold")),relief='groove',compound='center',image=MolButtImg,command=MolButCommand)
MolButt.pack(fill=X,expand=1)
ReaButtImg=PhotoImage(file="./icon/ReaSmall.gif") # change image
ReaButt = Button(sideFrame,text='A Single PES',font=tkFont.Font(font=("Courier", 20, "bold")),relief='groove',compound='center',image=ReaButtImg,command=ReaButCommand)
ReaButt.pack(fill=X,expand=1)
SysButtImg=PhotoImage(file="./icon/SysSmall.gif") # change image
SysButt = Button(sideFrame,text='A set of PESs',font=tkFont.Font(font=("Courier", 20, "bold")),relief='groove',compound='center',image=SysButtImg,command =InDeveloping) #
SysButt.pack(fill=X,expand=1)
DocButtImg=PhotoImage(file="./icon/DocSmall.gif") # change image
DocButt = Button(sideFrame,text='Supporting\nInformations',font=tkFont.Font(font=("Courier", 20, "bold")),relief='groove',compound='center',image=DocButtImg,command =InDeveloping) #
DocButt.pack(fill=X,expand=1)

# mainbody frame
mainbodyFrame = Frame(root)#,bg='red')
mainbodyFrame.pack(fill=BOTH,expand=1)
bgImage = PhotoImage(file='./icon/bg.gif') # chang image
Label(mainbodyFrame,image=bgImage,width=(winsizewid-sideButImaSize[1])).place(x=0,y=0,relwidth=1,relheight=1)#.pack(fill=X)
Label(mainbodyFrame,text='Welcome to SPARROW',font=("Courier" ,10, "bold"),relief='flat',width=(winsizewid-sideButImaSize[1])).pack(fill=X)
MainHelpText = '''\nSystematical Python Assistant for Reaction Rate cOefficient Widget.
                 \n Click the "A Single Molecule" or "A Single PES" 
                 \non the left side. For "A Single PES" widget, a folder with the 
                 \nlog/out files of all the molecules on the PES should be placed  
                 \nunder ./Gaussian, where ./ is the directory of inifile with the
                 \nreaction information of the PES'''
AuthorText = '''\nHong-Bo Zhang   hongbozhang@tsinghua.edu.cn'''
#Label(mainbodyFrame).pack()
Label(mainbodyFrame,text=MainHelpText,font=('Courier',10),anchor=W).pack()
Label(mainbodyFrame,text=AuthorText,font=('Courier',10),anchor=W).pack()

#print root.pack_slaves()
root.mainloop()

#############################Debug####################
##SparrowTopMenu = Menu(menuFrame)
##SparrowMenu = ["MolMenu","ReaMenu","SysMenu","DocMenu","HelMenu","QuiMenu"]
##for i in SparrowMenu:
##    i = Menu()
##i = 0
##for item in ['Molecule','Reaction','System','Document','Help','Quit']:
##    SparrowTopMenu.add_cascade(label=item,menu=SparrowMenu[i])
##    i = i + 1
##del i
