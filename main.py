import psycopg2
import hashlib 
from haystack.reader.farm import FARMReader
from haystack.retriever.sparse import ElasticsearchRetriever
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.pipeline import ExtractiveQAPipeline
from haystack.retriever.sparse import TfidfRetriever
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_socketio import SocketIO
from haystack.retriever import EmbeddingRetriever

import eventlet
from eventlet import wsgi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Key removed'
socketio = SocketIO(app)

document_store = InMemoryDocumentStore(similarity="cosine")
global reader
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)
global retriever
retriever = EmbeddingRetriever(document_store=document_store,
                               embedding_model="deepset/sentence_bert")
document_store.update_embeddings(retriever)

conn = psycopg2.connect(database="", user = "", password = "", host = "", port = "")
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS chatinfo (ID TEXT PRIMARY KEY, Passage TEXT NOT NULL)")

conn.commit()

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

def predict_ans(query):
    prediction = pipe.run(query=query, top_k_retriever=10, top_k_reader=5)
    return prediction['answers'][0]['answer']

@app.route('/')
def sessions():
    return render_template('index.html')

@app.route('/talk', methods=['GET', 'POST'])
def talk():
    global context
    context = str(request.form['passage'])
    result = hashlib.sha256(context.encode('utf-8')).hexdigest()
    try:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO chatinfo VALUES(%s,%s);", (result, context))
        except psycopg2.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
        cur.close()
    except Exception as e:
        print('ERROR:', e[0])
    dicts = [
    {
        'text': context
    }
    ]
    
    document_store.delete_all_documents()
    document_store.write_documents(dicts)
    document_store.update_embeddings(retriever)
    global pipe
    pipe = ExtractiveQAPipeline(reader, retriever)
    return render_template('chatbot.html',hash="Your hash is: "+str(result))

def messageReceived(methods=['GET', 'POST']):
    print('message received')

@app.route("/passage/<id>")
def func(id):
    cur.execute("SELECT Passage FROM chatinfo WHERE ID=%s",(id,))  
    rows = cur.fetchall()
    if(len(rows)==0):
        abort(404)
    global context
    context = rows[0][0]
    return redirect(url_for('talk2'))

@app.route('/talk2', methods=['GET', 'POST'])
def talk2():
    dicts = [
    {
        'text': context
    }
    ]
    
    document_store.delete_all_documents()
    document_store.write_documents(dicts)
    document_store.update_embeddings(retriever)
    global pipe
    pipe = ExtractiveQAPipeline(reader, retriever)
    return render_template('chatbot.html')

@app.route('/how')
def how():
    return render_template('how.html')
    
@app.route('/timel')
def timel():
    return render_template('timel.html')
    
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    if 'message' in json:
        query = str(json['message'])
        result=predict_ans(query)
        answer = {'message':''}
        answer['message'] = str(result)
        socketio.emit('my response', answer, callback=messageReceived)
    else:
        print('received my event: ' + str(json))

if __name__ == '__main__':
        wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)