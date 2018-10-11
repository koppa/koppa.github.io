#!/usr/bin/env python
import re
from collections import namedtuple
from pathlib import Path
from sys import argv
from itertools import chain

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

PHOTODIR = Path('static/photos')

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']


def create_photo(f):
    """
        Take a path to a photo
        Return Photo object with description
    """

    # just strip the clock
    exifdate = exifread.process_file(f.open('rb'))['EXIF DateTimeOriginal']
    dt = datetime.strptime(str(exifdate), "%Y:%m:%d %H:%M:%S")
    formatted_date = dt.strftime("%B %Y")

    return Photo(url=url_for('static', filename='/'.join(f.parts[-3:])),
                 title=f,
                 desc=formatted_date)


def _get__photos_subdir(path):
    """
        Take a path and return a list of Photo objects
    """
    return [create_photo(f) for f in path.iterdir()
            if f.is_file() and f.suffix in ALLOWED_EXTENSIONS]


def get_photos():
    """
        Return a dict of photos grouped by keyword

    """

    photos = {f.name: _get__photos_subdir(f)
              for f in PHOTODIR.iterdir()
              if f.is_dir()}

    ng = _get__photos_subdir(PHOTODIR)
    if ng:
        photos['nogroup'] = ng

    return photos

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


Article = namedtuple("Article", ['title', 'name', 'author', 'date', 'text'])
ARTICLEPATH = Path('articles')
ARTICLE_NOT_PUBLISHED = Path('not_published')


def article_files():
    if app.debug:
        return [f for f in chain(ARTICLEPATH.iterdir(),
                                 ARTICLE_NOT_PUBLISHED.iterdir())
                if f.is_file()]

    return [f for f in ARTICLEPATH.iterdir() if f.is_file()]


@app.route('/articles.html')
def articles():
    return render_template('articles.html', articles=articles_all())


def articles_all():
    return [article_get(f) for f in article_files()]


def article_get(file):
    if isinstance(file, str):
        for f in article_files():
            if f.name.startswith(f"{file}."):
                file = f
                break
        else:
            raise KeyError(f"Requesting article {file} and can't be found.")

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
