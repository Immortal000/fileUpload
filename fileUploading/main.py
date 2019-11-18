from flask import Flask, render_template,request, send_file
from flask_sqlalchemy import SQLAlchemy
import random,string
from io import BytesIO
characters = string.ascii_letters
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tmp/AllFiles.db'
app.config['SECRET_KEY']='A secret key!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class FileManage(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(300))
	extension = db.Column(db.String(300), unique=True)
	data = db.Column(db.LargeBinary)
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/',methods=['POST'])
def show():
	file = request.files['file']
	file_id = ''.join(random.sample(characters,5))
	newFile = FileManage(name=str(file.filename),extension=file_id,data=file.read())
	db.session.add(newFile)
	db.session.commit()
	return f'Saved file to Data base. Your file id = {file_id}'

@app.route('/<file_id>')
def file_id(file_id):
	check_file = FileManage.query.filter_by(extension=file_id).first()
	if check_file: 
		download_name = check_file.name
		return send_file(BytesIO(check_file.data),attachment_filename=check_file.name,as_attachment=True)
	else:
		return "wrong page or page not registered"

if __name__ == '__main__':
	app.run(debug=True)