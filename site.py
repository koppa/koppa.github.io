#!/usr/bin/env python
import re
from collections import namedtuple
from pathlib import Path
from sys import argv

from datetime import datetime
import exifread
import pypandoc
from flask import Flask, render_template, url_for, abort, json
from flask_frozen import Freezer
from flaskext.markdown import Markdown

USAGE = """
./site.py [build]
"""

app = Flask(__name__)
freezer = Freezer(app)

# Flask markdown extension, adds filters to jinja
Markdown(app)
# fix reload when using the markdown extension
app.jinja_env.auto_reload = True

Photo = namedtuple('Photo', ['url', 'title', 'desc'])

FOTODIR = Path('static/photos')

def format_date(inpstr):
    """ 2017:12:10 16:28:51 ==> December 2017 """

    # just strip the clock
    dt = datetime.strptime(str(inpstr), "%Y:%m:%d %H:%M:%S")
    return dt.strftime("%B %Y")

print(format_date("2017:12:10 16:28:51"))
assert format_date("2017:12:10 16:28:51") == "December 2017"
def get_photos():
    files = {f.name: [f_ for f_ in f.iterdir()] for f in FOTODIR.iterdir() if f.is_dir()}
    # files['nogroup'] = [f for f in FOTODIR.iterdir()]

    return {group: [Photo(url=url_for('static',
                                      filename='/'.join(f.parts[-3:])),
                          title=f,
                          desc=f"{format_date(exifread.process_file(f.open('rb'))['EXIF DateTimeOriginal'])}")
                    for f in fs if f.is_file() and f.name.endswith('.jpg')]
            for group, fs in files.items()}


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


Article = namedtuple("Article", ['title', 'name', 'author', 'date', 'text'])
ARTICLEPATH = Path('articles')


@app.route('/articles.html')
def articles():
    return render_template('articles.html', articles=articles_all())


def articles_all():
    out = []
    for f in ARTICLEPATH.iterdir():
        assert f.is_file()
        out.append(article_get(f))
    return out


def article_get(file):
    if isinstance(file, str):
        file = list(ARTICLEPATH.glob( f"{file}.*"))[0]


    jsonstring = pypandoc.convert_text(file.open('r').read(),
                                       'html5', 'markdown',
                                       extra_args=('--template', 'default.metatemplate'))

    dict = json.loads(jsonstring)
    author = dict.get('author', 'noauthor')
    if isinstance(author, list):
        assert len(author) == 1
        author = author[0]
    date = dict.get('date', 'nodate')
    title = dict.get('title', 'notitle').rstrip('\n')
    text = pypandoc.convert_text(file.open('r').read(), "html5", "markdown")
    return Article(author=author,
                   date=date,
                   title=title,
                   name=file.stem,
                   text=text)


@app.route('/article/<name>.html')
def article(name):
    if not re.match('^[a-zA-Z0-9_]+$', name):
        abort(404)

    article = article_get(name)

    return render_template('article.html', article=article)


@app.route('/photos.html')
def photos():
    photos = get_photos()
    return render_template('photos.html', photos=photos)


@app.route('/about.html')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    if len(argv) == 1:
        app.run(debug=True)
    elif len(argv) > 1 and argv[1] == 'build':
        freezer.freeze()
    else:
        print(USAGE)
