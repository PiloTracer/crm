'''database clear helper file'''
from dependencies import get_db


def delete_docs_except_design_views(db_name):
    '''executes the deletion of the documents'''
    db = {}

    if db_name in ["balance", "adj", "balances"]:
        db = get_db.get_dbbalance()
    elif db_name in ["trx", "transaction", "transactions"]:
        db = get_db.get_dbtrx()
    elif db_name in ["log", "logs"]:
        db = get_db.get_dblog()
    elif db_name in ["logtrx", "logtransactions"]:
        db = get_db.get_dblogtrx()
    else:
        return False, f"Invalid database name: {db_name}"

    docs_to_delete = [
        doc for doc in db.view('_all_docs', include_docs=True)
        if not doc.id.startswith('_design/')
    ]

    for doc in docs_to_delete:
        db.delete(doc.doc)

    return True, f"Deleted all non-design/view documents from: {db_name}"
