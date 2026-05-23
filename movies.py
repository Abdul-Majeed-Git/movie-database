import sqlite3
from tabulate import tabulate
#--------------------------------------------------------------------------------------------------------------
class Movie:
    def __init__(self,id,title,genre,rating) -> None:
        self.id = id
        self.title = title
        self.genre = genre
        self.rate = rating
#--------------------------------------------------------------------------------------------------------------

class MovieDatabase:
#--------------------------------------------------------------------------------------------------------------    
    def __init__(self,db_name) -> None:
        self.db_name = db_name
        self.create_table()
#--------------------------------------------------------------------------------------------------------------
    def create_table(self):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute(''' create table if not exists Movies(
                       ID integer primary key autoincrement,
                       title text,
                       genre text,
                       rate real
                       )''')
        con.commit()
        con.close()
#--------------------------------------------------------------------------------------------------------------
    def add_movie(self,movie_obj):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute('''insert or replace into Movies (title,genre,rate) 
                       values (?,?,?)''',(movie_obj.title,movie_obj.genre,movie_obj.rate))
        con.commit()
        con.close()
#---------------------------------------------------------------------------------------------------------------        
    def view_movies_list(self):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute('''select title, genre, rate from movies order by rate desc''')
        res = cursor.fetchall()

        print(tabulate(res,headers=["Title","Genre","Rating"],tablefmt='rounded_grid'))
        con.close()
#--------------------------------------------------------------------------------------------------------------
    def search_movie(self,search_item):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            try:
                cursor.execute('''select title,genre, rate from movies 
                                where title like ?''',
                                (f"%{search_item}%",))
                res = cursor.fetchall()
                if res:
                    print(tabulate(res,headers=["Title","Genre","Rating"], tablefmt="rounded_grid"))  
                else:
                    print("NO such movie found in the database")
            except sqlite3.Error as e:
                print("Database error: ",e)
#--------------------------------------------------------------------------------------------------------------                    
    def search_movie_by_rating(self,min_rate):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            try:
                cursor.execute('''select title , genre, rate from movies
                            where rate >= ? order by rate desc''',(min_rate,))
                res = cursor.fetchall()
                if res:
                    print(tabulate(res,headers=["Title","Genre","Rating"], tablefmt="rounded_grid"))
                else:
                    print(f"No movies found with a rating of {min_rate} or above.")
            except sqlite3.Error as e:
                print("Database Eror: ", e)
#--------------------------------------------------------------------------------------------------------------    
    def delete_movie(self,id):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute('''Select * from movies where id = ?''',(id,))
        row = cursor.fetchone()
        if row is None:
            print(f"There is such movie in database with ID:{id}")
            con.close()
            return False
        cursor.execute("delete from movies where id = ?",(id,))
        con.commit()
        con.close() 
        return True
#--------------------------------------------------------------------------------------------------------------        
    def delete_movie_database(self):
        with sqlite3.connect(self.db_name) as con:
            cursor = con.cursor()
            cursor.execute("drop table if exists movies")
            con.commit()
#--------------------------------------------------------------------------------------------------------------
    def view_movies_with_id(self):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute('''SELECT ID, title, genre, rate FROM movies ORDER BY rate DESC''')
        res = cursor.fetchall()
        con.close()
        if res:
            print(tabulate(res, headers=["ID", "Title", "Genre", "Rating"],tablefmt='rounded_grid'))
moviedb = MovieDatabase("movies.db")
try:
    while True:
        print("\n--- Movie Collection Management ---")
        print("1. Add Movie")
        print("2. View All Movies")
        print("3. Search Movie")
        print("4. Search Movie by minimum rating")
        print("5. Delete Movie by ID")
        print("6. Delete Entire Database Table")
        print("7. Add 40 sample movies to DB")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            title = input("Enter movie title: ").strip()
            while not title:
                print("Invalid input! Title feild cannot be empty!.")
                title = input("Enter movie title: ").strip()

            genre = input("Enter genre: ").strip()
            while not genre:
                print("Invalid input! Genre feild cannot be empty!")
                genre = input("Enter genre: ").strip()

            while True:
                rating_input = input("Enter rating (1-10): ").strip()
                if not rating_input:
                    print("Invalid input! rating feild cannot be empty!")
                    continue
                try:
                    rating = float(rating_input)
                    if 1<= rating <= 10:
                        break
                    else:
                        print("Rating must be between 1 and 10!")
                except ValueError:
                    print("Rating must be a number!")
            new_movie = Movie(None,title,genre,rating)
            moviedb.add_movie(new_movie)
            print("Movie added successfully!")

        elif choice == '2':
            print("\nMovie List:")
            moviedb.view_movies_list()

        elif choice == '3':
            search_term = input("Enter movie title or rate to search: ").strip()
            moviedb.search_movie(search_term)

        elif choice == '4':
            while True:
                min_rate = input("Enter rating(1-10): ").strip()
                if not min_rate:
                    print("Rating cannot be empty!")
                    continue
                try:
                    rating = float(min_rate)
                    if 1<= rating <=10:
                        moviedb.search_movie_by_rating(rating)
                        break
                    else:
                        print("Rating must be between 1 and 10!") 
                except ValueError:
                    print("Invalid Input! Please enter a valid number!")
        elif choice == '5':
            print("-----Current Movie List-----")
            moviedb.view_movies_with_id()
            movie_id = input("Enter the ID of the movie to delete: ").strip()
            if not movie_id:
                print("Movie ID field cannot be empty!")
            else:
                if moviedb.delete_movie(movie_id):
                    print(f"Movie with ID:{movie_id} deleted!")
        
                    

        elif choice == '6':
            confirm = input("Are you sure you want to delete all records? (y/n): ")
            if confirm.lower() == 'y':
                moviedb.delete_movie_database()
                print("Database table dropped.")
                moviedb.create_table()
        elif choice == '7':
            sample_movies = [
                ("Inception", "Sci-Fi", 8.8),
                ("The Dark Knight", "Action", 9.0),
                ("Interstellar", "Sci-Fi", 8.6),
                ("Pulp Fiction", "Crime", 8.9),
                ("The Matrix", "Sci-Fi", 8.7),
                ("Gladiator", "Action", 8.5),
                ("Avatar", "Fantasy", 7.8),
                ("The Godfather", "Crime", 9.2),
                ("Spirited Away", "Animation", 8.6),
                ("Parasite", "Thriller", 8.5),
                ("The Lion King", "Animation", 8.5),
                ("Avengers: Endgame", "Action", 8.4),
                ("Joker", "Drama", 8.4),
                ("Whiplash", "Drama", 8.5),
                ("The Prestige", "Mystery", 8.5),
                ("Fight Club", "Drama", 8.8),
                ("Se7en", "Mystery", 8.6),
                ("Goodfellas", "Biography", 8.7),
                ("The Departed", "Thriller", 8.5),
                ("The Terminator", "Sci-Fi", 8.1),
                ("The Shawshank Redemption", "Drama", 9.3),
                ("Forrest Gump", "Romance", 8.8),
                ("Dangal", "Action", 8.3),
                ("3 Idiots", "Comedy", 8.4),
                ("Schindler's List", "Biography", 9.0),
                ("The Lord of the Rings", "Fantasy", 8.9),
                ("Good Will Hunting", "Drama", 8.3),
                ("Shutter Island", "Mystery", 8.2),
                ("The Green Mile", "Crime", 8.6),
                ("Saving Private Ryan", "War", 8.6),
                ("Spiderman: Into the Spider-Verse", "Animation", 8.4),
                ("Dil Wale Dulhania Le Jayenge", "Romance", 8.0),
                ("Gangs of Wasseypur", "Action", 8.2),
                ("The Dark Knight Rises", "Action", 8.4),
                ("Django Unchained", "Western", 8.4),
                ("The Lion King", "Animation", 8.5),
                ("The Sixth Sense", "Thriller", 8.2),
                ("Zindagi Na Milegi Dobara", "Drama", 8.2),
                ("Your Name", "Animation", 8.4),
                ("Memento", "Mystery", 8.4)
            ]

            for title,genre,rate in sample_movies:
                movies = Movie(None,title,genre,rate)
                moviedb.add_movie(movies)

        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")
except KeyboardInterrupt:
    print()