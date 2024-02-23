

snowflake_prompt_template = """ 
Given an input question, first create a syntactically correct snowflake query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most 5 results. You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Be very strict about the syntax of the sql query. remember the following
1.If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
4. Make sure to generate a single snowflake sql code, not multiple.
5. Make sure to use the correct table name in the query.
7. take every step to ensure that the query does not make too big data pull.
8. be care with queries that asks for all data from a table. In those cases, you should limit the number of results to 10.
Some optional details can be included in the following section parse them 
from between '<<' and '>>'  
database name: <<db_name>>
schema name: <<schema_name>>  

in general sowflake has a hierarchy structure which is described below
database -> schema -> table -> column
 


Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Use the context provided to parse the table information:
Context:{context}

Question: {question}
"""

