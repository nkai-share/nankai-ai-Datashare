import os
import urllib.parse

EXCLUDE_DIRS = {'.git', '.github', 'docs', 'assets', '.vscode', 'node_modules', '__pycache__'}
EXCLUDE_FILES = {
    '.nojekyll',
    'README.md',
    'SUMMARY.md',
    '_navbar.md',
    '_sidebar.md',
    'generate_sidebar.py',
    'tempCodeRunnerFile.py',
}
SIDEBAR_PATH = '_sidebar.md'

def generate_sidebar():
    sidebar_content = [
        "* [🏠 首页](/) \n",
    ]
    folder_count = 0
    file_count = 0
    
    for root, dirs, files in os.walk('.', topdown=True):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.'))
        rel_path = os.path.relpath(root, '.')
        if rel_path == '.': continue
        level = rel_path.count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root)
        sidebar_content.append(f"{indent}* **{folder_name}**\n")
        folder_count += 1
        
        for file in sorted(files):
            if file in EXCLUDE_FILES or file.startswith('.'): continue
            ext = os.path.splitext(file)[1].lower()
            raw_path = os.path.join(rel_path, file).replace('\\', '/')
            url_path = urllib.parse.quote(raw_path)
            
            if ext != '.md':
                sidebar_content.append(f"{indent}  * [{file}]({url_path} ':ignore')\n")
            else:
                sidebar_content.append(f"{indent}  * [{file}]({url_path})\n")
            file_count += 1

    with open(SIDEBAR_PATH, 'w', encoding='utf-8') as f:
        f.writelines(sidebar_content)
    print(f"OK: sidebar updated with {folder_count} folders and {file_count} files.")

if __name__ == "__main__":
    generate_sidebar()
