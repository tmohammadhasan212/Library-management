from pathlib import Path
dir_path = Path(__file__).parent.parent / 'dataaaa.csv'
print(dir_path.resolve().suffix)