'''global logging'''
from datetime import datetime
from typing import Any, Dict
import json
import logging
import traceback
import time
import redis
from couchdb import Server, Session

from core.settings import SettingsLog
from models.model import MessageSchema
from models.classes import RabbitMessage

# Custom handler for CouchDB


class CustomFormatterDb(logging.Formatter):
    '''logging custom formatter for extra fields'''

    def format(self, record):
        if not hasattr(record, 'username'):
            record.username = 'N/A'
        if not hasattr(record, 'merchant'):
            record.merchant = 'N/A'

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
        '%(asctime)s - %(name)s - %(levelname)s - %(merchant)s - %(username)s - %(message)s'))  # noqa: E501 # pylint: disable = line-too-long

    # CouchDB handler
    couchdb_handler = CouchDBHandler(
        logdbsettings.couchdb_host, logdbsettings.couchdb_database,
        logdbsettings.couchdb_name, logdbsettings.couchdb_password
    )
    couchdb_handler.setFormatter(CustomFormatterDb(
        '%(asctime)s - %(name)s - %(levelname)s - %(merchant)s - %(username)s - %(message)s'))   # noqa: E501 # pylint: disable = line-too-long

    # Adding handlers to logger
    logbot.addHandler(file_handler)
    logbot.addHandler(couchdb_handler)

    return logbot


async def log_and_return_message(
        db_logtrx: Server,
        message: MessageSchema,
        log: Dict[str, Any],
        status: str,
        detail: str):
    '''Receives a message and a current log'''
    # Ensure the length is a positive integer

    message.status = status
    message.message = detail
    log["extra"] = [detail] + log["extra"]
    log["modidifeds"] = time.time()
    db_logtrx.save(log)
    await publishnewfile(log["filename"], True)
    return message


async def publishnewfile(filename, is_result=False):
    '''publishing a message to rabbitmq'''

    ele = filename.split("_")
    vdate = ele[0]  # pylint: disable=unused-variable # noqa: F841
    vchecksum = ele[1]  # pylint: disable=unused-variable # noqa: F841
    merch = ele[2]  # pylint: disable=unused-variable # noqa: F841
    message: RabbitMessage = RabbitMessage()
    message.type = "upload"
    message.channel = "newfile"
    message.header = "uploadresult" if is_result else "newfile"
    message.message = filename
    message.merchant = merch

    jsonstring = json.dumps(message.to_dict())
    publish_message('10.5.0.4', 6379, message.channel, jsonstring)

    # credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
    # connection = pika.BlockingConnection(pika.ConnectionParameters
    #   ('10.5.0.8', 5672, '/', credentials))  # noqa: E501
    # channel = connection.channel()
    # channel.queue_declare(queue='newfile')
    # jsonstring = json.dumps(message.__dict__)
    # channel.basic_publish(
    #    exchange='', routing_key='newfile', body=jsonstring)
    # connection.close()


def publish_message(redis_host, redis_port, channel, message):
    '''Publishing upload to redis'''
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, decode_responses=True)
    redis_client.publish(channel, message)


def publish_message_sock(redis_host, redis_port, channel, message):
    '''Publishing file parse to redis sockets'''
    redis_client = redis.StrictRedis(
        host=redis_host, port=redis_port, decode_responses=True)
    redis_client.publish(channel, message)
