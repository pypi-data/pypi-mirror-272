import logging
import os
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from ipaddress import IPv4Address, IPv4Network  # IPv4Network
from pathlib import Path
from typing import Any, Optional

from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Info import Info
from libsrg.LoggingAppBase import LoggingAppBase
from libsrg.Runner import Runner
from requests import Response, get

"""
This module is a sample application template for libsrg application logging
"""


class HostCreator:

    def __init__(self, address: IPv4Address, config: Config, group_paths: dict[str, Path], host_template_dir: Path):
        self.hostname_info = None
        self.is_localhost = None
        self.community = None
        self.map_dev_to_id: dict[str, str] = {}
        self.uname_hostname = "unknown"
        self.oui = None
        self.kernel_name: str = "unknown"
        self.mac_address: str = "unknown"
        self.oui: str = "unknown"
        self.group_path: Optional[Path] = None
        self.group_name: Optional[str] = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.address = address
        self.config = config
        self.group_paths = group_paths
        self.host_template_dir = host_template_dir
        #
        self.auto_tests: list[dict[str, Any]] = []
        self.auto_templates: list[str] = []
        self.can_ping = False
        self.can_ssh = False
        self.can_name = False
        self.can_snmp = False
        self.overwrite = self.config.get_item("overwrite")
        self.userat = None
        self.short = None
        self.ipaddrlist = None
        self.aliaslist = None
        self.fqdn = None
        # self.logger.info(f"Starting {address}")

    def identify(self):
        et = ElapsedTime("identify " + str(self.address))
        self.identify_inner()
        self.logger.debug(f"ElapsedTime {et}")

    def identify_inner(self):
        r = Runner(f"ping -q -c 4 -w 4 -i .25 -W .25 {self.address}", timeout=5, silent=True)
        self.can_ping = r.success
        if not self.can_ping:
            self.logger.debug(f"Can't ping {self.address}")
            return
        self.logger.info(f"Pinged {self.address}")
        try:
            self.fqdn, self.aliaslist, self.ipaddrlist = socket.gethostbyaddr(str(self.address))
            self.logger.info(f"Reverse DNS for Address: {self.address} Hostname: {self.fqdn}")
            self.can_name = True
        except socket.herror as e:
            self.logger.error(f"Reverse address lookup failed for {self.address} {e}", stack_info=True, exc_info=True)
        r2 = Runner(f"uname -n", timeout=5, userat=f"root@{self.address}", silent=True)
        self.can_ssh = r2.success
        if r2.success:
            self.uname_hostname = r2.so_lines[0]
        if r2.success and self.fqdn is None:
            self.fqdn = self.uname_hostname
            self.logger.info(f"uname -h for Address: {self.address} Hostname: {self.fqdn}")
            self.can_name = True
        if r2.success and self.fqdn != self.uname_hostname:
            self.logger.warning(
                f"Name conflict for {self.address} Reverse DNS: {self.fqdn} Uname: {self.uname_hostname}")
            self.can_name = False
        if self.fqdn is None:
            self.logger.warning(f"Can't find fqdn/hostname for {self.address}")
            self.can_name = False
            return
        localhost = self.config.get_item("localhost.fqdn")
        self.is_localhost = localhost == self.fqdn

        self.short = self.fqdn.split(".")[0]
        self.userat = f"root@{self.fqdn}"
        r = Runner(f"hostnamectl --json pretty", userat=self.userat, timeout=4, silent=True)
        self.can_ssh = r.success
        if r.success:
            self.hostname_info = Config.text_to_config(r.so_str)
            self.logger.info(r)
        r = Runner(f"uname -s", userat=self.userat, timeout=4, silent=True)
        if r.success:
            self.kernel_name = r.so_lines[0].strip()  # "Linux","Darwin"
        else:
            self.kernel_name = "unknown"
        r = Runner(f"arp {self.address}", timeout=4, silent=True)  # localhost not userat
        if r.success:
            for line in r.so_lines:
                parts = line.split()
                if parts[0] == "Address":
                    continue
                if parts[1] == "ether":
                    self.mac_address = parts[2].upper()
                    self.oui = self.mac_address[:8]
                    self.logger.info(f"{self.address=} {self.mac_address=} {self.oui=}")
        self.community = self.config.get_item("__SNMP_COMMUNITY__", secrets=True, default="public")
        cmd = ["snmpget", "-c", self.community, "-v2c", self.fqdn, "-Ovq", "iso.3.6.1.2.1.1.5.0"]
        r = Runner(cmd, timeout=4, silent=True)
        self.can_snmp = r.success

    def create_dev_map(self):
        """Builds a mapping between /dev/sdx and /dev/disk/by-id names"""
        if not self.can_ssh:
            return

        r = Runner("ls -l /dev/disk/by-id/*", userat=self.userat, timeout=4)
        if r.success:
            for line in r.so_lines:
                if "->" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "->":
                            by_id = parts[i - 1]
                            dev = parts[i + 1].replace("../../", "/dev/")
                            self.map_dev_to_id[dev] = by_id
                            break

    def get_dev_id(self, dev: str):
        """return disk/by_id if found, else dev unchanged"""
        if dev in self.map_dev_to_id:
            return self.map_dev_to_id[dev]
        return dev

    def process_host(self):
        et = ElapsedTime("process_host " + str(self.address))
        self.process_host_inner()
        self.logger.debug(f"ElapsedTime {et}")

    def process_host_inner(self):

        if not (self.can_ping and self.can_name):
            self.logger.debug(f"Skip Processing {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")
            return

        if not self.determine_group():
            self.logger.info(
                f"Skip Processing (no group) {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")
            return

        # self.logger.info(f"Start Processing {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")

        self.create_dev_map()

        self.write_host_file()
        self.write_host_template()
        self.logger.info(f"End Processing {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")

    def determine_group(self) -> bool:
        # lst = self.config.to_list()
        # self.logger.info(lst)
        if self.kernel_name in self.config:
            self.group_name = self.config.get_item(self.kernel_name)
        else:
            self.logger.error(f"Can't find group for {self.kernel_name}, dropping {self.address} {self.fqdn}")
            return False

        self.logger.info(f"{self.address} {self.short} assigned group {self.group_name}")
        explicit_group_assignments = Config(self.config.get_item("explicit_group_assignments", default={}))
        g0 = self.group_name
        self.logger.info(f"searching {str(self.address)=}, {self.short=}, {self.mac_address=}, {self.oui=}")
        gnew = explicit_group_assignments.get_item(str(self.address), self.short, self.mac_address, self.oui,
                                                   default=g0)
        if g0 != gnew:
            self.group_name = gnew
            self.logger.info(f"{self.address} {self.short} group reassigned {g0} -> {self.group_name}")

        if self.group_name in self.group_paths:
            self.group_path = self.group_paths[self.group_name]
        else:
            if self.group_name.lower().startswith(("drop", "!")):
                self.logger.warning(f"Group {self.group_name}, dropping {self.address} {self.short}")
                return False
            self.logger.error(f"Group {self.group_name} does not exist, dropping {self.address} {self.short}")
            return False
        return True

    def write_host_file(self):
        fname: Path = self.group_path / f"{self.fqdn}.json"
        if fname.exists() and not self.overwrite:
            self.logger.warning(f"Host file {fname} is already exists -- not overwriting")
            return
        additional_tests = Config(self.config.get_item("additional_tests", default={}))
        data = additional_tests.get_item(str(self.address), self.short, self.mac_address, self.oui, default={})

        ncon = Config(data)
        ncon.set_item("fqdn", self.fqdn)
        ncon.set_item("discovered_ipv4", str(self.address))
        ncon.set_item("discovered_mac", str(self.mac_address))
        ncon.set_item("discovered_oui", str(self.oui))

        ncon.set_item("short_name", self.short)
        templates = ncon.get_item("templates", default=[])
        templates.append(f"auto_{self.fqdn}")
        ncon.set_item("templates", templates)
        ncon.to_json_file(fname, indent=4)
        self.logger.info(f"Host config for {self.fqdn} added at {fname}")

    def add_test(self, d: dict[str, Any]):
        self.auto_tests.append(d)
        self.logger.info(f"{self.short} Adding test {len(self.auto_tests)} {d} ")

    def add_template(self, d: str):
        self.auto_templates.append(d)
        self.logger.info(f"{self.short} Adding template {len(self.auto_templates)} {d} ")

    def write_host_template(self):
        fname: Path = self.host_template_dir / f"auto_{self.fqdn}.json"
        if fname.exists() and not self.overwrite:
            self.logger.warning(f"Host file {fname} is already exists -- not overwriting")
            return
        ncon = Config()

        self.add_ping_intranet()
        self.add_df()
        self.add_linux_common()
        self.add_smart()
        self.add_zfs_stuff()
        self.add_cockpit()
        self.add_sestatus()
        self.add_sensors()
        self.add_snmp()
        self.add_apcaccess()
        self.add_nfs()
        self.add_smb()
        self.add_http()
        self.add_time_machine()

        ncon.set_item("intended_for", self.fqdn)
        ncon.set_item("tests", self.auto_tests)
        ncon.set_item("templates", self.auto_templates)
        ncon.to_json_file(fname, indent=4)
        self.logger.info(f"Host template for {self.fqdn} added at {fname}")

    def add_ping_intranet(self):
        if self.can_ping and not self.can_ssh:
            self.add_test(
                {
                    "test_type": "PingTest_D"
                })
        else:
            self.add_test(
                {
                    "test_type": "PingTest_A"
                })

    def add_linux_common(self):
        if self.can_ssh:
            self.add_test(
                {
                    "test_type": "Uname"
                })
            self.add_test(
                {
                    "test_type": "Uptime"
                })
            self.add_test(
                {
                    "test_type": "SystemctlFailed"
                })
            self.add_test(
                {
                    "test_type": "PendingUpdates"
                })
            self.add_test(
                {
                    "test_type": "IPV4_Address"
                })
            self.add_test(
                {
                    "test_type": "IPV6_Address"
                })

    def add_snmp(self):
        if not self.can_snmp:
            return
        self.add_test(
            {
                "test_type": "SNMP_id",
                "community": "{{__SNMP_COMMUNITY__}}",
            })

    def add_sensors(self):
        if self.can_ssh:
            r = Runner("sensors -j", userat=self.userat, timeout=5)
            if r.success:
                self.add_test(
                    {
                        "test_type": "Sensors"
                    })

    def add_cockpit(self):
        if self.can_ssh:
            r = Runner(f"systemctl is-enabled cockpit", userat=self.userat, timeout=5)
            if r.success:
                self.add_template("Cockpit")

    # noinspection HttpUrlsUsage
    def add_http(self):
        urls = [f"http://{self.fqdn}", f"https://{self.fqdn}"]
        if self.is_localhost:
            # don't test santa interface across instances
            # tends to pick up development testing and generate extra tests
            # which fail when development activity pauses or stops
            urls.append(f"http://{self.fqdn}:4242/")
        for url_ in urls:
            try:
                response: Response = get(url_, timeout=5)
                code = response.status_code
                ok = code in [200]
                self.logger.info(f"Response from {url_=} -> {code=} {ok=}")
                if ok:
                    self.add_test(
                        {
                            "test_type": "HTTPTest",
                            "url": url_
                        })
            except Exception as e:
                self.logger.warning(f"Exception while trying to get {url_=} -> {e}")

    def add_nfs(self):
        if self.can_ssh:
            r = Runner(f"exportfs -s", userat=self.userat, timeout=5)
            if r.success:
                share_list = [line.split()[0] for line in r.so_lines]
                if len(share_list) > 0:
                    self.add_test(
                        {
                            "test_type": "Shares_NFS",
                            "shares": share_list
                        })

    def add_smb(self):
        if self.can_ssh:
            smb_username = self.config.get_item("__SECRET__SMB_USER", secrets=True, default=None, allow_none=True)
            smb_password = self.config.get_item("__SECRET__SMB_PASS", secrets=True, default=None, allow_none=True)
            if smb_username and smb_password:
                r = Runner(f"smbclient -L  {self.fqdn} -U {smb_username} --password {smb_password}", timeout=5)
            else:
                r = Runner(f"smbclient -L  {self.fqdn}", timeout=5)
            if r.success:
                share_list = [line.strip().split()[0] for line in r.so_lines if "Disk" in line]
                if smb_username and smb_password:
                    self.add_test(
                        {
                            "test_type": "Shares_SMB",
                            "shares": share_list,
                            "smb_username": "{{__SECRET__SMB_USER}}",
                            "smb_password": "{{__SECRET__SMB_PASS}}",
                        })
                else:
                    self.add_test(
                        {
                            "test_type": "Shares_SMB",
                            "shares": share_list,
                        })

    def add_sestatus(self):
        if self.can_ssh:
            r = Runner(f"sestatus", userat=self.userat, timeout=5)
            if r.success:
                self.add_test({"test_type": "SE_Status"})

    # noinspection PyTestUnpassedFixture
    def add_smart(self):
        if self.can_ssh:
            r = Runner(f"smartctl --scan --json", userat=self.userat, timeout=8)
            #  "devices": [
            #     {
            #       "name": "/dev/sda",
            #       "info_name": "/dev/sda",
            #       "type": "scsi",
            #       "protocol": "SCSI"
            #     },
            #     {
            #       "name": "/dev/sdb",
            #       "info_name": "/dev/sdb",
            if r.success:
                txt = '\n'.join(r.so_lines)
                # self.logger.info(f"{txt}")
                con = Config(Config.text_to_dict(txt))
                if "devices" in con:
                    devs = con.get_item("devices")
                    for dev_ in devs:
                        dev_name = dev_.get("name")
                        by_id = self.get_dev_id(dev_name)
                        cmd = {
                            "dev": by_id,
                            "dev_raw": dev_name,
                            "test_type": "SmartCtl"
                        }
                        self.add_test(cmd)

    def add_apcaccess(self):
        if self.can_ssh:
            r = Runner("apcaccess -u", userat=self.userat, timeout=5, retries=1)
            if r.success:
                cmd = {
                    "test_type": "ApcAccess"
                }
                self.add_test(cmd)

    def add_df(self):
        if self.can_ssh:
            r = Runner(f"cat /etc/fstab", userat=self.userat, timeout=5)
            if r.success:
                # #
                # # /etc/fstab
                # # Created by anaconda on Thu Mar 14 21:16:25 2024
                # #
                # # Accessible filesystems, by reference, are maintained under '/dev/disk/'.
                # # See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
                # #
                # # After editing this file, run 'systemctl daemon-reload' to update systemd
                # # units generated from this file.
                # #
                # /dev/mapper/rhel_kylo-root /                       xfs     defaults        0 0
                # UUID=abf33b68-bf8c-4a55-8189-98d9ec34e699 /boot                   xfs     defaults        0 0
                # UUID=925A-976A          /boot/efi               vfat    umask=0077,shortname=winnt 0 2
                # /dev/mapper/rhel_kylo-home /home                   xfs     defaults        0 0
                # /dev/mapper/rhel_kylo-swap none                    swap    defaults        0 0
                for line in r.so_lines:
                    if line.startswith(("#", ";")):
                        continue
                    parts = line.split()
                    if len(parts) >= 2:
                        path = parts[1]
                        path.strip()
                        if path in ["none", "/proc", "swap"]:
                            continue
                        instance_name = path.replace("/", "_")
                        cmd = {
                            "test_type": "DiskFree",
                            "path": path,
                            "instance_name": instance_name
                        }
                        self.add_test(cmd)

    def add_time_machine(self):
        if not self.can_ssh:
            return
        r = Runner("zfs list -H -o mountpoint", userat=self.userat, timeout=10)
        if not r.success:
            return
        for line in r.so_lines:
            r2 = Runner(f"ls {line}/*bundle/com.apple.TimeMachine.MachineID.plist", userat=self.userat,
                        timeout=10)
            pth = Path(line)
            nam = Path(pth.name).name
            if r2.success:
                cmd = {
                    "test_type": "TimeMachine",
                    "path": line,
                    "instance_name": nam
                }
                self.add_test(cmd)

    # noinspection PyTestUnpassedFixture
    def add_zfs_stuff(self):
        if not self.can_ssh:
            return
        r = Runner("zpool list -H -o name", userat=self.userat, timeout=10)
        if not r.success:
            return
        cmd = {
            "test_type": "ZFS_Version",
            "period": 900
        }
        self.add_test(cmd)
        for poolname in r.so_lines:
            cmd = {
                "test_type": "Zpool_Status",
                "instance_name": poolname,
                "period": 300,
                "pool": poolname
            }
            self.add_test(cmd)
            cmd = {
                "test_type": "Zpool_Free",
                "instance_name": poolname,
                "period": 300,
                "pool": poolname
            }
            self.add_test(cmd)
        zvols_processed = []
        r = Runner("cat /etc/pyznap/pyznap.conf", userat=self.userat, timeout=4)
        if r.success:
            data = Config(Config.text_to_dict('\n'.join(r.so_lines)))
            for vol_name in data.keys():
                sdata = data[vol_name]
                if sdata.get("snap", "no") == "yes":
                    cmd = {
                        "par_0": vol_name,
                        "test_type": "ZFS_Snapshots_Master"
                    }
                    self.add_test(cmd)
                    zvols_processed.append(vol_name)
        r = Runner("zfs list -H -o name", userat=self.userat, timeout=10)
        zvols = r.so_lines
        for vol_name in zvols:
            # Looking for vols with no child vols
            matched = False
            for vol_name2 in zvols:
                if vol_name == vol_name2:
                    continue
                if vol_name2.startswith(vol_name):
                    matched = True
                    break
            if matched:
                continue
            if vol_name in zvols_processed:
                continue
            if not self.check_age_of_snapshots(vol_name):
                continue
            cmd = {
                "par_0": vol_name,
                "test_type": "ZFS_Snapshots_Copy"
            }
            self.add_test(cmd)
            zvols_processed.append(vol_name)

    def check_age_of_snapshots(self, vol) -> bool:
        zargs = ["/sbin/zfs", "list", "-H", "-t",
                 "snapshot", "-r",
                 "-d1", "-o", "name,creation", "-S", "creation", vol]
        r = Runner(zargs, userat=self.userat, timeout=15)
        lines = r.so_lines
        ret = r.ret
        if ret != 0:
            res_str = f"UNKNOWN - Command Error 0x{ret:04x} {vol}"
            self.logger.warning(res_str)
            return False
        else:
            minutes = 60
            crit_t = timedelta(0, minutes * 60)

            # reg=re.compile(r'auto-([-0-9:_.]*)')
            # regp=re.compile(r'[-:_.]+')
            dtnow = datetime.now()
            if lines:
                for line in lines:
                    parts = line.split('\t')
                    self.logger.info(parts)
                    # name = parts[0]
                    if len(parts) > 1:
                        dat_a = parts[1]
                        dt = datetime.strptime(dat_a, '%a %b %d %H:%M %Y')
                        age = dtnow - dt
                        self.logger.info(f"Snapshot {vol} age {age} minutes")
                        return age <= crit_t
        return False


class MakeLists(LoggingAppBase):

    def __init__(self):
        super().__init__()  # super defines self.logger
        self.local_plugins_config_dir = None
        self.local_plugin_modules_dir = None
        self.candidate_hosts: list[HostCreator] = []
        self.network_dir = None
        self.mobile_dir = None
        self.iot_dir = None
        self.hosts_dir = None
        self.secrets_path = None
        self.local_tests_dir = None
        self.local_template_dir = None
        self.host_template_dir = None
        self.host_nodes_dir = None
        self.santa_config_dir = None
        self.user_config = Config()
        self.group_path_dict: dict[str, Path] = dict()

        self.is_root = os.getuid() == 0
        if self.is_root:
            assumed_dir = Path("/opt/Santa_IW/CONFIG")
        else:
            assumed_dir = Path.home() / "Santa_IW" / "CONFIG"
        # local_info = Info("localhost")
        # local_info.dump()

        # setup any program specific command line arguments
        self.parser.add_argument('--dir', help="Dir to generate files into", dest='santa_config_dir',
                                 default=str(assumed_dir))
        self.parser.add_argument('--config', help="Configuration File", dest='config', default=None)
        self.parser.add_argument('--threads', help="Number of threads in pool", dest='num_threads', type=int,
                                 default=32)

        # invoke the parser
        self.perform_parse()

        # create output dir if missing
        self.santa_config_dir = Path(self.args.santa_config_dir)
        if not self.santa_config_dir.exists():
            self.santa_config_dir.mkdir()
        self.logger.info(f"Santa_IW config output to {self.santa_config_dir}")

        # form path to where makelist config will reside in output dir
        self.makelist_path_perm = self.santa_config_dir / "santa_makelist.json"

        # figure out where the defaults files live
        my_file = __file__
        self.module_dir = Path(my_file).parent
        self.install_parent_dir = self.module_dir.parent.parent
        self.logger.info(f"Install parent dir {self.install_parent_dir}")
        self.install_dir_path = self.module_dir / "INSTALL_CONFIG"
        self.minimal_makelist_path = self.install_dir_path / "minimal_makelist.json"

        # use command line config path if given
        if self.args.config is not None:
            self.makelist_path = Path(self.args.config)
        else:
            # else use file in output dir if it exists
            self.makelist_path = self.santa_config_dir / "santa_makelist.json"
            if not self.makelist_path.exists():
                # finally, use file from install dir as fallback
                self.makelist_path = self.minimal_makelist_path

        self.logger.info(f"Santa_IW makelist input config is {self.makelist_path}")
        self.info = Info()
        self.localhost_config = self.info.to_config("localhost.")
        self.config = Config(self.makelist_path, self.localhost_config)

        if self.makelist_path_perm != self.makelist_path:
            self.config.to_json_file(self.makelist_path_perm, indent=4)
            self.logger.info(f"Santa_IW makelist input config saved to  {self.makelist_path_perm}")

        self.worker_pool = ThreadPoolExecutor(max_workers=self.args.num_threads)
        self.logger.info(f"Started pool with {self.args.num_threads} threads")

        self.create_dirs()
        self.loop_over_scans()
        # self.scan_network(self.args.network)
        self.write_config()
        #

    def create_dirs(self) -> None:
        self.logger.info(f"Santa_IW dir: {self.santa_config_dir}")

        nuke_old_hosts = self.config.get_item("nuke_old_hosts", default=False)

        # top directory for node definitions
        self.host_nodes_dir = self.santa_config_dir / 'HOST_NODES'
        if nuke_old_hosts and self.host_nodes_dir.exists():
            _ = Runner(f"rm -rf {self.host_nodes_dir}")

        self.host_nodes_dir.mkdir(parents=True, exist_ok=True)
        self.user_config.set_item("nodedirs", [
            "{{__CONFIG__}}/HOST_NODES",
        ])

        # this dir holds automatically generated templates for each host
        self.host_template_dir = self.santa_config_dir / 'AUTO_HOST_TEMPLATES'
        self.host_template_dir.mkdir(parents=True, exist_ok=True)

        # this is where a user can add their own templates
        self.local_template_dir = self.santa_config_dir / 'LOCAL_TEMPLATES'
        self.local_template_dir.mkdir(parents=True, exist_ok=True)
        self.user_config.set_item("templatedirs", [
            "{{__CONFIG__}}/LOCAL_TEMPLATES",
            "{{__CONFIG__}}/AUTO_HOST_TEMPLATES",
            "{{__INSTALL__}}/TEMPLATES",
        ])

        # this is where a user can add their own plugins
        self.local_plugin_modules_dir = self.santa_config_dir / 'LOCAL_PLUGIN_MODULES'
        self.local_plugin_modules_dir.mkdir(parents=True, exist_ok=True)
        self.user_config.set_item("plugin_modules_dirs", [
            "{{__CONFIG__}}/LOCAL_PLUGIN_MODULES",
            "{{__INSTALL__}}/PLUGIN_MODULES",
        ])

        # this is where a user can add their own plugin configurations
        self.local_plugins_config_dir = self.santa_config_dir / 'LOCAL_PLUGIN_CONFIG'
        self.local_plugins_config_dir.mkdir(parents=True, exist_ok=True)
        self.user_config.set_item("plugin_config_dirs", [
            "{{__CONFIG__}}/LOCAL_PLUGIN_CONFIG",
            "{{__INSTALL__}}/PLUGIN_CONFIG",
        ])

        # this is where a user can add their own tests
        self.local_tests_dir = self.santa_config_dir / 'LOCAL_TESTS'
        self.local_tests_dir.mkdir(parents=True, exist_ok=True)
        self.user_config.set_item("testdirs", [
            "{{__CONFIG__}}/LOCAL_TESTS",
            "{{__INSTALL__}}/TESTS",
        ])

        # create group subdirectories below HOST_NODES
        groups: dict[str, Any] = self.config.get_item("groups")
        for group, gconfig in groups.items():
            # if the given group name contains a slash "HOSTS/RPI"
            # this will magically create nested groups
            # groupz is just the last part of this name
            groupz = group.split('/')[-1]
            path = self.host_nodes_dir / group
            path.mkdir(parents=True, exist_ok=True)
            self.group_path_dict[group] = path
            # data in config should just reflect th last part of this name
            con = Config(dict({
                "short_name": groupz,
                "tests": [],
                "templates": []
            }), gconfig)

            con.to_json_file(path / f'__{groupz}.json', indent=4)
            self.logger.info(f"Santa_IW group path {group} at {path}")

        self.secrets_path = self.santa_config_dir.parent / "SECRETS" / "santa_secrets.json"
        if not self.secrets_path.exists():
            placeholder = Config()
            placeholder.set_item("__SECRETS_HELP__", "https://gitlab.com/SRG_gitlab/santa-is-watching/-/wikis/Secrets")
            placeholder.to_json_file(self.secrets_path, indent=4)

        Config.set_secrets(self.secrets_path)

    @classmethod
    def demo(cls):
        _ = MakeLists()

    def write_config(self):
        pout = self.santa_config_dir / 'santa_config.json'
        nuke_user_config = bool(self.config.get_item("nuke_user_config", default=False))
        if pout.exists() and not nuke_user_config:
            self.logger.warning(f"Santa_IW config file {pout} already exists -- not overwritten")
        else:
            self.user_config.to_json_file(pout, indent=4)

    def loop_over_scans(self):
        scan_defaults = self.config.get_item("scan_defaults")
        scans = self.config.get_item("scans")
        for scan in scans:
            scan_config = Config(scan, scan_defaults, self.config)
            self.perform_one_scan(scan_config)

        self.logger.info(f"Phase one, identify hosts")
        futures = [self.worker_pool.submit(candidate.identify) for candidate in self.candidate_hosts]
        for future in futures:
            future.result()
        self.logger.info(f"Phase two, process hosts")
        futures = [self.worker_pool.submit(candidate.process_host) for candidate in self.candidate_hosts if
                   candidate.can_ping]
        for future in futures:
            future.result()

    def perform_one_scan(self, scan_config: Config):
        first_ip = scan_config.get_item("first_ip")
        last_ip = scan_config.get_item("last_ip")
        if first_ip.lower() == "auto":
            local_info = Info("localhost")
            r = Runner("ip -oneline addr", timeout=5)
            for line in r.so_lines:
                if local_info.ip in line:
                    # 2: enp0s31f6    inet 10.0.4.32/24 brd 10.0.4.255 scope global dynamic noprefixroute enp0s31f6\       valid_lft 3076sec preferred_lft 3076sec
                    parts = line.split()
                    cidr_range = parts[3]
                    break
            else:
                self.logger.error(f"Could not find ip address {local_info.ip} in {r.so_lines}")
                exit(1)
            network = IPv4Network(cidr_range, strict=False)
            net0 = network.network_address
            netz = network.broadcast_address
            inet0 = self.ipv4_to_int(net0) + 1
            inetz = self.ipv4_to_int(netz) - 1
            inetz = min(inetz, inet0 + 512 - 3)
            first_address = IPv4Address(inet0)
            last_address = IPv4Address(inetz)
            self.logger.info(f"Santa_IW auto will scan {first_address} -> {last_address}")
        else:
            first_address = IPv4Address(first_ip)
            last_address = IPv4Address(last_ip)
        self.logger.info(
            f"{first_address=} {first_address.packed=} {first_address.compressed=} {last_address.exploded=} {last_address.version=}")
        first_int = self.ipv4_to_int(first_address)
        last_int = self.ipv4_to_int(last_address)
        num = last_int - first_int
        self.logger.info(f"Scanning {num=} addresses {first_address=} {last_address=}")
        for iaddr in range(first_int, last_int + 1):
            ip = IPv4Address(iaddr)
            self.logger.info(f"Scanning {ip=} {iaddr=:x}")
            x = HostCreator(address=ip, config=scan_config, host_template_dir=self.host_template_dir,
                            group_paths=self.group_path_dict)
            self.candidate_hosts.append(x)

    # noinspection PyMethodMayBeStatic
    def ipv4_to_int(self, ipv4: IPv4Address) -> int:
        byts = ipv4.packed
        v: int = 0
        for byte in byts:
            v = v * 256 + byte
        return v


if __name__ == '__main__':
    MakeLists.demo()
