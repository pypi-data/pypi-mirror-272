import argparse
import atexit
import logging
import logging.config
import os
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None


import libsrg.LoggingCounter
from libsrg.Config import Config
from libsrg.Info import Info
from libsrg.LoggingCounter import LoggingCounter

from Santa_IW.TreeRoot import TreeRoot


class Main:
    """
    Main starts up the application by:
    - Initializing the logger
    - Parsing the command line
    - Instantiating TreeRoot with args
    - Passing control to the TreeRoot

    TreeRoot will be the overall control class for this application.
    It is a singleton and all application objects will be discoverable from there.

    """

    def __init__(self):

        """ Initializing the santa application """
        my_file = __file__
        santa_module_dir = Path(my_file).parent
        santa_clone_dir = santa_module_dir.parent
        santa_opt_dir = santa_clone_dir.parent
        santa_log_dir = santa_opt_dir / "LOGS"
        santa_db_dir = santa_opt_dir / "DB"
        santa_secrets_dir = santa_opt_dir / "SECRETS"
        santa_user_config_dir = santa_opt_dir / "CONFIG"
        install_dir_path = santa_module_dir / "INSTALL_CONFIG"

        parser_args = {}
        self.parser = argparse.ArgumentParser(**parser_args)
        self.parser.add_argument('--config', help="path to configuation file", dest='config_file')
        self.parser.add_argument("--level", help="Logging level at santa.log", action='store',
                                 choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")
        self.parser.add_argument("--console", help="Logging level at console (stderr)", action='store',
                                 choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR")

        self.args = self.parser.parse_args()

        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed": {
                    "format": "%(asctime)s %(levelname)-8s %(lineno)4d %(name) 20s.%(funcName)-22s -- %(message)s"
                }
            },
            "handlers": {

                "counter": {
                    "class": "libsrg.LoggingCounter.LoggingCounter",
                    "level": "DEBUG",
                    "formatter": "detailed",
                },
                "stderr": {
                    "class": "logging.StreamHandler",
                    "level": self.args.console.upper(),
                    "formatter": "detailed",
                    "stream": "ext://sys.stderr"
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": self.args.level.upper(),
                    "formatter": "detailed",
                    "filename": santa_log_dir / "santa.log",
                    "maxBytes": 100_000_000,
                    "backupCount": 5,
                    "mode": "a"
                }
            },
            "root": {
                "level": "DEBUG",
                "handlers": [
                    "stderr",
                    "file",
                    "counter"
                ]
            }
        }
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger(self.__class__.__name__)
        atexit.register(libsrg.LoggingCounter.LoggingCounter.log_counters)

        # any major issues here are assumed fatal
        # no heroics, but I do want to log what happens (as soon as logging is running).
        self.exit_counter = 0
        try:



            # figure out where the defaults file lives
            defaults_file_path = install_dir_path / "santa_defaults.json"

            startup_config=Config()
            # remember where install files are
            startup_config["__INSTALL__"] = str(install_dir_path)
            startup_config["__CONFIG__"] = str(santa_user_config_dir)
            startup_config["__SANTA_MODULE_DIR__"] = str(santa_module_dir)
            startup_config["__SANTA_CLONE_DIR__"] = str(santa_clone_dir)
            startup_config["__SANTA_OPT_DIR__"] = str(santa_opt_dir)
            startup_config["__SANTA_LOG_DIR__"] = str(santa_log_dir)
            startup_config["__SANTA_DB_DIR__"] = str(santa_db_dir)
            startup_config["__SANTA_SECRETS_DIR__"] = str(santa_secrets_dir)

            if tomllib:
                with open(santa_clone_dir / "pyproject.toml", 'rb') as fp:
                    toml_dict = tomllib.load(fp)
                version = toml_dict["tool"]["poetry"]["version"]
            else:
                version = "0.0.0"
            startup_config["SANTA_VERSION"] = version


            # Get localhost info
            localhost_info = Info()
            localhost_config= localhost_info.to_config("localhost_")
            localhost_config.set_item("localhost_is_root", os.geteuid() == 0)
            localhost_config.set_item("fqdn", localhost_info.fqdn)

            # load the defaults file
            defaults_config = Config(defaults_file_path,localhost_config,startup_config)

            config_file_path = Path(self.args.config_file) if self.args.config_file is not None \
                else santa_user_config_dir / "santa_config.json"

            # noinspection PyUnboundLocalVariable
            primary_config = Config(config_file_path, defaults_config)


            self.treeroot = TreeRoot(primary_config)
            self.treeroot.start()
            LoggingCounter.rotate_files()
            exit(0)

        except Exception as e:
            self.logger.exception(f"Fatal: {type(e)} {e}", stack_info=True, exc_info=True)
            exit(1)


if __name__ == '__main__':
    _ = Main()
