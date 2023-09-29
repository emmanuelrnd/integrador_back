from ..models.user_model import User

from flask import request

from decimal import Decimal

from app.models.exceptions import UserNotFound,InvalidDataError
class UserController:
    """User controller class"""

    @classmethod
    def get(cls, user_id):
        """Get a user by id"""
        user = User(user_id=user_id)
        result = User.get(user)
        if result is not None:
            return result.serialize(), 200
        else:
            raise UserNotFound(f"User with id {user_id} not found")
        
    @classmethod
    def get_all(cls):
        """Get all films"""
        film_objects = User.get_all()
        films = []
        for user in film_objects:
            films.append(user.serialize())
        return films, 200
    
    @classmethod
    def create(cls):
        """Create a new user"""
        data = request.json
        descripcion = """Se deben cumplir los siguientes requisitos:
    
                    • El atributo title debe tener tres caracteres como mínimo.
                    • Los atributos language_id y rental_duration deben ser números enteros.
                    • Como hemos mencionado, los atributos rental_rate y replacement_cost son
                    de tipo Decimal en la base de datos y los convertimos a un número entero
                    multiplicando por 100 al momento de serializar la película. No obstante, no existe
                    una validación para estos campos al momento de registrar una nueva película. Por
                    lo tanto, se solicita validar que estos campos sean números enteros.
                    • En cuanto al atributo last_update y el id de la película, estos son generados
                    automáticamente por la base de datos y en la misma consulta de inserción. Por lo
                    tanto, no deben ser ingresados por el usuario, pues serán ignorados.
                    • Por último, para el atributo special_features se solicita validar que el valor ingresado
                    sea una lista de strings, y que cada string sea uno de los siguientes: Trailers,
                    Commentaries, Deleted Scenes, Behind the Scenes."""
        # TODO: Validate data
        if data.get('rental_rate') is not None:
            if isinstance(data.get('rental_rate'), int):
                data['rental_rate'] = Decimal(data.get('rental_rate'))/100
        
        if data.get('replacement_cost') is not None:
            if isinstance(data.get('replacement_cost'), int):
                data['replacement_cost'] = Decimal(data.get('replacement_cost'))/100

        if data.get('title') is not None:
            if len(data.get('title')) < 3:
                raise InvalidDataError(descripcion)
            
        if data.get('language_id') is not None:
            if not isinstance(data.get('language_id'),int):
                raise InvalidDataError(descripcion)
            
        if data.get('rental_duration') is not None:
            if not isinstance(data.get('rental_duration'),int):
                raise InvalidDataError(descripcion)

        if data.get('special_features') is not None:
            if not isinstance(data.get('special_features'),list):
                raise InvalidDataError(descripcion)
            else:
                 elementos = ["Trailers","Commentaries", "Deleted Scenes", "Behind the Scenes"]
                 for i in data.get('special_features'):
                    if i in elementos:
                        break
                    else:
                        raise InvalidDataError(descripcion)

        user = User(**data)
        User.create(user)
        return {'message': 'User created successfully'}, 201

    @classmethod
    def update(cls, user_id):
        """Update a user"""
        descripcion = """Se deben cumplir los siguientes requisitos:
    
                    • El atributo title debe tener tres caracteres como mínimo.
                    • Los atributos language_id y rental_duration deben ser números enteros.
                    • Como hemos mencionado, los atributos rental_rate y replacement_cost son
                    de tipo Decimal en la base de datos y los convertimos a un número entero
                    multiplicando por 100 al momento de serializar la película. No obstante, no existe
                    una validación para estos campos al momento de registrar una nueva película. Por
                    lo tanto, se solicita validar que estos campos sean números enteros.
                    • En cuanto al atributo last_update y el id de la película, estos son generados
                    automáticamente por la base de datos y en la misma consulta de inserción. Por lo
                    tanto, no deben ser ingresados por el usuario, pues serán ignorados.
                    • Por último, para el atributo special_features se solicita validar que el valor ingresado
                    sea una lista de strings, y que cada string sea uno de los siguientes: Trailers,
                    Commentaries, Deleted Scenes, Behind the Scenes."""
        data = request.json
        # TODO: Validate data
        if data.get('rental_rate') is not None:
            if isinstance(data.get('rental_rate'), int):
                data['rental_rate'] = Decimal(data.get('rental_rate'))/100
        
        if data.get('replacement_cost') is not None:
            if isinstance(data.get('replacement_cost'), int):
                data['replacement_cost'] = Decimal(data.get('replacement_cost'))/100
        if data.get('title') is not None:
            if len(data.get('title')) < 3:
                raise InvalidDataError(descripcion)
            
        if data.get('language_id') is not None:
            if not isinstance(data.get('language_id'),int):
                raise InvalidDataError(descripcion)
            
        if data.get('rental_duration') is not None:
            if not isinstance(data.get('rental_duration'),int):
                raise InvalidDataError(descripcion)
        
        if data.get('special_features') is not None:
            if not isinstance(data.get('special_features'),list):
                raise InvalidDataError(descripcion)
            else:
                 elementos = ["Trailers","Commentaries", "Deleted Scenes", "Behind the Scenes"]
                 for i in data.get('special_features'):
                    if i in elementos:
                        break
                    else:
                        raise InvalidDataError(descripcion)
        

                    
        data['user_id'] = user_id

        user = User(**data)

        # TODO: Validate user exists
        User.update(user)
        return {'message': 'User updated successfully'}, 200
    
    @classmethod
    def delete(cls, user_id):
        """Delete a user"""
        user = User(user_id=user_id)

        # TODO: Validate user exists
        User.delete(user)
        return {'message': 'User deleted successfully'}, 204