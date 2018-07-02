from user import User
class ISOI:
    def __init__(self):
        pass

    @property
    def users(self):
        pass
        
    def valid_user(self,username,password):
        if username == 'admin' and password == 'admin':
            user = User(username)
            return user
        else:
            return None

    def get_user_id(self, user_id):
        # get user information from db
        valid_user=User.query.filter_by(id=id).first()
        if valid_user is not None:
            return valid_user
        return None