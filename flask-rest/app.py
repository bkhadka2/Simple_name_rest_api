from flask import Flask
from flask import render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Name(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        contact_name = Name(first_name=fname, last_name=lname)
        names = Name.query.order_by(Name.first_name).all()
        try:
            db.session.add(contact_name)
            db.session.commit()
            return redirect('/display')
        except:
            error = 'Could not add name'
            return render_template('error.html', error=error)
    else:
        return render_template('index.html')
    
@app.route('/display', methods=['GET'])
def display_all_names():
    names = Name.query.order_by(Name.first_name).all()
    return render_template('welcome.html', names=names)

@app.route('/api/display', methods=['GET'])
def api_display():
    names = Name.query.order_by(Name.first_name).all()
    response = {}
    for elem in names:
        response[elem.id] = elem.first_name + ' ' + elem.last_name
    return jsonify(response)

@app.route('/api/display/<int:id>', methods=['GET'])
def api_display_particular(id):
    name = Name.query.filter_by(id = id).first()
    response = {}
    response[name.id] = name.first_name + ' ' + name.last_name
    return jsonify(response)

@app.route('/api/update/<int:id>', methods=['PUT']) # Update is put
def api_update(id):
    name_to_update = Name.query.get_or_404(id)
    name_to_update.id = request.json['id']
    name_to_update.first_name = request.json['first_name']
    name_to_update.last_name = request.json['last_name']    
    db.session.commit()
    return redirect('/api/display')

@app.route('/api/delete/<int:id>', methods=['DELETE'])
def api_delete(id):
    name_to_delete = Name.query.get_or_404(id)
    try:
        db.session.delete(name_to_delete)
        db.session.commit()
    except:
        error = 'Could not delete name'
        return render_template('error.html', error=error)
    return redirect('/api/display')  