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
    print(f"entering myFunction {e.window.get_str(e, 0)}")
    ans = ""
    for k in range(len(myGene.ou)):
        ans += "%d %d "%(myGene.ou[k],myGene.vals[k])
    return ans[:-1]; # suppression du ' ' final


myGene = geneControler()
connected = myGene.connect()

if connected != True:
    MyWindowErr = webui.window()
    MyWindowErr.show("controlGeneWebuiError.html",webui.browser.firefox)
    MyWindowErr.bind("getError", getError )
    webui.wait()
    exit(1)

MyWindow = webui.window()
MyWindow.show("controlGeneWebui.html",webui.browser.firefox)
MyWindow.bind("myFunction", myFunction) 

webui.wait()
# wrssdnuw_di
