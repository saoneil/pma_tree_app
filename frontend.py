import tkinter as tk
from tkinter import ttk
import pandas as pd
import backend
import tree_logic
import xlsx_to_pdf


def update_gup_dan_options():
    black_belt = black_belt_combobox.get()
    if black_belt == "Black Belts":
        gup_dan_combobox['values'] = ('1 - 1st Dan', '2 - 2nd Dan', '3 - 3rd Dan', '4 - 4-6th Dan')
    elif black_belt == "All":
        gup_dan_combobox['values'] = ['']
    else:
        gup_dan_combobox['values'] = (
            '', '10 - White Belt', '9 - Yellow Stripe', '8 - Yellow Belt', '7 - Green Stripe', '6 - Green Belt',
            '5 - Blue Stripe', '4 - Blue Belt', '3 - Red Stripe', '2 - Red Belt', '1 - Black Stripe'
        )
def search():
    event_name_adj,event_name_complete_adj,gender_adj,black_belt_adj,gup_dan_adj,height_min_adj,height_max_adj,weight_min_adj,weight_max_adj,age_min_adj,age_max_adj,team_adj,exclude_ids_adj = collect_search_params()
    backend.filter_grid(event_name_adj,event_name_complete_adj,gender_adj,black_belt_adj,gup_dan_adj,height_min_adj,height_max_adj,weight_min_adj,weight_max_adj,age_min_adj,age_max_adj,team_adj,exclude_ids_adj)
    df = backend.return_grid()
    display_data(df)
def clear_filters():
    event_combobox.set('')
    gender_combobox.set('')
    height_min_entry.delete(0, 'end')
    height_max_entry.delete(0, 'end')
    weight_min_entry.delete(0, 'end')
    weight_max_entry.delete(0, 'end')
    age_min_entry.delete(0, 'end')
    age_max_entry.delete(0, 'end')
    team_entry.delete(0, 'end')
    exclude_ids_entry.delete(0, 'end')
    black_belt_combobox.set('')
    gup_dan_combobox.set('')
def display_data(data):
    # save the current df to the global variable, print for debugging
    backend.current_filtered_df = data
    #print(backend.current_filtered_df)

    for widget in data_frame_area.winfo_children():
        widget.destroy()

    # Create vertical scrollbar
    y_scrollbar = ttk.Scrollbar(data_frame_area, orient="vertical")
    y_scrollbar.pack(side="right", fill="y")

    # Create horizontal scrollbar
    x_scrollbar = ttk.Scrollbar(data_frame_area, orient="horizontal")
    x_scrollbar.pack(side="bottom", fill="x")

    table = ttk.Treeview(
        data_frame_area,
        yscrollcommand=y_scrollbar.set,  # Link vertical scrollbar
        xscrollcommand=x_scrollbar.set,  # Link horizontal scrollbar
        show="headings"  # Hide the default index column
    )
    table['columns'] = list(data.columns)

    for col in list(data.columns):
        table.column(col, width=100)
        table.heading(col, text=col)

    for index, row in data.iterrows():
        table.insert('', 'end', values=list(row))

    table.pack(fill='both', expand=True)

    # Configure scrollbars
    y_scrollbar.config(command=table.yview)
    x_scrollbar.config(command=table.xview)
def collect_search_params():
    event_name = event_combobox.get()
    gender = gender_combobox.get()
    black_belt = black_belt_combobox.get()
    gup_dan = gup_dan_combobox.get()
    height_min = height_min_entry.get()
    height_max = height_max_entry.get()
    weight_min = weight_min_entry.get()
    weight_max = weight_max_entry.get()
    age_min = age_min_entry.get()
    age_max = age_max_entry.get()
    team = team_entry.get()
    exclude_ids = exclude_ids_entry.get()
    
    event_name_adj = event_name if event_name != "" else "1"
    event_name_complete_adj = "athlete" if event_name == "" else event_name
    gender_adj = "M" if gender == "Male" else "F" if gender == "Female" else 'M", "F'
    black_belt_adj = "0" if black_belt == "Color Belts" else "1" if black_belt == "Black Belts" else "0,1"
    gup_dan_adj = gup_dan[0] if gup_dan != "" else "1,2,3,4,5,6,7,8,9,10"
    height_min_adj = height_min if height_min != "" else 0
    height_max_adj = height_max if height_max != "" else 1000
    weight_min_adj = weight_min if weight_min != "" else 0
    weight_max_adj = weight_max if weight_max != "" else 1000
    age_min_adj = age_min if age_min != "" else 0
    age_max_adj = age_max if age_max != "" else 1000
    team_adj = team if team != "" else ""
    exclude_ids_adj = exclude_ids if exclude_ids != "" else 0

    return event_name_adj,event_name_complete_adj,gender_adj,black_belt_adj,gup_dan_adj,height_min_adj,height_max_adj,weight_min_adj,weight_max_adj,age_min_adj,age_max_adj,team_adj,exclude_ids_adj
def collect_event_param():
    event_name = event_combobox.get()
    event_name_adj = event_name if event_name != "" else "1"
    return event_name_adj
def build_xlsx_trees():
    backend.current_event_filter = backend.find_event_value(collect_event_param())
    tree_logic.generate_xlsx_files()


root = tk.Tk()
root.title("PMA - Tournament App")
root.geometry('1500x700')  # Set the default window size

# Create the main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Create the search panel on the left side
search_panel = ttk.Frame(main_frame, width=200)
search_panel.pack(side='left', fill='y', padx=(0, 10))

search_label = ttk.Label(search_panel, font = 'Verdana 15 bold underline', text="Search Panel")
search_label.pack(pady=(10, 15))

# Event
event_label = ttk.Label(search_panel, text="Event:")
event_label.pack()
event_combobox = ttk.Combobox(search_panel, values=[
    "",
    "Individual Patterns",
    "Individual Sparring",
    "Individual Special Technique",
    "Individual Power Test",
    "Team Pre-Arranged Sparring",
    "Team Patterns",
    "Team Sparring",
    "Team Special Technique",
    "Team Power Test"
], width=30)
event_combobox.pack(pady=(0, 10))

# Gender
gender_label = ttk.Label(search_panel, text="Gender:")
gender_label.pack()
gender_combobox = ttk.Combobox(search_panel, values=["", "Male", "Female"], width=10)
gender_combobox.pack(pady=(0, 10))

# Height
height_label = ttk.Label(search_panel, text="Height:")
height_label.pack()
height_frame = ttk.Frame(search_panel)
height_frame.pack(pady=(0, 10))

height_min_label = ttk.Label(height_frame, text="Min:")
height_min_label.pack(side="left")
height_min_entry = ttk.Entry(height_frame, width=7)
height_min_entry.pack(side="left")

height_max_label = ttk.Label(height_frame, text="Max:")
height_max_label.pack(side="left", padx=(10, 0))
height_max_entry = ttk.Entry(height_frame, width=7)
height_max_entry.pack(side="left")

# Weight
weight_label = ttk.Label(search_panel, text="Weight:")
weight_label.pack()
weight_frame = ttk.Frame(search_panel)
weight_frame.pack(pady=(0, 10))

weight_min_label = ttk.Label(weight_frame, text="Min:")
weight_min_label.pack(side="left")
weight_min_entry = ttk.Entry(weight_frame, width=7)
weight_min_entry.pack(side="left")

weight_max_label = ttk.Label(weight_frame, text="Max:")
weight_max_label.pack(side="left", padx=(10, 0))
weight_max_entry = ttk.Entry(weight_frame, width=7)
weight_max_entry.pack(side="left")

# Age
age_label = ttk.Label(search_panel, text="Age:")
age_label.pack()
age_frame = ttk.Frame(search_panel)
age_frame.pack(pady=(0, 10))

age_min_label = ttk.Label(age_frame, text="Min:")
age_min_label.pack(side="left")
age_min_entry = ttk.Entry(age_frame, width=7)
age_min_entry.pack(side="left")

age_max_label = ttk.Label(age_frame, text="Max:")
age_max_label.pack(side="left", padx=(10, 0))
age_max_entry = ttk.Entry(age_frame, width=7)
age_max_entry.pack(side="left")

# Team
team_label = ttk.Label(search_panel, text="Team:")
team_label.pack()
team_entry = ttk.Entry(search_panel, width=30)
team_entry.pack(pady=(0, 10))

# Black Belt
rank_label = ttk.Label(search_panel, text="Rank (Belt Color, Gup/Dan):")
rank_label.pack(pady=(5, 0))
rank_frame = ttk.Frame(search_panel)
rank_frame.pack(pady=(0, 10))

black_belt_label = ttk.Label(rank_frame, text="Belt:", font = "Verdana 8")
black_belt_label.pack(side="left")
black_belt_combobox = ttk.Combobox(rank_frame, values=["", "Black Belts", "Color Belts"], state="readonly", width=7)
black_belt_combobox.pack(side="left")

# Gup/Dan
gup_dan_label = ttk.Label(rank_frame, text="#:", font = "Verdana 8")
gup_dan_label.pack(side="left", padx=(10, 0))
gup_dan_combobox_var = tk.StringVar()
gup_dan_combobox = ttk.Combobox(rank_frame, state="readonly", textvariable=gup_dan_combobox_var, width=15)
gup_dan_combobox.pack(side="left")

# Bind the lambda function to the combobox
black_belt_combobox.bind("<<ComboboxSelected>>", lambda event: update_gup_dan_options())

# Exclude IDs
exclude_ids_label = ttk.Label(search_panel, text="Exclude IDs (e.g. 1,2,5):")
exclude_ids_label.pack()
exclude_ids_entry = ttk.Entry(search_panel, width=20)
exclude_ids_entry.pack(pady=(0, 10))

# Search Button
search_button = ttk.Button(search_panel, text="Search", command=search)
search_button.pack(pady=(10, 0))
clear_button = ttk.Button(search_panel, text="Clear", command=clear_filters)
clear_button.pack(pady=(5, 0))

# Horizontal Line
horizontal_line = ttk.Separator(search_panel, orient='horizontal')
horizontal_line.pack(fill='x', pady=10)

# Button Section
button_section = ttk.Frame(search_panel)
button_section.pack()

# Generate XLSX Tree Button
generate_xlsx_button = ttk.Button(button_section, text="Generate XLSX Tree", command=build_xlsx_trees)
generate_xlsx_button.pack(side='left', padx=5)

# Convert Files to PDF Button
convert_pdf_button = ttk.Button(button_section, text="Convert Files to PDF", command=xlsx_to_pdf.run_script)
convert_pdf_button.pack(side='left', padx=5)

# Reset All Entries Button
reset_entries_button = ttk.Button(button_section, text="Reset All Entries", command=backend.reset_sql_start_over)
reset_entries_button.pack(side='left', padx=5)

# Create the data frame area on the right side
data_frame_area = ttk.Frame(main_frame)
data_frame_area.pack(side='right', fill='both', expand=True)

## call the update options function intially to set the options for the default value
update_gup_dan_options()
# Bind the lambda function to the combobox
black_belt_combobox.bind("<<ComboboxSelected>>", lambda event: update_gup_dan_options())


#########################
#########################
# INTIIAL GRID LOAD
#########################
#########################
df = backend.return_grid()
display_data(df)



root.mainloop()