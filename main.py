def citirefisier(file_path):
    tranz = {}
    stare_initiala = None
    stare_finala = None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
                tranzitie = line.strip().split()
                if len(tranzitie) == 3:
                    stare = tranzitie[0]
                    litera = tranzitie[1]
                    stare2 = tranzitie[2]
                    tranz.setdefault(stare, {})[litera] = stare2
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith("q"):
                states = line.strip().split()
                stare_initiala = states[0]
                stare_finala= states[1:]

    stari = set()
    alfabet = set()

    for stare in tranz.keys():
        stari.add(stare)
        for litera in tranz[stare].keys():
            alfabet.add(litera)

    return stari, alfabet, stare_initiala, stare_finala, tranz

def automatminimal(stari, alfabet, stare_initiala, stare_finala, tranz):
    # separare stari finale de cele ne-finale
    starinefin = set(stari) - set(stare_finala)

    # noi stări,realtii de echivalenta
    relatii = [list(stare_finala), list(starinefin)]
    starinoi = [set(stare_finala), set(starinefin)]

    # selectare relatii de echivalenta
    sw = True
    while sw:
        sw = False
        for i, relatie in enumerate(relatii):
            relatiinoi = []
            for stare in relatie:
                relatiegasita = False
                for j, starinoim in enumerate(starinoi):
                    if suntrelatii(stare, starinoim, tranz):
                        relatiinoi.append(stare)
                        relatiegasita = True
                        if j != i:
                            sw = True
                            starinoi[i].remove(stare)
                            starinoi[j].add(stare)
                        break
                if not relatiegasita:
                    relatiinoi.append(stare)
            relatii[i] = relatiinoi

    # noul automat
    starinoim = set()
    stare_initialanoua = None
    starefinalanoua = set()
    tranznoi = {}

    for relatie in relatii:
        starenoua = ''.join(sorted(relatie))
        starinoim.add(starenoua)
        if stare_initialanoua in relatie:
            stare_initialanoua = starenoua
        if any(stare in stare_finala for stare in relatie):
            starefinalanoua.add(starenoua)

        for litera in alfabet:
            starenoua = None
            for stare in relatie:
                if litera in tranz[stare]:
                    starenoua = tranz[stare][litera]
                    break
            if starenoua:
                tranznoi.setdefault(starenoua, {})[litera] = starenoua

    return starinoim, alfabet, stare_initialanoua, starefinalanoua, tranznoi


def suntrelatii(stare, starem, tranz):
    for litera in tranz[stare]:
        if tranz[stare][litera] not in starem:
            return False
    return True
stari, alfabet, stareinitiala, starefinala, tranz = citirefisier('input.in')
starinoi,alfabetnou, stareinitialanoua,starefinalanoua, tranznoi = automatminimal(stari, alfabet, stareinitiala, starefinala, tranz)

print("Stări:", starinoi)
print("Alfabet:", alfabetnou)
print("Tranziții:")
for stare in starinoi:
    if stare in tranznoi:
        for litera in tranznoi[stare]:
            stareurm = tranznoi[stare][litera]
            print(f"{stare} --({litera})--> {stareurm}")








