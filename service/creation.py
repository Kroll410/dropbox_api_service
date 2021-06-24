import dropbox.exceptions
import dropbox.files
from config import Config


def create_file(folder_path, files):
    path = '' if folder_path == '' else '/' + folder_path
    with dropbox.Dropbox(oauth2_access_token=Config.TOKEN) as dbx:
        for file in files.values():
            try:
                dbx.files_upload(f=file.stream.read(), path=path, mute=True, mode=dropbox.files.WriteMode('add'))
            except dropbox.exceptions.ApiError as error:
                return error
    return True


def create_folder(folder_path):
    folder_path = '/' + folder_path
    try:
        with dropbox.Dropbox(oauth2_access_token=Config.TOKEN) as dbx:
            dbx.files_create_folder(folder_path, autorename=False)
    except dropbox.exceptions.ApiError as error:
        return error
    return True
