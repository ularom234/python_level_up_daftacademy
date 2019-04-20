# app.py

from flask import Flask, request, Response, session, redirect, url_for, jsonify, render_template
from functools import wraps
from flask import g
import sqlite3

 
app = Flask(__name__)


#DATABASE = 'chinook_my.db'
DATABASE = 'chinook.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, error, status_code=None, payload=None):
        super().__init__(self)
        self.error = error
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.error
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/')
def root():
    return 'Hello!'


@app.route('/genres')
def genres():
    db = get_db()
    genres_rows = db.execute('''
        SELECT genres.Name, count(tracks.GenreId)
        FROM genres
        LEFT JOIN tracks ON genres.GenreId = tracks.GenreId
        GROUP BY genres.Name
    ''').fetchall()
    return jsonify(dict(genres_rows))




@app.route('/tracks', methods = ['POST','GET'])
def tracks_list():
    if request.method == 'GET':
        return get_tracks()
    elif request.method == 'POST':
        return post_tracks()
    else:
        return 400
    
def get_tracks():
    db = get_db()
    a = request.args

    if ('per_page' in a):
        per_page = int(a['per_page']) 
    else:
        per_page = -1

    limit = per_page


    if ('page' in a):
        page = int(a['page'])
    else:
        page = 0

    page_index = page - 1
    offset = page_index * per_page

    if 'artist' in a:
    
        data = db.execute('''
            SELECT tracks.Name FROM tracks 
            JOIN albums ON tracks.AlbumId = albums.AlbumId 
            JOIN artists ON albums.ArtistId = artists.ArtistId 
            WHERE artists.name = ? 
            ORDER BY tracks.Name COLLATE NOCASE
            LIMIT ? OFFSET ?;
            ''', (a['artist'], limit, offset))
    else:
        data = db.execute('SELECT name FROM tracks ORDER BY name COLLATE NOCASE LIMIT ? OFFSET ?;', (limit, offset))
    return jsonify([row[0] for row in data.fetchall()])

def post_tracks():
    db = get_db()
    print('wczytalem baze')
    json_data = request.get_json()
    print(json_data)

    if not json_data:
        return 400

    else:
        try:
            album_id = json_data.get('album_id')
            media_type_id = json_data.get('media_type_id')
            genre_id = json_data.get('genre_id')
            name = json_data.get('name')
            composer = json_data.get('composer')
            milliseconds = json_data.get('milliseconds')
            bbytes = json_data.get('bytes')
            price = json_data.get('price')
            if album_id is None or media_type_id is None or genre_id is None or name is None or composer is None or milliseconds is None or bbytes is None or price is None:
                raise InvalidUsage('missing data')
        except:
            return 'incoplete data', 400

        try:
            db.execute('''
                INSERT INTO tracks (name, albumid, mediatypeid, genreid, composer,
                    milliseconds, bytes, unitprice) 
       			    VALUES (?,?,?,?,?,?,?,?)
                    ''',(name, album_id, media_type_id, genre_id, composer, milliseconds, bbytes, price))

            data = db.execute('''SELECT * FROM tracks
							 WHERE trackid = (SELECT MAX(trackid)  FROM tracks)''').fetchone()
        except sqlite3.IntegrityError as error:
                raise error

        return jsonify(data)
 




if __name__ == '__main__':
    app.run(debug=True)
