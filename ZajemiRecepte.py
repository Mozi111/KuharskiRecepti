import re
import orodja

def zajemi_recepte():
    for i in range(0,100):
         spletna_stran = 'https://www.kulinarika.net/recepti/seznam/'
         parametri = '?sort=popularnost&offset={}'.format(i*12)
         naslov = spletna_stran + parametri
         ime_datoteke = 'ReceptiHTML/Stran{:02}.html'.format(i)
         orodja.shrani(naslov, ime_datoteke)

zajemi_recepte()

regex_recepta = re.compile(
          r'''<a href='/recepti/.*?' title='Objava recepta: (?P<objava>\d{0,2}\.\d{0,2}\.\d{0,4})<br>.*?'''
          r'''(Število mnenj: (?P<stmnenj>\d*).*?)?'''
          r'''(<br><br>Zadnja fotografija: (?P<zadnjafoto>\d{0,2}\.\d{0,2}\.\d{0,4}))?'''
          r'''(<br>Število fotografij: (?P<stfoto>\d*)'>)?'''
          r'''(<img src='.*?'></a>)?'''
          r'''</div><h3 class='single-line'>'''
          r'''(<img class='ikona-zdrav-recept tiptip' src='/grafika6/ikona-zdravo.png' title='(?P<zdravajed>.*?)' />)?'''
          r'''<a href='/recepti/(?P<id>\d*)/.*?' '''
          r'''title='Objava recepta: \d{0,2}\.\d{0,2}\.\d{0,4}(<br>Število mnenj: \d*)?'''
          r'''(<br><br>Zadnja fotografija: \d{0,2}\.\d{0,2}\.\d{0,4})?'''
          r'''(<br>Število fotografij: \d*)?'''
          r'''.?>(?P<naslov>.*?)</a>.*?'''
          r'''tezavnost'><img src='/grafika6/ikona-(?P<tezavnost1>.*?)\.png' alt='Zahtevnost' '''
          r'''title='zahtevnost'><img src='/grafika6/ikona-(?P<tezavnost2>.*?)\.png' alt='Zahtevnost' '''
          r'''title='zahtevnost'><img src='/grafika6/ikona-(?P<tezavnost3>.*?)\.png' alt='Zahtevnost' '''
          r'''title='zahtevnost'><img src='/grafika6/ikona-(?P<tezavnost4>.*?)\.png' alt='Zahtevnost' '''
          r'''title='zahtevnost'><img src='/grafika6/ikona-(?P<tezavnost5>.*?)\.png' alt='Zahtevnost'.*?'''
          r'''(<span class='cas'>(?P<priprava>.*?)</span></p>.*?)?'''
          r'''(kolicina: (?P<kolicina>.*?)</p></div>.*?)?'''
          r'''(<img class='spol' src='.*?' title='(?P<spol>.*?)'.*?)?'''
          r'''(a class='username' href='/uporabniki/seznam/(?P<idavtorja>.*?)/'>(?P<avtor>.*?)</a>.*?)?'''
          r'''<p class='kategorija no-mobile-640'>(?P<kategorija>.*?)(:\W(?P<podkategorija>.*?))?</p>'''
          ,flags=re.DOTALL)

def izloci_podatke_receptov(imenik):
     recepti = []
     for html_datoteka in orodja.datoteke(imenik):
          for recept in re.finditer(regex_recepta, orodja.vsebina_datoteke(html_datoteka)):
               recepti.append(pocisti_recept(recept))
     return recepti

def pocisti_recept(recept):
     podatki = recept.groupdict()
     podatki['id'] = int(podatki['id'])
     podatki['naslov'] = podatki['naslov'].strip()
     podatki['objava'] = str(podatki['objava'])
     # Ce je priprava v minutah, shrani kot stevilo
     # Ce je priprava 4+ ur shrani kot besedilo
     if podatki['priprava']:
         if podatki['priprava'].split()[1] != "ur":
             podatki['priprava'] = int(podatki['priprava'].split()[0])
     if podatki['stmnenj']:
        podatki['stmnenj'] = int(podatki['stmnenj'])
     if podatki['stfoto']:
        podatki['stfoto'] = int(podatki['stfoto'])
     #Prešteje zahtevnost recepta
     zahtevnost = 0
     for i in range(1,6):
         if podatki['tezavnost'+str(i)] == "utez":
             zahtevnost += 1
     podatki['zahtevnost'] = zahtevnost
     del podatki['tezavnost1']
     del podatki['tezavnost2']
     del podatki['tezavnost3']
     del podatki['tezavnost4']
     del podatki['tezavnost5']
     # Ce podatkov o bolj zdravi jedi ni
     #if not podatki['zdravajed']:
     #     podatki['zdravajed'] = "Ni podano"

     podatki['avtor'] = {'id': podatki['idavtorja'], 'avtor': podatki['avtor'], 'spol': podatki['spol']}
     del podatki['idavtorja']
     del podatki['spol']
     return podatki

def razdeli_tabelo(recepti):
     avtorji, kategorije, povezave = [], [], []
     viden_avtor = []

     for recept in recepti:
          if recept['kategorija']:
               if recept['podkategorija']:
                   kategorije.append({'recept': recept['id'], 'kategorija': recept['kategorija'],
                                      'podkategorija': recept['podkategorija']})
                   del recept['kategorija']
                   del recept['podkategorija']
               else:
                    kategorije.append({'recept': recept['id'], 'kategorija': recept['kategorija']})
                    del recept['kategorija']
                    del recept['podkategorija']
          avtor = recept['avtor']
          if avtor['id'] not in viden_avtor:
              viden_avtor.append(avtor['id'])
              avtorji.append(avtor)
          povezave.append({'recept': recept['id'], 'avtor': avtor['id']})
          del recept['avtor']
     return recepti, avtorji, kategorije, povezave

recepti = izloci_podatke_receptov('ReceptiHTML/')
recepti, avtorji, kategorije, povezave = razdeli_tabelo(recepti)
orodja.zapisi_tabelo(recepti, ['id', 'naslov', 'objava', 'letoobjave', 'zahtevnost', 'priprava', 'kolicina', 'stmnenj', 'stfoto',
                      'zadnjafoto', 'letofoto', 'zdravajed'], 'ReceptiCSV/recepti.csv')
orodja.zapisi_tabelo(avtorji, ['id', 'avtor', 'spol'], 'ReceptiCSV/avtorji.csv')
orodja.zapisi_tabelo(povezave, ['recept', 'avtor'], 'ReceptiCSV/povezave.csv')
orodja.zapisi_tabelo(kategorije, ['recept', 'kategorija', 'podkategorija'], 'ReceptiCSV/kategorije.csv')
print("Končano!")