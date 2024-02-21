Control du générateur avec webui

Il y a 4 fichiers concernés:
- controlGeneWebui.py
- controlGeneWebui.html
- controlGeneWebui.css
- controlGeneWebui.js

Le script python qu'on lance (controlGeneWebui.py) contient le nom d'un
fichier html (controlGeneWebui.html) lié au fichier css(controlGeneWebui.css).

Rajouter au fichier html en haut après <body> le ligne:
<script src="/webui.js"></script>

De plus le fichier html scripte un fichier javascript (script.js).

Appel depuis powershell:
      C:\msys64\mingw64\bin\python.exe .\controlGeneWebui.py
Appel depuis msys2:
      /mingw64/bin/python controlGeneWebui.py
      ATTENTION:
      /usr/bin/python controlGeneWebui.py DONNE L'ERREUR
      webui_lib error: Unsupported OS
      Please download the latest webui_lib lib from https://webui.me

Remarque si on utilise /usr/bin/python on obtient l'erreur:
webui_lib error: Unsupported OS
Please download the latest webui_lib lib from https://webui.me


Le Fri Dec 15 20:38:16 CET 2023 Geoffroy passe : il déconseille webui car
c'est finalement un seul developpeur. Je décide de finir quand même en
prévoyant un timer javascript qui interroge le python a intervalle régulier
il faudrait doubler les cases modifiables pour avoir la valeur actuelle
et la valeur proposée avec un bouton pour envoyer les valeurs proposées.
Geoffroy conseille electronjs.org qui serait une solution 100% javascript.
Javascript a une librairie modbus. Electron encapsule le frontend et le
backend tous deux en js, et qui communique par IPC. Le "déploiement" est
bien prévu.


1) Le bouton generateur sert a mettre en chauffage DOIT ETRE FAIT EN PREMIER
2) Le bouton Gaz declenche le debit d'amorce NE PEUT ETRE FAIT QU'APRES 1)
3) Le bouton plasma debutte le process et NE PEUT ETRE FAIT QU'APRES 2)
