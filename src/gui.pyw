import easygui
import sys, os



def kill_shells():
    ch=" "
    for c in child:
        ch=ch+str(c.pid)
    s="os\\kill1.bat"+ch
    print s
    os.system(s)
    
    

def main_func():
    k=True
    
    # when debugging in wing ide comment the above line
    while k:
        ch=easygui.indexbox("SWMM 5 Evolutionary Algorithm\n Assela Pathirana (2012)\n Running at:"+os.getcwd(),image="gui\logo2.gif", choices=["Project directory","Shell","Stop","Close-Plots","About", "Exit"])
        print ch
        about="""
    About SWMM5-EA
    SWMM5 EA was written by Assela Pathirana 
    for the original purpose of demonstrating 
    the application of evolutionary algorithms 
    in urban drainage. 
    
    The code of EPA SWMM 5 and the optimization library
    inspyred (inspyred: Bio-inspired Algorithms in Python) 
    are used to build this package. 
    There are numerous othr python modules used 
    in this product. 
    
    Feel free to distribute this to anyone 
    as long as you don't ask anything in return. 
    Can be downloaded at 
    http://assela.pathirana.net/SWMM5-EA
    assela @ pathirana.net
    """
        if ch==4:
            easygui.buttonbox(about, image="gui\logo.gif", choices=["OK"])
        if ch==5:
            if("Yes"==easygui.buttonbox("Do you want to exit (Will close all running simulations, plot windows etc.?", choices=["Yes","No!"])):
                kill_all()
                k=False    
        if ch==0:
            os.startfile(os.getcwd()+os.sep+"projects")
        if ch==1:
            import subprocess
            #os.system("dos.bat")
            child.append(subprocess.Popen("cmd os\\dos.bat"))
        if ch==2:

            if("OK"==easygui.buttonbox("This will kill any running optimizations",  choices=["OK","Cancel!"])):
                ch = kill_shells()
        if ch==3:
            if("OK"==easygui.buttonbox("This close all the plot windows",  choices=["OK","Cancel!"])):
                kill_gnuplot()


  
def kill_gnuplot():
    os.system("os\\kill2.bat")

def kill_all():
    kill_shells()
    kill_gnuplot()

if __name__ == "__main__":
    global child
    child=[]
    os.chdir("..") # this is for the benefit of the installed program. Will make running withint the project problematic. 
    main_func()
