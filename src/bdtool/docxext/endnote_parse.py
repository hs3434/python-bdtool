import re

def parse_endnote_txt(file_path):
    """
    解析EndNote导出的TXT格式文件，支持多篇文献（空行分隔）
    
    参数:
        file_path: EndNote TXT文件路径
        
    返回:
        list: 包含多个字典的列表，每个字典代表一篇文献
    """
    # 用于匹配字段名的正则表达式（如 "Author: "）
    field_pattern = re.compile(r'^([\w\s\/\*]+?):\s')  # 支持带空格、/和*的字段名
    
    references = []
    current_reference = {}
    current_field = None
    current_value = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取所有行，保留空行信息
        lines = [line.rstrip('\n') for line in file]
    
    for line in lines:
        # 处理空行分隔符
        if not line.strip():  # 遇到空行
            # 如果当前有正在处理的文献
            if current_reference or current_field:
                # 保存最后一个字段
                if current_field and current_value:
                    current_reference[current_field] = ' '.join(current_value).strip()
                
                # 将当前文献添加到列表
                if current_reference:
                    references.append(current_reference)
                
                # 重置状态，准备处理下一篇文献
                current_reference = {}
                current_field = None
                current_value = []
            continue  # 跳过空行
        
        # 尝试匹配字段名（如 "Author: "）
        match = field_pattern.match(line)
        if match:
            # 如果有正在处理的字段，先保存
            if current_field and current_value:
                current_reference[current_field] = ' '.join(current_value).strip()
            
            # 提取新字段名并清理
            current_field = match.group(1).strip()
            # 提取字段值（去除字段名和冒号后的部分）
            field_value = line[match.end():].strip()
            current_value = [field_value] if field_value else []
        else:
            # 处理字段值换行的情况（继续添加到当前字段值）
            if current_field:
                current_value.append(line.strip())
    
    # 处理文件末尾没有空行的最后一篇文献
    if current_reference or current_field:
        if current_field and current_value:
            current_reference[current_field] = ' '.join(current_value).strip()
        if current_reference:
            references.append(current_reference)
    
    return references

def func(dic: dict, path: str):
    import os
    import time
    import random
    from scholarly import scholarly
    scholarly.set_retries(2)
    for key in dic:
        title = dic[key]
        delay = random.uniform(8, 12)
        time.sleep(delay)
        print(title)
        search_query = scholarly.search_pubs(title)
        pub = next(search_query)
        print(pub)
        pub_type = pub['bib'].get("type", "Journal Article") 
        with open(os.path.join(path, key + ".txt"), "w", encoding="utf-8") as file:
            file.write(f"Title: {pub['bib']['title']}\n")
            file.write(f"Author: {", ".join(pub['bib']['author'])}\n")
            file.write(f"Journal: {pub['bib']['venue']}\n")
            file.write(f"Year: {pub['bib']['pub_year']}\n\n")
    
# 使用示例
if __name__ == "__main__":
    file_path = "/home/bio-24/projects/rnaseq/input/My EndNote Library.txt"  # 替换为你的文件路径
    
    try:
        references = parse_endnote_txt(file_path)
        
        print(f"成功解析 {len(references)} 篇文献\n")
        
        # 打印每篇文献的基本信息
        for i, ref in enumerate(references, 1):
            print(f"文献 {i}:")
            print(f"标题: {ref.get('Title', '无标题')}")
            print(f"作者: {ref.get('Author', '无作者信息')}")
            print(f"期刊: {ref.get('Journal', '无期刊信息')}")
            print("---")  # 分隔线
            
    except FileNotFoundError:
        print(f"错误: 文件 '{file_path}' 不存在")
    except Exception as e:
        print(f"解析错误: {str(e)}")
