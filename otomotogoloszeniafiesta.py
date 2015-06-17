import urllib.request
import smtplib
from datetime import datetime

u = 'http://otomoto.pl/osobowe/slaskie/ford/fiesta/mk7-2008/?search%5Bfilter_float_price%3Ato%5D=30000&search%5Bfilter_float_mileage%3Ato%5D=125000&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_float_door_count%3Afrom%5D=5&search%5Bfilter_enum_no_accident%5D=1&search%5Border%5D=filter_float_price%3Aasc'
f = urllib.request.urlopen(u)
contents = str(f.read())
f.close()
i = 0
j = 0
counter = 1
ilosc_olgoszen = 0
ilosc_nowych = 0
kryteria = 'kryteria: <strong>'
ogloszenia = '<h3 class="om-title"><a href="http://otomoto.pl/'
linkogl = 'http://otomoto.pl/'
lista = []
listaNowych = []
listaStarych = []
ogloszeniaOld = ('/home/pi/OtoMoToOgloszenia/ogloszeniaOldFiesta.txt')

def wczytajOgloszenia ():
    global u,i,j,contents,counter, ilosc_ogloszen, kryteria, ogloszenia, lista
    #while True:
    #    i = contents.find(kryteria, i)
    #    if i == -1:
    #        print ('Nie znaleziono')
    #        break
    #     print ('Znaleziono ogłoszeń:')
    #    end_ilosc = contents.find('<',i+18)
    #    ilosc_ogloszen = int(contents[i+18:end_ilosc])   
    #    print (ilosc_ogloszen)
    #    break
    while True:
        j = contents.find (ogloszenia, j)
        if j == -1:
            break
        koniec_linku = contents.find('>',j + len(ogloszenia))
        lista.insert(counter,  (linkogl + contents[j+len(ogloszenia):koniec_linku - 1]+ '\n'))
        j = koniec_linku 
        counter = counter + 1


def wczytajOgloszeniaOld ():
    global ogloszeniaOld
    plikOgloszeniaOld = open (ogloszeniaOld)
    line = plikOgloszeniaOld.readline()
    i = 0
    while line != '': 
        listaStarych.insert(i, line)
        line = plikOgloszeniaOld.readline()
        i = i + 1
    plikOgloszeniaOld.close()
#    print('Wczytano starych ogloszen: ' + str(i))


def zapiszOgloszeniaOld ():
    global ogloszeniaOld, lista
    i = 0
    plikOgloszeniaOld = open (ogloszeniaOld, 'w')
    for item in lista:
        plikOgloszeniaOld.write(item)
        i = i + 1
#    print ('Zapisano nowych rekordow: ' + str(i))
    plikOgloszeniaOld.close()


def sprawdzNowe ():
    global lista, listaStarych, listaNowych, ilosc_nowych
    i = 0
    for item in lista:
        try:
            index = listaStarych.index(item)
        except ValueError:
            listaNowych.insert(i,item)
            i = i+1

    ilosc_nowych  = i
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print (time+ ' Nowe ogloszenia:' + str(i))
    for item2 in listaNowych:
        print (item2)


def sendMail ():
    global listaNowych

    if len(listaNowych) < 1:
        return

    gmail_user = "raspberry.bencol@gmail.com"
    gmail_pwd = "Snowboard2"
    FROM = 'raspberry.bencol@gmail.com'
    TO = ['robert.gorecki@gmail.com'] #must be a list
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    SUBJECT = "Nowe Oglosznie z Otomoto z: " + time
    TEXT = "Lista Nowych Ogloszen: \n"
    i = 0    
    for item in listaNowych:
        i = i + 1
        TEXT = TEXT + str(i) + '. \t' + item + '\n'
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail at : ' + time)
    except:
        print ('failed to send mail at: ' + time)

print ('=====================================================================================')
wczytajOgloszenia()
wczytajOgloszeniaOld()
zapiszOgloszeniaOld()
sprawdzNowe()
sendMail()
print ('=====================================================================================\n')
