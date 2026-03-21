from flask import Flask,render_template,request,redirect
import redis

from api import groq_provider
from cache import redis_text, redis_pdf
from pdf_handler import text_based_extraction as tpdf
from yt_handler import transcript_extractor

app=Flask(__name__)
app.secret_key = "new2_random_string_here"

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

n_groq=1
HISTORY_TTL = 60 * 60 * 24  # 24 hours

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/prompt', methods=['POST'])
def prompt():

    global n_groq

    data = request.get_json(silent=True)

    if not data:
        print("NO JSON RECEIVED")
        return {'message': 'No JSON received'}, 400

    prompt=data.get('prompt')
    model=data.get('model')

    #checks whether the prompt is cached or not
    cache_groq=redis_text.get_cached_response(prompt)

    try:
        if model == 'Groq':

            chat_history=list(map(lambda x:r.hgetall(x), r.lrange("chat_history_groq",0,-1)))

            if "youtube.com/watch" in prompt or "youtu.be/" in prompt:

                if cache_groq:
                    response=cache_groq
                else:
                    transcript = transcript_extractor.get_transcript(prompt)
                    response = groq_provider.response(transcript,chat_history)

                    redis_text.set_cached_response(prompt,response)

            else:
                if cache_groq:
                    response=cache_groq
                else:

                    #response from llm
                    response=groq_provider.response(prompt,chat_history)
                        
                    #the code below handles history, that will be send to llm as assistant
                    r.hset(f'message:{n_groq}',mapping={'role':'assistant','content':prompt})
                    r.expire(f'message:{n_groq}',HISTORY_TTL)
                    
                    r.lpush('chat_history_groq',f'message:{n_groq}')
                    r.expire('chat_history_groq',HISTORY_TTL)
                    
                    n_groq+=1

                    if r.ttl('chat_history_groq') == -1:
                        r.expire('chat_history_groq', HISTORY_TTL)

                    #the code below sets cache
                    redis_text.set_cached_response(prompt,response)

            return {'message':response}

        return {'message': 'Invalid model selected'}
    
    except Exception as e:
        print(f"Error: {e}")
        return {'message': "Sorry, the AI is having trouble right now."}

    
@app.route('/clear')
def clear():
    global n_groq
    n_groq=1
    r.flushall()
    return redirect('/')

@app.route('/upload',methods=['POST'])
def upload_files():
    if not request.files.get('file'):
        return {'message': 'Error: No file part'}, 400
    
    file = request.files.get('file')

    if file.filename=='':
        return {'message': 'Error: No selected file'}, 400
        
    if file.content_type=='application/pdf':

        cache_pdf=redis_pdf.get_cache_file(file)
        if cache_pdf:
            return {'message':cache_pdf}
        else:
            r = tpdf.text_extraction(file)
            pdf_response=groq_provider.response(r,[])
                
            redis_pdf.set_cache_file(file,pdf_response)
            return {'message':pdf_response}
        
    return {'message':'Error: Upload pdf Only'} , 400