from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

eng = create_engine('mysql://root:root@127.0.0.1:3306/cinematic')
Base = declarative_base()


class Directors(Base):
    __tablename__ = 'directors'

    director_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    surname = Column(String(30), nullable=False)
    rating = Column(Integer, nullable=False)
    movies = relationship('Movies', back_populates='director', cascade="all, delete")

    def __repr__(self):
        max = ''
        rating= 0
        for movie in self.movies:
            if movie.rating >= rating and movie.director_id == self.director_id:
                rating = movie.rating
                max = movie.title
        return f'{max}'


class Movies(Base):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    year = Column(Integer, nullable=False)
    category = Column(String(30), nullable=False)
    director_id = Column(Integer, ForeignKey('directors.director_id'), nullable=False)  # if no cascade(deletion of movies) needed, change nullable to True
    rating = Column(Integer, nullable=False)
    director = relationship('Directors', back_populates='movies')

    def __repr__(self):
        return {self.rating: self.title}


Base.metadata.create_all(eng)
