import re
from dbapp import db
from models import User
from flask_jwt_extended import create_access_token

def registering(email,password,role):

    if (not email or not password or not role):
        return ({"success":False, "Error":" you cant leave the required fields as empty "})
    
    existing_user=User.query.filter_by(email=email).first()

    if (existing_user):
        return ({"success":False, "Error":" user already exists "})

    def Email(email):
        pattern=r"^[a-zA-Z0-9.+_%-]+@[a-zA-Z0-9.-]+\.[a-zA-z]{2,}$"
        return (bool(re.match(pattern,email)))
    
    check=Email(email)

    if(not check):
        return ({"success":False, "Error":" please enter a valid email address "})
    
    def PassWord(password):
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!*%&?])[A-Za-z\d@$!%*?&]{8,}$"
        return (bool(re.match(pattern,password)))
    
    check=PassWord(password)

    if(not check):
        return ({"success":False, "Error":" Your password is too weak. It must be at least 8 characters long and include a mix of lowercase (a-z), uppercase (A-Z), numbers (0-9), and special symbols ( . + _ % - # )."})
    
    new_user=User(email=email,role=role)

    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    return ({"success":True, "Message":f" {role} successfully registered "})



def logingin(email,password):

    if (not email or not password):
        return ({"success":False, "Error":" Email and Password required "})
    
    user_exists=User.query.filter_by(email=email).first()

    if( not user_exists):
        return ({"success":False, "Error":"Invalid credentials-Email"})
    
    if (not user_exists.check_password(password)):
        return ({"success":False,"Error":"Invalid credentials-password"})
    

    additional_tokens={"role":user_exists.role}

    access_token=create_access_token(identity=str(user_exists.id),additional_claims=additional_tokens)

    return ({"success":True, "access_token":access_token}) 

