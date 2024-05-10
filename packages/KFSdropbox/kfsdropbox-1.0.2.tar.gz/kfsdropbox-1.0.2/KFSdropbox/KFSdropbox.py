# Copyright (c) 2024 구FS, all rights reserved. Subject to the MIT licence in `licence.md`.
import dropbox.dropbox_client, dropbox.exceptions, dropbox.files
import os
import requests
import time


def list_files(dbx: dropbox.dropbox_client.Dropbox, path: str, not_exist_ok=True) -> list[str]:
    """
    Takes dropbox instance and returns list of all filenames in specfied directory. Depending on not_exist_ok, a non-existing directory will return an empty list or raise dropbox.exceptions.ApiError.
    
    Arguments:
    - dbx: dropbox instance to refer to
    - path: path to desired directory
    - not_exist_ok: if directory at path does not exist: return empty list or raise dropbox.exceptions.ApiError

    Returns:
    - file_names: list of file_names in directory of path

    Raises:
    - dropbox.exceptions.ApiError: if directory at path does not exist and not_exist_ok is false
    """
    
    file_names: list[str]=[]    # file names to return


    while True:
        try:
            result=dbx.files_list_folder(path)  # read first batch of file names
        except dropbox.exceptions.ApiError:     # folder does not exist
            if not_exist_ok==True:              # if folder not existing is ok:
                return []                       # return empty list
            else:                               # otherwise forward dropbox exception
                raise
        except (dropbox.exceptions.InternalServerError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):  # connection unexpectedly failed or timed out: try again
            time.sleep(1)
            continue
        else:
            break

    file_names+=[entry.name for entry in result.entries if isinstance(entry, dropbox.files.FileMetadata)==True]     # append file names, exclude all non-files #type:ignore

    while result.has_more==True:                                                                                    # as long as more file names still unread: continue #type:ignore
        result=dbx.files_list_folder_continue(result.cursor) #type:ignore
        file_names+=[entry.name for entry in result.entries if isinstance(entry, dropbox.files.FileMetadata)==True] # append file names, exclude all non-files #type:ignore

    file_names.sort()   # sort file names before returning

    return file_names


def upload_file(dbx: dropbox.dropbox_client.Dropbox, source_filepath: str, destination_filepath: str) -> None:  # upload specified to dropbox, create folders as necessary, if file exists already replace
    """
    Takes dropbox instance and uploads source file to destination filepath in dropbox.

    Arguments:
    - dbx: dropbox instance to refer to
    - source_filepath: filepath to file to upload
    - destination_filepath: filepath to file in 
    """
    
    CHUNK_SIZE: float=pow(2, 22)   # upload in 4MiB chunks
    
    
    file_size=os.path.getsize(source_filepath)  # source file size [B]


    with open(source_filepath, "rb") as file:
        if file_size<=CHUNK_SIZE:   # if smaller than chunk size: upload everything at once
            dbx.files_upload(file.read(), destination_filepath, dropbox.files.WriteMode.overwrite)
            return                  # job done
        
        while True:                                                                                 # if file bigger than chunk size: start to upload in several chunks
            try:
                upload_session_start_result=dbx.files_upload_session_start(file.read(CHUNK_SIZE))   # start upload session
            except requests.exceptions.SSLError:                                                    # if SSLError because max retries exceeded or something: retry lol
                time.sleep(1)
                continue                                                                            # TODO deadlock potential
            else:
                break
        cursor=dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id, offset=file.tell()) # type:ignore
        commit=dropbox.files.CommitInfo(path=destination_filepath)
        
        while file.tell()<file_size:             # keep uploading as long as not reached file end
            if CHUNK_SIZE<file_size-file.tell(): # if regular upload call:
                dbx.files_upload_session_append(file.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                cursor.offset=file.tell()
            else:                                # if last upload call
                dbx.files_upload_session_finish(file.read(CHUNK_SIZE), cursor, commit)

    return
# source: https://stackoverflow.com/questions/37397966/dropbox-api-v2-upload-large-files-using-python