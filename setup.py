import pathlib
from setuptools import setup
from Cython.Build import cythonize

# 📂 Folders to cythonize in execution order
TARGET_FOLDERS = [
    "skills",
    "core",
]

# 🚫 Directories to exclude
EXCLUDE_DIRS = {
    "templates",
    "__pycache__",
    ".git",
    ".github",
    "env",
    "venv",
    ".venv",
}

# 🚫 Files to exclude
EXCLUDE_FILES = {
    "setup.py",
    "pyproject.toml",
    "README.md",
    ".env",
}


def is_valid_file(path: pathlib.Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    if path.name in EXCLUDE_FILES:
        return False
    return True


def collect_python_files(folder_name: str) -> list:
    folder_path = pathlib.Path(folder_name)

    if not folder_path.exists():
        print(f"Warning: Folder not found: {folder_name}")
        return []

    files = [
        str(p)
        for p in folder_path.rglob("*.py")
        if is_valid_file(p)
    ]

    return files


# 🔍 Collect files in configured folder order
py_files = []

for folder in TARGET_FOLDERS:
    print(f"\nScanning folder: {folder}")

    folder_files = collect_python_files(folder)

    if not folder_files:
        print(f"   No valid Python files found.")
        continue

    print(f"   Found {len(folder_files)} files")

    for f in folder_files:
        print(f"   - {f}")

    py_files.extend(folder_files)


print("\nFinal cythonization order:")
for idx, f in enumerate(py_files, start=1):
    print(f"{idx}. {f}")


setup(
    ext_modules=cythonize(
        py_files,
        compiler_directives={
            "language_level": "3",
            "boundscheck": False,
        },
        force=True,
    ),
)
