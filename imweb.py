from flask import Flask,request,render_template,url_for,redirect,send_file
app=Flask(__name__)

LIB_FOLDER='pics'

ALLOWED_EXTENSIONS=set(['jpg','bmp','jpeg','png'])
def allowed_files(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def img_path(root = LIB_FOLDER):
    import os
    for root,dirs,files in os.walk(root):
        for f in files:
            path = os.path.join(root,f)
            if allowed_files(path):
                yield path

IMGS = list(img_path())

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
    for idx, elem in enumerate(IMGS):
        if elem == path:
            next_path = IMGS[(idx + 1)%len(IMGS)]
            prev_path = IMGS[(idx -1)%len(IMGS)]
            break
    return render_template("show.html", file_path = path, img_link = url_for('img', path = path), next_img_link = url_for('show',path = next_path) , prev_img_link = url_for('show',path = prev_path))

# show the file list
@app.route('/ls/')
def list_file():
    # response string
    output = ""
    for p in IMGS:
        output += '''<p><a href="{link}">{name}</a></p>'''\
        .format(link=url_for("show",path = p),name = p)
    return output

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)
