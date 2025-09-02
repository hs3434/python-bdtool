from __future__ import annotations
from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT


def remove_existing_relationship(doc, rel_type):
    """
    删除文档中指定类型的现有关联（避免与模板关联冲突）
    :param doc: 目标文档（docx.Document 对象）
    :param rel_type: 关联类型（如 RT.STYLES、RT.NUMBERING）
    """
    # 获取文档的部件关系集合
    rels = doc._part.rels
    # 筛选并删除指定类型的关联
    rel_ids_to_remove = [rel_id for rel_id, rel in rels.items() if rel.reltype == rel_type]
    for rel_id in rel_ids_to_remove:
        del rels[rel_id]


def use_template(template_file):
    """
    基于模板创建新文档，复用模板的所有核心部件（样式、编号、字体、脚注、尾注等）
    :param template_file: 模板文件路径（.docx）
    :return: 继承所有模板部件的新文档（docx.Document 对象）
    """
    # 1. 加载模板文档和创建新文档
    template = Document(template_file)
    new_doc = Document()  # 新文档默认包含基础部件，需替换为模板的部件

    # 3. 关联模板的核心部件（按优先级排序，确保格式一致性）
    part_mapping = [
        # (模板部件属性名, 关联类型, 可选：是否必选)
        ("_styles_part", RT.STYLES, True),          # 样式部件（核心，控制字体/段落样式）
        ("numbering_part", RT.NUMBERING, True),     # 编号部件（控制列表编号格式）
        ("font_table_part", RT.FONT_TABLE, False),  # 字体表部件（控制文档中使用的字体）
        ("footnotes_part", RT.FOOTNOTES, False),    # 脚注部件（继承模板的脚注配置）
        ("endnotes_part", RT.ENDNOTES, False),      # 尾注部件（继承模板的尾注配置）
        ("settings_part", RT.SETTINGS, False),      # 设置部件（控制页面设置、打印配置等）
        ("web_settings_part", RT.WEB_SETTINGS, False),  # 网页设置部件（适配网页预览）
        ("theme_part", RT.THEME, False),            # 主题部件（控制文档配色、字体方案）
    ]

    for part_attr, rel_type, is_required in part_mapping:
        # 3.1 检查模板是否存在该部件
        template_part = getattr(template._part, part_attr, None)
        if not template_part:
            if is_required:
                raise ValueError(f"模板缺失必需部件：{part_attr}（{rel_type}），无法继续创建文档")
            else:
                # print(f"模板缺失可选部件：{part_attr}（{rel_type}），将使用新文档默认配置")
                continue
        remove_existing_relationship(new_doc, rel_type)
        # 建立新关联（relate_to 会自动生成唯一关联ID）
        new_doc._part.relate_to(
            target=template_part,
            reltype=rel_type,
            is_external=False  # 内部部件，非外部链接
        )
    # 4. 可选：复用模板的文档主体结构（若需继承模板的内容框架，如页眉页脚）
    # 注意：若只需复用格式而非内容，可注释此部分；若需保留内容框架，取消注释
    # if template._part.body:
    #     new_doc._part.body = template._part.body.clone()

    return new_doc