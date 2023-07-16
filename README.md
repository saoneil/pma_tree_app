****
# Files
Save the files to a local folder. Note that the **SQLAlchemy** implementation uses a personal library that connects to the database using the "get_session" and "create_engine" methods. The only use of the SQLAlchemy library is to return pandas.Dataframe objects and execute/commit SQL queries. If the end result of your implementation is the same, there should be no issues.


# Description
The purpose of the app is to create .xlsx and .pdf files of tournament draws simply and quickly. The search panel allows the user to filter the tournament entries based on a number of criteria including **event, gender, height, weight, age, team, belt and rank**. It also allows you to specifically exclude a record from the returned grid. You can then create the actual tree files by clicking buttons in the lower left part of the screen.


# Usage
### Setting Up SQL
The app requires two tables, **tournament_schedule** and  **temp_table** in a SQL schema called **pma_tournaments**, by default. The MyQL object descriptions are in the **sql_objects** folder. The entries from your tournament should be inserted manually into the database - most of the information is self explanatory, the fields called **<event_name>_complete** should be inserted **=0** by default.
### Creating .xlsx files
Once the SQL database is set up and the method of connection is established, you can run the **frontend.py** script, which will run the GUI for the app. From here, you can use the search panel to limit the records that are returned in the grid. Once you have a "division" set within the grid, you can click the **Generate XLSX Tree** button, which will prompt the user to select a file location. Once selected, see the "Technical Section" below for a description of how exactly the program works. Once the file is saved, those records will be removed from future search grids. Once all the desired trees are created, the user can use the **Convert Files to PDF** which will popup another tkinter window. The new window allows the user to select a number of files to stage for conversion. Once selected from the file dialog, the file names will be displayed in the secondary window. You can then choose to reset all the file names, or convert them. Once the **Convert Files** button is clicked, you'll be prompted for a save location for the pdf versions of the file.


# Technical Description of Tree Logic
The tree creation portion of the script works as follows: <br>
1) The temp_table stores the currently diplayed/filtered version of the entire grid.
2) When the **Generate XLSX Tree** button is clicked, all the records are in the temp_table are processed to determine how many records there are, and how many "bye" entries must be inserted to result in a division list that is a perfect power of 2 (**2^n**). This will be the total division list.
3) Once the total division list is generated, the entries will be grouped by their team (club) and randomly ordered so that the team being assigned the bye draws will be random.
4) The program then opens a copy of the appropriate template, and prints the records from the total division list into the appropriate positions within the document (including advancing the bye rounds), then prompts the user to save that file.
5) The **<event_name>_complete** fields are stamped **=1** when a file is created with those specific records so that those records cannot be searched again (for a specific event).