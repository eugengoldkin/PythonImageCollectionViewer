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
    return sorted(data, key=lambda x: (datetime.strptime(x["date"], "%d.%m.%Y"), x["title"]))

# Filter by artists
def filter_by_artists(data, artists):
    return [item for item in data if any(artist in item['artists'] for artist in artists)]

# Filter by genre
def filter_by_genre(data, genres):
    return [item for item in data if any(genre in item['genre'] for genre in genres)]

# Function to create a sorted list of unique artists
def get_sorted_artists(data):
    artists = set()  # Use a set to remove duplicates
    for item in data:
        artists.update(item["artists"])  # Add artists from each dictionary
    return sorted(artists)  # Return a sorted list of unique artists

# Function to create a sorted list of unique genres
def get_sorted_genres(data):
    genres = set()  # Use a set to remove duplicates
    for item in data:
        genres.update(item["genre"])  # Add genres from each dictionary
    return sorted(genres)  # Return a sorted list of unique genres

# Start processing from the current directory
myDict = process_directories(current_directory)

#print(myDict)

artists = {
    "column1": ["Artist1", "Artist2", "Artist3"],
    "column2": ["Artist4", "Artist5", "Artist6"],
    "column3": ["Artist7", "Artist8"]
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



# Functions for each menu point
def home_action():
    list_action()

def list_action(dictionary = myDict):
    hide_all_dynamic_frames()
    list_container.pack(fill=tk.BOTH, expand=True, pady=20)
    for widget in list_container.winfo_children():
        widget.destroy()
    
    for index, item in enumerate(dictionary):
        row = index // cards_per_row
        col = index % cards_per_row
        create_entry_card(item, row, col)

# Shows all Genre in three columns
def genre_action():
    hide_all_dynamic_frames()
    print("Genre clicked")

# Shows all Characters in three columns
def character_action():
    hide_all_dynamic_frames()
    print("Character clicked")

# Shows all Groups in three columns
def group_action():
    hide_all_dynamic_frames()
    print("Group clicked")

# Shows all Artists in three columns
def artist_action():
    hide_all_dynamic_frames()
    artist_container.pack(fill=tk.BOTH, expand=True, pady=20)


def search_action():
    hide_all_dynamic_frames()
    search_container.pack(pady=20)
    print("Search clicked")

def handle_search():
    query = search_entry.get()
    print("Search query:", query)

def artist_clicked(artist_name):
    print("Artist selected:", artist_name)

def hide_all_dynamic_frames():
    search_container.pack_forget()
    artist_container.pack_forget()
    list_container.pack_forget()
    detail_container.pack_forget()
    if image_container is not None:
        image_container.pack_forget()
    
def create_entry_card(data, row, col):
    box = tk.Frame(list_container, bg=ACTIVE_BG, bd=1, relief=tk.RIDGE, padx=10, pady=10, width=1500, height=235)
    box.grid(row=row, column=col, padx=10, pady=10, sticky="nw")
    box.pack_propagate(False)  # fix size to width & height of contents

    # Load image
    img_path = os.path.join(data["folder"], data["files"][0])
    try:
        img = Image.open(img_path)
        img = img.resize((150, 225))
        photo = ImageTk.PhotoImage(img)
        image_refs.append(photo)

        img_label = tk.Label(box, image=photo, bg=ACTIVE_BG, cursor="hand2")
        img_label.pack(side=tk.LEFT)
        img_label.bind("<Button-1>", lambda e: on_entry_click(data))
    except Exception as e:
        print(f"Image load error for {img_path}: {e}")
        placeholder = tk.Label(box, text="No Image", width=14, height=6, bg="#444", fg="white", cursor="hand2")
        placeholder.pack(side=tk.LEFT)
        placeholder.bind("<Button-1>", lambda e: on_entry_click(data))

    # Text content
    info_frame = tk.Frame(box, bg=ACTIVE_BG)
    info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

    title_lbl = tk.Label(info_frame, text=data["title"], font=("Arial", 14, "bold"),
                         fg=FG_COLOR, bg=ACTIVE_BG, anchor="w", cursor="hand2")
    title_lbl.pack(anchor="w")
    title_lbl.bind("<Button-1>", lambda e: on_entry_click(data))

    artist_frame = tk.Frame(info_frame, bg=ACTIVE_BG)
    artist_frame.pack(anchor="w")
    tk.Label(artist_frame, text="Artists: ", fg=FG_COLOR, bg=ACTIVE_BG).pack(side=tk.LEFT)
    for i, artist in enumerate(data["artists"]):
        artist_lbl = tk.Label(artist_frame, text=artist, fg="#00BFFF", bg=ACTIVE_BG, cursor="hand2")
        artist_lbl.pack(side=tk.LEFT)
        artist_lbl.bind("<Button-1>", lambda e, name=artist: artist_clicked(name))
        if i < len(data["artists"]) - 1:
            tk.Label(artist_frame, text=", ", fg=FG_COLOR, bg=ACTIVE_BG).pack(side=tk.LEFT)

    genre_lbl = tk.Label(info_frame, text="Genre: " + ", ".join(data["genre"]),
                         fg=FG_COLOR, bg=ACTIVE_BG, anchor="w")
    genre_lbl.pack(anchor="w")

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
    frame_id =canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
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
root.geometry("1600x800")
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

# Inner frame to hold columns and center them
artist_inner = tk.Frame(artist_container, bg=BG_COLOR)
artist_inner.pack(side=tk.TOP, pady=20)

# Create 3 columns
for i, column in enumerate(["column1", "column2", "column3"]):
    col_frame = tk.Frame(artist_inner, bg=BG_COLOR)
    col_frame.grid(row=0, column=i, padx=20, sticky="n")

    for artist in artists[column]:
        btn = tk.Button(
            col_frame,
            text=artist,
            command=lambda name=artist: artist_clicked(name),
            bg="#1E1E1E",
            fg=FG_COLOR,
            activebackground=ACTIVE_BG,
            activeforeground=FG_COLOR,
            font=("Arial", 12),
            relief=tk.FLAT,
            width=40,
            pady=5
        )
        btn.pack(pady=5)

artist_container.pack_forget()

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