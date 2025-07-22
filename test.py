import os

f = []

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to skip unwanted directories
        dirs[:] = [
            d for d in dirs
            if d != '.venv' and d != '__pycache__' and not d.startswith('.')
        ]
        for file in files:
            # print(os.path.join(root, file))
            f.append(os.path.join(root, file))
    return f

# Example usage
print(list_files('.'))
