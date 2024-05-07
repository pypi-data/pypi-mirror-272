from turbo_boot.singleton_meta import SingletonMeta
from turbo_boot.config_loader import ConfigLoader
import logging
from logging.handlers import RotatingFileHandler
from turbo_boot.logging_level import LoggingLevel
import sys
import os

def get_boolean(val: str) -> bool:
    if val is None:
        return None
    if len(val.strip()) == 0:
        return False
    if val.upper() == "TRUE":
        return True
    elif val.upper() == "FALSE":
        return False
    return False
    
class Logger(metaclass=SingletonMeta):
    def __init__(self, config_loader: ConfigLoader) -> None:
        self.__config_loader = config_loader
        self.__logger_name = (self.__config_loader.get_config("turbo-boot.logging.name") or "app")
        self.__logger = logging.getLogger(self.__logger_name)
        self.__setup_logging()
    
    def __setup_logging(self):
        self.__global_log_level = str(self.__config_loader.get_config("turbo-boot.logging.level") or "INFO")
        self.__global_log_format = (self.__config_loader.get_config("turbo-boot.logging.format") or '%(asctime)s | %(levelname)8s | %(lineno)d | %(message)s')
        self.__setup_console_handler()
        self.__setup_file_handler()
        
    def __setup_file_handler(self):
        if (get_boolean(self.__config_loader.get_config("turbo-boot.logging.file-handler.enabled")) or False):
            logger = self.__logger
            log_dir = (self.__config_loader.get_config("turbo-boot.logging.file-handler.dir-name") or "./")
            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir)
                except:
                    log_dir = '/tmp' if sys.platform.startswith('linux') else '.'
            
            log_file_name = (self.__config_loader.get_config("turbo-boot.logging.file-handler.file-name") or "app")
            log_file_path = os.path.join(log_dir, log_file_name) + '.log'
            
            log_file_max_bytes = int((self.__config_loader.get_config("turbo-boot.logging.file-handler.max-bytes") or '20000'))
            log_file_backup_count = int((self.__config_loader.get_config("turbo-boot.logging.file-handler.backup-count") or '5'))
            
            logger.file_handler = RotatingFileHandler(log_file_path, maxBytes=log_file_max_bytes, backupCount=log_file_backup_count)
            logger.file_handler.setLevel(LoggingLevel[str(self.__config_loader.get_config("turbo-boot.logging.file-handler.level") or self.__global_log_level).upper()].value)
            logger.file_handler.setFormatter(logging.Formatter((self.__config_loader.get_config("turbo-boot.logging.file-handler.format") or self.__global_log_format)))
            logger.addHandler(logger.file_handler)
    
    def __setup_console_handler(self):
        if (get_boolean(self.__config_loader.get_config("turbo-boot.logging.console-handler.enabled")) or True):
            logger = self.__logger
            logger.stdout_handler = logging.StreamHandler(sys.stdout)
            
            logger.stdout_handler.setLevel(LoggingLevel[str(self.__config_loader.get_config("turbo-boot.logging.console-handler.level") or self.__global_log_level).upper()].value)
            logger.stdout_handler.setFormatter(logging.Formatter((self.__config_loader.get_config("turbo-boot.logging.console-handler.format") or self.__global_log_format)))
            logger.addHandler(logger.stdout_handler)

    def info(self, log_msg):
        self.__logger.info(log_msg)
    
    def warning(self, log_msg):
        self.__logger.warning(log_msg)
        
    def debug(self, log_msg):
        self.__logger.debug(log_msg)
    
    def error(self, log_msg):
        self.__logger.error(log_msg)
    
    def critical(self, log_msg):
        self.__logger.critical(log_msg)
