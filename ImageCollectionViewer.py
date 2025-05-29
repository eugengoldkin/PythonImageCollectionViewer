import os
import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk
import os


# Get the current directory of the script
current_directory = Path(__file__).parent

# Define a function to check if a file is an image based on its extension
def is_image(file_name):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    return any(file_name.lower().endswith(ext) for ext in image_extensions)

# Define the main function to process the directories and JSON files
def process_directories(start_dir):
    result = []
    # Walk through all directories starting from the given start_dir
    for root, dirs, files in os.walk(start_dir):
        json_files = [f for f in files if f.endswith('.json')]
        
        # If there's a JSON file in the directory, process it
        for json_file in json_files:
            json_path = os.path.join(root, json_file)
            
            try:
                # Open and load the content of the JSON file
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Find all image files in the same folder and sort them alphabetically
                image_files = [f for f in os.listdir(root) if is_image(f)]
                image_files.sort()  # Sort alphabetically
                
                # Add the folder path to the dictionary
                data['folder'] = root

                # Count the number of images
                size = len(image_files)
                
                # Make sure the fields are filled
                if not data.get('characters'):
                    data['characters'] = ["No Characters"]
                if not data.get('artists'):
                    data['artists'] = ["No Artists"]
                if not data.get('genre'):
                    data['genre'] = ["No Genre"]
                if not data.get('group'):
                    data['group'] = ["No Group"]

                # Update the dictionary with the list of image files and the count
                data['size'] = size
                data['files'] = image_files
                
                # Write the updated data back into the JSON file
                #with open(json_path, 'w', encoding='utf-8') as f:
                #   json.dump(data, f, ensure_ascii=False, indent=4)
                result.append(data)
                #print(f"Processed {json_file} in {root}")
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {json_file} in {root}")
            except Exception as e:
                print(f"An error occurred while processing {json_file} in {root}: {e}")
    return result

# Function to sort by date and title
def sort_by_date_and_title(data):
    return sorted(data, key=lambda x: (-datetime.strptime(x["date"], "%d.%m.%Y").timestamp(), x["title"]))

# Filter by artists
def filter_by_artists(data, artists):
    return [item for item in data if any(artist in item['artists'] for artist in artists)]

# Filter by groups
def filter_by_group(data, groups):
    return [item for item in data if any(group in item['group'] for group in groups)]

# Filter by genre
def filter_by_genre(data, genres):
    return [item for item in data if any(genre in item['genre'] for genre in genres)]

# Filter by character
def filter_by_character(data, characters):
    return [item for item in data if any(character in item['characters'] for character in characters)]

# Function to create a sorted list of unique artists
def get_sorted_artists(data):
    artists = set()  # Use a set to remove duplicates
    for item in data:
        artists.update(item["artists"])  # Add artists from each dictionary
    return sorted(artists)  # Return a sorted list of unique artists

# Function to create a sorted list of unique groups
def get_sorted_groups(data):
    groups = set()  # Use a set to remove duplicates
    for item in data:
        groups.update(item["group"])  # Add groups from each dictionary
    return sorted(groups)  # Return a sorted list of unique artists

# Function to create a sorted list of unique genres
def get_sorted_genres(data):
    genres = set()  # Use a set to remove duplicates
    for item in data:
        genres.update(item["genre"])  # Add genres from each dictionary
    return sorted(genres)  # Return a sorted list of unique genres

# Function to create a sorted list of unique characters
def get_sorted_characters(data):
    characters = set()  # Use a set to remove duplicates
    for item in data:
        characters.update(item["characters"])  # Add characters from each dictionary
    return sorted(characters)  # Return a sorted list of unique characters

def split_sorted_list_to_dict(input_list):
    # Step 1: Sort the list alphabetically
    sorted_list = sorted(input_list)

    # Step 2: Compute size of each group
    n = len(sorted_list)
    group_size = n // 3
    remainder = n % 3

    # Step 3: Split into 3 groups, distributing the remainder
    groups = {}
    start = 0
    for i in range(3):
        end = start + group_size + (1 if i < remainder else 0)
        groups[f"column{i+1}"] = sorted_list[start:end]
        start = end
        
    return groups


# Start processing from the current directory
myDict = sort_by_date_and_title(process_directories(current_directory))

#print(myDict)

artists = {
    "column1": ["Artist1", "Artist2", "Artist3"],
    "column2": ["Artist4", "Artist5", "Artist6"],
    "column3": ["Artist7", "Artist8"]
}
genre = {
    "column1": ["Genre 01", "Genre 02", "Genre 03", "Genre 04", "Genre 05"],
    "column2": ["Genre 06", "Genre 07", "Genre 08", "Genre 09", "Genre 10"],
    "column3": ["Genre 11", "Genre 12", "Genre 13", "Genre 14"]
}
character = {
    "column1": ["Character 01", "Character 02", "Character 03", "Character 04", "Character 05", "Character 06"],
    "column2": ["Character 07", "Character 08", "Character 09", "Character 10", "Character 11", "Character 12"],
    "column3": ["Character 13", "Character 14", "Character 15", "Character 16", "Character 17", "Character 18"]
}
group = {
    "column1": ["Group 01", "Group 02", "Group 03", "Group 04", "Group 05", "Group 06", "Group 07"],
    "column2": ["Group 08", "Group 09", "Group 10", "Group 11", "Group 12", "Group 13", "Group 14"],
    "column3": ["Group 15", "Group 16", "Group 17", "Group 18", "Group 19", "Group 20", "Group 21"]
}


# Globals
image_refs = []
cards_per_row = 3
current_image_index = 0
current_image_data = None  # Holds full data entry
current_fullscreen_canvas = None
current_fullscreen_photo = None

# Dark mode colors
BG_COLOR = "#2E2E2E"
BG_BUTTON_COLOR = "#1E1E1E"
FG_COLOR = "#FFFFFF"
ACTIVE_BG = "#444444"
HIGHLIGHT_BG = ACTIVE_BG
BUTTON_BG = BG_BUTTON_COLOR
CARD_ARTIST_FONT = ("Arial", 12, "bold")
CARD_ARTIST_COLOR = "#A1D0FB"
CARD_SIZE_FONT = ("Arial", 10, "bold")
CARD_SIZE_COLOR = "#FFFFFF"
CARD_SIZE_BG_COLOR = "#6B6B6B"
CARD_GENRE_FONT = ("Arial", 8)
CARD_GENRE_COLOR = "#FFFFFF"
CARD_GENRE_BG_COLOR = "#3B79C5"
CARD_GROUP_FONT = ("Arial", 8)
CARD_GROUP_COLOR = "#FFFFFF"
CARD_GROUP_BG_COLOR = BG_COLOR
CARD_CHARACTER_FONT = ("Arial", 8)
CARD_CHARACTER_COLOR = "#FFFFFF"
CARD_CHARACTER_BG_COLOR = BG_COLOR

# ===================================
#    Functions for each menu point
# ===================================

# Shows all collections in a grid
def home_action():
    """
    Shows an overview of all the picture collections in a grid with up to 30 elements.
    The function **list_action()** is called with it'S default values.

    Returns:
        None: This function only generates a view.
    """
    list_action()

# Shows collections in a grid
def list_action(dictionary = myDict, iteration_start = 0):
    """
    Shows an overview of the picture collections in a grid with up to 30 elements 
    beginning with iteration_start element of the dictionary list.

    Parameters:
        dictionary (list(dict)): A list of dictionaries containing meta data about picture collections. Defaults to myDict which contains a list of all picture collections.
        iteration_start (int): The starting index for iteration and therefor the index of the first element to be shown. Defaults to 0, which is the first element of myDict.

    Returns:
        None: This function only generates a view.
    """
    hide_all_dynamic_frames()
    list_container.pack(fill=tk.BOTH, expand=True, pady=20)
    for widget in list_container.winfo_children():
        widget.destroy()
    
    # --- Scrollable Canvas Setup ---
    canvas = tk.Canvas(list_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # --- Card Container ---
    card_container = tk.Frame(scrollable_frame, bg=BG_COLOR)
    card_container.pack(pady=20)

    iter_start = iteration_start if iteration_start < len(dictionary) else max(iteration_start-30, 0)
    iter_end = min(iter_start+30, len(dictionary))
    max_columns = 3
    row = 0
    col = 0
    for index, entry in enumerate(dictionary[iter_start:iter_end], start=iter_start):
        row = index // max_columns
        col = index % max_columns

        frame = tk.Frame(card_container, bg=ACTIVE_BG, padx=10, pady=10, width=550, height=235)
        frame.grid(row=row, column=col, padx=7, pady=7)
        # Prevent the frame from resizing to fit contents
        frame.grid_propagate(False)
        frame.pack_propagate(False)

        create_entry_card(entry, frame)

    # shows the previous 30 elements
    frame_left = tk.Frame(card_container, bg=ACTIVE_BG, padx=5, pady=5)
    frame_left.grid(row=row+1, column=0, padx=7, pady=10)
    button_left = tk.Button(
                frame_left,
                text= "Previous",
                bg=BUTTON_BG,
                fg=FG_COLOR,
                activebackground=ACTIVE_BG,
                activeforeground=FG_COLOR,
                relief=tk.FLAT,
                font=("Arial", 12),
                command=lambda: list_action(dictionary, max(iter_start - 30, 0)),
                cursor="hand2",
                width=40
            )
    button_left.pack(anchor="w")
    
    # shows which elements are currenty visible in the grid
    frame_middle = tk.Frame(card_container, bg=ACTIVE_BG, padx=5, pady=5)
    frame_middle.grid(row=row+1, column=1, padx=7, pady=10)
    tk.Label(frame_middle, text=str(iter_start+1) + " - " + str(iter_end), fg=CARD_GROUP_COLOR, 
             bg=ACTIVE_BG, font=("Arial", 14)).pack(side=tk.LEFT)

    # shows the next 30 elements
    frame_right = tk.Frame(card_container, bg=ACTIVE_BG, padx=5, pady=5)
    frame_right.grid(row=row+1, column=2, padx=7, pady=10)
    button_right = tk.Button(
                frame_right,
                text= "Next",
                bg=BUTTON_BG,
                fg=FG_COLOR,
                activebackground=ACTIVE_BG,
                activeforeground=FG_COLOR,
                relief=tk.FLAT,
                font=("Arial", 12),
                command=lambda: list_action(dictionary, iter_start + 30),
                cursor="hand2",
                width=40
            )
    button_right.pack(anchor="e")

    # --- Scroll & Keyboard Navigation ---
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_arrow_key(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-3, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(3, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    canvas.bind_all("<Up>", _on_arrow_key)
    canvas.bind_all("<Down>", _on_arrow_key)

# Shows all Genre in three columns
def genre_action():
    """
    Shows all Genre in three columns. It uses the gloabal variable **genre**, which is a dictionary with 
    the keys *column1*, *column2* and *column3* containing a third of the genre each. 
    Clicking on one of the buttons will call the function **genre_clicked(name)** which in turn should 
    show all entities of the specified genre.

    Returns:
        None: This function only generates a view.
    """
    hide_all_dynamic_frames()

    for widget in genre_container.winfo_children():
        widget.destroy()

    genre_container.pack(fill=tk.BOTH, expand=True)

    # --- Scrollable Canvas Setup ---
    canvas = tk.Canvas(genre_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(genre_container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create frame inside canvas
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    # Resize canvas content to always match canvas width for centering
    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # --- Genre Inner Frame ---
    genre_inner = tk.Frame(scrollable_frame, bg=BG_COLOR)
    genre_inner.pack(pady=20)

    # Use grid for three columns
    columns = ["column1", "column2", "column3"]

    for col_index, col_name in enumerate(columns):
        col_frame = tk.Frame(genre_inner, bg=BG_COLOR)
        col_frame.grid(row=0, column=col_index, padx=20, sticky="n")

        for item in genre.get(col_name, []):
            btn = tk.Button(
                col_frame,
                text=item,
                bg=BUTTON_BG,
                fg=FG_COLOR,
                activebackground=ACTIVE_BG,
                activeforeground=FG_COLOR,
                relief=tk.FLAT,
                font=("Arial", 12),
                command=lambda name=item: genre_clicked(name),
                cursor="hand2",
                width=40
            )
            btn.pack(pady=5, anchor="w")

    # --- Mousewheel + Keyboard Support ---
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_arrow_key(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    canvas.bind_all("<Up>", _on_arrow_key)
    canvas.bind_all("<Down>", _on_arrow_key)

# Shows all Characters in three columns
def character_action():
    """
    Shows all characters in three columns. It uses the gloabal variable **character**, which is a dictionary with 
    the keys *column1*, *column2* and *column3* containing a third of the characters each. 
    Clicking on one of the buttons will call the function **character_clicked(name)** which in turn should 
    show all entities with the specified character.

    Returns:
        None: This function only generates a view.
    """
    hide_all_dynamic_frames()

    for widget in character_container.winfo_children():
        widget.destroy()

    character_container.pack(fill=tk.BOTH, expand=True)

    # --- Scrollable Canvas Setup ---
    canvas = tk.Canvas(character_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(character_container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create frame inside canvas
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    # Resize canvas content to always match canvas width for centering
    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # --- Character Inner Frame ---
    character_inner = tk.Frame(scrollable_frame, bg=BG_COLOR)
    character_inner.pack(pady=20)

    # Use grid for three columns
    columns = ["column1", "column2", "column3"]

    for col_index, col_name in enumerate(columns):
        col_frame = tk.Frame(character_inner, bg=BG_COLOR)
        col_frame.grid(row=0, column=col_index, padx=20, sticky="n")

        for item in character.get(col_name, []):
            btn = tk.Button(
                col_frame,
                text=item,
                bg=BUTTON_BG,
                fg=FG_COLOR,
                activebackground=ACTIVE_BG,
                activeforeground=FG_COLOR,
                relief=tk.FLAT,
                font=("Arial", 12),
                command=lambda name=item: character_clicked(name),
                cursor="hand2",
                width=40
            )
            btn.pack(pady=5, anchor="w")

    # --- Mousewheel + Keyboard Support ---
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_arrow_key(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    canvas.bind_all("<Up>", _on_arrow_key)
    canvas.bind_all("<Down>", _on_arrow_key)

# Shows all Groups in three columns
def group_action():
    """
    Shows all group in three columns. It uses the gloabal variable **group**, which is a dictionary with 
    the keys *column1*, *column2* and *column3* containing a third of the groups each. 
    Clicking on one of the buttons will call the function **group_clicked(name)** which in turn should 
    show all entities of the specified group.

    Returns:
        None: This function only generates a view.
    """
    hide_all_dynamic_frames()

    for widget in group_container.winfo_children():
        widget.destroy()

    group_container.pack(fill=tk.BOTH, expand=True)

    # --- Scrollable Canvas Setup ---
    canvas = tk.Canvas(group_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(group_container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create frame inside canvas
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    # Resize canvas content to always match canvas width for centering
    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # --- Group Inner Frame ---
    group_inner = tk.Frame(scrollable_frame, bg=BG_COLOR)
    group_inner.pack(pady=20)

    # Use grid for three columns
    columns = ["column1", "column2", "column3"]

    for col_index, col_name in enumerate(columns):
        col_frame = tk.Frame(group_inner, bg=BG_COLOR)
        col_frame.grid(row=0, column=col_index, padx=20, sticky="n")

        for item in group.get(col_name, []):
            btn = tk.Button(
                col_frame,
                text=item,
                bg=BUTTON_BG,
                fg=FG_COLOR,
                activebackground=ACTIVE_BG,
                activeforeground=FG_COLOR,
                relief=tk.FLAT,
                font=("Arial", 12),
                command=lambda name=item: group_clicked(name),
                cursor="hand2",
                width=40
            )
            btn.pack(pady=5, anchor="w")

    # --- Mousewheel + Keyboard Support ---
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_arrow_key(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    canvas.bind_all("<Up>", _on_arrow_key)
    canvas.bind_all("<Down>", _on_arrow_key)

# Shows all Artists in three columns
def artist_action():
    """
    Shows all artists in three columns. It uses the gloabal variable **artists**, which is a dictionary with 
    the keys *column1*, *column2* and *column3* containing a third of the artists each. 
    Clicking on one of the buttons will call the function **artist_clicked(name)** which in turn should 
    show all entities of the specified artist.

    Returns:
        None: This function only generates a view.
    """
    hide_all_dynamic_frames()

    for widget in artist_container.winfo_children():
        widget.destroy()

    artist_container.pack(fill=tk.BOTH, expand=True)

    # --- Scrollable Canvas Setup ---
    canvas = tk.Canvas(artist_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(artist_container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create frame inside canvas
    scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)
    window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    # Resize canvas content to always match canvas width for centering
    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # --- Artist Inner Frame ---
    artist_inner = tk.Frame(scrollable_frame, bg=BG_COLOR)
    artist_inner.pack(pady=20)

    # Use grid for three columns
    columns = ["column1", "column2", "column3"]

    for col_index, col_name in enumerate(columns):
        col_frame = tk.Frame(artist_inner, bg=BG_COLOR)
        col_frame.grid(row=0, column=col_index, padx=20, sticky="n")

        for artist in artists.get(col_name, []):
            btn = tk.Button(
                col_frame,
                text=artist,
                bg=BUTTON_BG,
                fg=FG_COLOR,
                activebackground=ACTIVE_BG,
                activeforeground=FG_COLOR,
                relief=tk.FLAT,
                font=("Arial", 12),
                command=lambda name=artist: artist_clicked(name),
                cursor="hand2",
                width=40
            )
            btn.pack(pady=5, anchor="w")

    # --- Mousewheel + Keyboard Support ---
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_arrow_key(event):
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    canvas.bind_all("<Up>", _on_arrow_key)
    canvas.bind_all("<Down>", _on_arrow_key)

# Shows the Search View TODO: Improve the view with more options
def search_action():
    hide_all_dynamic_frames()
    search_container.pack(pady=20)

# =======================================
#    Filtered Views of the collections
# =======================================

# Does a search   TODO: Implement
def handle_search():
    query = search_entry.get()
    print("Search query:", query)

# Shows a list of all works of the artist
def artist_clicked(artist_name):
    """
    Shows a list of all works of the artist in a grid with up to 30 elements.
    The list **myDict** is filtered for **artist_name** and then the function 
    **list_action(dict)** is called with the filtered list as input.

    Parameters:
        artist_name (str): The name of the artist whos work the list has to be filtered for.
   
    Returns:
        None: This function only generates a view.
    """
    list_action(filter_by_artists(myDict, [artist_name]))

# Shows a list of all works of the genre
def genre_clicked(genre_name):
    """
    Shows a list of all works of the genre in a grid with up to 30 elements.
    The list **myDict** is filtered for **genre_name** and then the function 
    **list_action(dict)** is called with the filtered list as input.

    Parameters:
        genre_name (str): The name of the genre to which the picture collections have to be filtered for.
   
    Returns:
        None: This function only generates a view.
    """
    list_action(filter_by_genre(myDict, [genre_name]))

# Shows a list of all works with the character  TODO: Implement
def character_clicked(character_name):
    """
    Shows a list of all works with the character in a grid with up to 30 elements.
    The list **myDict** is filtered for **character_name** and then the function 
    **list_action(dict)** is called with the filtered list as input.

    Parameters:
        character_name (str): The name of the character for which the picture collections have to be filtered for.
   
    Returns:
        None: This function only generates a view.
    """
    list_action(filter_by_character(myDict, [character_name]))

# Shows a list of all works of the group  TODO: Implement
def group_clicked(group_name):
    print("Group selected:", group_name)

# =======================================
#      Help functions for main views
# =======================================

# Hides all dynamic frames to prevent frame overlaping
def hide_all_dynamic_frames():
    """
    Hides all dynamic frames to prevent frame overlaping.
    """
    search_container.pack_forget()
    artist_container.pack_forget()
    genre_container.pack_forget()
    character_container.pack_forget()
    group_container.pack_forget()
    list_container.pack_forget()
    detail_container.pack_forget()
    if image_container is not None:
        image_container.pack_forget()

# Create an entry card for the main view   
def create_entry_card(data, parent):
    #box = tk.Frame(list_container, bg=ACTIVE_BG, bd=1, relief=tk.RIDGE, padx=10, pady=10, width=1500, height=235)
    #box.grid(row=row, column=col, padx=10, pady=10, sticky="nw")
    #box.pack_propagate(False)  # fix size to width & height of contents

    # Load image
    img_path = os.path.join(data["folder"], data["files"][0])
    try:
        img = Image.open(img_path)
        img = img.resize((150, 225))
        photo = ImageTk.PhotoImage(img)
        image_refs.append(photo)

        img_label = tk.Label(parent, image=photo, bg=ACTIVE_BG, cursor="hand2")
        img_label.pack(side=tk.LEFT)
        img_label.bind("<Button-1>", lambda e: on_entry_click(data))
    except Exception as e:
        print(f"Image load error for {img_path}: {e}")
        placeholder = tk.Label(parent, text="No Image", width=14, height=6, bg="#444", fg="white", cursor="hand2")
        placeholder.pack(side=tk.LEFT)
        placeholder.bind("<Button-1>", lambda e: on_entry_click(data))

    # Text content
    info_frame = tk.Frame(parent, bg=ACTIVE_BG)
    info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

    title_lbl = tk.Label(info_frame, text=data["title"], font=("Arial", 14, "bold"),
                         fg=FG_COLOR, bg=ACTIVE_BG, anchor="w", cursor="hand2")
    title_lbl.pack(anchor="w")
    title_lbl.bind("<Button-1>", lambda e: on_entry_click(data))

    artist_frame = tk.Frame(info_frame, bg=ACTIVE_BG)
    artist_frame.pack(anchor="w")
    #tk.Label(artist_frame, text="Artists: ", fg=FG_COLOR, bg=ACTIVE_BG).pack(side=tk.LEFT)
    for i, artist in enumerate(data["artists"]):
        artist_text = artist
        if i < len(data["artists"]) - 1:
            artist_text += ","
        artist_lbl = tk.Label(artist_frame, text=artist_text, fg=CARD_ARTIST_COLOR, 
                              font=CARD_ARTIST_FONT, bg=ACTIVE_BG, cursor="hand2")
        artist_lbl.pack(side=tk.LEFT)
        artist_lbl.bind("<Button-1>", lambda e, name=artist: artist_clicked(name))

    size_lbl = tk.Label(info_frame, text="Size: " + str(data["size"]), fg=CARD_SIZE_COLOR, 
                        bg=CARD_SIZE_BG_COLOR, font=CARD_SIZE_FONT, anchor="w")
    size_lbl.pack(anchor="w")

    group_frame1 = tk.Frame(info_frame, bg=ACTIVE_BG)
    group_frame1.pack(anchor="w")
    tk.Label(group_frame1, text="Group: ", fg=CARD_GROUP_COLOR, bg=ACTIVE_BG, font=CARD_GROUP_FONT).pack(side=tk.LEFT)
    for i, group in enumerate(data["group"]):
        group_text = group
        if i < len(data["group"]) - 1:
            group_text += ","
        group_lbl = tk.Label(group_frame1, text=group_text, fg=CARD_GROUP_COLOR,
                             font=CARD_GROUP_FONT, bg=CARD_GROUP_BG_COLOR, cursor="hand2")
        group_lbl.pack(side=tk.LEFT)
        group_lbl.bind("<Button-1>", lambda e, name=group: group_clicked(name))

    character_frame1 = tk.Frame(info_frame, bg=ACTIVE_BG)
    character_frame1.pack(anchor="w")
    tk.Label(character_frame1, text="Characters: ", fg=CARD_CHARACTER_COLOR, bg=ACTIVE_BG, font=CARD_CHARACTER_FONT).pack(side=tk.LEFT)
    for i, character in enumerate(data["characters"]):
        character_text = character
        if i < len(data["characters"]) - 1:
            character_text += ","
        character_lbl = tk.Label(character_frame1, text=character_text, fg=CARD_CHARACTER_COLOR,
                             font=CARD_CHARACTER_FONT, bg=CARD_CHARACTER_BG_COLOR, cursor="hand2")
        character_lbl.pack(side=tk.LEFT)
        character_lbl.bind("<Button-1>", lambda e, name=character: character_clicked(name))

    genre_frame1 = tk.Frame(info_frame, bg=ACTIVE_BG)
    genre_frame1.pack(anchor="w")
    tk.Label(genre_frame1, text="Genre: ", fg=CARD_GENRE_COLOR, bg=ACTIVE_BG, font=CARD_GENRE_FONT).pack(side=tk.LEFT)
    for i, genre in enumerate(data["genre"]):
        if 2*i < len(data["genre"]):
            genre_text = genre
            if i < len(data["genre"]) - 1:
                genre_text += ","
            genre_lbl = tk.Label(genre_frame1, text=genre_text, fg=CARD_GENRE_COLOR, 
                                font=CARD_GENRE_FONT, bg=CARD_GENRE_BG_COLOR, cursor="hand2")
            genre_lbl.pack(side=tk.LEFT)
            genre_lbl.bind("<Button-1>", lambda e, name=genre: genre_clicked(name))

    genre_frame2 = tk.Frame(info_frame, bg=ACTIVE_BG)
    genre_frame2.pack(anchor="w")
    for i, genre in enumerate(data["genre"]):
        if 2*i >= len(data["genre"]):
            genre_text = genre
            if i < len(data["genre"]) - 1:
                genre_text += ","
            genre_lbl = tk.Label(genre_frame2, text=genre_text, fg=CARD_GENRE_COLOR, 
                                font=CARD_GENRE_FONT, bg=CARD_GENRE_BG_COLOR, cursor="hand2")
            genre_lbl.pack(side=tk.LEFT)
            genre_lbl.bind("<Button-1>", lambda e, name=genre: genre_clicked(name))



def on_entry_click(data):
    hide_all_dynamic_frames()
    global current_image_data
    current_image_data = data
    detail_container.pack(fill=tk.BOTH, expand=True, pady=20)

    # Clear old content
    for widget in detail_container.winfo_children():
        widget.destroy()

    # Create scrollable canvas inside detail_container
    canvas = tk.Canvas(detail_container, bg=BG_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(detail_container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG_COLOR)

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    frame_id = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # This makes sure that everything is centered
    def on_canvas_resize(event):
        x = (detail_container.winfo_width() - scroll_frame.winfo_width()) / 2
        canvas.coords(frame_id, (x, 0))
        bbox = (0, 0, detail_container.winfo_width(), scroll_frame.winfo_height())
        canvas.config(scrollregion=bbox)
    canvas.bind("<Configure>", on_canvas_resize)
    canvas.bind("<Enter>", on_canvas_resize)

    # This allows you to scroll with the Mousewheel
    def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)  # For Windows/macOS
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # For Linux
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # Main box
    main_box = tk.Frame(scroll_frame, bg=ACTIVE_BG, padx=20, pady=20)
    main_box.pack(pady=10, padx=20, fill=tk.X)

    # Left: Main image
    img_path = os.path.join(data["folder"], data["files"][0])
    filename = data["files"][0]
    try:
        img = Image.open(img_path)
        img = img.resize((200, 300))
        photo = ImageTk.PhotoImage(img)
        image_refs.append(photo)
        img_label = tk.Label(main_box, image=photo, bg=ACTIVE_BG, cursor="hand2")
        img_label.pack(side=tk.LEFT, padx=10)
        img_label.bind("<Button-1>", lambda e, f=filename: on_image_click(f))
    except Exception as e:
        print(f"Image load error for {img_path}: {e}")
        placeholder = tk.Label(main_box, text="No Image", width=25, height=10, bg="#444", fg="white")
        placeholder.pack(side=tk.LEFT, padx=10)

    # Right: Info
    info_frame = tk.Frame(main_box, bg=ACTIVE_BG)
    info_frame.pack(side=tk.LEFT, padx=20, anchor="n")

    tk.Label(info_frame, text=data["title"], font=("Arial", 16, "bold"),
             fg=FG_COLOR, bg=ACTIVE_BG).pack(anchor="w", pady=2)

    artist_frame = tk.Frame(info_frame, bg=ACTIVE_BG)
    artist_frame.pack(anchor="w")
    tk.Label(artist_frame, text="Artists: ", fg=FG_COLOR, bg=ACTIVE_BG).pack(side=tk.LEFT)
    for i, artist in enumerate(data["artists"]):
        artist_lbl = tk.Label(artist_frame, text=artist, fg="#00BFFF", bg=ACTIVE_BG, cursor="hand2")
        artist_lbl.pack(side=tk.LEFT)
        artist_lbl.bind("<Button-1>", lambda e, name=artist: artist_clicked(name))
        if i < len(data["artists"]) - 1:
            tk.Label(artist_frame, text=", ", fg=FG_COLOR, bg=ACTIVE_BG).pack(side=tk.LEFT)

    tk.Label(info_frame, text="Genre: " + ", ".join(data["genre"]),
             fg=FG_COLOR, bg=ACTIVE_BG).pack(anchor="w", pady=2)

    tk.Label(info_frame, text="Folder: " + data["folder"],
             fg=FG_COLOR, bg=ACTIVE_BG).pack(anchor="w", pady=2)

    # Mini thumbnails
    thumbs_frame = tk.Frame(scroll_frame, bg=BG_COLOR)
    thumbs_frame.pack(pady=20)

    thumbs_per_row = 8
    for i, file in enumerate(data["files"]):
        try:
            thumb_path = os.path.join(data["folder"], file)
            img = Image.open(thumb_path)
            img.thumbnail((150, 150))
            thumb_photo = ImageTk.PhotoImage(img)
            image_refs.append(thumb_photo)

            lbl = tk.Label(thumbs_frame, image=thumb_photo, bg=BG_COLOR, cursor="hand2")
            lbl.grid(row=i // thumbs_per_row, column=i % thumbs_per_row, padx=5, pady=5)
            lbl.bind("<Button-1>", lambda e, f=file: on_image_click(f))
        except Exception as e:
            print(f"Thumb load error for {file}: {e}")

def on_image_click(filename):
    global current_image_index, current_image_data

    if not current_image_data:
        return

    # Get current image index in the list
    if filename in current_image_data["files"]:
        current_image_index = current_image_data["files"].index(filename)
    else:
        return  # Filename not found

    show_fullscreen_image()

def show_fullscreen_image():
    global current_image_index, current_image_data
    global current_fullscreen_canvas, current_fullscreen_photo
    global image_container

    # Hide other frames like detail_container
    hide_all_dynamic_frames()

    # Destroy existing image_container if any
    if image_container is not None:
        image_container.destroy()

    # Create new container for fullscreen image
    image_container = tk.Frame(root, bg=BG_COLOR)  # or parent frame instead of root
    image_container.pack(fill=tk.BOTH, expand=True)

    for widget in image_container.winfo_children():
        widget.destroy()

    # --- Image Canvas ---
    canvas = tk.Canvas(image_container, bg=BG_COLOR, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    current_fullscreen_canvas = canvas

    # --- Close Button as Overlay ---
    close_button = tk.Button(
        image_container,
        text="✕",
        bg=ACTIVE_BG,
        fg=FG_COLOR,
        relief=tk.FLAT,
        font=("Arial", 18, "bold"),
        command=return_to_entry_view,
        cursor="hand2",
        bd=0,
        highlightthickness=0
    )

    # Overlay it in top-right corner with some padding
    close_button.place(relx=1.0, x=-20, y=20, anchor="ne")

    # --- Render the image ---
    def render_image():
        global current_fullscreen_photo
        image_container.update_idletasks()
        w = image_container.winfo_width()
        h = image_container.winfo_height()
        try:
            filename = current_image_data["files"][current_image_index]
            path = os.path.join(current_image_data["folder"], filename)
            img = Image.open(path)
            img.thumbnail((w, h), resample=Image.Resampling.BICUBIC)
            current_fullscreen_photo = ImageTk.PhotoImage(img)

            canvas.delete("all")
            canvas.create_image(w // 2, h // 2, image=current_fullscreen_photo)
        except:
            pass

    # Bind events
    canvas.bind("<Button-1>", lambda e: show_next_image())
    image_container.bind("<Configure>", lambda e: render_image())

    # Keyboard navigation
    canvas.focus_set()
    canvas.bind("<Right>", lambda e: show_next_image())
    canvas.bind("<Left>", lambda e: show_previous_image())
    canvas.bind("<Escape>", lambda e: return_to_entry_view())
    
    render_image()

def show_next_image():
    global current_image_index, current_image_data

    if not current_image_data:
        return

    current_image_index = (current_image_index + 1) % len(current_image_data["files"])
    show_fullscreen_image()

def show_previous_image():
    global current_image_index, current_image_data

    if not current_image_data:
        return

    current_image_index = (current_image_index - 1) % len(current_image_data["files"])
    show_fullscreen_image()

def return_to_entry_view():
    if current_image_data:
        on_entry_click(current_image_data)

# Create main window
root = tk.Tk()
root.title("Dark Mode GUI")
root.geometry("1800x900")
root.configure(bg=BG_COLOR)

# Create top menu bar as a frame
menu_frame = tk.Frame(root, bg=BG_BUTTON_COLOR, height=40)
menu_frame.pack(fill=tk.X, side=tk.TOP)

menu_inner = tk.Frame(menu_frame, bg=BG_BUTTON_COLOR)
menu_inner.pack(expand=True)

# Button style settings
button_config = {
    "bg": BG_BUTTON_COLOR,
    "fg": FG_COLOR,
    "activebackground": BG_BUTTON_COLOR,
    "activeforeground": FG_COLOR,
    "bd": 0,
    "highlightthickness": 0,
    "font": ("Arial", 12),
    "padx": 15,
    "pady": 5
}

# Add buttons to the top menu
menu_items = [
    ("Home", home_action),
    ("Artist", artist_action),
    ("Genre", genre_action),
    ("Character", character_action),
    ("Group", group_action),
    ("Search", search_action),
]

for name, action in menu_items:
    btn = tk.Button(menu_inner, text=name, command=action, **button_config)
    btn.pack(side=tk.LEFT, pady=5)

# === Search Bar ===

search_container = tk.Frame(root, bg=BG_COLOR)

search_entry = tk.Entry(search_container, font=("Arial", 14), width=40, bg="#1E1E1E", fg=FG_COLOR, 
                        insertbackground=FG_COLOR, relief=tk.FLAT)
search_entry.pack(side=tk.LEFT, ipady=8, padx=(0, 10))

search_button = tk.Button(search_container, text="Search", command=handle_search,
                          bg=ACTIVE_BG, fg=FG_COLOR, font=("Arial", 14), relief=tk.FLAT)
search_button.pack(side=tk.LEFT)

search_container.pack_forget()

# === Artist Grid ===

artist_container = tk.Frame(root, bg=BG_COLOR)
artist_container.pack_forget()

# === Genre Grid ===

genre_container = tk.Frame(root, bg=BG_COLOR)
genre_container.pack_forget()

# === Character Grid ===

character_container = tk.Frame(root, bg=BG_COLOR)
character_container.pack_forget()

# === Group Grid ===
group_container = tk.Frame(root, bg=BG_COLOR)
group_container.pack_forget()

# === Container for List View ===
list_container = tk.Frame(root, bg=BG_COLOR)
list_container.pack_forget()  # hidden by default
for i in range(cards_per_row):
    list_container.grid_columnconfigure(i, weight=1)

# === Container for Detail View ===
detail_container = tk.Frame(root, bg=BG_COLOR)
detail_container.pack_forget()  # hidden by default

# === Container for Image View ===
image_container = None

# Run the application
root.mainloop()