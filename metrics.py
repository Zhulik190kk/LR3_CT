import os
import re

def analyze_code_metrics(directory_path):
    valid_extensions = {'.cpp', '.c', '.h', '.hpp', '.cs', '.java'}
    
    total_lines_all = 0
    empty_lines_all = 0
    comments_count_all = 0
    logical_lines_all = 0
    
    keywords_regex = re.compile(r'\b(if|else if|else|try|catch|switch|for|while|do|return|break|goto|continue|throw)\b')
    semicolon_regex = re.compile(r';')
    
    single_line_comment = re.compile(r'//.*')
    multi_line_comment_start = re.compile(r'/\*')
    multi_line_comment_end = re.compile(r'\*/')

    for root, _, files in os.walk(directory_path):
        for file in files:
            if not any(file.endswith(ext) for ext in valid_extensions):
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            except Exception as e:
                continue

            in_multiline_comment = False
            
            for line in lines:
                total_lines_all += 1
                stripped = line.strip()
                
                if not stripped:
                    empty_lines_all += 1
                    continue
                
                if in_multiline_comment:
                    comments_count_all += 1
                    if multi_line_comment_end.search(stripped):
                        in_multiline_comment = False
                    continue
                
                if multi_line_comment_start.search(stripped):
                    comments_count_all += 1
                    in_multiline_comment = True
                    if multi_line_comment_end.search(stripped):
                        in_multiline_comment = False
                    continue
                    
                if single_line_comment.search(stripped):
                    comments_count_all += 1
                    if stripped.startswith('//'):
                        continue
                
                clean_code = re.sub(r'for\s*\([^)]*\)', 'for()', stripped)
                clean_code = single_line_comment.sub('', clean_code)

                logical_lines_all += len(keywords_regex.findall(clean_code))
                logical_lines_all += len(semicolon_regex.findall(clean_code))

    allowed_empty_lines = min(empty_lines_all, int(total_lines_all * 0.25))
    physical_lines = total_lines_all - empty_lines_all + allowed_empty_lines

    comment_ratio = comments_count_all / physical_lines if physical_lines > 0 else 0

    print("="*40)
    print("РЕЗУЛЬТАТИ АНАЛІЗУ МЕТРИК КОДУ")
    print("="*40)
    print(f"Загальна кількість рядків:   {total_lines_all}")
    print(f"Кількість порожніх рядків:   {empty_lines_all}")
    print(f"Враховані порожні рядки:     {allowed_empty_lines} (не більше 25%)")
    print("-" * 40)
    print(f"Фізичні рядки коду (PSLOC):  {physical_lines}")
    print(f"Логічні рядки коду (LSLOC):  {logical_lines_all}")
    print("-" * 40)
    print(f"Рядків з коментарями (Nc):   {comments_count_all}")
    print(f"Рівень коментування (F):     {comment_ratio:.3f}")
    
    if comment_ratio >= 0.1:
        print("Статус коментування:         В НОРМІ (>= 0.1)")
    else:
        print("Статус коментування:         НЕДОСТАТНЬО (< 0.1)")
    print("="*40)

if __name__ == "__main__":
    target_directory = input("Введіть шлях до каталогу з вихідним кодом: ")
    if os.path.exists(target_directory):
        analyze_code_metrics(target_directory)
    else:
        print("Вказаний шлях не знайдено!")