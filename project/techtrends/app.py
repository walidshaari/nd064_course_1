import sqlite3
import os, sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging


## Global variabls
db_connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global   db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    #increment number of connections metrics
    db_connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    ## app.logger.info('Article %s retrieved!' %post)
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.info('A non-existing article is accessed and a 404 page is returned')
      return render_template('404.html'), 404
    else:
      app.logger.info("Article %s retrieved," %post["title"])
      return render_template('post.html', post=post)

# Define healthz endpoint
@app.route('/healthz')
def healthz():
  response = app.response_class(
            response=json.dumps({"result":" OK - healthy"}),
            status=200,
            mimetype='application/json'
    )

  return response

def post_count():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('select count(*) from posts')
    return cursor.fetchone()[0]

# Define metrics endpoint
@app.route('/metrics')
def metrics():
  response = app.response_class(
            response=json.dumps({"db_connection_count": db_connection_count, "post_count": post_count() }),
            status=200,
            mimetype='application/json'
    )

  return response
# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Us page retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info('New article created %s ' %title)
            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
  loglevel = os.getenv("LOGLEVEL", "DEBUG").upper()
  loglevel = (
      getattr(logging, loglevel)
      if loglevel in ["CRITICAL", "DEBUG", "ERROR", "INFO", "WARNING",]
      else logging.DEBUG
  )
  # Set logger to handle STDOUT and STDERR

  stdout_handler = logging.StreamHandler(sys.stdout)
  stderr_handler = logging.StreamHandler(sys.stderr)
  handlers = [stderr_handler, stdout_handler]
  format_output = '%(asctime)s - %(name)s - %(message)s'

  logging.basicConfig(format=format_output, level=loglevel, handlers=handlers)

  app.run(host='0.0.0.0', port='3111')
