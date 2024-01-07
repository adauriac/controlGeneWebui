from controlGenePyCli import *
from webui import webui

"""
example d'acces aux registres de la carte + webui = LA TOTALE
"""

def getError(e : webui.event):
    global connected
    print(f"from python {connected} ")
    return connected

def myFunction(e : webui.event):
    global myGene
    print(f"entering myFunction with {e.window.get_str(e, 0)} |")
    if not myGene.watched:
        return "error"
    myGene.getRegisters()
    ans = ""
    for k in range(len(myGene.ou)):
        ans += "%d %d "%(myGene.ou[k],myGene.vals[k])
    print("python says I will return "+ans[:-1])
    return ans[:-1]; # suppression du ' ' final

def errorTreatement(input):
    global MyWindow
    print("errorTreatement entering with %s !"%input)
    MyWindow.script('alert("Lost connection");window.close();');

myGene = geneControler(errorTreatement)
connected = myGene.connect()

if connected != True:
    MyWindowErr = webui.window()
    MyWindowErr.show("controlGeneWebuiError.html",webui.browser.firefox)
    MyWindowErr.bind("getError", getError )
    webui.wait()
    exit(1)
eG=""
MyWindow = webui.window()
MyWindow.show("controlGeneWebui.html",webui.browser.firefox)
MyWindow.bind("myFunction", myFunction) 

webui.wait()
# wrssdnuw_di
