#resources/errors.py
#Reference: https://www.psycopg.org/docs/errors.html
class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class AlreadyExistsError(Exception):
    pass

class UpdatingError(Exception):
    pass

class DeletingError(Exception):
    pass

class NotExistsError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "AlreadyExistsError": {
         "message": "Object already exists",
         "status": 400
     },
     "UpdatingError": {
         "message": "Updating added by other is forbidden",
         "status": 403
     },
     "DeletingError": {
         "message": "Deleting added by other is forbidden",
         "status": 403
     },
     "NotExistsError": {
         "message": "Object with given id doesn't exists",
         "status": 400
     }
}