def table_priv(sp):
    sp = list(map(lambda x: list(map(lambda y: y.text, x)), sp))
    if "-" not in (*sp[0], *sp[1], *sp[2]):
        return "Ничья!"
    for i in "⭕❌":
        if [i, i, i] in [
            *sp,
            [sp[0][0], sp[1][1], sp[2][2]],
            [sp[0][2], sp[1][1], sp[2][0]],
            [sp[0][0], sp[1][0], sp[2][0]],
            [sp[0][1], sp[1][1], sp[2][1]],
            [sp[0][2], sp[1][2], sp[2][2]],
        ]:
            return i