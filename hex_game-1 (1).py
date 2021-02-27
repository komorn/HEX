#import random
moves = []
pocet_riadkov = 6
pocet_stlpcov = 6
max_hlbka = 6
hodnoty = [[[500, 0] for j in range(pocet_stlpcov)] for a in range(pocet_riadkov)]
hodnoty_B = [[[500, 0] for j in range(pocet_stlpcov)] for a in range(pocet_riadkov)]
dlzkyH = []
dlzkyD = []
dlzkyHB = []
dlzkyDB = []
values = [[" " for i in range(pocet_stlpcov)] for j in range(pocet_riadkov)]


def vykresli_pole(h):
    """funkcia na vykreslenie hracieho pola - kedykoľvek ju zavolám, vykreslím mi hracie pole pre
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
        a = input()
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
    ohodnot("B")
    ohodnot_B("W")

    print(hodnoty[0])
    print(hodnoty[1])
    print(hodnoty[2])
    print(hodnoty[3])
    print(hodnoty[4])
    print(hodnoty[5])

    print(hodnoty_B[0])
    print(hodnoty_B[1])
    print(hodnoty_B[2])
    print(hodnoty_B[3])
    print(hodnoty_B[4])
    print(hodnoty_B[5])

    naj = [0, 0, 0, 10];

    for riadok in range(pocet_riadkov):
        for stlpec in range(pocet_stlpcov):
            if values[riadok][stlpec] == " ":
                if hodnoty_B[riadok][stlpec][0] == 0:
                    naj = [riadok, stlpec, hodnoty_B[riadok][stlpec][1], hodnoty_B[riadok][stlpec][0]]
                else:
                    if hodnoty[riadok][stlpec][0] < naj[3]:
                        naj = [riadok, stlpec, hodnoty[riadok][stlpec][1], hodnoty[riadok][stlpec][0]]
                    elif hodnoty[riadok][stlpec][0] == naj[3] and hodnoty[riadok][stlpec][1] >= naj[2]:
                        naj = [riadok, stlpec, hodnoty[riadok][stlpec][1], hodnoty[riadok][stlpec][0]]

    values[naj[0]][naj[1]] = "B"
    moves.append([naj[0], naj[1], "B"])
    return naj[0], naj[1]


def getSusedia(row, col, znak):
    """funkcia, ktorou ziskam vsetkych susedov daneho policka na pozicii (row,col) s rovnakym znakom"""
    susedia = set()
    for i, j in [(-1, 1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1)]:
        if (row + i) in range(pocet_riadkov) and \
                (col + j) in range(pocet_stlpcov):
            if values[row + i][col + j] == znak:
                susedia.add((row + i, col + j))
    return susedia


def getSusedia_ohodnot(row, col, znak):
    """funkcia, ktorou ziskam vsetkych susedov daneho policka na pozicii (row,col), ktori neobsahuju zadany
    znak"""
    susedia = set()
    for i, j in [(-1, 1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1)]:
        if (row + i) in range(pocet_riadkov) and \
                (col + j) in range(pocet_stlpcov):
            if values[row + i][col + j] != znak:
                susedia.add((row + i, col + j))
    return susedia


def ohodnot(znak):
    """funkcia, ktorá pre každé políčko vyhodnotí ako dobrá/zlá táto pozícia je -
     vyhodnocuje pomocou dvoch pomocných funkcií - ohodnotD a ohodnotH"""
    for i in range(pocet_riadkov):
        for a in range(pocet_stlpcov):
            hodnoty[i][a] = [0, 0]  # počiatočne nastavým hodnoty políčka na 0,0
            if values[i][a] == " ":
                list.clear(dlzkyD)
                list.clear(dlzkyH)
                if a == 0:  # prvý stĺpec
                    mxd = max_hlbka
                    mxh = 0
                    hodnoty[i][a][1] = ohodnotD(i, a, znak, -1, -1, 0, 0, mxd)  # pocet ciest z policka v stĺpci A doprava
                    ohodnotH(i, a, znak, -1, -1, 0, 0, mxh)

                elif a == 5:
                    mxh = max_hlbka  # posledny stlpec
                    mxd = 0
                    hodnoty[i][a][1] = ohodnotH(i, a, znak, -1, -1, 0, 0, mxh)  # pocet ciest dolava
                    ohodnotD(i, a, znak, -1, -1, 0, 0, mxd)
                else:  # iny stlpec ako prvy/posledny
                    for c in range(1, max_hlbka + 1):
                        mxd = c
                        mxh = max_hlbka - c
                        hodnoty[i][a][1] += ((ohodnotH(i, a, znak, -1, -1, 0, 0, mxh)) *
                                             (ohodnotD(i, a, znak, -1, -1, 0, 0, mxd)))
                        # pocet ciest dokopy z daneho policka dolava+doprava
                if dlzkyH and dlzkyD:
                    hodnoty[i][a][0] = min(dlzkyH) + min(dlzkyD)  # minimalna celkova dlzka cesty zlava doprava
                else:
                    hodnoty[i][a][0] = 500
    return


def ohodnotH(row, col, znak, prevx, prevy, pocet_ciest, hlbka, mx):  # vlavo
    """funkcia, ktorou ziskam pocet ciest z daneho policka dolava a zaroven ziskam dlzku danej cesty"""
    susedia = getSusedia_ohodnot(row, col, znak)
    if (values[row][col] != "W" and col != 0):
        hlbka += 1
    if col == 0:
        if values[row][col] == "W" and hlbka != 0:
            hlbka -= 1
        dlzkyH.append(hlbka)
    if (col != 0 and hlbka < mx):
        for sused in susedia:
            if (sused[1] == col - 1 or (sused[1] == col and (sused[0] != prevx or sused[1] != prevy))):
                if sused[1] == 0:
                    pocet_ciest += 1
                pocet_ciest += ohodnotH(sused[0], sused[1], znak, row, col, 0, hlbka, mx)
                if (values[sused[0]][sused[1]] == "W") and col == 1:  # nema zmysel sem umiestnovat - radsej inde
                    pocet_ciest = 0
    return pocet_ciest


def ohodnotD(row, col, znak, prevx, prevy, pocet_ciest, hlbka, mx):  # vpravo
    """funkcia, ktorou ziskam pocet ciest z daneho policka doprava a zaroven ziskam dlzku danej cesty"""
    susedia = getSusedia_ohodnot(row, col, znak)
    if (values[row][col] != "W" and col != 5):
        hlbka += 1
    if col == 5:
        if values[row][col] == "W" and hlbka != 0:
            hlbka -= 1
        dlzkyD.append(hlbka)
    if (col != 5 and hlbka < mx):
        for sused in susedia:
            if (sused[1] == col + 1 or (sused[1] == col and (sused[0] != prevx or sused[1] != prevy))):
                if sused[1] == 5:
                    pocet_ciest += 1
                pocet_ciest += ohodnotD(sused[0], sused[1], znak, row, col, 0, hlbka, mx)
                if (values[sused[0]][sused[1]] == "W") and col == 4:  # nema zmysel sem umiestnovat - radsej inde
                    pocet_ciest = 0
    return pocet_ciest


def ohodnot_B(znak):
    """funkcia, ktorá pre každé políčko vyhodnotí ako dobrá/zlá táto pozícia je -
     vyhodnocuje pomocou dvoch pomocných funkcií - ohodnotD a ohodnotH"""
    for i in range(pocet_riadkov):
        for a in range(pocet_stlpcov):
            hodnoty_B[i][a] = [0, 0]
            if values[i][a] == " ":
                list.clear(dlzkyDB)
                list.clear(dlzkyHB)
                if i == 0:  # prvý stĺpec
                    mxd = 3    #max_hlbka
                    mxh = 0
                    hodnoty_B[i][a][1] = ohodnotD_B(i, a, znak, -1, -1, 0, 0, mxd)
                    ohodnotH_B(i, a, znak, -1, -1, 0, 0, mxh)

                elif i == 5:   #posledny stlpec
                    mxh = 3    #max_hlbka
                    mxd = 0
                    hodnoty_B[i][a][1] = ohodnotH_B(i, a, znak, -1, -1, 0, 0, mxh)  # pocet ciest hore
                    ohodnotD_B(i, a, znak, -1, -1, 0, 0, mxd)
                else:  # iny stlpec ako prvy/posledny
                    for c in range(1, 3 + 1):
                        mxd = c
                        mxh = 3 - c    #max_hlbka - c
                        hodnoty_B[i][a][1] += ((ohodnotH_B(i, a, znak, -1, -1, 0, 0, mxh)) * (ohodnotD_B(i, a, znak, -1, -1, 0, 0, mxd)))
                        # pocet ciest dokopy z daneho policka dolava+doprava
                if dlzkyHB and dlzkyDB:
                    hodnoty_B[i][a][0] = min(dlzkyHB) + min(dlzkyDB)  # minimalna celkova dlzka cesty
                else:
                    hodnoty_B[i][a][0] = 500
    return


def ohodnotH_B(row, col, znak, prevx, prevy, pocet_ciest, hlbka, mx):  # hore
    """funkcia, ktorou ziskam pocet ciest z daneho policka dolava a zaroven ziskam dlzku danej cesty"""
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
    """funkcia, ktorou ziskam pocet ciest z daneho policka doprava a zaroven ziskam dlzku danej cesty"""
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
    """funkcia pre kontrolu vyhry bieleho hraca"""
    fronta = [(i, 0) for i in range(pocet_riadkov) if values[i][0] == znak]
    prava = [(i, pocet_stlpcov - 1) for i in range(pocet_riadkov) if values[i][-1] == znak]
    visited = set()
    while len(fronta) > 0:
        x, y = fronta.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for (a, b) in getSusedia(x, y, znak):
            if (a, b) not in visited:
                if (a, b) in prava:
                    return "W"  # je cesta/vyhra
                fronta.append((a, b))
    return False


def prehladavanie_hex_B(znak):
    """funkcia pre kontrolu vyhry cierneho hraca"""

    frontaB = [(0, i) for i in range(pocet_stlpcov) if values[0][i] == znak]  # horny okraj
    dolny = [(pocet_riadkov - 1, i) for i in range(pocet_stlpcov) if values[-1][i] == znak]  # dolny okraj hracieho pola
    visited = set()
    while len(frontaB) > 0:
        x, y = frontaB.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for (a, b) in getSusedia(x, y, znak):
            if (a, b) not in visited:
                if (a, b) in dolny:
                    return "B"  # existuje cesta zhora dole
                frontaB.append((a, b))
    return False


def hra(kolo):
    kolo = 0
    vitaz = None

    while not vitaz:
        kolo += 1
        if kolo % 2 == 1:
            aktivny_hrac = "W"
        else:
            aktivny_hrac = "B"

        print('Kolo: ' + str(kolo) + '\n'
              + 'Na ťahu: ' + str(aktivny_hrac))

        vykresli_pole(values)

        if aktivny_hrac == "W":
            print('Zadajte súradnice - číslo riadku a stĺpec bez medzery (napr. 1A):')
            tah = hrac_input()

        if aktivny_hrac == "B":
            tah = hra_pocitac()

        if (prehladavanie_hex_W("W")):
            vitaz = prehladavanie_hex_W("W")
        elif (prehladavanie_hex_B("B")):
            vitaz = prehladavanie_hex_B("B")

        if vitaz in ["W", "B"]:
            vykresli_pole(values)
            print(vitaz + " " + "VYHRAL HRU")


hra(0)
