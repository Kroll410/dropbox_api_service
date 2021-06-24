import dropbox.exceptions
from flask import request
from flask_restful import Resource, Api
from wsgi import app
from service import querying, creation


class File(Resource):

    def get(self, content=''):
        try:
            return querying.get_files_recursively(content), 200
        except LookupError:
            return {'message': 'Not found'}, 404

    def post(self, content):
        if not request.files:
            if not isinstance(error := creation.create_folder(content), dropbox.exceptions.ApiError):
                return {'message': 'success'}, 201
            else:
                return {'message': 'failed', 'error': str(error)}, 404
        else:
            if not isinstance(error := creation.create_file(content, request.files), dropbox.exceptions.ApiError):
                return {'message': 'success'}, 201
            else:
                return {'message': 'failed', 'error': str(error)}, 404


api = Api(app)
api.add_resource(File, '/data/', '/data/<path:content>')
