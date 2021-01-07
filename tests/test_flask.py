# http://www.pythondoc.com/flask-restful/first.html

from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# curl -i http://localhost:5000
@app.route('/')
def test_hello_world():
    return 'Hello World!'


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

# curl -i http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def test_get_tasks():
    return jsonify({'tasks':tasks})

# curl -i http://localhost:5000/todo/api/v1.0/tasks/2
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def test_get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Read a book"}' http://localhost:5000/todo/api/v1.0/tasks
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def test_create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
         }
         tasks.append(task)
         return jsonify({'task': task}), 201

@app.errorhandler(404)
def test_not_found(error):
    return make_response(jsonify({'error':'Not found'), 404)

if __name__ == '__main__':
    app.debug =  True
    app.run()
