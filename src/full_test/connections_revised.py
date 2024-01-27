# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def flip(p, bits=9):
    d = (2**bits)//2
    if p < d:
        return p + d
    return p - d


def build(k=4):
    npod = k                    # number of pods
    nspn = k//2                 # number of spines
    nspns = (k//2) ** 2         # number of spine switches
    nspnp = nspns//nspn         # number of spine switches per spine
    nfabs = nrcks = (k**2) // 2 # number of fabric and rack switches
    nfabp = nrckp = nfabs//npod # number of frabric and rack switches per pod
    nhsts = (k**3) // 4         # number of hosts
    nhstp = nhsts//nrcks        # number of hosts per rack switch

    print(f"{npod=}, {nspn=}, {nspns=}, {nspnp=}, {nfabs=}, {nfabp=}, {nhsts=} \n\n")

    # spine switches
    spn_mat = [[None]*nspnp for _ in range(nspn)]
    spn_switches = []
    for sid in range(nspn):
        for ssid in range(nspnp):
            spn_mat[sid][ssid] = f"spn_{sid}_{ssid}"
            spn_switches.append(f"spn_{sid}_{ssid}")

    print(f"Adding {len(spn_switches)} spine switches!")
    print(*spn_mat, sep="\n", end="\n\n")
    # print(spn_switches, nspns)
    assert(len(spn_switches) == nspns)
    print("\n")

    # fabric switches
    fab_mat = [[None]*nspn for _ in range(npod)]
    fab_switches = []
    for pid in range(npod):
        for sid in range(nspn):
            fab_mat[pid][sid] = f"fab_{sid}_{pid}"
            fab_switches.append(f"fab_{sid}_{pid}")

    print(f"Adding {len(fab_switches)} fabric switches!")
    print(*fab_mat, sep="\n", end="\n\n")
    # print(fab_switches, nfabs)
    assert(len(fab_switches) == nfabs)
    print("\n")

    # rack switches
    rck_mat = [[None]*nrckp for _ in range(npod)]
    rck_switches = []
    for pid in range(npod):
        for rid in range(nrckp):
            rck_mat[pid][rid] = f"rck_{pid}_{rid}"
            rck_switches.append(f"rck_{pid}_{rid}")

    print(f"Adding {len(rck_switches)} rack switches!")
    print(*rck_mat, sep="\n", end="\n\n")
    # print(rck_switches, nrcks)
    assert(len(rck_switches) == nrcks)
    print("\n")
    
    # hosts
    hst_mat = [[[None]*nhstp for _ in range(nrckp)] for _ in range(npod)]
    hosts = []
    for pid in range(npod):
        for rid in range(nrckp):
            for hid in range(nhstp):
                hst_mat[pid][rid][hid] = f"hst_{pid}_{rid}_{hid}"
                hosts.append(f"hst_{pid}_{rid}_{hid}")

    print(f"Adding {len(hosts)} rack switches!")
    print(*hst_mat, sep="\n", end="\n\n")
    # print(hosts, nhsts)
    assert(len(hosts) == nhsts)
    print("\n")

    # connect hosts to rack switches
    print("Connecting hosts to rack switches!")
    for h in hosts:
        pid, rid, hid = (int(n) for n in h.split('_')[1:])
        r = rck_mat[pid][rid]
        print(f"{h}:0 --> {r}:{hid}")
    print("\n")

    # connect rack switches to fabric switches
    print("Connecting rack switches to fabric switches!")
    for r in rck_switches:
        pid, rid = (int(n) for n in r.split('_')[1:])
        fs = fab_mat[pid]
        for i, f in enumerate(fs):
            print(f"{r}:{flip(i)} --> {f}:{rid}")
    print("\n")

    # connect fabric switches to spine switches
    # print("Connecting fabric switches to spine switches!")
    # for f in fab_switches:
    #     sid, pid = (int(n) for n in f.split('_')[1:])
    #     print(sid, pid)
    # print("\n")

    # connect spine switches to fabric switches
    print("Connecting spine switches to fabric switches!")
    for s in spn_switches:
        sid, ssid = (int(n) for n in s.split('_')[1:])
        # print(sid, ssid, [f[sid] for f in fab_mat])
        fs = [f[sid] for f in fab_mat]
        for f in fs:
            fsid, fpid = (int(n) for n in f.split('_')[1:])
            port = ssid
            if fpid < k//2:
                print(f"{s}:{fpid%(k//2)}\t--> {f}:{flip(port)}")
            else:
                print(f"{s}:{flip(fpid%(k//2))}\t--> {f}:{flip(port)}")

build(int(input("Enter k: ")))
