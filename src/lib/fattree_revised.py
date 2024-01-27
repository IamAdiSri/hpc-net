# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from p4utils.mininetlib.network_API import NetworkAPI


class FatTreeTopo(NetworkAPI):
    def __init__(self, loglevel="info"):
        super().__init__()
        self.setLogLevel(loglevel)

    def setup(self, src, k=4):
        """
        Initializes a FatTree Mininet Topology
        with P4 switches using a custom program.

        Args:
            src : Location of P4 source file
            k   : Size of FatTree

        Returns:
            None
        """

        def flip(p):
            if p < 256:
                return p + 256
            return p - 256

        npod = k                    # number of pods
        nspn = k//2                 # number of spines
        nspns = (k//2) ** 2         # number of spine switches
        nspnp = nspns//nspn         # number of spine switches per spine
        nfabs = nrcks = (k**2) // 2 # number of fabric and rack switches
        nfabp = nrckp = nfabs//npod # number of frabric and rack switches per pod
        nhsts = (k**3) // 4         # number of hosts
        nhstp = nhsts//nrcks        # number of hosts per rack switch

        # spine switches
        spn_mat = [[None]*nspnp for _ in range(nspn)]
        spn_switches = []
        for sid in range(nspn):
            for ssid in range(nspnp):
                s = self.addP4Switch(f"spn_{sid}_{ssid}")
                spn_mat[sid][ssid] = s
                spn_switches.append(s)

        # fabric switches
        fab_mat = [[None]*nspn for _ in range(npod)]
        fab_switches = []
        for pid in range(npod):
            for sid in range(nspn):
                f = self.addP4Switch(f"fab_{sid}_{pid}")
                fab_mat[pid][sid] = f
                fab_switches.append(f)

        # rack switches
        rck_mat = [[None]*nrckp for _ in range(npod)]
        rck_switches = []
        for pid in range(npod):
            for rid in range(nrckp):
                r = self.addP4Switch(f"rck_{pid}_{rid}")
                rck_mat[pid][rid] = r
                rck_switches.append(r)

        # deploy switch program to all switches
        self.setP4SourceAll(src)

        # hosts
        hst_mat = [[[None]*nhstp for _ in range(nrckp)] for _ in range(npod)]
        hosts = []
        for pid in range(npod):
            for rid in range(nrckp):
                for hid in range(nhstp):
                    h = self.addHost(f"hst_{pid}_{rid}_{hid}")
                    hst_mat[pid][rid][hid] = h
                    hosts.append(h)

        # connect hosts to rack switches
        print("Connecting hosts to rack switches!")
        for h in hosts:
            pid, rid, hid = (int(n) for n in h.split('_')[1:])
            r = rck_mat[pid][rid]
            self.addLink(h, r)
            self.setIntfPort(h, r, 0)
            self.setIntfPort(r, h, hid)

        # connect rack switches to fabric switches
        print("Connecting rack switches to fabric switches!")
        for r in rck_switches:
            pid, rid = (int(n) for n in r.split('_')[1:])
            fs = fab_mat[pid]
            for i, f in enumerate(fs):
                self.addLink(r, f)
                self.setIntfPort(r, f, flip(i))
                self.setIntfPort(f, r, rid)

        # connect spine switches to fabric switches
        print("Connecting spine switches to fabric switches!")
        for s in spn_switches:
            sid, ssid = (int(n) for n in s.split('_')[1:])
            # print(sid, ssid, [f[sid] for f in fab_mat])
            fs = [f[sid] for f in fab_mat]
            for f in fs:
                fsid, fpid = (int(n) for n in f.split('_')[1:])
                port = ssid
                self.addLink(s, f)
                if fpid < k//2:
                    self.setIntfPort(s, f, fpid%(k//2))
                else:
                    self.setIntfPort(s, f, flip(fpid%(k//2)))
                self.setIntfPort(f, s, flip(port))

        self.ft_hosts = hosts