import ast


# Function to safely evaluate string representations of lists
def parse_list_from_env(env_value):
    try:
        return ast.literal_eval(env_value)
    except (ValueError, SyntaxError):
        return []
