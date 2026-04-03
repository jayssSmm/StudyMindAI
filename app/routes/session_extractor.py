from flask import Blueprint, jsonify
from app.extensions import db
from app.models.sessions import Session
from sqlalchemy import select

bp=Blueprint('session_extract',__name__)

@bp.route('/session')
def session():
    session_extractor_query=select(Session)
    sessions = db.session.scalars(session_extractor_query).all()

    session_list=[]
    for session in sessions:
        session_list.append({
            'user_id':session.user_id,
            'title':session.title
        })

    return jsonify(session_list)