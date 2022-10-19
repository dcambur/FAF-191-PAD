class UserIdentity:
    def __init__(self, jwt_identity):
        self.id = jwt_identity["id"]
        self.user = jwt_identity["username"]
        self.full_identity = jwt_identity
