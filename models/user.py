from config.db import connectToMySQL

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM Usuario WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL('cd_exam2').query_db(query, data)
        return cls(result[0]) if result else None
    
    @classmethod
    def insert_one(cls, first_name, last_name, email, password):
        query = """
        INSERT INTO Usuario (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        result = connectToMySQL('cd_exam2').query_db(query, data)

        return cls({
            "id": result, 
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        })

    
    @classmethod
    def get_non_friends(cls, user_id):
        query = """
        SELECT * FROM Usuario
        WHERE id != %(user_id)s
        AND id NOT IN (
            SELECT amigo_2 FROM Amigos WHERE amigo_1 = %(user_id)s
            UNION
            SELECT amigo_1 FROM Amigos WHERE amigo_2 = %(user_id)s
        );
        """
        data = {'user_id': user_id}
        results = connectToMySQL('cd_exam2').query_db(query, data)

        return [cls(row) for row in results]
    
    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM Usuario WHERE id = %(user_id)s;"
        data = {'user_id': user_id}
        result = connectToMySQL('cd_exam2').query_db(query, data)
        return cls(result[0]) if result else None

