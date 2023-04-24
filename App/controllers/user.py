from App.models import User
from App.database import db

def create_user(firstname, lastname, username, email, phone, password):
    newuser = User(firstname=firstname, lastname=lastname, username=username, email=email, phone=phone, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_username(id, username):
    user = get_user(id)
    user2 = get_user_by_username(username)
    if user and not user2 :
        user.username = username
        db.session.add(user)
        db.session.commit()
        return user
    return None

def update_password(id, password, new_password):
    user = User.check_password(get_user(id), password)

    if user:
        user = User.set_password(get_user(id), new_password)
        db.session.add(user)
        db.session.commit()
        return user
    return None


# Friends
def is_friends_with(self, user):
    return self.friends.filter(Friendship.friend_id == user.id).count() > 0

def add_friend(self, user):
    if not self.is_friends_with(user):
        self.friends.append(user)
        user.friends.append(self)
        db.session.commit()

def remove_friend(self, user):
    if self.is_friends_with(user):
        self.friends.remove(user)
        user.friends.remove(self)
        db.session.commit()

def get_friends(self):
    return self.friends.all()