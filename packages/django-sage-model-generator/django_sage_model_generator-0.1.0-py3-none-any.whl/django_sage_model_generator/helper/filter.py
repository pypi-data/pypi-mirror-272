def snake_to_pascal_case(name):
    return ''.join(word.capitalize() for word in name.split('_'))