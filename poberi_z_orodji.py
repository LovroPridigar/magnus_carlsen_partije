import orodja
import re
import requests

STEVILO_STRANI = 129

seznam_slovarjev = []

vzorec_bloka = re.compile(r'class="master-games-clickable-link master-games-td-user".*?'
                          r'<tr class="master-games-master-game v-board-popover"', 
                          flags=re.DOTALL)

beli_crni = re.compile(r'<span class="master-games-username">'
                   r'(?P<ime1>.*?)'
                   r'</span>')

rating = re.compile(r'<span class="master-games-user-rating">'
                    r'(?P<rating>\(\d\d\d\d\))'
                    r'</span>')


id_igre = re.compile(r'class="master-games-clickable-link master-games-td-user".*?'
                     r'href="https://www.chess.com/games/view/(?P<id>\d*)"', flags=re.DOTALL)


st_potez = re.compile(r'href="https://www.chess.com/games/view/........".*?'
                      r'title="(?P<st_potez>\d{0,3})"', flags=re.DOTALL)

leto = re.compile(r'href="https://www.chess.com/games/view/........".*?'
                      r'title="(?P<st_potez>\d\d\d\d)"', flags=re.DOTALL)

rezultat = re.compile(r'href="https://www.chess.com/games/view/........".*?'
                      r'title="(?P<st_potez>.{1,8}-.{1,8})"', flags=re.DOTALL)

poteze = re.compile(r'href="https://www.chess.com/games/view/........".*?'
                    r'title="(?P<st_potez>1\..*?)">', flags=re.DOTALL)

najdeni_filmi = 0


for stran in range(STEVILO_STRANI):

    url = f'https://www.chess.com/games/search?fromSearchShort=1&p1=Magnus%20Carlsen&page={stran + 1}'
    datoteka = f'zbrani_podatki/carlsen_partije_{stran + 1}.html' 
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)
    
    seznam_rating = rating.findall(vsebina)[:]
    seznam_let = leto.findall(vsebina)[:]
    seznam_rezultat = rezultat.findall(vsebina)[:]
    seznam_st_potez = st_potez.findall(vsebina)[:]
    seznam_potez = poteze.findall(vsebina)[:]

    if len(id_igre.findall(vsebina)) * 2 != len(rating.findall(vsebina)):
        for i in range(40):
            seznam_rating.append(0)
    
    if len(id_igre.findall(vsebina)) * 2 != len(leto.findall(vsebina)):
        for i in range(40):
            seznam_let.append(0)
    
    if len(id_igre.findall(vsebina)) * 2 != len(rezultat.findall(vsebina)):
        for i in range(40):
            seznam_rezultat.append(0)                                               # trenutno je to resitev v sili, ki vodi do napacno obdelanih podatkov
    
    if len(id_igre.findall(vsebina)) * 2 != len(st_potez.findall(vsebina)):
        for i in range(40):
            seznam_st_potez.append(0)
    
    if len(id_igre.findall(vsebina)) * 2 != len(poteze.findall(vsebina)):
        for i in range(40):
            seznam_potez.append(0)

    for partija in range(len(id_igre.findall(vsebina))):
        slovar_podatkov = {}
        slovar_podatkov["id_igre"] = int(id_igre.findall(vsebina)[partija])
        slovar_podatkov["imena"] = f"{beli_crni.findall(vsebina)[2 * partija]} vs. {beli_crni.findall(vsebina)[2 * partija + 1]}"
        slovar_podatkov["rating"] = f"{seznam_rating[2*partija]} , {seznam_rating[2*partija + 1]}"
        slovar_podatkov["rezultat"] = f"{seznam_rezultat[partija]}"
        slovar_podatkov["st_potez"] = int(seznam_st_potez[partija])
        slovar_podatkov["leto"] = int(seznam_let[partija])
        slovar_podatkov["poteze"] = f"{seznam_st_potez[partija]}"
        seznam_slovarjev.append(slovar_podatkov)




orodja.zapisi_csv(seznam_slovarjev, ["id_igre", "imena", "rating", "rezultat", "st_potez", "leto", "poteze"], "obdelani_podatki/partije.csv")



