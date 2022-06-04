### ファイルの行番号を指定して、特定行を抽出
# https://python-academia.com/file-extract/
import os

dir_path = r'C:\ *--- 任意のディレクトリ ---* '
file_name = 'file1.txt'

file_path = os.path.join(dir_path, file_name)

with open(file_path) as f:
    lines = f.readlines()


print(lines[2])
# Orange 100

lines_strip = [ line.strip() for line in lines[2:5] ]
print(lines_strip)
# ['Orange 100', 'Grape 500', 'Apple 200']