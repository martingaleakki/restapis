from flask import Flask, request
from sqlalchemy import create_engine
from apis import puppies as puppies_api
app = Flask(__name__)
# Create the appropriate app.route functions. Test and see if they work


@app.route('/puppies', methods=['GET','POST'])
def puppiesFunction():
    if request.method == 'GET':
        return puppies_api.getAllPuppies()
    elif request.method == 'POST':
        name = request.args.get('name', '')
        description = request.args.get('description', '')
        return puppies_api.makeANewPuppy(name, description)


@app.route('/puppies/<int:id>', methods=['GET','PUT','DELETE'])
def puppiesFunctionId(id):
    if request.method == 'GET':
        return puppies_api.getPuppy(id)
    elif request.method == 'PUT':
        return puppies_api.updatePuppy(id)
    elif request.method == 'DELETE':
        return puppies_api.deletePuppy(id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
