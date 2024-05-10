import re

def extract_tables_and_aliases(query):
    # Normalize the query to simplify processing
    query = query.upper().replace('\n', ' ').replace('\t', ' ')
    
    # Use regex to find table names and aliases
    results = []
    # Define regex patterns for FROM/JOIN clauses, capturing table names and aliases
    pattern = re.compile(r'\b(?:FROM|JOIN)\b\s+(\w+)\s+(?:AS\s+(\w+)|(\w+))?\s*(?=(?:ON|LEFT JOIN|JOIN|WHERE|\bGROUP\b|\bHAVING\b|\bORDER\b|$))', re.IGNORECASE)
    matches = pattern.findall(query)
    for match in matches:
        table_name, alias1, alias2 = match
        # Determine the alias based on the matched groups
        alias = alias1 if alias1 else alias2
        # If alias is not provided, use an empty string
        results.append({"Table Name": table_name, "Alias": alias if alias else ''})
    
    # Additional step to remove aliases that are used in subqueries
    subquery_aliases = re.findall(r'\b(?:AS\s+)?(\w+)\s*$', query, re.IGNORECASE | re.MULTILINE)
    results = [res for res in results if res['Alias'] not in subquery_aliases]
    
    return results
