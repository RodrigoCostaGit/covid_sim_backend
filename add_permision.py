from app import app, db, Users
from werkzeug.security import generate_password_hash
import uuid



#adds a user to the database.db
def signup_user(password,name): 
   hashed_password = generate_password_hash(password, method='sha256')
   new_user = Users(public_id=str(uuid.uuid4()), name=name, password=hashed_password, admin=False)
   db.session.add(new_user) 
   db.session.commit()   
   print("user added")



signup_user("298sdgf3tsdgf","dotinho")
