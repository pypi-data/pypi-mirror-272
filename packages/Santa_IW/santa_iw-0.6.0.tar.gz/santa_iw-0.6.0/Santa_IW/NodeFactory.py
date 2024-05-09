from collections import ChainMap
from pathlib import Path
from typing import Any

from libsrg.Config import Config

from Santa_IW.Node import Node
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TemplateFactory import TemplateFactory
from Santa_IW.TestBase import TestBase
from Santa_IW.TestFactory import TestFactory
from Santa_IW.Utils import log_entry_and_exit


class NodeFactory(Subassembly):
    """
    Factory for creating Nodes from json data.

    """

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        # self.logger.info(map_chain_as_str(self.args))
        self.nodemap: dict[str, Any] = {}

    def start(self) -> None:
        self.set_annotation("Loading Nodes...")
        self.log_internal_status(Status.OK, "Started", assess=True)
        # self.logger.info("Started")
        # self.logger.info(map_chain_as_str(self.args))
        tf: TestFactory = self.config().get_item("test_factory")
        tpf: TemplateFactory = self.config().get_item("template_factory")
        nodedirs: list[str] = self.config().get_item("nodedirs")
        for nodedir in nodedirs:
            dpath = Path(nodedir).resolve()
            self.process_node_subdir(dpath, group_below=self.tree_root_subassembly, tf=tf, tpf=tpf)

        self.set_annotation("Done")
        self.log_internal_status(Status.OK, "Done", assess=True)
        # self.logger.info("Finished")

    def process_node_subdir(self, dpath, group_below: Subassembly, tf: TestFactory, tpf: TemplateFactory):
        self.logger.info(f"Looking in {dpath} for group below {group_below.name()}")
        if dpath.is_dir():
            # first pass (group_pass=True) we are looking for special __file
            for group_pass in [True, False]:
                count_in_pass = 0
                for nodefile in dpath.glob("*.json"):
                    special = nodefile.stem.startswith("__")
                    if group_pass != special:
                        continue
                    self.logger.info(f"loading {nodefile}")
                    # noinspection PyBroadException
                    try:
                        data = Config(nodefile)
                        data["__LOADED_FROM__"] = str(nodefile)
                    except Exception as e:
                        msg = f"Error parsing {nodefile} {e}"
                        self.log_internal_status(Status.CRITICAL, msg)
                        self.logger.exception(msg, stack_info=True, exc_info=True)
                        continue
                    if int(data.get_item("register", default=1)) == 0:
                        self.logger.info(f"node not registered {nodefile} to {data}")
                        continue
                    if group_pass:
                        count_in_pass += 1
                        if count_in_pass > 1:
                            msg = f"More than one special node file in directory {nodefile}"
                            self.logger.info(msg)
                            self.log_internal_status(Status.CRITICAL, msg, assess=True)
                            raise Exception(msg)
                        if "group_below" in data:
                            group_below = data["group_below"]
                    self.logger.info(f"parsed {nodefile} to {data} below {group_below.name()}")
                    tpf.apply_templates(data)
                    short_name = data.get_item("short_name")
                    self.log_internal_status(Status.OK, f"Creating node {short_name} below {group_below.name()}")
                    node = Node(instance_config=data, short_name=short_name, parent=group_below)
                    self.nodemap[short_name] = node
                    if group_pass:
                        group_below = node
                    tf.create_tests_for_node(node, data)
            # all files in this directory processed, examine subdirs
            for subdir in dpath.iterdir():
                if not subdir.is_dir():
                    continue
                self.process_node_subdir(subdir, group_below, tf=tf, tpf=tpf)

    def start_nodes(self):
        self.logger.info(self.nodemap)
        for node in self.nodemap.values():
            self.logger.info(f"Starting {node}")
            node.start()

    @log_entry_and_exit
    def create(self, node_args: ChainMap[str, Any], test_args: dict[str, Any]) -> TestBase:
        name = test_args["test_type"]
        # self.logger.info(f"Creating {name} from\n {map_chain_as_str(self.nodemap)}")
        test_class = self.nodemap[name]
        test = test_class(node_args, test_args)
        return test
