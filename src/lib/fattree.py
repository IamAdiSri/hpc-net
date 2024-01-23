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

        # |pods| = k

        # |spine switches} = (k//2)**2
        self.spn_switches = [self.addP4Switch(f"spn{i}") for i in range((k // 2) ** 2)]

        # |fabric switches| = (k**2)//2
        self.fab_switches = [self.addP4Switch(f"fab{i}") for i in range(k**2 // 2)]

        # |rack switches| = (k**2)//2
        self.rck_switches = [self.addP4Switch(f"rck{i}") for i in range(k**2 // 2)]

        # deploy switch program to all switches
        self.setP4SourceAll(src)

        # |self.ft_hosts| = (k**3)//4
        self.ft_hosts = [self.addHost(f"hst{i}") for i in range(k**3 // 4)]

        # Connect spine switches to fabric switches
        fab_conns = [[] for _ in range(len(self.fab_switches))]
        for c in range((k // 2) ** 2):
            for pod in range(k):
                f = pod * (k // 2) + c // (k // 2)

                s_port = pod % (k // 2)
                if pod >= k // 2:
                    s_port = flip(s_port)
                    f_port = s_port
                else:
                    f_port = flip(s_port)

                self.addLink(self.spn_switches[c], self.fab_switches[f])
                self.setIntfPort(self.spn_switches[c], self.fab_switches[f], c + s_port)
                self.setIntfPort(self.fab_switches[f], self.spn_switches[c], c + f_port)
                fab_conns[f].append(c + f_port)

        # Connect fabric switches to rack switches
        rck_conns = [[] for _ in range(len(self.rck_switches))]
        for f in range((k**2) // 2):
            si = f // (k // 2) * (k // 2)
            for t in range(si, si + k // 2):
                f_port = flip(fab_conns[f][t % (k // 2)])
                r_port = fab_conns[f][t % (k // 2)]

                self.addLink(self.fab_switches[f], self.rck_switches[t])
                self.setIntfPort(self.fab_switches[f], self.rck_switches[t], f_port)
                self.setIntfPort(self.rck_switches[t], self.fab_switches[f], r_port)

                rck_conns[t].append(r_port)

        # Connect rack switches to hosts
        hst_conns = [[] for _ in range(len(self.ft_hosts))]
        for t in range((k**2) // 2):
            si = t * (k // 2)
            for s in range(si, si + k // 2):
                r_port = flip(rck_conns[t][s % (k // 2)])
                h_port = rck_conns[t][s % (k // 2)]

                self.addLink(self.rck_switches[t], self.ft_hosts[s])
                self.setIntfPort(self.rck_switches[t], self.ft_hosts[s], r_port)
                self.setIntfPort(self.ft_hosts[s], self.rck_switches[t], h_port)
                hst_conns[s].append(h_port)