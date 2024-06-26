# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from p4utils.mininetlib.network_API import NetworkAPI


class FatTreeTopo(NetworkAPI):
    """
    Setup a FatTree Mininet Topology
    with P4 switches using a custom program.

    Args:
        k: Size of FatTree
        p4src: Location of P4 source file
        drop_port: Switch port to send dropped packets to
        ctrl_port: Switch port to forward packets to controller
        p4rt: Use P4Runtime if True
        loglevel: Set logging level

    Returns:
        None
    """

    def __init__(
        self, k, p4src, drop_port=511, ctrl_port=None, p4rt=False, loglevel="info"
    ):
        super().__init__()
        self.k = k
        self.p4src = p4src
        self.drop_port = drop_port
        self.ctrl_port = ctrl_port
        self.p4rt = p4rt

        self.setLogLevel(loglevel)
        self.setCompiler(p4rt=p4rt)

    def setup(self):
        def flip(p):
            return (p + self.k // 2) % self.k

        if not self.p4rt:
            addSwitch = lambda s: self.addP4Switch(
                s,
                drop_port=self.drop_port,
            )
        else:
            addSwitch = lambda s: self.addP4RuntimeSwitch(
                s,
                drop_port=self.drop_port,
                # cpu_port=True,
                # cpu_port_num=self.ctrl_port,
            )

        npod = self.k  # number of pods
        nspn = self.k // 2  # number of spines
        nspns = (self.k // 2) ** 2  # number of spine switches
        nspnp = nspns // nspn  # number of spine switches per spine
        nfabs = nrcks = (self.k**2) // 2  # number of fabric and rack switches
        nfabp = nrckp = nfabs // npod  # number of frabric and rack switches per pod
        nhsts = (self.k**3) // 4  # number of hosts
        nhstp = nhsts // nrcks  # number of hosts per rack switch

        # spine switches
        spn_mat = [[None] * nspnp for _ in range(nspn)]
        spn_switches = []
        for ssid in range(nspnp):
            for sid in range(nspn):
                s = addSwitch(f"s_{ssid}_{sid}")
                spn_mat[sid][ssid] = s
                spn_switches.append(s)

        # fabric switches
        fab_mat = [[None] * nspn for _ in range(npod)]
        fab_switches = []
        for pid in range(npod):
            for sid in range(nspn):
                f = addSwitch(f"f_{pid}_{sid}")
                fab_mat[pid][sid] = f
                fab_switches.append(f)

        # rack switches
        rck_mat = [[None] * nrckp for _ in range(npod)]
        rck_switches = []
        for pid in range(npod):
            for rid in range(nrckp):
                r = addSwitch(f"r_{pid}_{rid}")
                rck_mat[pid][rid] = r
                rck_switches.append(r)

        # deploy switch program to all switches
        self.setP4SourceAll(self.p4src)

        # enable CPU port on all switches
        if self.ctrl_port:
            self.enableCpuPortAll()

        # hosts
        hst_mat = [[[None] * nhstp for _ in range(nrckp)] for _ in range(npod)]
        hosts = []
        for pid in range(npod):
            for rid in range(nrckp):
                for hid in range(nhstp):
                    h = self.addHost(f"h_{pid}_{rid}_{hid}")
                    hst_mat[pid][rid][hid] = h
                    hosts.append(h)

        # connect hosts to rack switches
        for h in hosts:
            pid, rid, hid = (int(n) for n in h.split("_")[1:])
            r = rck_mat[pid][rid]
            self.addLink(h, r)
            self.setIntfPort(h, r, 0)
            self.setIntfPort(r, h, hid)

        # connect rack switches to fabric switches
        for r in rck_switches:
            pid, rid = (int(n) for n in r.split("_")[1:])
            fs = fab_mat[pid]
            for i, f in enumerate(fs):
                self.addLink(r, f)
                self.setIntfPort(r, f, flip(i))
                self.setIntfPort(f, r, rid)

        # connect spine switches to fabric switches
        for s in spn_switches:
            ssid, sid = (int(n) for n in s.split("_")[1:])
            fs = [f[sid] for f in fab_mat]
            for f in fs:
                fpid, fsid = (int(n) for n in f.split("_")[1:])
                port = ssid
                self.addLink(s, f)
                if fpid < self.k // 2:
                    self.setIntfPort(s, f, fpid % (self.k // 2))
                else:
                    self.setIntfPort(s, f, flip(fpid % (self.k // 2)))
                self.setIntfPort(f, s, flip(port))

        self.ft_switches = {
            "rck": rck_switches,
            "fab": fab_switches,
            "spn": spn_switches,
        }
        self.ft_hosts = hosts
