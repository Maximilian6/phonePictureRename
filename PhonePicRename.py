import os
import shutil
from pathlib import Path
from PIL import Image #https://pillow.readthedocs.io/en/stable/reference/Image.html
from PIL.ExifTags import TAGS #https://www.thepythoncode.com/article/extracting-image-metadata-in-python

#path to the pictures
pth = "C:\\pics" #<- insert path here 
fail_pth = "C:\\pics_fail"
#saves all Elements in a list
entries = Path(pth)

#lists to determine counter
ctrl_date = []
ctrl_count = []

fail = 0
fail_lst = []

#Loop over each picture to fill the lists of names
for entry in entries.iterdir():
    check = 0
    while(check == 0):
        try:
            img = Image.open(pth+"\\"+entry.name) #open picture file
            check = 1
        except:
            shutil.move(pth+"\\"+entry.name,fail_pth+"\\"+entry.name)

    exifdata = img.getexif() #list with exif data
    data = exifdata.get(306) #Creation date - tag_id
    year = data[:4]
    #print(year)
    month = data[5:7]
    #print(month)
    day = data[8:10]
    #print(day)
    #print(tag+":")
    datum = year+' '+month+' '+day

    #determine the counters
    if(datum in ctrl_date): #if date is in the list
        i = ctrl_date.index(datum)
        c = ctrl_count[i]+1
        ctrl_count[i] = c #save i at date in control
        count = str(c).zfill(4)
    else: #else add it to the list with i=0
        ctrl_date.append(datum)
        ctrl_count.append(0)
        count = str(0).zfill(4)
    #print(ctrl_date)
    #print(ctrl_count)
    img.close()


    #rename
    try:
        print(entry.name+": Done")
        old = pth+"\\"+entry.name
        new = pth+"\\"+datum+'_i_'+count+'.JPG'
        if(old != new):
            os.rename(old,new)

    except:
        print("Fail!")
        fail = fail + 1
        fail_lst.append(entry.name)

print(fail_lst)
print("Number of failed Pictures:"+str(fail))
