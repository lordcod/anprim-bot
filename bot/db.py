
databases = {}

def get_table(table_name: str) -> dict:
    global databases
    if table_name not in databases:
        databases[table_name] = {}
    
    return databases[table_name]

def get(table_name: str, key: int|str) -> any:
    table = get_table(table_name)
    return table.get(key)

def set(table_name: str, key: int|str, value: any) -> None:
    table = get_table(table_name)
    table[key] = value
