from flask import Flask,request,render_template,url_for,redirect,send_file
app=Flask(__name__)

LIB_FOLDER='pics'
app.config['LIB_FOLDER']=LIB_FOLDER

ALLOWED_EXTENSIONS=set(['jpg','bmp','jpeg','png'])
def allowed_files(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# index page
@app.route('/')
def index():
	return render_template("index.html") + list_file()

# return the img file content
@app.route('/img/')
def img():
	path = request.args.get('path')
	return send_file(path,mimetype='image')

# show image with other data
@app.route('/show/')
def show():
    path = request.args.get('path')
    return render_template("show.html", file_path = path, img_link = url_for('img', path = path) )

# show the file list
@app.route('/ls/')
def list_file():
    # response string
	output = ""
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
