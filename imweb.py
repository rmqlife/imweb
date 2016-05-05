from flask import Flask,request,render_template,url_for,redirect
app=Flask(__name__)

LIB_FOLDER='pics'
app.config['LIB_FOLDER']=LIB_FOLDER

ALLOWED_EXTENSIONS=set(['jpg','bmp','jpeg','png'])
def allowed_files(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
	return render_template("index.html") 

@app.route('/show/')
def show():
#	return file_path
	path = request.args.get('path')
	return render_template('show.html',file_path = path, img_link = url_for('static',filename = path))

@app.route('/ls/')
def list_file():
	output=""
	print app.config['LIB_FOLDER']
	from os import walk, path
	for root,dirs,files in walk(app.config['LIB_FOLDER']):
		for filename in files:
			full_path = path.join(root,filename)
			if allowed_files(filename):
				output += '''<p><a href="{link}">{name}</a></p>'''\
				.format(link=url_for("show",path=full_path),name=full_path)
	return output

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)
