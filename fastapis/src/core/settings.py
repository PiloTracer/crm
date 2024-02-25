'''Settings management classes'''
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


class Settings():
    '''Settings for transactions database'''
    app_name: str = "W-Financial"
    couchdb_name: str = os.getenv("COUCHDB_couchdb_name")
    couchdb_password: str = os.getenv("COUCHDB_couchdb_password")
    couchdb_host: str = os.getenv("COUCHDB_couchdb_host")
    couchdb_database: str = os.getenv("COUCHDB_couchdb_database")


class SettingsJWT():
    '''Settings for users database'''
    jwt_secret: str = os.getenv("AUTH_secret")
    jwt_algorithm: str = os.getenv("AUTH_algorithm")
    jwt_expires: int = int(
        os.getenv("AUTH_ACCESS_TOKEN_EXPIRE_MINUTES", "720"))


class Settings2():
    '''Settings for users database'''
    app_name: str = "W-Financial"
    couchdb_name: str = os.getenv("COUCHDB2_couchdb_name")
    couchdb_password: str = os.getenv("COUCHDB2_couchdb_password")
    couchdb_host: str = os.getenv("COUCHDB2_couchdb_host")
    couchdb_database: str = os.getenv("COUCHDB2_couchdb_database")


class SettingsLog():
    '''Settings for log database'''
    app_name: str = "W-Financial"
    couchdb_name: str = os.getenv("COUCHDBLOG_couchdb_name")
    couchdb_password: str = os.getenv("COUCHDBLOG_couchdb_password")
    couchdb_host: str = os.getenv("COUCHDBLOG_couchdb_host")
    couchdb_database: str = os.getenv("COUCHDBLOG_couchdb_database")
    file_path: str = f"{os.getenv("COUCHDBLOG_file_path")}log_{
        datetime.now().strftime('%Y%m%d')}.log"


class SettingsLogTrx():
    '''Settings for log database'''
    app_name: str = "W-Financial"
    couchdb_name: str = os.getenv("COUCHDBLOGTRX_couchdb_name")
    couchdb_password: str = os.getenv("COUCHDBLOGTRX_couchdb_password")
    couchdb_host: str = os.getenv("COUCHDBLOGTRX_couchdb_host")
    couchdb_database: str = os.getenv("COUCHDBLOGTRX_couchdb_database")
    file_path: str = f"{os.getenv("COUCHDBLOGTRX_file_path")}logtrx_{
        datetime.now().strftime('%Y%m%d')}.log"


class SettingsMerchant():
    '''Settings for log database'''
    app_name: str = "W-Financial"
    couchdb_name: str = os.getenv("COUCHDBMERCH_couchdb_name")
    couchdb_password: str = os.getenv("COUCHDBMERCH_couchdb_password")
    couchdb_host: str = os.getenv("COUCHDBMERCH_couchdb_host")
    couchdb_database: str = os.getenv("COUCHDBMERCH_couchdb_database")


class SettingsBalance():
    '''Settings for log database'''
    app_name: str = "W-Financial"
    couchdb_name: str = os.getenv("COUCHDBBAL_couchdb_name")
    couchdb_password: str = os.getenv("COUCHDBBAL_couchdb_password")
    couchdb_host: str = os.getenv("COUCHDBBAL_couchdb_host")
    couchdb_database: str = os.getenv("COUCHDBBAL_couchdb_database")
