from config.db import connectToMySQL
from .user import User

class Amigos:
    def __init__(self, data):
        self.amigo_1 = data['amigo_1']
        self.amigo_2 = data['amigo_2']

    @classmethod
    def get_friends(cls, user_id):
        query = """
        SELECT * FROM Amigos 
        WHERE amigo_1 = %(user_id)s OR amigo_2 = %(user_id)s;
        """
        data = {'user_id': user_id}
        results = connectToMySQL('cd_exam2').query_db(query, data)
        
        friends = []
        for row in results:
            if row['amigo_1'] == user_id:
                friend_id = row['amigo_2']
            else:
                friend_id = row['amigo_1']
            
            friend = User.get_by_id(friend_id)
            if friend:
                friends.append(friend)
        
        return friends

    @classmethod
    def add_friend(cls, user_id, friend_id):
        existing_friends = cls.get_friends(user_id)
        if friend_id in existing_friends:
            return 
        query = """
        INSERT INTO Amigos (amigo_1, amigo_2) 
        VALUES (%(user_id)s, %(friend_id)s);
        """
        data = {
            'user_id': user_id,
            'friend_id': friend_id
        }
        connectToMySQL('cd_exam2').query_db(query, data)
    
    @classmethod
    def remove_friend(cls, user_id, friend_id):
        query = """
        DELETE FROM Amigos 
        WHERE (amigo_1 = %(user_id)s AND amigo_2 = %(friend_id)s) 
        OR (amigo_1 = %(friend_id)s AND amigo_2 = %(user_id)s);
        """
        data = {
            'user_id': user_id,
            'friend_id': friend_id
        }
        connectToMySQL('cd_exam2').query_db(query, data)
    
    @classmethod
    def are_friends(cls, user_id, friend_id):
        query = """
        SELECT COUNT(*) FROM Amigos
        WHERE (amigo_1 = %(user_id)s AND amigo_2 = %(friend_id)s)
        OR (amigo_1 = %(friend_id)s AND amigo_2 = %(user_id)s);
        """
        data = {'user_id': user_id, 'friend_id': friend_id}
        result = connectToMySQL('cd_exam2').query_db(query, data)
        return result[0]['COUNT(*)'] > 0 

