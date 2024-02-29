'''Helper for file operations'''
from ast import Dict
import hashlib
from typing import List
import aiofiles
from fastapi import UploadFile
from dependencies.get_db import get_dblogtrx
from models.modelhelper import LogTrxModel
from routers.routes import counter_next_leading_0


async def write_file_in_chunks(file_path, contents, chunk_size=1024*1024):
    '''save a file in chunks'''
    status = False
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            for i in range(0, len(contents), chunk_size):
                await f.write(contents[i:i + chunk_size])
            status = True
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")
        status = False

    return status


async def save_uploaded_file(file: UploadFile, directory: str, prefix: str) \
        -> str:
    """Save the uploaded file to the specified directory."""
    status = False
    felements = List[str]
    try:
        contents = await file.read()
        hash256 = hashlib.md5(contents).hexdigest()
        filename = f'{prefix}_{hash256}_{file.filename}'
        felements = file.filename.split("_")
        file_path = f'{directory}/{filename}'
        status = await write_file_in_chunks(file_path, contents)
        return filename, status
    # pylint: disable=broad-exception-caught
    except Exception as exc:  # noqa: F841 #pylint: disable=unused-variable
        return None, False
    finally:
        await file.close()
        o_log = LogTrxModel()
        o_log.id = \
            f'{int(o_log.createds*1000)}_{counter_next_leading_0("uploadredis")}'
        o_log.merchant = felements[0]
        o_log.created_merchant = None
        o_log.created_by = None
        o_log.message = get_original_file_name(filename).lower()
        o_log.partdate = int(prefix)
        o_log.doc_id = hash256
        o_log.parent = hash256
        o_log.status = status
        o_log.src = "File"
        o_log.extra = {"message": "-"}
        db_logtrx = get_dblogtrx()
        doc: Dict = o_log.to_dict()
        # pylint: disable = unused-variable
        doc_id, doc_rev = db_logtrx.save(doc)  # noqa: W0612


def get_original_file_name(input_string: str) -> str:
    '''kind of returns the original name of the file'''
    parts = input_string.split("_")

    if len(parts) > 3:
        result = "_".join(parts[3:])
    else:
        result = ""

    return result
