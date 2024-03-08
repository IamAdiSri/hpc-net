# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from lib.controller import Controller
from p4utils.mininetlib.network_API import NetworkAPI


class FatTreeTopo(NetworkAPI):
    def __init__(self, loglevel="info"):
        super().__init__()
        self.setLogLevel(loglevel)

    def setup(self, src, k=4, ctrl_port=None):
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
            return (p + k // 2) % k

        npod = k  # number of pods
        nspn = k // 2  # number of spines
        nspns = (k // 2) ** 2  # number of spine switches
        nspnp = nspns // nspn  # number of spine switches per spine
        nfabs = nrcks = (k**2) // 2  # number of fabric and rack switches
        nfabp = nrckp = nfabs // npod  # number of frabric and rack switches per pod
        nhsts = (k**3) // 4  # number of hosts
        nhstp = nhsts // nrcks  # number of hosts per rack switch

        # spine switches
        spn_mat = [[None] * nspnp for _ in range(nspn)]
        spn_switches = []
        for ssid in range(nspnp):
            for sid in range(nspn):
                # s = self.addP4Switch(f"spn_{ssid}_{sid}")
                s = self.addP4RuntimeSwitch(f"spn_{ssid}_{sid}")
                spn_mat[sid][ssid] = s
                spn_switches.append(s)

        # fabric switches
        fab_mat = [[None] * nspn for _ in range(npod)]
        fab_switches = []
        for pid in range(npod):
            for sid in range(nspn):
                # f = self.addP4Switch(f"fab_{pid}_{sid}")
                f = self.addP4RuntimeSwitch(f"fab_{pid}_{sid}")
                fab_mat[pid][sid] = f
                fab_switches.append(f)

        # rack switches
        rck_mat = [[None] * nrckp for _ in range(npod)]
        rck_switches = []
        for pid in range(npod):
            for rid in range(nrckp):
                # r = self.addP4Switch(f"rck_{pid}_{rid}")
                r = self.addP4RuntimeSwitch(f"rck_{pid}_{rid}")
                rck_mat[pid][rid] = r
                rck_switches.append(r)

        # deploy switch program to all switches
        self.setP4SourceAll(src)

        # hosts
        hst_mat = [[[None] * nhstp for _ in range(nrckp)] for _ in range(npod)]
        hosts = []
        for pid in range(npod):
            for rid in range(nrckp):
                for hid in range(nhstp):
                    h = self.addHost(f"hst_{pid}_{rid}_{hid}")
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
            # print(sid, ssid, [f[sid] for f in fab_mat])
            fs = [f[sid] for f in fab_mat]
            for f in fs:
                fpid, fsid = (int(n) for n in f.split("_")[1:])
                port = ssid
                self.addLink(s, f)
                if fpid < k // 2:
                    self.setIntfPort(s, f, fpid % (k // 2))
                else:
                    self.setIntfPort(s, f, flip(fpid % (k // 2)))
                self.setIntfPort(f, s, flip(port))

        self.ft_switches = {
            "rck": rck_switches,
            "fab": fab_switches,
            "spn": spn_switches,
        }
        self.ft_hosts = hosts

        if ctrl_port:
            # make one more host for the controller
            self.ctrl = self.addHost(f"ctrl")

            # add links to every switch
            self.ctrl_map = {}
            for p, switch in enumerate(rck_switches + fab_switches + spn_switches):
                self.ctrl_map[switch] = p
                self.addLink(switch, self.ctrl)
                self.setIntfPort(switch, self.ctrl, ctrl_port)
                self.setIntfPort(self.ctrl, switch, p)
