import pymongo
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime
import pandas as pd

try:

    # MongoDB Connection
    client = pymongo.MongoClient('mongodb+srv://sangeeth:fwKxrnGyD5cLyv1l@cluster0.m811i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    db = client['sample_mflix']
    collection = db['movies']

    # SQLAlchemy setup
    Base = declarative_base()

    class Movie(Base):
        __tablename__ = 'movies'
        
        # MongoDB _id as a text-based unique key
        _id = Column(String(255), primary_key=True)  # Use String for the MongoDB _id    
        title = Column(String(255))
        year = Column(Integer)
        rated = Column(String(10))
        released = Column(Date)
        runtime = Column(Integer)
        genre = Column(String(255))
        director = Column(String(255))
        actors = Column(String(255))
        plot = Column(String)
        language = Column(String(50))
        country = Column(String(50))
        awards = Column(String(255))
        poster = Column(String(255))
        imdb_id = Column(String(50))
        type = Column(String(50))
        dvd = Column(Date)
        box_office = Column(Float)
        production = Column(String(100))
        website = Column(String(255))

    # SQLite engine and session setup
    engine = create_engine('sqlite:///moviesdb.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch data from MongoDB
    movies_cursor = collection.find()

    # Function to convert MongoDB data to a dictionary that matches SQLAlchemy model
    def transform_movie_data(movie):
        transformed = {
            '_id': str(movie.get('_id')),  # Convert MongoDB _id to string
            'title': movie.get('title','Unknown'),
            'year': movie.get('year',0),
            'rated': movie.get('rated','Unknown'),
            'released': movie.get('released'),
            'runtime': movie.get('runtime',0),
            'genre': ', '.join(movie.get('genres', [])),
            'director': movie.get('director','Unknown'),
            'actors': movie.get('actors','Unknown'),
            'plot': movie.get('plot','Unknown'),
            'language': movie.get('language','Unknown'),
            'country': movie.get('country','Unknown'),
            'awards': ', '.join(movie.get('awards', [])),
            'poster': movie.get('poster','Unknown'),
            'imdb_id': movie.get('imdb_id','Unknown'),
            'type': movie.get('type','Unknown'),
            'dvd': movie.get('dvd'),
            'box_office': movie.get('boxOffice',0),
            'production': movie.get('production','Unknown'),
            'website': movie.get('website','Unknown')
        }
        
        # Handle the 'released' and 'dvd' dates
        if transformed['released']:
            transformed['released'] = pd.to_datetime(transformed['released'], errors='coerce').date()
        if transformed['dvd']:
            transformed['dvd'] = pd.to_datetime(transformed['dvd'], errors='coerce').date() 

        return transformed

    # Insert data into SQLite using SQLAlchemy ORM
    for movie in movies_cursor:
        movie_data = transform_movie_data(movie)
        
        # Create a new Movie object with the transformed data
        new_movie = Movie(**movie_data)
        
        # Add the new movie to the session
        session.add(new_movie)
except Exception as e:
    print(e)        

finally:
    #Commit the transaction for each movie (you can also batch this if needed)
    session.commit()
    # Close the session
    session.close()
    print("Data imported successfully!")
    
    # Print data from SqlLite DB
    print("Printing data....")
    movies_data1 = session.query(Movie).limit(10).all()
    for movie in movies_data1:
        print(vars(movie))