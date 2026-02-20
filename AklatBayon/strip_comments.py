import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_block_comment = False
    
    is_python = filepath.endswith('.py')
    is_js_or_vue = filepath.endswith('.js') or filepath.endswith('.vue') or filepath.endswith('.css')
    
    for line in lines:
        stripped = line.lstrip()
        
        if is_python:
            if stripped.startswith('#') and not stripped.startswith('#!'):
                continue
                
        if is_js_or_vue:
            if stripped.startswith('//'):
                continue
            if stripped.startswith('/*') and '*/' in stripped:
                continue
            if stripped.startswith('/*'):
                in_block_comment = True
                continue
                
            if in_block_comment:
                if '*/' in stripped:
                    in_block_comment = False
                continue
                
            if stripped.startswith('<!--') and '-->' in stripped:
                continue

        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def run():
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ('node_modules', '.git', 'dist', '.vscode', 'staticfiles', '__pycache__')]
        for file in files:
            if file.endswith(('.py', '.js', '.vue', '.css')):
                process_file(os.path.join(root, file))

if __name__ == '__main__':
    run()
    print("Done stripping comments.")
