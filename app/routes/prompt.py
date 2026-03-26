from flask import Blueprint,request

bp=Blueprint('prompt',__name__)

@bp.route('/prompt', methods=['POST'])
def prompt():

    data = request.get_json(silent=True)

    if not data:
        print("NO JSON RECEIVED")
        return {'message': 'No JSON received'}, 400

    prompt=data.get('prompt')
    model=data.get('model')

    cache_groq=redis_text.get_cached_response(prompt)