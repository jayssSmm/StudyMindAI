from flask import Flask,render_template,request,redirect
from api import groq_provider
from cache import redis_cache
import os
import redis
from pdf_handler import text_based_extraction as tpdf

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
    global n_groq

    if request.method=='POST':

        prompt=request.form.get('prompt')
        model=request.form.get('model')

        cache_groq=redis_cache.get_cached_response(prompt)
        try:
            if model=='Groq':
                if cache_groq:
                    response=cache_groq
                else:
                    chat_history=list(map(lambda x:r.hgetall(x), r.lrange("chat_history_groq",0,-1)))
                    print(chat_history)
                    response=groq_provider.response(prompt,chat_history)
                    
                    #the code below handles history, that will be send to llm as assistant
                    r.hset(f'message:{n_groq}',mapping={'role':'assistant','content':response})
                    r.expire(f'message:{n_groq}',HISTORY_TTL)
                    r.lpush('chat_history_groq',f'message:{n_groq}')
                    r.expire('chat_history_groq',HISTORY_TTL)
                    n_groq+=1

                    #the code below sets cache
                    raw = redis_cache.set_cached_response(prompt,response)
                    if raw:
                        print("Error: data not cached / statefull prompt")

            return render_template('index.html',data=response)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', data="Sorry, the AI is having trouble right now.")

    return render_template('index.html')

@app.route('/clear')
def clear():
    global n_groq
    n_groq=1
    r.flushall()
    return redirect('/')

@app.route('/upload',methods=['POST'])
def upload_files():
    if not request.files.getlist('file'):
        return {'message': 'Error: No file part'}, 400
    file = request.files.getlist('file')
    
    for f in file:
        if f.filename=='':
            return {'message': 'Error: No selected file'}, 400
        
        if f.content_type=='application/pdf':
            r = tpdf.text_extraction(f)
            return {'message':r}
        
        f.save(os.path.join('uploads', f.filename))
    return {'message': 'Files uploaded successfully'}