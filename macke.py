import re
import orodja

cene = []
naslovi = []
opisi = []

for stran in range(1,100):
    spletna_stran = 'https://www.kulinarika.net/recepti/seznam/?sort=popularnost&offset=72'
    naslov = '{}/recepti/seznam/?sort=popularnost&offset={}'.format(spletna_stran, (stran * 12))
    datoteka = 'ReceptiHTML/{:02}.html'.format(stran)
    orodja.shrani(naslov, datoteka)
#     with open(datoteka) as folder:
#         vsebina = folder.read()
#         for ujemanje in re.finditer("""class\=\"price\">.*?\<\/div\>""", vsebina):
#             cene.append(ujemanje)
#             print(ujemanje)
#         for ujemanje in re.finditer("""\<h3\>\<a title=\".*?\"""", vsebina):
#             naslovi.append(ujemanje)
#             print(ujemanje)
#         #for ujemanje in re.finditer("""""", vsebina):
#         #    opisi.append(ujemanje)
#         #    print(ujemanje)
# print("TEST")
# for i in range(len(naslovi)):
#     print(naslovi[i])
#     print(cene[i])

