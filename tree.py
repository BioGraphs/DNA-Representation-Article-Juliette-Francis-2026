import os

def print_tree(path='.', prefix='', max_depth=2, depth=0):
    if depth > max_depth:
        return
    entries = sorted(e for e in os.listdir(path) if not e.startswith('.') and e not in ('__pycache__',))
    for i, entry in enumerate(entries):
        connector = '└── ' if i == len(entries) - 1 else '├── '
        print(prefix + connector + entry)
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            extension = '    ' if i == len(entries) - 1 else '│   '
            print_tree(full_path, prefix + extension, max_depth, depth + 1)

print_tree('.')