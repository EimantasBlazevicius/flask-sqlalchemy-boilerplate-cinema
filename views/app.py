from flask import render_template, request, url_for, redirect
from sqlalchemy.orm import sessionmaker

from config import *
from models import cinema

Session = sessionmaker(bind=cinema.eng)
session = Session()


@app.route("/", methods=["GET", "POST"])
def movies():
    if request.method == "GET":
        all_movies = session.query(cinema.Movies).all()
        all_directors = session.query(cinema.Directors.director_id, cinema.Directors.name,
                                      cinema.Directors.surname).all()
        return render_template('create_movie.html', movies=all_movies, directors=all_directors)
    elif request.method == "POST":
        title = request.form['title']
        category = request.form['category']
        year = int(request.form['year'])
        rating = int(request.form['rating'])
        director_id = request.form['director']
        new_movie = cinema.Movies(title=title, category=category, year=year, rating=rating, director_id=director_id)
        session.add(new_movie)
        session.commit()
        return redirect(url_for('movies'))


@app.route("/directors", methods=["GET", "POST"])
def directors():
    if request.method == "GET":
        all_directors = session.query(cinema.Directors).all()
        return render_template('create_director.html', directors=all_directors)
    elif request.method == "POST":
        name = request.form['name']
        surname = request.form['surname']
        rating = int(request.form['rating'])
        new_dir = cinema.Directors(name=name, surname=surname, rating=rating)
        session.add(new_dir)
        session.commit()
        return redirect(url_for('directors'))


@app.route("/movies/delete/<movie_id>", methods=["POST"])
def delete_movie(movie_id):
    movie_to_delete = session.query(cinema.Movies).get(movie_id)
    session.delete(movie_to_delete)
    session.commit()
    return redirect(url_for('movies'))


@app.route("/directors/delete/<dir_id>", methods=["POST"])
def delete_director(dir_id):
    dir_to_delete = session.query(cinema.Directors).get(dir_id)
    session.delete(dir_to_delete)
    session.commit()
    return redirect(url_for('directors'))


@app.route("/movies/update/<movie_id>", methods=["GET", "POST"])
def update_movie(movie_id):
    if request.method == "GET":
        all_movies = session.query(cinema.Movies).all()
        all_directors = session.query(cinema.Directors.director_id, cinema.Directors.name,
                                      cinema.Directors.surname).all()
        movie_to_be_updated = session.query(cinema.Movies).get(movie_id)
        return render_template('update_movie.html', movies=all_movies, directors=all_directors,
                               movie_to_be_updated=movie_to_be_updated)

    elif request.method == "POST":
        movie_to_update = session.query(cinema.Movies).get(movie_id)

        movie_to_update.title = request.form['title']
        movie_to_update.category = request.form['category']
        movie_to_update.year = int(request.form['year'])
        movie_to_update.rating = int(request.form['rating'])
        movie_to_update.director_id = request.form['director']
        session.commit()

        return redirect(url_for('movies'))


@app.route("/directors/update/<dir_id>", methods=["GET", "POST"])
def update_director(dir_id):
    if request.method == "GET":
        all_directors = session.query(cinema.Directors).all()
        director_to_be_updated = session.query(cinema.Directors).get(dir_id)
        return render_template('update_director.html', directors=all_directors,
                               director_to_be_updated=director_to_be_updated)

    elif request.method == "POST":
        dir_to_update = session.query(cinema.Directors).get(dir_id)

        dir_to_update.name = request.form['name']
        dir_to_update.surname = request.form['surname']
        dir_to_update.rating = int(request.form['rating'])
        session.commit()

        return redirect(url_for('directors'))


if __name__ == "__main__":
    app.run(debug=True)
