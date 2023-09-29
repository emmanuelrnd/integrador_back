from flask import jsonify

class CustomException(Exception):

    def __init__(self, status_code, name = "Custom Error", description = 'Error'): 
        super().__init__()
        self.description = description
        self.name = name
        self.status_code = status_code

    def get_response(self):
        response = jsonify({
            'error': {
                'code': self.status_code,
                'name': self.name,
                'description': self.description,
            }
        })
        response.status_code = self.status_code
        return response
    

class UserNotFound(CustomException):
    def __init__(self, description="Error 2"):
        super().__init__(status_code=404, name="User Not Found", description=description)

class InvalidDataError(CustomException):
    def __init__(self, description="Error 3"):
        super().__init__(status_code=400, name="Invalid Data", description=description)