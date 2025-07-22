#Importing the necessary Libraries
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
#importing the matplotlib for plotting
import matplotlib.pyplot as plt

#Defining the function to execute the SQL Query
def execute_sql(db: Session, sql_query: str) -> List[Dict[str, Any]]:

    try:
        result = db.execute(text(sql_query))

        rows = result.fetchall()
        if rows:
            columns = result.keys()
            rows_as_dicts = [dict(zip(columns, row)) for row in rows]
            return rows_as_dicts
        else:
            return [{"message": "Query executed successfully, no data returned", "rows_affected": len(rows)}]
    except Exception as error:
        print(f"Error executing SQL Query: {error}")
        print(f"Problematic Query: {sql_query}")
        return [{"error":str(error), "query":sql_query}]

#Defining the function to visualize the result    
def generate_img(result, graph_type="bar"):
    data = list(result)

    if not data:
        print("No data to visualize")
        return
    
    columns = list(data[0].keys())
    x = [row[columns[0]] for row in data]
    y = [row[columns[1]] for row in data]

    plt.figure(figsize=(8,4))

    if graph_type=="bar":
        plt.bar(x,y,color='skyblue')
    elif graph_type=="line":
        plt.plot(x,y,marker='o')
    elif graph_type=="pie":
        plt.pie(y,labels=x,autopct="%1.1f%%")

    plt.title(f"{graph_type.capitalize()} Chart of {columns[1]} by {columns[0]}")
    plt.xlabel(columns[0])
    plt.ylabel(columns[1])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()