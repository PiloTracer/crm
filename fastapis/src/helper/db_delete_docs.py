'''database clear helper file'''
from asyncio import Server
from dependencies import get_db


def delete_docs_except_design_views(db_name):
    '''executes the deletion of the documents'''
    db = {}

    if (db_name == "*.*"):
        db = get_db.get_dbbalance()
        execute_delete(db)
        db = get_db.get_dblog()
        execute_delete(db)
        db = get_db.get_dblogtrx()
        execute_delete(db)
        db = get_db.get_dbmerchant()
        execute_delete(db)
        db = get_db.get_dbtrx()
        execute_delete(db)
        db = get_db.get_dbusr()
        execute_delete(db)
    elif db_name in ["balance", "adj", "balances"]:
        db = get_db.get_dbbalance()
        execute_delete(db)
    elif db_name in ["log", "logs"]:
        db = get_db.get_dblog()
        execute_delete(db)
    elif db_name in ["logtrx", "logtransactions", "trxlog", "log_trx"]:
        db = get_db.get_dblogtrx()
        execute_delete(db)
    elif db_name in ["merchant", "merchants"]:
        db = get_db.get_dbmerchant()
        execute_delete(db)
    elif db_name in ["trx", "transaction", "transactions"]:
        db = get_db.get_dbtrx()
        execute_delete(db)
    elif db_name in ["user", "users"]:
        db = get_db.get_dbusr()
        execute_delete(db)
    else:
        return False, f"Invalid database name: {db_name}"

    return True, f"Deleted all non-design/view documents from: {db_name}"


def execute_delete(db: Server):
    '''Perform the delete command'''
    docs_to_delete = [
        doc for doc in db.view('_all_docs', include_docs=True)
        if not doc.id.startswith('_design/')
    ]

    for doc in docs_to_delete:
        db.delete(doc.doc)
