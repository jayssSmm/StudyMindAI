from flask import Blueprint,request
from app.services.cache_services import redis_text
from app.history import redis_history
from app.services.yt_services import transcript_extractor
from app.services.llm_services import groq_provider
from app.services.db_services import session_table
from flask_jwt_extended import jwt_required,get_jwt_identity

bp=Blueprint('prompt',__name__)

@bp.route('/prompt', methods=['POST'])
@jwt_required()
def prompt():

    data = request.get_json(silent=True)

    if not data:
        print("NO JSON RECEIVED")
        return {'message': 'No JSON received'}, 400

    prompt=data.get('prompt')
    model=data.get('model')

    cache_groq=redis_text.get_cached_response(prompt)
    user_id=get_jwt_identity()
    session_title=''

    try:
        if model == 'Groq':

            if not session_title:
                session_title=session_table.add_session(user_id,(groq_provider.session_title(prompt)))
                if not session_title:
                    response='Error: Invalid title'

            chat_history=redis_history.get_last_ten_messages()

            if "youtube.com/watch" in prompt or "youtu.be/" in prompt:
                if cache_groq:
                    response=cache_groq
                else:
                    transcript = transcript_extractor.get_transcript(prompt)
                    response = groq_provider.response(transcript,chat_history)

                    redis_text.set_cached_response(prompt,response)
                    redis_history.set_history(response)
            
            else:
                if cache_groq:
                    response=cache_groq
                else:

                    #response from llm
                    response=groq_provider.response(prompt,chat_history)
                            
                    #the code below handles history, that will be send to llm as assistant
                    redis_history.set_history(response)

                    #the code below sets cache
                    redis_text.set_cached_response(prompt,response)
                    
            return {'message':response}

        return {'message': 'Invalid model selected'}
    
    except Exception as e:
        print(f"Error: {e}")
        return {'message': "Sorry, the AI is having trouble right now."}