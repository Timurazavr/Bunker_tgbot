from random import shuffle

sp: list = []
sl_rol = {}
sl: dict = {
    "mir": 0,
    "maf": 0,
    "sher": 0,
    "det": 0,
    "doc": 0,
    "bab": 0,
}


def rols(sl):
    spis = []
    for k, v in sl.items():
        spis.extend([k] * v)
    for i in range(3):
        shuffle(spis)
    return spis
