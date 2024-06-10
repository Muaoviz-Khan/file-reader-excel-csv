

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/fileparse'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    country = db.Column(db.String(20))

    def __init__(self, name, age, country):
        self.name = name
        self.age = age
        self.country = country

class PostSchema(ma.Schema):
    class Meta:
        fields = ("name", "age", "country")     

post_schema = PostSchema()
posts_schema = PostSchema(many=True)  

@app.route("/csv", methods=['POST'])
def upload_files():
    uploaded_file = request.files['filename']
    if uploaded_file.filename != '':
        col_names = ['name', 'age', 'country']
        csv_data = pd.read_csv(uploaded_file, names=col_names, header=None)
        a=0
        for i, row in csv_data.iterrows():
            a+=1
            if a==1:
                continue
            else:    
                new_detail = Details(row['name'], row['age'], row['country'])
                db.session.add(new_detail)
        
        db.session.commit()
        return jsonify({"message": "CSV data uploaded successfully!"}), 200
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/excel', methods=['POST'])
def upload_excel():
    file = request.files['filename']
    if file.filename != '':
        data = pd.read_excel(file)
        a=0
        for i, row in data.iterrows():
            a+=1
            if a==1:
                continue
            else:    
                new_detail = Details(row['name'], row['age'], row['country'])
                db.session.add(new_detail)
        
        db.session.commit()
        return jsonify({"message": "Excel data uploaded successfully!"}), 200
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/get',methods=['GET'])
def getall():
    data=Details.query.all()
    result=posts_schema.dump(data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True) 