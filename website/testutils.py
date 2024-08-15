file = open("tablecount.bin", "rb").read()
tablecount = int(file)
print(tablecount)
email = 'table'+str(tablecount)+'@gmail.com'
username = 'Masa '+str(tablecount)
password = 'Masa'+str(tablecount)

import qrcode
img = qrcode.make('https://localhost/masa'+str(tablecount))
type(img)  # qrcode.image.pil.PilImage
imgname="masa"+str(tablecount)+".png"
img.save(imgname)

tablecount= tablecount+1
print(tablecount)
tablecount=bytes(str(tablecount), encoding="utf-8")
with open("tablecount.bin", "wb") as file:
    file.write(tablecount)
    print(tablecount)
file.close()
