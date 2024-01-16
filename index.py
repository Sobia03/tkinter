# Importing tkinter module
import tkinter as tk
# Importing different modules from tkinter 
from tkinter import ttk, Entry, messagebox
# Importing Image, ImageTk modules from PIL library to generate images
from PIL import Image, ImageTk
# Importing requests module to make http requests
import requests
# Importing random module to geenrate random values
import random
# Importing io (input/output) module to work with file-like objects
import io
# Importing BytesIO to work with binary data
from io import BytesIO
# Importing datetime to work with dates
from datetime import datetime
# Importing Button module for macOS
from tkmacosx import Button


# Creating a class for intro window
class IntroWindow:
    def __init__(self, main):
        self.main= main                # Creating main output window
        self.main.title("Movie Mania")     # Giving a title to the intro window
        self.main.geometry("900x680")      # Setting the window size
        self.main.resizable(0, 0)          # Disabling resizing the window
        
         # creating a frame to place all content in it
        self.frame_main= tk.Frame(main, width=900, height=680)
        self.frame_main.pack()
        
        # Setting a background image and resizing it
        self.img = Image.open("bg.png")
        self.resized = self.img.resize((950,680))          # Resizing the image 
        self.new_img = ImageTk.PhotoImage(self.resized)
        ex = tk.Label(self.frame_main, image = self.new_img)
        ex.place(x = 0, y = 0)
        
        # Button that takes to MoveMania
        open_btn= Button(self.frame_main, text="Open", command=self.open, highlightbackground="#034863", font=("Helvetica", 20), bg="white")
        open_btn.place(x=390, y=350)
        
        # intializing the app as none
        self.app=None
    
    def open(self):
        # destroying the intro window
        self.frame_main.destroy()
        # calling the MovieMania class
        inst = MovieMania(self.main)
        

# Using the api key and base url generated from themoviedb api after authentication
api= 'ccc69b61cbc6d16936b780dda14c54d6'
base= 'https://api.themoviedb.org/3/'

# Creating a class for all functions and tabs
class MovieMania:
    def __init__(self, root):
        # Creating output window
        self.root = root
        # Giving a title to window
        self.root.title("Movie Mania")
        # Setting the window size
        self.root.geometry("980x750")
        # Disabling resizing the window
        self.root.resizable(0, 0)

        # Creating a notebook for multiple tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both') 
        # styling the notebook
        style=ttk.Style()
        style.configure("TNotebook.Tab", font=("Helvetica", 16), padding=[10,5])   
        
        # Setting variables for different elements 
        self.poster_label= None
        self.details_text = None
        self.cast_text = None
        self.result_canvas = None
        
        # Creating first tab to display movie details and cast
        self.details_tab()
        # Creating second tab to display upcoming movies
        self.upcoming_tab()
        # Creating third tab to display recommended movies
        self.recommend_tab()
        # Creating fourth tab to display movies based on actors
        self.actor_works_tab()
        
        self.poster_images = {}
        
    # Creating a function to clear all content in tabs
    def clear_tab(self, tab_frame):
        for widget in tab_frame.winfo_children():
            # destroying all widgets in tab
            widget.destroy()
    
    # First Tab (Movie Details with cast)
    # Creating a function to display first tab 
    def details_tab(self):
        tab1= ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Movie Details")
        
        # Setting a background image to the tab and resizing it
        self.img = Image.open("pic (10).png")
        self.resized = self.img.resize((980,700))          # Resizing the image to fit tab
        self.new_img = ImageTk.PhotoImage(self.resized)
        ex = tk.Label(tab1, image = self.new_img)
        ex.place(x = 0, y = 0)
        
        # Instruction label for user to enter movie name
        ent_mov_name= tk.Label(tab1, text="Enter movie name to see its details",font=("Georgia",24), bg="#012E46" )
        ent_mov_name.place(x=280,y=32)
        
        # Entry widget for user to enter movie name
        entry= Entry(tab1, width=17, font=("Helvetica",17), bg="#E6E6E6", fg="black",  highlightbackground="#447D99")
        entry.place(x=290,y=93)
        
        # Button to get movie details and poster        
        details_button= Button(tab1, text="Show Details", highlightbackground="#012E46", font=("Helvetica", 17), bg="white", command=lambda: self.update_frame(entry))
        details_button.place(x=510, y=95)
        
        # Creating a label to display movie poster
        self.poster_label= tk.Label(tab1, bg="#01263B")
        self.poster_label.pack(side=tk.LEFT, padx=20)
        
        # creating text widget to display movie details
        self.details_text= tk.Text(tab1, wrap=tk.WORD, height=12, width=30, font=("Georgia",16), padx=20, bg="#E6E6E6",highlightbackground="#447D99", fg="black")
        self.details_text.config(state=tk.DISABLED)  # Making the text read only
        self.details_text.place(x=490, y=180)
        
        # creating text widget to display cast names
        self.cast_text = tk.Text(tab1, wrap=tk.WORD, height=10, width=23, font=("Georgia",16), padx=15, bg="#E6E6E6",highlightbackground="#447D99", fg="black")
        self.cast_text.config(state=tk.DISABLED)  # Make the text widget read-only
        self.cast_text.place(x=532, y=440)
        
    def update_frame(self, entry):
        # getting user input from entry widget
        movie_name = entry.get()
        # checking if movie is available
        if movie_name:
            # calling get_movie_details to get details about the movie
            title, image_url, synopsis, cast = self.get_movie_details(movie_name)
            if title and image_url:
                # Getting movie poster and displaying it
                response = requests.get(image_url)
                img_data = response.content
                img = Image.open(io.BytesIO(img_data))
                # resizing the poster
                img.thumbnail((420,470))
                img = ImageTk.PhotoImage(img)

                # Updating poster label with new image
                self.poster_label.config(image=img)
                self.poster_label.image = img
                self.poster_label.place(x=85, y=170)

                # Updating movies detail text widget
                self.details_text.config(state=tk.NORMAL)  # Making the text writable
                self.details_text.delete(1.0, tk.END)  # Clearing text already present
                self.details_text.insert(tk.END, f"\nSynopsis:\n\n{synopsis}")
                self.details_text.config(state=tk.DISABLED)  # Making the text read-only

                # Updating cast text widget
                self.cast_frame(cast)
            # displaying error message if details for the entered movie are not found
            else:
                messagebox.showerror("Not", "Details for movie '" + str(movie_name) + "' not available.")
        # displaying error message if incorrect movie name is entered
        else:
            messagebox.showerror("not","Enter a valid movie name.")

                
# function to configure cast text      
    def cast_frame(self, cast):
        self.cast_text.config(state=tk.NORMAL)  # Making the text writable
        self.cast_text.delete(1.0, tk.END)  # Clearing text already present
        self.cast_text.insert(tk.END,"\nCast:\n\n" + "\n".join(cast))
        self.cast_text.config(state=tk.DISABLED)  # Making the text read-only

       
    # creating a function to get movie details
    def get_movie_details(self, movie_name):
        endpoint= '/search/movie'            # defining api endpoint for searching movies
        # constructing url for movie search
        url= f'{base}{endpoint}?api_key={api}&query={movie_name}'
        response= requests.get(url)     # making request to api 
        data= response.json()    # review the response as json 
        
        # checking if 'results' key exists
        if 'results' in data and len(data['results']) > 0:
            # Getting details of first result
            movie= data['results'][0]    
            title= movie.get('title')
            poster_path= movie.get('poster_path')
            overview= movie.get('overview')
            
            # Checking if movie title and poster are available or not
            if title and poster_path:
                # getting more details 
                movie_id= movie.get('id')
                cast_url= f'{base}/movie/{movie_id}/credits?api_key={api}'
                cast_response= requests.get(cast_url)
                cast_data= cast_response.json()
                
                # getting cast info from response
                cast= [actor['name'] for actor in cast_data.get('cast', [])]
                
                # constructing image url with the help of poster_path
                image_url= f'https://image.tmdb.org/t/p/w500/{poster_path}'
                
                # returning the retrived data
                return title, image_url, overview, cast
        # returning none if no deatails are found
        return None, None, None, None
    
    
 # Second Tab (Upcoming movies)
    def upcoming_tab(self):
        # creating a tab for upcoming movies
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text='Upcoming Releases')
        
        # Setting a background image to the tab and resizing it
        self.img2 = Image.open("pic (10).png")
        self.resized2 = self.img2.resize((980,700))          # Resizing the image to fit tab
        self.new_img2 = ImageTk.PhotoImage(self.resized2)
        ex2 = tk.Label(tab2, image = self.new_img2)
        ex2.place(x = 0, y = 0)

        # label to instruct user
        press= tk.Label(tab2, text="Click on the button to check upcoming movies",font=("Georgia",24), bg="#012D45")
        press.place(x=220, y=15)
        
        # Buttton to search for upcoming movies    
        upcoming_btn= Button(tab2, text="Show Upcoming Releases", highlightbackground="#012E46", font=("Helvetica", 17), bg="white", command=self.upcoming_releases)
        upcoming_btn.place(x=350, y=60)

        # Frame to display upcoming movies
        self.result_frame = tk.Frame(tab2, bg="#023750")
        self.result_frame.place(x=7, y=100)  
        
    def upcoming_releases(self):
        # constructing url to get upcoming movies
        upcoming_url = f"{base}movie/upcoming"
        params = {
            'api_key': api
        }
        # making a request to get upcoming movies
        response = requests.get(upcoming_url, params=params)
        data = response.json()
        # calling display_results to display upcoming movies
        self.display_results(data)
        
    # function to display result
    def display_results(self, data):
        # clearing previous results
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # displaying only four upcoming movies
        for i, movie in enumerate(data['results'][:8]):
            mov_release_date = movie.get('release_date', '')
            release_date = datetime.strptime(mov_release_date, '%Y-%m-%d').date()

            # Loading movie posters
            poster_path = movie.get('poster_path', '')
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w154/{poster_path}"
                response = requests.get(poster_url)
                # Generate a unique cache identifier based on the movie ID
                cache_identifier = f"{movie['id']}_{i}"
                poster_data = Image.open(io.BytesIO(response.content))
                poster_image = ImageTk.PhotoImage(poster_data)
                # Store the poster image with the cache identifier in a dictionary
                self.poster_images[cache_identifier] = poster_image
            else:
                # using a default image if no poster available
                poster_image = ImageTk.PhotoImage(Image.new('RGB', (160, 240), color='white'))

            # Label to displaying movie poster
            poster_label = tk.Label(self.result_frame, image=poster_image)
            poster_label.image = poster_image
            poster_label.grid(row=i // 4 * 2, column=i % 4, padx=5, pady=5)    # To display 4 images in row

            # displaying movie details right below the poster
            upcoming_mov_name = tk.Text(self.result_frame, height=2, width=33, bg="#023750", fg="white", highlightbackground="#023750")
            upcoming_mov_name.insert(tk.END, f"{movie['title']} - {release_date}\n")
            upcoming_mov_name.grid(row=(i // 3) * 2 + 1, column=i % 3, padx=5, pady=5)  

            
    # Third tab ( Recommendations)
    def recommend_tab(self):
        tab3=ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Recommendation")
        
        # Setting a background image to the tab and resizing it
        self.img3 = Image.open("pic (10).png")
        self.resized3 = self.img3.resize((980,700))          # Resizing the image to fit tab
        self.new_img3 = ImageTk.PhotoImage(self.resized3)
        ex3 = tk.Label(tab3, image = self.new_img3)
        ex3.place(x = 0, y = 0)
        
        self.genreVar= tk.StringVar()
        self.yearVar= tk.StringVar()
        
        # label to instruct user
        label_rec= tk.Label(tab3, text="Select a genre and enter year to get a recommendation.", font=("Georgia",24), bg="#012A42")
        label_rec.place(x=170, y=20)
        # Creating a dropdown and label for genres
        label_year= tk.Label(tab3, text="Select Genre:", font=("Georgia",20), bg="#012E46")
        label_year.place(x=285, y=70)
        genres= self.get_genres()
        gen_dropdown= tk.OptionMenu(tab3, self.genreVar, *genres)
        gen_dropdown.config(font=("Helvetica",17), bg="gray", fg="black")
        gen_dropdown.place(x=290, y=115)
        
        # Label and entry widget for user to enter year
        label_year= tk.Label(tab3, text="Enter Release Year:", font=("Georgia",20), bg="#012E46")
        label_year.place(x=485, y=70)
        label_year= tk.Entry(tab3, textvariable=self.yearVar, font=("Helvetica",17), width=12, bg="#E6E6E6", fg="black")
        label_year.place(x=505, y=115)
        
        # Button for getting recommendation
        recom_btn= Button(tab3, text="Get Recommendation", command=self.find_mov, font=("Helvetica",17), highlightbackground="#012E44")
        recom_btn.place(x=365, y=180)
        
        # Label to display the recommendation
        self.result_label= tk.Label(tab3, text="", font=("Georgia",16), bg="#2F5365", fg="white")
        self.result_label.place(x=340, y= 580)
        
        # Label to display recommended movie poster
        self.poster_label_recom= tk.Label(tab3, bg="#02273E")
        self.poster_label_recom.place(x=100,y=290)
        
    
    # creating a function to gey movies according to genre and release year
    def get_genres(self):
        # constructing url to get a list of genres 
        genres_url= f"{base}genre/movie/list?api_key={api}&language=en-US"
        # making request to genres api
        response= requests.get(genres_url)
        # review the response as json
        genres_data= response.json().get('genres', [])
        # retriving genre names
        genres= [genre['name'] for genre in genres_data]
        # returning genre list
        return genres
    
    def find_mov(self):
        # getting user input
        genre= self.genreVar.get()
        year= self.yearVar.get()
        # displaying error message if genre is not selected
        if not genre:
            messagebox.showerror("Error", "Error!, Please select a genre.")
            return
        # displaying error message if anything other then digit is entered
        if year and not year.isdigit():
            messagebox.showerror("Error", "Error!, Release year should be a number.")
            return
    
        # retriving a list of movies based on user input of year and genre
        movies= self.get_movies(genre, year)
        # checking if movies are found
        if movies:
            # selecting random movie from list
            mov_selected= random.choice(movies)
            title= mov_selected.get('title', 'N/A')
            synopsis= mov_selected.get('synopsis', "No synopsis available.")
            poster_path= mov_selected.get('poster_path')
            # checking if a correct poster path is available
            if poster_path:
                # constructing poster url
                poster_url= f"https://image.tmdb.org/t/p/w500{poster_path}"
                # getting  poster image
                poster_image= self.get_movie_poster(poster_url)
                # displaying movie info
                self.mov_info(title, synopsis, poster_image)
            else:
                # displaying movie info without poster
                self.mov_info(title, synopsis, None)
        else:
            # displaying a message if no movies are found 
            self.mov_info("No movies found.","", None)
            
    def get_movie_poster(self, url):
        # making request to get movie poster
        response= requests.get(url)
        # getting binary content of response
        poster_data= response.content
        
        # opening image and creating a thumbnail
        image= Image.open(io.BytesIO(poster_data))
        image.thumbnail((320, 320))      # sizing the image
        # returning the image as a PhotoImage object
        return ImageTk.PhotoImage(image=image)
    
    # function to display movie info
    def mov_info(self, title, synopsis, poster_image):
        # creating a formatted string with selected movie minfo
        upcoming_mov_name= f"Selected Movie:\nTitle: {title}\nSynopsis: {synopsis}"
        self.result_label.config(text=upcoming_mov_name)
        # checking if poster is available
        if poster_image:
            self.poster_label_recom.config(image=poster_image)
            self.poster_label_recom.image= poster_image
            self.poster_label_recom.place(x=360, y=250)
    
    # function to get movies by genre and year
    def get_movies(self, genre, year):
        # constructing url to get a movies based on year and genre
        discover_url= f"{base}discover/movie"
        params={
            'api_key': api,
            'with_genres': self.get_genres_id(genre),
            'primary_release_year': year,
            'language': 'en-US'
        }
        # making a request to get movies
        response= requests.get(discover_url, params=params)
        # review the response as json
        movies_data= response.json().get('results', [])
        # returning the movie list
        return movies_data
    
    def get_genres_id(self, genre_name):
        # constructing url to get movies genre list
        genres_url= f"{base}genre/movie/list?api_key={api}&language=en-US"
        # making a request to get genre list
        response= requests.get(genres_url)
        # review the response as json
        genre_data= response.json().get('genres',[])
        # finding specific genre id 
        for genre in genre_data:
            if genre['name']== genre_name:
                return genre['id']
            # returning None if genre is not found
        return None
    
    
    # Fourth Tab (Actors Works)
    def actor_works_tab(self):
        # creating a fourth tab to search for movies by the actors starring in it
        tab4= ttk.Frame(self.notebook)
        self.notebook.add(tab4, text="Search by Actors")
        
        # Setting a background image to the tab and resizing it
        self.img4 = Image.open("pic (10).png")
        self.resized4 = self.img4.resize((980,700))          # Resizing the image to fit tab
        self.new_img4 = ImageTk.PhotoImage(self.resized4)
        ex4 = tk.Label(tab4, image = self.new_img4)
        ex4.place(x= 0, y= 0)
        
        # Label to enter actors name
        actor_label= tk.Label(tab4, text="Enter Actors name to search for their movies:", font=("Georgia",24), bg="#012C43", fg="white")
        actor_label.place(x=220, y=25)
        
        # Entry field for user to enter actors name
        actor_entry= tk.Entry(tab4, font=("Helvetica",17), width=16)
        actor_entry.place(x=280, y=80)
        
        # Button to get movies of the actor
        actor_mov_btn= Button(tab4, text="Find", command= lambda: self.get_actor_info(actor_entry.get()), font=("Helvetica",18), highlightbackground="#012E44")
        actor_mov_btn.place(x=510,y=80)
        
        # Canvas to display upcoming movies
        self.result_canvas = tk.Canvas(tab4)
        # making the canvas invisible until button is clicked
        self.result_canvas.pack_forget()
        # setting a background image to the canvas
        self.background_image = tk.PhotoImage(file="pic (10).png") 
        # Add the background image to the Canvas
        self.result_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        
    
    # Function to get actors movies
    def get_actor_info(self, actor_name):
        # Making result canvas visible when upcoming button is clicked
        self.result_canvas.place(x=0, y=130, relwidth=1, relheight=0.9)
        # making api request to search for actor
        url= f'{base}/search/person'
        params={'api_key': api, 'query': actor_name}
        response= requests.get(url, params=params)
        
        # checking if response is successful
        if response.status_code== 200:     
            results= response.json().get('results',[])
            # checking if results are available
            if results:
                actor_id= results[0]['id']
                movies_data= self.get_actors_films(actor_id)
                self.act_info_display(movies_data)
            # if results not available then displaying an error message 
            else:
                messagebox.showerror("Not Found","Actor Not Found.\nEnter Correct Name Please.")
        # printing a message in terminal
        else:
            print("Actor Info Not Found")
            
    # function to get movies of a actor by their id
    def get_actors_films(self, actor_id):
         # making api request to search for actor by id
        url= f'{base}/person/{actor_id}/movie_credits'
        params= {'api_key': api}
        response= requests.get(url, params=params)
        # checking if response is successful 
        if response.status_code== 200:
            movies_data= response.json().get('cast',[])
            return movies_data
        # printing a message in terminal if actor not found
        else:
            print("Actor Movies Not Found")
            return[]
        
    # function to display movie info 
    def act_info_display(self, movies_data):
        self.clear_act_info()
        num_columns = 2
        # Using for loop to iterate through each movie in data
        for x, film in enumerate(movies_data, start=1):
            mov_title= film['title']
            mov_poster_path= film['poster_path']
            mov_img_url= f'https://image.tmdb.org/t/p/w500/{mov_poster_path}' if mov_poster_path else ''    # link for movie poster
            
            # Label to display movie name
            mov_label= tk.Label(self.result_canvas, text=mov_title, font=("Georgia",18), bg="#01263B")
            mov_label.grid(row=(x - 1) // num_columns * 2 + 1, column=(x - 1) % num_columns, padx=90, pady=5, sticky=tk.W)

            # displaying the movie poster
            if mov_img_url:
                try:
                    response= requests.get(mov_img_url)
                    response.raise_for_status()    # raising an error if response is unsuccessful
                    img_data= Image.open(io.BytesIO(response.content)).convert('RGB')
                    img_data.thumbnail((90,140))      # sizing the poster
                    img_photo= ImageTk.PhotoImage(img_data)
                    # label to display the result retrived from data
                    mov_img_label= ttk.Label(self.result_canvas, image=img_photo)
                    mov_img_label.image= img_photo
                    mov_img_label.grid(row=(x - 1) // num_columns * 2, column=(x - 1) % num_columns, padx=100, pady=5, sticky=tk.W)
                # if unable to get image then printing a message in terminal
                except requests.exceptions.RequestException as e:
                    print(f"Failed to get image for {mov_title}: {e}")
            # if image not found then printing a message in terminal
            else:
                print(f"No image available for {mov_title}.")
    
    # Creating a function to clear all content in tab
    def clear_act_info(self):
        for widget in self.result_canvas.winfo_children():
            widget.destroy()
            
             
# checking if script is running as main program
if __name__ == "__main__":
    root = tk.Tk()
    app = IntroWindow(root)
    # starting the gui app
    root.mainloop()