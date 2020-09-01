from flask import Flask, jsonify
from celery import Celery
from celery.result import AsyncResult
import time


app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'pyamqp://host.docker.internal//'
app.config['CELERY_RESULT_BACKEND'] = 'redis://host.docker.internal'

mac_windows='host.docker.internal'

celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def server_status():
    return jsonify(status='server is running'), 200

@celery.task(bind=True)
def dummy_task(self):
    #task simulation
    time.sleep(10)
    return {'gender': 'male','text': 'blah blah'}

@app.route('/task', methods=['POST'])
def task():
    task = dummy_task.apply_async()
    return jsonify(statusCode=202,id=task.id), 202

@app.route('/task/<id>')
def status(id):
    task = celery.AsyncResult(id)
    return jsonify(statusCode=200,state=task.state, data=task.info), 200
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)