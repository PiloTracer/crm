#from bloom_filter import BloomFilter
from couchdb import Server

#bloomfilter_db_path = '/crmdir/bloom/data/bloom_filter.db'
#b = BloomFilter(max_elements=10000000000, error_rate=0.01, filename=bloomfilter_db_path)

def is_duplicate_transaction(trx_id: str, db: Server):
    return False
    #if trx_id in b:
    #    #return True
    #    if trx_id in db:
    #        return True
    #    else:
    #        return False
    #else:
    #    b.add(trx_id)
    #    return False
