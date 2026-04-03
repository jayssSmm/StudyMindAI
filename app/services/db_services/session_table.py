from app.extensions import db
from app.models.sessions import Session


def add_session(user, title):
    
    if title.strip()=='':
        return False
    
    db.session.add(Session(user_id=user, title=title))
    db.session.commit()
    return True
    