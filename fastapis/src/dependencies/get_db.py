'''database manager'''
from couchdb import Server
from core.settings import Settings, Settings2, \
    SettingsLog, SettingsMerchant, SettingsBalance


def get_dbtrx():
    '''get db for transactions and files'''
    settings = Settings()
    # print(settings.couchdb_name)
    couch = Server(url=settings.couchdb_host)
    couch.resource.credentials = (
        settings.couchdb_name, settings.couchdb_password)

    try:
        db = couch[settings.couchdb_database]
    except Exception:  # pylint: disable=broad-except
        db = couch.create(settings.couchdb_database)

    return db


def get_dbusr():
    '''get db for users'''
    settings = Settings2()
    couch = Server(url=settings.couchdb_host)
    couch.resource.credentials = (
        settings.couchdb_name, settings.couchdb_password)
    try:
        db = couch[settings.couchdb_database]
    except Exception:  # pylint: disable=broad-except
        db = couch.create(settings.couchdb_database)

    return db


def get_dblog():
    '''get db for users'''
    settings = SettingsLog()
    couch = Server(url=settings.couchdb_host)
    couch.resource.credentials = (
        settings.couchdb_name, settings.couchdb_password)
    try:
        db = couch[settings.couchdb_database]
    except Exception:  # pylint: disable=broad-except
        db = couch.create(settings.couchdb_database)

    return db


def get_dblogtrx():
    '''get db for users'''
    settings = SettingsLog()
    couch = Server(url=settings.couchdb_host)
    couch.resource.credentials = (
        settings.couchdb_name, settings.couchdb_password)
    try:
        db = couch[settings.couchdb_database]
    except Exception:  # pylint: disable=broad-except
        db = couch.create(settings.couchdb_database)

    return db


def get_dbmerchant():
    '''get db for users'''
    settings = SettingsMerchant()
    couch = Server(url=settings.couchdb_host)
    couch.resource.credentials = (
        settings.couchdb_name, settings.couchdb_password)
    try:
        db = couch[settings.couchdb_database]
    except Exception:  # pylint: disable=broad-except
        db = couch.create(settings.couchdb_database)

    return db


def get_dbbalance():
    '''get db for balance transactions'''
    settings = SettingsBalance()
    couch = Server(url=settings.couchdb_host)
    couch.resource.credentials = (
        settings.couchdb_name, settings.couchdb_password)
    try:
        db = couch[settings.couchdb_database]
    except Exception:  # pylint: disable=broad-except
        db = couch.create(settings.couchdb_database)

    return db
