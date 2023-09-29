from ..database import DatabaseConnection
from app.models.exceptions import UserNotFound
class User:
    """user model class"""

    def __init__(self, user_id = None, email = None, password = None, 
                 nacimiento = None, usuario = None, 
                 contraseña = None, foto = None,
                 rental_rate = None, length = None, replacement_cost = None,
                 rating = None, special_features = None, last_update = None):
        """Constructor method"""
        self.user_id = user_id
        self.email = email
        self.password = password
        self.nacimiento = nacimiento
        self.usuario = usuario
        self.contraseña = contraseña
        self.foto = foto
        
    def serialize(self):
        """Serialize object representation
        Returns:
            dict: Object representation
        Note:
            - The last_update attribute is converted to string
            - The special_features attribute is converted to list if it is not
            null in the database. Otherwise, it is converted to None
            - The attributes rental_rate and replacement_cost are converted to 
            int, because the Decimal type may lose precision if we convert 
            it to float
        """
        if self.special_features is not None:
            special_features = list(self.special_features)
        else:
            special_features = None
        return {
            "user_id": self.user_id,
            "email": self.email,
            "password": self.password,
            "nacimiento": self.nacimiento,
            "usuario": self.usuario,
            "contraseña": self.contraseña,
            "foto": self.foto,
            
        }
    
    @classmethod
    def get(cls, user):
        """Get a user by id
        Args:
            - user (user): user object with the id attribute
        Returns:
            - user: user object
        """

        query = """SELECT user_id, email, password, nacimiento,
        usuario, contraseña, foto 
        FROM integrador.user WHERE user_id = %s"""
        params = user.user_id,
        result = DatabaseConnection.fetch_one(query, params=params)

        if result is not None:
            return cls(*result)
        return None
    
    @classmethod
    def get_all(cls):
        """Get all users
        Returns:
            - list: List of user objects
        """
        query = """SELECT user_id, email, password, nacimiento,
        usuario, contraseña, foto
        FROM integrador.user"""
        results = DatabaseConnection.fetch_all(query)

        users = []
        if results is not None:
            for result in results:
                users.append(cls(*result))
        return users
    
    @classmethod
    def create(cls, user):
        """Create a new user
        Args:
            - user (user): user object
        """
        query = """INSERT INTO integrador.user (email, password, nacimiento,
        usuario, contraseña, foto) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
        
        if user.special_features is not None:
            special_features = ','.join(user.special_features)
        else:
            special_features = None
        params = user.email, user.password, user.nacimiento, \
                 user.usuario, user.contraseña, \
                 user.foto, user.rental_rate, user.length, \
                 user.replacement_cost, user.rating, special_features
        DatabaseConnection.execute_query(query, params=params)

    @classmethod
    def exists(cls,user_id):
        query = "SELECT * FROM integrador.user WHERE user_id = %s"
        params = (user_id,)
        resultado = DatabaseConnection.fetch_one(query,params=params)
        return resultado
    
    @classmethod
    def update(cls, user):
        """Update a user
        Args:
            - user (user): user object
        """

        if not cls.exists(user.user_id):
            raise UserNotFound(f"user with id {user.user_id} not found")
        
        allowed_columns = {'email', 'password', 'nacimiento',
                           'usuario', 'contraseña',
                           'foto'}
        query_parts = []
        params = []
        for key, value in user.__dict__.items():
            if key in allowed_columns and value is not None:
                if key == 'special_features':
                    if len(value) == 0:
                        value = None
                    else:
                        value = ','.join(value)
                query_parts.append(f"{key} = %s")
                params.append(value)
        params.append(user.user_id)

        query = "UPDATE integrador.user SET " + ", ".join(query_parts) + " WHERE user_id = %s"
        DatabaseConnection.execute_query(query, params=params)
    
    @classmethod
    def delete(cls, user):
        """Delete a user
        Args:
            - user (User): user object with the id attribute
        """
        if not cls.exists(user.user_id):
            raise UserNotFound(f"user with id {user.user_id} not found")
        query = "DELETE FROM integrador.user WHERE user_id = %s"
        params = user.user_id,
        DatabaseConnection.execute_query(query, params=params)