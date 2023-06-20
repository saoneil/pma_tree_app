import os
import pandas as pd
import urllib, urllib.parse
import mysql.connector as sql
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from resources.resources import get_connection, get_dataframe, execute_sql, execute_sproc


mysql_host = os.environ.get('mysql_host')
mysql_user = os.environ.get('mysql_user')
mysql_pass = os.environ.get('mysql_pass')

## setting a global df so that we can pass the param into the completion function
global current_filtered_df, current_event_filter
current_filtered_df = pd.DataFrame()
current_event_filter = ""

def find_event_value(event_name:str):
    ## find the event name as it appears in the DB
    event_dict = {
    "Individual Patterns":"individual_patterns",
    "Individual Sparring":"individual_sparring",
    "Individual Special Technique":"individual_special_technique",
    "Individual Power Test":"individual_power_test",
    "Team Pre-Arranged Sparring":"team_prearranged_sparring",
    "Team Patterns":"team_patterns",
    "Team Sparring":"team_sparring",
    "Team Special Technique":"team_special_technique",
    "Team Power Test":"team_power_test",
    "1":"1",
    "athlete":"athlete"
    }
    for key in event_dict:
        if event_name in key:
            return event_dict[key]
def return_grid():
    ## returns the entire temp table
    grid_df = get_dataframe(get_connection("pma_tournaments"), "select * from temp_table;")
    return grid_df
def filter_grid(
    event_name,
    event_name_complete,
    gender,
    black_belt,
    gup_dan,
    height_min,
    height_max,
    weight_min,
    weight_max,
    age_min,
    age_max,
    team,
    exclude_ids
    ):
    
    ## find the proper name of the event from the dropdown selection
    sql_event_name1 = find_event_value(event_name)
    sql_event_name2 = find_event_value(event_name_complete)

    ## truncate the temp_table
    schema_name = "pma_tournaments"
    dburi = f'mysql://{mysql_user}:{urllib.parse.quote(mysql_pass)}@{mysql_host}/{schema_name}' # type: ignore
    db = create_engine(dburi)
    con1 = db.connect()
    table_name = "temp_table"
    truncate_query = text(f"TRUNCATE TABLE {table_name}")
    con1.execute(truncate_query)
    con1.commit()
    
    ## insert into the temp table using the filter criteria passed into this function
    sql_filter_main_table = f"""
    INSERT INTO temp_table
    SELECT * FROM registration_data_raw
    where
    {sql_event_name1} = 1   ## event selector
    and {sql_event_name2}_complete = 0   ## event completion selector
    and gender in ("{gender}")
    and black_belt in ({black_belt})
    and gup_dan in ({gup_dan})
    and height between {height_min} and {height_max}
    and weight between {weight_min} and {weight_max}
    and ROUND(((TO_DAYS(NOW()) - TO_DAYS(`registration_data_raw`.`date_of_birth`)) / 365),1) between {age_min} and {age_max}
    and team like "%{team}%"
    and id not in({exclude_ids})
    ;
    """
    #print(sql_filter_main_table)
    schema_name = "pma_tournaments"
    dburi = f'mysql://{mysql_user}:{urllib.parse.quote(mysql_pass)}@{mysql_host}/{schema_name}' # type: ignore
    db = create_engine(dburi)
    con2 = db.connect()
    insert_query = text(sql_filter_main_table)
    con2.execute(insert_query)
    con2.commit()

    #set the global grid instance and event name + return the df
    current_filtered_df = return_grid()
    current_event_filter = sql_event_name1
def mark_event_complete(event:str, id_list:list):
    for id in id_list:
        update_sql = f"""
        update registration_data_raw
        set {event}_complete = 1
        where id = {id}
        """
        execute_sql(get_connection("pma_tournaments"), update_sql)
def reset_sql_start_over():
    ## insert into the temp table using the filter criteria passed into this function
    start_over_sql = f"""
    update registration_data_raw
    set
    individual_patterns_complete = 0,
    individual_sparring_complete = 0,
    individual_special_technique_complete = 0,
    individual_power_test_complete = 0,
    team_prearranged_sparring_complete = 0,
    team_patterns_complete = 0,
    team_sparring_complete = 0,
    team_special_technique_complete = 0,
    team_power_test_complete = 0
    """
    schema_name = "pma_tournaments"
    dburi = f'mysql://{mysql_user}:{urllib.parse.quote(mysql_pass)}@{mysql_host}/{schema_name}' # type: ignore
    db = create_engine(dburi)
    con = db.connect()
    insert_query = text(start_over_sql)
    con.execute(insert_query)
    con.commit()
