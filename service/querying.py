import dropbox.exceptions
import dropbox.files
from config import Config
from datetime import date, datetime


def get_file(path):
    with dropbox.Dropbox(oauth2_access_token=Config.TOKEN) as dbx:
        meta, f = dbx.files_download(path)
        return f.content.decode('utf-8')


def get_files_recursively(path=''):
    files = {
        'current_folder': u''.join(path.split('/')[-1]),
        'files': [],
        'folders': [],
    }
    path = '' if path == '' else '/' + path
    with dropbox.Dropbox(oauth2_access_token=Config.TOKEN) as dbx:

        parent_folder, filename = path.rsplit('/', 1)
        if filename in [x.name for x in dbx.files_list_folder(f'{parent_folder}').entries
                        if isinstance(x, dropbox.files.FileMetadata)]:
            return get_file(path)

        try:
            folder = dbx.files_list_folder(f'{path}').entries
        except dropbox.exceptions.ApiError:
            return {'message': 'failed', 'error': 'File not found'}

        for file in folder:
            file_data = {}
            for attr in getattr(file, '_all_field_names_'):
                value = getattr(file, attr)
                if isinstance(value, (date, datetime)):
                    value = value.isoformat()

                file_data.update({
                    attr: value
                })
            if isinstance(file, dropbox.files.FolderMetadata):
                files['folders'].append(file_data)
            elif isinstance(file, dropbox.files.FileMetadata):
                files['files'].append(file_data)
            else:
                raise TypeError('Unknown file type')

    return files
