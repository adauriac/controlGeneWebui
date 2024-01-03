from controlGenePyCli import *
from webui import webui

"""
example d'acces aux registres de la carte + webui = LA TOTALE
"""

def my_function2(e : webui.event):
    global myGene
    print(f"entering my_function2 {e.window.get_str(e, 0)}")
    ans = ""
    for k in range(len(myGene.ou)):
        ans += "%d %d "%(myGene.ou[k],myGene.vals[k])
    return ans[:-1]; # suppression du ' ' final

def my_function(e:webui.event):
    global myGene
    k = myGene.index["Puissance limite basse"] 
    ans = myGene.vals[0]
    print(f"hello from python {e} k= {k}, ans={ans}")
    print(f"e.bind_id {e.bind_id}")
    print(f"e.element {e.element}")
    print(f"e.event_num {e.event_num}")
    print(f"e.event_type {e.event_type}")
    print(f"e.window {e.window}")
    return ans

myGene = geneControler()
connected = myGene.connect()

MyWindow = webui.window()
if connected==True:
    MyWindow.show("controlGeneWebui.html",webui.browser.firefox)
else:
    MyWindow.show("controlGeneWebuiError.html",webui.browser.firefox)
    exit(1)

# MyWindow.bind("powerLowLimit", my_function)
# MyWindow.bind("powerHighLimit", my_function)
MyWindow.bind("my_function2", my_function2) # Geoffroy a prpose ca
MyWindow.bind("go", my_function)
webui.wait()
# wrssdnuw_di
