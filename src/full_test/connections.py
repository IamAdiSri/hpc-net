def flip(p):
    if p < 256:
        return p + 256
    return p - 256


def build(k=4):
    # |pods| = k

    # |spine switches} = (k//2)**2
    spn_switches = [f"spn{i}" for i in range((k // 2) ** 2)]
    print(f"Added {len(spn_switches)} spine switches!")

    # |fabric switches| = (k**2)//2
    fab_switches = [f"fab{i}" for i in range(k**2 // 2)]
    print(f"Added {len(fab_switches)} fabric switches!")

    # |rack switches| = (k**2)//2
    rck_switches = [f"tor{i}" for i in range(k**2 // 2)]
    print(f"Added {len(rck_switches)} rack switches!")

    # |hosts| = (k**3)//4
    hosts = [f"srv{i}" for i in range(k**3 // 4)]
    print(f"Added {len(hosts)} hosts!")

    print("\n")

    # Connect spine switches to fabric switches
    fab_conns = [[] for _ in range(len(fab_switches))]
    for c in range((k // 2) ** 2):
        for pod in range(k):
            f = pod * (k // 2) + c // (k // 2)

            s_port = pod % (k // 2)
            if pod >= k // 2:
                s_port = flip(s_port)
                f_port = s_port
            else:
                f_port = flip(s_port)

            print(f"spn_{c}_{c+s_port} --> fab_{f}_{c+f_port}")
            fab_conns[f].append(c + f_port)

    for i in range(len(fab_conns)):
        print(f"fab_{i}", fab_conns[i])
    print("\n")

    # Connect fabric switches to rack switches
    rck_conns = [[] for _ in range(len(rck_switches))]
    for f in range((k**2) // 2):
        si = f // (k // 2) * (k // 2)
        for t in range(si, si + k // 2):
            print(
                f"fab_{f}_{flip(fab_conns[f][t%(k//2)])} --> rck_{t}_{fab_conns[f][t%(k//2)]}"
            )
            rck_conns[t].append(fab_conns[f][t % (k // 2)])

    for i in range(len(rck_conns)):
        print(f"rck_{i}", rck_conns[i])
    print("\n")

    # Connect rack switches to hosts
    hst_conns = [[] for _ in range(len(hosts))]
    for t in range((k**2) // 2):
        si = t * (k // 2)
        for s in range(si, si + k // 2):
            print(
                f"rck_{t}_{flip(rck_conns[t][s%(k//2)])} --> hst_{s}_{rck_conns[t][s%(k//2)]}"
            )
            hst_conns[s].append(rck_conns[t][s % (k // 2)])

    for i in range(len(hst_conns)):
        print(f"hst_{i}", hst_conns[i])
    print("\n")


build()
