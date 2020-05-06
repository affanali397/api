from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Db Model
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

# Package Schema
class PackageSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price')


package_schema = PackageSchema()
packages_schema = PackageSchema(many=True)

#create a package
@app.route('/package', methods=['POST'])
def add_package():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']

    new_package = Package(name, description, price)

    db.session.add(new_package)
    db.session.commit()
    
    return package_schema.jsonify(new_package)

# Run Server
if __name__ =='__main__':
    app.run(debug=True)


