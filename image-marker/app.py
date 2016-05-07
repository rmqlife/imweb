import threading
import os
import random

from flask import Flask, render_template, request


app = Flask(__name__)
db = open('markers.db', 'a')
_lock = threading.Lock()


def load_imgs(root='pics', suffix=".jpg"):
    for r, dirs, files in os.walk(root):
        for f in files:
            if f.lower().endswith(suffix):
                yield os.path.join(r, f)


def load_marked():
    try:
        return [l.split(",")[0] for l in open('markers.db').readlines()]
    except:
        pass
    return []

IMGS = list(load_imgs())
MARKED = set(load_marked())
print IMGS

def mark(img, box):
    print img, box
    _lock.acquire()
    try:
        db.write(img)
        for v in box:
            db.write(", ")
            db.write("%0.4f" % v)
        db.write("\n")
        db.flush()
        MARKED.add(img)
    finally:
        print 'release'
        _lock.release()


def get_box(form):
    for v in ('x0', 'y0', 'x1', 'y1'):
        p = form[v]
        if not p:
            yield 0
        a, b = p.split('/')
        yield float(a)/float(b)


def find_one():
    for img in IMGS:
        if img not in MARKED:
            return img


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        if 'skip' in request.form:
            box = [-1, -1, -1, -1]
        else:
            box = list(get_box(request.form))
        try:
            mark(request.form['file'], box)
        except:
            pass
    img = find_one()
    if img:
        return render_template("index.html", img=img)
    else:
        return "All images are marked."


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
