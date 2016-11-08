# Kuharski recepti

Za projektno nalogo sem s strani [kulinarika.net](https://www.kulinarika.net) zbral prvih 1200 receptov po popularnosti.

Podatki so ločeni v štiri csv datoteke:
* recepti.csv
* kategorije.csv
* avtorji.csv
* povezave.csv

## Zbrani podatki
Recepti vsebujejo:
* id recepta
* naslov
* datum objave
* zahtevnost (1 = najlažje, 5 = najtežje)
* čas priprave
* kolicino hrane
* število mnenj
* število fotografij
* datum zadnje fotografije
* ali je jed bolj zdrava

Kategorije vsebujejo:
* id recepta
* kategorija
* podkategorija

Avtorji vsebujejo:
* id avtorja
* ime avtorja
* spol avtorja

Povezave vsebujejo:
* id recepta
* id avtorja

### Cilj
Analiziral bom recepte.