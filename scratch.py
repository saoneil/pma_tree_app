from resources.resources import get_connection, get_dataframe, execute_sql, execute_sproc
from sqlalchemy.sql import text

select_sql = "update temp_table set first_name = 'sean';"
select_sql_query = text(select_sql)

cn = get_connection("pma_tournaments")
execute_sql(cn, select_sql_query)