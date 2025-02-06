from fastapi import HTTPException, status
from typing import IO
import filetype

def validate_file_size_type(file: IO):
    FILE_SIZE = 2097152  # 2MB
    accepted_file_types = ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"]
    
    # Reset file pointer and detect file type
    file.file.seek(0)
    file_info = filetype.guess(file.file)
    file.file.seek(0)  # Reset again after reading
    
    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to determine file type",
        )
    
    detected_extension = file_info.extension.lower()
    if detected_extension not in accepted_file_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )
    
    real_file_size = 0
    # Iterate over file chunks
    for chunk in iter(lambda: file.file.read(4096), b""):
        real_file_size += len(chunk)
        if real_file_size > FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large"
            )
    file.file.seek(0)  # Reset pointer for subsequent reads
