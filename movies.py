import sqlite3
class Movie:
    def __init__(self,id,title,genre,rating) -> None:
        self.id = id
        self.title = title
        self.genre = genre
        self.rate = rating

class MovieDatabase:
    def __init__(self,db_name) -> None:
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        con = sqlite3.connect("movies.db")
        cursor = con.cursor()
        cursor.execute(''' create table if not exists Movies(
                       ID integer primary key autoincrement,
                       title text,
                       genre text,
                       rate integer
                       )''')
        con.commit()
        con.close()
    def add_movie(self,movie_obj):
        con = sqlite3.connect("movies.db")
        cursor = con.cursor()
        cursor.execute('''insert or replace into Movies (title,genre,rate) 
                       values (?,?,?)''',(movie_obj.title,movie_obj.genre,movie_obj.rate))
        con.commit()
        con.close()
    def view_movies_list(self):
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute('''select * from movies''')
        res = cursor.fetchall()

        from tabulate import tabulate
        print(tabulate(res,headers=["ID","Title","Genre","Rating"]))
        con.close()
    def search_movie(self,search_item):
        with sqlite3.connect("movies.db") as con:
            cursor = con.cursor()
            try:
                cursor.execute('''select Id,title,genre, rate from movies 
                                where title like ? or id like ?''',(f"%{search_item}%",f"%{search_item}%"))
                res = cursor.fetchall()
                if res:
                    from tabulate import tabulate
                    print(tabulate(res,headers=["ID","Title","Genre","Rating"]))  
                else:
                    print("NO such movie found in the database")
            except sqlite3.Error as e:
                print("Database error: ",e)
                    
    def delete_movie(self,id):
        moviedb.view_movies_list()
        con = sqlite3.connect(self.db_name)
        cursor = con.cursor()
        cursor.execute('''Delete from movies where id = ?''',id)
        con.commit()
        con.close() 
    def delete_movie_database(self):
        with sqlite3.connect("movies.db") as con:
            cursor = con.cursor()
            cursor.execute("drop table if exists movies")
            con.commit()

moviedb = MovieDatabase("movies.db")

while True:
    print("\n--- Movie Collection Management ---")
    print("1. Add Movie")
    print("2. View All Movies")
    print("3. Search Movie")
    print("4. Delete Movie by ID")
    print("5. Delete Entire Database Table")
    print("6. Exit")
    
    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        title = input("Enter movie title: ")
        genre = input("Enter genre: ")
        rating = input("Enter rating (1-10): ")
        new_movie = Movie(None,title,genre,rating)
        moviedb.add_movie(new_movie)
        print("Movie added successfully!")

    elif choice == '2':
        print("\nMovie List:")
        moviedb.view_movies_list()

    elif choice == '3':
        search_term = input("Enter movie title or ID to search: ")
        moviedb.search_movie(search_term)

    elif choice == '4':
        movie_id = input("Enter the ID of the movie to delete: ")
        moviedb.delete_movie((movie_id,))
        print(f"Movie with ID {movie_id} deleted.")

    elif choice == '5':
        confirm = input("Are you sure you want to delete all records? (y/n): ")
        if confirm.lower() == 'y':
            moviedb.delete_movie_database()
            print("Database table dropped.")
            moviedb.create_table()

    elif choice == '6':
        print("Exiting program.")
        break
    else:
        print("Invalid choice, please try again.")