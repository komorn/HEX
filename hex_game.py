"""Hra HEX je hra dvoch hracov, ktory sa snazia spojit dve protilahle strany. Hraci sa v tahoch striedaju
a kazdy vzdy zafarbi jedno policko. Tah je nevratny a obsadene policko sa neda prefarbit.
Hra konci vyhrou jedneho z hracov - nikdy nie remizou.

Hracia plocha hry je 6x6 policok.

V hre sa striedaju hrac W(pouzivatel) a hrac B(pocitac).

Pouzivatel sa snazi spojit lavy okraj hracieho pola s pravym okrajom.

Pocitac sa snazi spojit horny okraj hracieho pola s lavym okrajom."""

print("HRA HEX".center(70, "-"))

pocet_riadkov = 6
pocet_stlpcov = 6
max_hlbka = 8                   #do akej hlbky prehladava cesty hraca W

hodnoty = [[[500, 0] for j in range(pocet_stlpcov)] for a in range(pocet_riadkov)]
# pole pre ohodnotenie policok z pohladu supera(W)

hodnoty_B = [[[500, 0] for j in range(pocet_stlpcov)] for a in range(pocet_riadkov)]
# pole pre ohodnotenie policok z pohladu supera(B)

dlzkyL = []       #dlzka cesty od daneho policka dolava
dlzkyP = []       #dlzka cesty od daneho policka doprava
dlzkyHB = []      #dlzka cesty od daneho policka hore
dlzkyDB = []      #dlzka cesty od daneho policka dole

values = [[" " for i in range(pocet_stlpcov)] for j in range(pocet_riadkov)]
#pole policok kde sa umiestnuju tahy


def vykresli_pole(h):
    """funkcia na vykreslenie hracieho pola - kedykoľvek ju zavolám, vykreslí mi hracie pole pre
    moju hru hex"""

    print("      A       B       C       D       E       F   ")
    print("    / - \\ - / - \\ - / - \\ - / - \\ - / - \\ - / - \\")
    for i in range(pocet_riadkov):
        print(str(i + 1) + " " * (i * 4) + " |   {}   |   {}   |   {}   |   {}   |   {}   |   {}   |".format(*h[i]))
        print(" " * (i * 4) + "    \\ - / - \\ - / - \\ - / - \\ - / - \\ - / - \\ - / - \\")
    print('\n\n')


def hrac_input():
    """funkcia pre zadávanie súradníc v hracom poli hex, kam chce hráč umiestnit svoj znak - funkcia taktiež
    kontroluje podmienku či hráč nezadal súradnice mimo pola, ak áno vypýta si od neho nové.
    Po korektnom zadaní súradníc znak umiestni na hráčom zadané súradnice a vykreslí updateovanú hraciu plochu"""

    a = input()
    while (len(a) != 2 or a[0] < "1" or a[0]> "6" or
           a[1] < "A" or (a[1]>"F" and a[1] <"a") or a[1] > "f"):      #kontrola podmienky spravneho vstupu
        print("Nespravny format vstupu, zadajte znovu")
        return hrac_input()
    b = a[1]
    b = b. upper()
    riadok = int(a[0]) -1
    stlpec = ord(b) - 65
    if values[riadok][stlpec] != " ":
        print("toto policko je uz obsadene")
        return hrac_input()
    values[riadok][stlpec] = "W"
    return riadok, stlpec

def hra_pocitac():
    """funkcia pre generovanie ťahu počítača - vyberá taký ťah, ktorý zablokuje súperovu najkratšiu cestu
    do výhry a zároveň tam súper má najvyšší počet možných ciest. Ak má počítač 1 alebo 2 ťahy do výhry, tak
    generuje ťah na toto políčko"""
    ohodnot("B")      #hodnoti policka z pohladu supera
    ohodnot_B("W")    #hodnoti policka zo svojho pohladu

    naj = [0, 0, 0, 10];       #najlepsi tah

    for riadok in range(pocet_riadkov):
        for stlpec in range(pocet_stlpcov):
            if values[riadok][stlpec] == " ":
                if hodnoty_B[riadok][stlpec][0] == 0 and hodnoty_B[riadok][stlpec][1] > 0:
                    #pocitacu chyba jeden tah do dokoncenia spoja zhora dole, a zaroven tu ma moznost vytvorenia spoja
                    naj = [riadok, stlpec, hodnoty_B[riadok][stlpec][1], hodnoty_B[riadok][stlpec][0]]
                else:        #ak pocitac nema v dosahu 1 tahu vyhru
                    if hodnoty[riadok][stlpec][0] < naj[3]:      #vybera najkratsiu dlzku do spojenia stran superom
                        naj = [riadok, stlpec, hodnoty[riadok][stlpec][1], hodnoty[riadok][stlpec][0]]
                    elif hodnoty[riadok][stlpec][0] == naj[3] and hodnoty[riadok][stlpec][1] >= naj[2]:
                        #navyse vybera take policko, na ktorom ma super najviacej moznosti vytvorenia spoja
                        naj = [riadok, stlpec, hodnoty[riadok][stlpec][1], hodnoty[riadok][stlpec][0]]

    values[naj[0]][naj[1]] = "B"            #sem umiestni svoj znak
    return naj[0], naj[1]


def getSusedia(row, col, znak):
    """funkcia, ktora mi vrati vsetkych susedov daneho policka (na pozicii (row,col)) s rovnakym znakom"""

    susedia = set()
    for i, j in [(-1, 1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1)]:      #hlada ich vo vsetkych smeroch
        if (row + i) in range(pocet_riadkov) and \
                (col + j) in range(pocet_stlpcov):
            if values[row + i][col + j] == znak:                 #ak je na susednej pozicii rovnaky znak
                susedia.add((row + i, col + j))
    return susedia


def getSusedia_ohodnot(row, col, znak):
    """funkcia, ktora mi vrati vsetkych susedov daneho policka (na pozicii (row,col)), ktori neobsahuju zadany
    znak"""

    susedia = set()
    for i, j in [(-1, 1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1)]:       #hlad vo vsetkych smeroch
        if (row + i) in range(pocet_riadkov) and \
                (col + j) in range(pocet_stlpcov):
            if values[row + i][col + j] != znak:                    #ak na susednej pozicii nie je rovnaky znak
                susedia.add((row + i, col + j))
    return susedia


def ohodnot(znak):
    """funkcia, ktorá pre každé políčko vyhodnotí ako dobrá/zlá táto pozícia je(pre hráča W) -
     vyhodnocuje pomocou dvoch pomocných funkcií - ohodnotP a ohodnotL"""

    for i in range(pocet_riadkov):
        for a in range(pocet_stlpcov):
            hodnoty[i][a] = [0, 0]  # počiatočne nastavým hodnoty políčka na 0,0
            if values[i][a] == " ":
                list.clear(dlzkyL)
                list.clear(dlzkyP)
                if a == 0:  # prvý stĺpec
                    mxd = max_hlbka
                    mxh = 0
                    hodnoty[i][a][1] = ohodnotP(i, a, znak, -1, -1, 0, 0, mxd)  # pocet ciest z policka v stĺpci A doprava
                    ohodnotL(i, a, znak, -1, -1, 0, 0, mxh)

                elif a == 5:
                    mxh = max_hlbka  # posledny stlpec
                    mxd = 0
                    hodnoty[i][a][1] = ohodnotL(i, a, znak, -1, -1, 0, 0, mxh)  # pocet ciest dolava
                    ohodnotP(i, a, znak, -1, -1, 0, 0, mxd)
                else:  # iny stlpec ako prvy/posledny
                    for c in range(1, max_hlbka + 1):
                        mxd = c
                        mxh = max_hlbka - c
                        hodnoty[i][a][1] += ((ohodnotL(i, a, znak, -1, -1, 0, 0, mxh)) *
                                             (ohodnotP(i, a, znak, -1, -1, 0, 0, mxd)))
                        # pocet ciest dokopy z daneho policka dolava+doprava

                if dlzkyL and dlzkyP:
                    hodnoty[i][a][0] = min(dlzkyL) + min(dlzkyP)  # minimalna celkova dlzka cesty zlava doprava
                else:
                    hodnoty[i][a][0] = 500
    return


def ohodnotL(row, col, znak, prevx, prevy, pocet_ciest, hlbka, mx):          # vlavo
    """funkcia, ktorou ziskam pocet ciest z daneho policka dolava a zaroven ziskam dlzku danej cesty"""

    susedia = getSusedia_ohodnot(row, col, znak)

    if (values[row][col] != "W" and col != 0):
        hlbka += 1

    if col == 0:
        if values[row][col] == "W" and hlbka != 0:
            hlbka -= 1
        dlzkyL.append(hlbka)

    if (col != 0 and hlbka < mx):
        for sused in susedia:
            if (sused[1] == col - 1 or (sused[1] == col and (sused[0] != prevx or sused[1] != prevy))):
                if sused[1] == 0:
                    pocet_ciest += 1
                pocet_ciest += ohodnotL(sused[0], sused[1], znak, row, col, 0, hlbka, mx)
                if (values[sused[0]][sused[1]] == "W") and col == 1:  # nema zmysel sem umiestnovat - radsej inde
                    pocet_ciest = 0
    return pocet_ciest


def ohodnotP(row, col, znak, prevx, prevy, pocet_ciest, hlbka, mx):  # vpravo
    """funkcia, ktorou ziskam pocet ciest z daneho policka doprava a zaroven ziskam dlzku danej cesty"""

    susedia = getSusedia_ohodnot(row, col, znak)

    if (values[row][col] != "W" and col != 5):
        hlbka += 1

    if col == 5:
        if values[row][col] == "W" and hlbka != 0:
            hlbka -= 1
        dlzkyP.append(hlbka)

    if (col != 5 and hlbka < mx):
        for sused in susedia:
            if (sused[1] == col + 1 or (sused[1] == col and (sused[0] != prevx or sused[1] != prevy))):
                if sused[1] == 5:
                    pocet_ciest += 1
                pocet_ciest += ohodnotP(sused[0], sused[1], znak, row, col, 0, hlbka, mx)
                if (values[sused[0]][sused[1]] == "W") and col == 4:  # nema zmysel sem umiestnovat - radsej inde
                    pocet_ciest = 0
    return pocet_ciest


def ohodnot_B(znak):
    """funkcia, ktorá pre každé políčko vyhodnotí ako dobrá/zlá táto pozícia je (pre hráča B) -
     vyhodnocuje pomocou dvoch pomocných funkcií - ohodnotD_B a ohodnotH_B, táto funkcia pojde
     len do hĺbky 3 - to mi stačí pre prehľadanie možnej výhry do 1/2 ťahov"""

    for i in range(pocet_riadkov):
        for a in range(pocet_stlpcov):
            hodnoty_B[i][a] = [0, 0]
            if values[i][a] == " ":
                list.clear(dlzkyDB)
                list.clear(dlzkyHB)
                if i == 0:  # prvý riadok
                    mxd = 3    #max_hlbka
                    mxh = 0
                    hodnoty_B[i][a][1] = ohodnotD_B(i, a, znak, -1, -1, 0, 0, mxd)
                    ohodnotH_B(i, a, znak, -1, -1, 0, 0, mxh)

                elif i == 5:   #posledny riadok
                    mxh = 3    #max_hlbka
                    mxd = 0
                    hodnoty_B[i][a][1] = ohodnotH_B(i, a, znak, -1, -1, 0, 0, mxh)  # pocet ciest hore
                    ohodnotD_B(i, a, znak, -1, -1, 0, 0, mxd)
                else:  # iny riadok ako prvy/posledny
                    for c in range(1, 3 + 1):
                        mxd = c
                        mxh = 3 - c    #max_hlbka - c
                        hodnoty_B[i][a][1] += ((ohodnotH_B(i, a, znak, -1, -1, 0, 0, mxh)) * (ohodnotD_B(i, a, znak, -1, -1, 0, 0, mxd)))
                        # pocet ciest dokopy z daneho policka hore + dole

                if dlzkyHB and dlzkyDB:
                    hodnoty_B[i][a][0] = min(dlzkyHB) + min(dlzkyDB)  # minimalna celkova dlzka cesty
                else:
                    hodnoty_B[i][a][0] = 500
    return


def ohodnotH_B(row, col, znak, prevx, prevy, pocet_ciest, hlbka, mx):  # hore
    """funkcia, ktorou ziskam pocet ciest z daneho policka hore a zaroven ziskam dlzku danej cesty"""

    susedia = getSusedia_ohodnot(row, col, znak)

    if (values[row][col] != "B" and row != 0):
        hlbka += 1

    if row == 0:
        if values[row][col] == "B" and hlbka != 0:
            hlbka -= 1
        dlzkyHB.append(hlbka)

    if (row != 0 and hlbka < mx):
        for sused in susedia:
            if (sused[0] == row - 1 or (sused[0] == row and (sused[0] != prevx or sused[1] != prevy))):
                if sused[0] == 0:
                    pocet_ciest += 1
                pocet_ciest += ohodnotH_B(sused[0], sused[1], znak, row, col, 0, hlbka, mx)
    return pocet_ciest


def ohodnotD_B(row, col, znak, prevx, prevy, pocet_ciest, hlbka, mx):  # dole
    """funkcia, ktorou ziskam pocet ciest z daneho policka dole a zaroven ziskam dlzku danej cesty"""

    susedia = getSusedia_ohodnot(row, col, znak)

    if (values[row][col] != "B" and row != 5):
        hlbka += 1

    if row == 5:
        if values[row][col] == "B" and hlbka != 0:
            hlbka -= 1
        dlzkyDB.append(hlbka)

    if (row != 5 and hlbka < mx):
        for sused in susedia:
            if (sused[0] == row + 1 or (sused[0] == row and (sused[0] != prevx or sused[1] != prevy))):
                if sused[0] == 5:
                    pocet_ciest += 1
                pocet_ciest += ohodnotD_B(sused[0], sused[1], znak, row, col, 0, hlbka, mx)
    return pocet_ciest


def prehladavanie_hex_W(znak):
    """funkcia pre kontrolu vyhry bieleho hraca - prehladavanie do sirky, hlada cestu zlava doprava"""

    fronta = [(i, 0) for i in range(pocet_riadkov) if values[i][0] == znak]             #lavy okraj
    prava = [(i, pocet_stlpcov - 1) for i in range(pocet_riadkov) if values[i][-1] == znak]     #pravy okraj
    visited = set()

    while len(fronta) > 0:
        x, y = fronta.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for (a, b) in getSusedia(x, y, znak):           #prechadzam susedov policka s rovnakym znakom
            if (a, b) not in visited:
                if (a, b) in prava:                     #ak najdem suseda v pravom okraji, existuje cesta
                    return "W"  # je cesta/vyhra
                fronta.append((a, b))
    return False


def prehladavanie_hex_B(znak):
    """funkcia pre kontrolu vyhry cierneho hraca - prehladavanie do sirky, hlada cestu zhora dole"""

    frontaB = [(0, i) for i in range(pocet_stlpcov) if values[0][i] == znak]  # horny okraj
    dolny = [(pocet_riadkov - 1, i) for i in range(pocet_stlpcov) if values[-1][i] == znak]  # dolny okraj hracieho pola
    visited = set()

    while len(frontaB) > 0:
        x, y = frontaB.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for (a, b) in getSusedia(x, y, znak):               #prechadzam susedov policka s rovnakym znakom
            if (a, b) not in visited:
                if (a, b) in dolny:                         #ak najdem suseda v dolnom okraji, existuje cesta
                    return "B"  # existuje cesta zhora dole
                frontaB.append((a, b))
    return False


def hra(kolo):
    """hlavna funkcia pre priebeh hry, kontrola aktivneho hraca, posun kola, vola funkcie pre vstup hraca a
    pre tah pocitaca, kontroluje podmienku splnenia vyhry"""

    kolo = 0
    vitaz = None                    #zaciname bez vitaza

    while not vitaz:                #dokym nemame vitaza
        kolo += 1                   #posun kola
        if kolo % 2 == 1:           #ak sme v neparnom kole aktivny hrac je W(biely)
            aktivny_hrac = "W"
        else:                       #ak sme v parnom kole aktivny hrac je B(cierny)
            aktivny_hrac = "B"

        print('Kolo: ' + str(kolo) + '\n'
              + 'Na ťahu: ' + str(aktivny_hrac))

        vykresli_pole(values)

        if aktivny_hrac == "W":     #ak je W aktivny hrac zavola funkciu pre tah hraca
            print('Zadajte súradnice - číslo riadku a stĺpec bez medzery (napr. 1A):')
            tah = hrac_input()

        if aktivny_hrac == "B":     #ak je B aktivny hrac zavola funkciu pre tah pocitaca
            tah = hra_pocitac()

        if (prehladavanie_hex_W("W")):                  #kontrola ci nemame vitaza
            vitaz = prehladavanie_hex_W("W")
        elif (prehladavanie_hex_B("B")):
            vitaz = prehladavanie_hex_B("B")

        if vitaz in ["W", "B"]:                         #ak mame vitaza, koniec hry, vypise vitaza
            vykresli_pole(values)
            print(vitaz + " " + "VYHRAL HRU")


hra(0)
