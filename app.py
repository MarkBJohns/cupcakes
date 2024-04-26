from flask import Flask, jsonify, request, render_template, abort
from models import db, connect_db, default_cupcake, Cupcake
from forms import AddCupcakeForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SECRET_KEY'] = 'secret_key'

connect_db(app)

with app.app_context():
    db.create_all()
    
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'Cupcake': Cupcake}
    
@app.route('/')
def home_page():
    form = AddCupcakeForm()
    return render_template('index.html', form=form)

@app.route('/api/cupcakes')
def show_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [Cupcake.serialize(c) for c in cupcakes]
    return jsonify(serialized)
    
@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"]
    )
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:c_id>')
def show_cupcake(c_id):
    cupcake = Cupcake.query.get_or_404(c_id)
    serialized = Cupcake.serialize(cupcake)
    return jsonify(serialized)

@app.route('/api/cupcakes/<int:c_id>', methods=['PATCH'])
def update_cupcake(c_id):
    cupcake = Cupcake.query.get_or_404(c_id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", default_cupcake)
    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())
    
@app.route('/api/cupcakes/<int:c_id>', methods=['DELETE'])
def delete_cupcake(c_id):
    cupcake = Cupcake.query.get(c_id)
    if cupcake is None:
        abort(404)
    message = {f"cupcake {cupcake.id}": "deleted"}
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message)