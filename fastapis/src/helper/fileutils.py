'''Helper for file operations'''
import hashlib
import aiofiles
from fastapi import UploadFile


async def save_uploaded_file(file: UploadFile, directory: str, prefix: str) \
        -> str:
    """Save the uploaded file to the specified directory."""
    try:
        contents = await file.read()
        hash256 = hashlib.md5(contents).hexdigest()
        filename = f'{prefix}_{hash256}_{file.filename}'
        file_path = f'{directory}/{filename}'
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(contents)
        return filename
    finally:
        await file.close()
