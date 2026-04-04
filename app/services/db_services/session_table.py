from app.extensions import db
from app.models.sessions import Session


def add_session(user, title):
    
    if title.strip()=='':
        return False
    
    session = (Session(user_id=user, title=title))
    db.session.add(session)
    db.session.commit()
    return session.id
    