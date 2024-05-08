import configparser
import logging
import multiprocessing
from pathlib import Path

import wgse

logging.getLogger().setLevel(logging.DEBUG)


class WGSEDefaults:
    """Specify some directory where to find configuration files."""

    WGSE_FOLDER = Path(wgse.__file__).parents[1]
    LOCAL_CONFIG = Path(WGSE_FOLDER, "configuration", "main.ini")
    GLOBAL_CONFIG = Path(Path.home(), ".wgse", "main.ini")


class GeneralConfig:
    def __init__(self) -> None:
        self.last_path: Path = Path.home()
        self.log_level: str = "DEBUG"


class ExternalConfig:
    def __init__(self) -> None:
        self.root: Path = Path(WGSEDefaults.WGSE_FOLDER, "3rd_party")
        self.threads: int = multiprocessing.cpu_count()


class RepositoryConfig:
    def __init__(self) -> None:
        self.repository: Path = Path(WGSEDefaults.WGSE_FOLDER, "repository")
        self.metadata: Path = Path(self.repository, "metadata")
        self.temporary: Path = Path(self.repository, "temp")


class AlignmentStatsConfig:
    def __init__(self) -> None:
        self.skip: int = 40000
        self.samples: int = 20000


class ConfigurationManager:
    GENERAL: GeneralConfig = GeneralConfig()
    EXTERNAL: ExternalConfig = ExternalConfig()
    REPOSITORY: RepositoryConfig = RepositoryConfig()
    ALIGNMENT_STATS: AlignmentStatsConfig = AlignmentStatsConfig()

    def __init__(self) -> None:
        self.load()

    def load(self) -> None:
        self._parser = configparser.ConfigParser()
        logging.info(
            f"Found file {WGSEDefaults.LOCAL_CONFIG}: {WGSEDefaults.LOCAL_CONFIG.exists()}"
        )
        logging.info(
            f"Found file {WGSEDefaults.GLOBAL_CONFIG}: {WGSEDefaults.GLOBAL_CONFIG.exists()}"
        )
        self._parser.read(WGSEDefaults.LOCAL_CONFIG)
        self._parser.read(WGSEDefaults.GLOBAL_CONFIG)

        for var_name, var_value in ConfigurationManager.__dict__.items():
            if var_name.startswith("__"):
                continue
            if getattr(var_value, "__dict__") == None:
                continue
            if type(var_value) == type(ConfigurationManager.load):
                continue

            section = var_name.lower()
            if section not in self._parser:
                continue
            for key, value in self._parser[section].items():
                if key not in var_value.__dict__:
                    logging.warning(f"Configuration {section}.{key} not known")
                    continue
                if value is None:
                    continue
                var_type = type(var_value.__dict__[key])
                var_value.__dict__[key] = var_type(value)

    def save(self, save_defaults=False):
        for var_name, var_value in ConfigurationManager.__dict__.items():
            if var_name.startswith("__"):
                continue
            if getattr(var_value, "__dict__") == None:
                continue
            if type(var_value) == type(ConfigurationManager.load):
                continue

            default_item = type(var_value)()
            section = var_name.lower()
            if section not in self._parser:
                self._parser.add_section(section)
            for key, value in var_value.__dict__.items():
                if default_item.__dict__[key] != value or save_defaults:
                    self._parser[section][key] = str(value)
            if len(self._parser[section]) == 0 and not save_defaults:
                self._parser.remove_section(section)
        ordered_config_paths = [WGSEDefaults.GLOBAL_CONFIG, WGSEDefaults.LOCAL_CONFIG]
        if not any([x.exists() for x in ordered_config_paths]):
            with ordered_config_paths[1].open("wt") as f:
                pass
        for config in ordered_config_paths:
            if not config.exists():
                continue
            with config.open("wt") as f:
                self._parser.write(f)
            break


MANAGER_CFG = None
if MANAGER_CFG is None:
    MANAGER_CFG = ConfigurationManager()
