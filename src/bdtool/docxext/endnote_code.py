import random
import time
from typing import Dict, Optional

def generate_endnote_field_code(ref_dict: Dict[str, str]) -> str:
    """
    将文献字典转换为EndNote域代码格式
    
    参数:
        ref_dict: 包含文献信息的字典
        
    返回:
        str: 生成的EndNote域代码
    """
    # 文献类型映射表 (EndNote ref-type 数值)
    ref_type_map = {
        "Journal Article": "17",
        "Book": "6",
        "Book Section": "7",
        "Conference Paper": "47",
        "Thesis": "32",
        "Report": "3",
        "Web Page": "51"
    }
    
    # 获取基本字段，不存在则使用默认值
    record_num = ref_dict.get("Record Number", "0")
    author = ref_dict.get("Author", "Unknown Author")
    title = ref_dict.get("Title", "No Title")
    journal = ref_dict.get("Journal", "")
    year = ref_dict.get("Year", "")
    volume = ref_dict.get("Volume", "")
    issue = ref_dict.get("Issue", "")
    pages = ref_dict.get("Pages", "")
    
    # 确定文献类型
    ref_type_name = ref_dict.get("Reference Type", "Journal Article")
    ref_type_code = ref_type_map.get(ref_type_name, "0")
    
    # 生成foreign-keys所需的随机ID和时间戳
    timestamp = str(int(time.time()))
    random_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=32))
    
    # 构建期刊信息字符串
    periodical_info = []
    if journal:
        periodical_info.append(journal)
    if year:
        periodical_info.append(year)
    if volume:
        periodical_info.append(f"Vol {volume}")
    if issue:
        periodical_info.append(f"Iss {issue}")
    if pages:
        periodical_info.append(f"pp {pages}")
    
    periodical_text = ". ".join(periodical_info) if periodical_info else "No periodical info"
    
    # 构建域代码模板
    field_code_template = ''' ADDIN EN.CITE <EndNote><Cite>
<Author>{author}</Author>
<RecNum>{record_num}</RecNum>
<DisplayText><style face="superscript">[{record_num}]</style></DisplayText>
<record>
<rec-number>{record_num}</rec-number>
<foreign-keys>
<key app="EN" db-id="{random_id}" timestamp="{timestamp}">{record_num}</key>
</foreign-keys>
<ref-type name="{ref_type_name}">{ref_type_code}</ref-type>
<contributors>
<authors>
<author>{author}</author>
</authors>
</contributors>
<titles>
<title>{title}</title>
<secondary-title>{periodical_text}</secondary-title>
</titles>
<periodical>
<full-title>{periodical_text}</full-title>
</periodical>
<dates>
<year>{year}</year>
</dates>
<urls>
</urls>
</record>
</Cite></EndNote>'''
    
    # 替换模板中的占位符
    field_code = field_code_template.format(
        author=author,
        record_num=record_num,
        random_id=random_id,
        timestamp=timestamp,
        ref_type_name=ref_type_name,
        ref_type_code=ref_type_code,
        title=title,
        periodical_text=periodical_text,
        year=year
    )
    
    # 移除多余的空行，美化格式
    return '\n'.join([line for line in field_code.split('\n') if line.strip()])

# 使用示例
if __name__ == "__main__":
    # 示例文献字典
    example_ref = {
        "Reference Type": "Journal Article",
        "Record Number": "15",
        "Author": "Yu, G., Wang, L. G., Han, Y. and He, Q. Y.",
        "Year": "2012",
        "Title": "clusterProfiler: an R package for comparing biological themes among gene clusters",
        "Journal": "Omics",
        "Volume": "16",
        "Issue": "5",
        "Pages": "284-7",
        "DOI": "10.1089/omi.2011.0118"
    }
    
    # 生成域代码
    endnote_code = generate_endnote_field_code(example_ref)
    print("生成的EndNote域代码：")
    print(endnote_code)
    
    # 可以将结果写入文件
    # with open("endnote_code.txt", "w", encoding="utf-8") as f:
    #     f.write(endnote_code)
