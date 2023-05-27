import os
import shutil
from pathlib import Path
from PIL import Image #https://pillow.readthedocs.io/en/stable/reference/Image.html
import exifread #https://github.com/ianare/exif-py

pth = input("Bitte Pfad der Bilder eingben: ")
fail_pth = input("Bitte Pfad für fehlerhafte Bilder eingeben: ")
#speichert alle Elemente in einer Liste
entries = Path(pth)

#Listen um Zähler zu bestimmen
ctrl_date = []
ctrl_count = []

fail = 0
fail_lst = []

#Schleife über jedes Bild und füllen der Liste names
try:
    for entry in entries.iterdir():
        check = 0
        while(check == 0):
            try:
                img = open(pth+"\\"+entry.name, 'rb')#öffnen der Bilddatei
                check = 1
            except:
                shutil.move(pth+"\\"+entry.name,fail_pth+"\\"+entry.name)

        #exifdata = img.getexif() #Liste mit den Bild daten der Datei
        data = exifread.process_file(img,details=False)["EXIF DateTimeOriginal"]#exifdata.get(306)# Foto aufnahmedatum - s. https://exiv2.org/tags.html
        #print(data)
        #print(type(data))
        year = data.printable[:4]
        #print(year)
        month = data.printable[5:7]
        #print(month)
        day = data.printable[8:10]
        #print(day)
        #print(tag+":")
        datum = year+' '+month+' '+day

        #bestimmen des Zählers
        if(datum in ctrl_date): #wenn das datum in der Liste
            i = ctrl_date.index(datum)
            c = ctrl_count[i]+1
            ctrl_count[i] = c #speichern von i bei datum in control
            count = str(c).zfill(4)
        else: #sont füge es hinzu mit i = 0
            ctrl_date.append(datum)
            ctrl_count.append(0)
            count = str(0).zfill(4)
        #print(ctrl_date)
        #print(ctrl_count)
        img.close()

        #umbennen
        try:

            old = pth+"\\"+entry.name
            new = pth+"\\"+datum+'_i_'+count+'.JPG'
            if(old != new):
                os.rename(old,new)
                print(entry.name+": Done")
            else:
                print(entry.name+": alt = neu")
        except:
            fail = fail + 1
            fail_lst.append(entry.name)
            print("\_(#_#)_/")

    print(fail_lst)
    print("Fehler:"+str(fail))
except Exception as err:
    print("Error:",err)
    input("Eine Taste drücken um das Fenster zu schließen...")