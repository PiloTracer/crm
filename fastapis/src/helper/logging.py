'''global logging'''
import logging
import traceback
from datetime import datetime
from couchdb import Server, Session

from core.settings import SettingsLog

# Custom handler for CouchDB


class CustomFormatterDb(logging.Formatter):
    '''logging custom formatter for extra fields'''

    def format(self, record):
        if not hasattr(record, 'username'):
            record.username = 'N/A'  # You can change 'N/A' to any default value you prefer
        if not hasattr(record, 'merchant'):
            record.merchant = 'N/A'  # You can change 'N/A' to any default value you prefer

        # Call the original formatter to do the actual message formatting
        return super().format(record)


class CustomFormatterFile(logging.Formatter):
    '''logging custom formatter for extra fields'''

    def format(self, record):
        record.username = getattr(record, 'username', 'N/A')
        record.merchant = getattr(record, 'merchant', 'N/A')

        # Call the original formatter to do the actual message formatting
        return super().format(record)


class LocalFileHandler(logging.Handler):
    '''logging couchdb handler'''

    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file

    def emit(self, record):
        # Enhanced log entry structure

        try:
            # Write to file
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(self.format(record) + '\n')
        except Exception as e:  # pylint: disable=broad-except
            print(f"Failed to set up local file handler: {e}")


class CouchDBHandler(logging.Handler):
    '''logging couchdb handler'''

    def __init__(self, db_url, db_name, username, password):
        super().__init__()
        self.db_url = db_url
        self.db_name = db_name
        session = Session(retry_delays=range(10))
        self.server = Server(db_url, session=session)
        self.server.resource.credentials = (username, password)
        self.db = self.server[db_name]

    def emit(self, record):
        # Enhanced log entry structure
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'name': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
            'path': record.pathname,
            'function': record.funcName,
            'merchant': getattr(record, 'merchant', None),
            'username': getattr(record, 'username', None),
            'line': record.lineno,
        }

        if record.exc_info:
            log_entry['exception'] = traceback.format_exc()

        try:
            self.db.save(log_entry)
        except Exception as e:  # pylint: disable=broad-except
            print(f"Failed to set up CouchDB handler: {e}")

# Setting up global logger


def setup_logger():
    '''logging file handler'''
    logdbsettings = SettingsLog()

    logbot = logging.getLogger('global_logger')
    logbot.setLevel(logging.INFO)

    # File handler
    file_handler = LocalFileHandler(logdbsettings.file_path)
    file_handler.setFormatter(CustomFormatterFile(
        '%(asctime)s - %(name)s - %(levelname)s - %(merchant)s - %(username)s - %(message)s'))

    # CouchDB handler
    couchdb_handler = CouchDBHandler(
        logdbsettings.couchdb_host, logdbsettings.couchdb_database,
        logdbsettings.couchdb_name, logdbsettings.couchdb_password
    )
    couchdb_handler.setFormatter(CustomFormatterDb(
        '%(asctime)s - %(name)s - %(levelname)s - %(merchant)s - %(username)s - %(message)s'))

    # Adding handlers to logger
    logbot.addHandler(file_handler)
    logbot.addHandler(couchdb_handler)

    return logbot
