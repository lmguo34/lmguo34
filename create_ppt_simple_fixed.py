#!/usr/bin/env python3
import zipfile
import os
import datetime

def create_ppt_simple():
    # 创建一个临时目录来存储 pptx 文件的内容
    temp_dir = "/tmp/ppt_simple_fixed"
    os.makedirs(temp_dir, exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "ppt"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "ppt", "slides"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "ppt", "slides", "_rels"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "ppt", "slideLayouts"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "ppt", "slideMasters"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "ppt", "theme"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "docProps"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "_rels"), exist_ok=True)
    
    # 复制模板文件
    template_dir = "/tmp/pptx-template"
    if os.path.exists(template_dir):
        # 复制 docProps
        for file_name in os.listdir(os.path.join(template_dir, "docProps")):
            src_path = os.path.join(template_dir, "docProps", file_name)
            dst_path = os.path.join(temp_dir, "docProps", file_name)
            if os.path.isfile(src_path):
                with open(src_path, "rb") as f_src:
                    with open(dst_path, "wb") as f_dst:
                        f_dst.write(f_src.read())
        
        # 复制 theme
        for file_name in os.listdir(os.path.join(template_dir, "ppt", "theme")):
            src_path = os.path.join(template_dir, "ppt", "theme", file_name)
            dst_path = os.path.join(temp_dir, "ppt", "theme", file_name)
            if os.path.isfile(src_path):
                with open(src_path, "rb") as f_src:
                    with open(dst_path, "wb") as f_dst:
                        f_dst.write(f_src.read())
        
        # 复制 slideLayouts
        for file_name in os.listdir(os.path.join(template_dir, "ppt", "slideLayouts")):
            src_path = os.path.join(template_dir, "ppt", "slideLayouts", file_name)
            dst_path = os.path.join(temp_dir, "ppt", "slideLayouts", file_name)
            if os.path.isfile(src_path):
                with open(src_path, "rb") as f_src:
                    with open(dst_path, "wb") as f_dst:
                        f_dst.write(f_src.read())
        
        # 复制 slideMasters
        for file_name in os.listdir(os.path.join(template_dir, "ppt", "slideMasters")):
            src_path = os.path.join(template_dir, "ppt", "slideMasters", file_name)
            dst_path = os.path.join(temp_dir, "ppt", "slideMasters", file_name)
            if os.path.isfile(src_path):
                with open(src_path, "rb") as f_src:
                    with open(dst_path, "wb") as f_dst:
                        f_dst.write(f_src.read())
        
        # 复制 presentation.xml
        with open(os.path.join(template_dir, "ppt", "presentation.xml"), "rb") as f_src:
            with open(os.path.join(temp_dir, "ppt", "presentation.xml"), "wb") as f_dst:
                f_dst.write(f_src.read())
        
        # 复制 presProps.xml
        with open(os.path.join(template_dir, "ppt", "presProps.xml"), "rb") as f_src:
            with open(os.path.join(temp_dir, "ppt", "presProps.xml"), "wb") as f_dst:
                f_dst.write(f_src.read())
        
        # 复制 tableStyles.xml
        with open(os.path.join(template_dir, "ppt", "tableStyles.xml"), "rb") as f_src:
            with open(os.path.join(temp_dir, "ppt", "tableStyles.xml"), "wb") as f_dst:
                f_dst.write(f_src.read())
        
        # 复制 viewProps.xml
        with open(os.path.join(template_dir, "ppt", "viewProps.xml"), "rb") as f_src:
            with open(os.path.join(temp_dir, "ppt", "viewProps.xml"), "wb") as f_dst:
                f_dst.write(f_src.read())
        
        # 复制 [Content_Types].xml
        with open(os.path.join(template_dir, "[Content_Types].xml"), "rb") as f_src:
            with open(os.path.join(temp_dir, "[Content_Types].xml"), "wb") as f_dst:
                f_dst.write(f_src.read())
        
        # 复制 _rels/.rels
        with open(os.path.join(template_dir, "_rels", ".rels"), "rb") as f_src:
            with open(os.path.join(temp_dir, "_rels", ".rels"), "wb") as f_dst:
                f_dst.write(f_src.read())
    
    # 复制 slides
    for slide_num in range(1, 9):
        src_slide_path = os.path.join(template_dir, "ppt", "slides", f"slide{slide_num}.xml")
        dst_slide_path = os.path.join(temp_dir, "ppt", "slides", f"slide{slide_num}.xml")
        if os.path.exists(src_slide_path):
            with open(src_slide_path, "rb") as f_src:
                with open(dst_slide_path, "wb") as f_dst:
                    f_dst.write(f_src.read())
        
        src_rels_path = os.path.join(template_dir, "ppt", "slides", "_rels", f"slide{slide_num}.xml.rels")
        dst_rels_path = os.path.join(temp_dir, "ppt", "slides", "_rels", f"slide{slide_num}.xml.rels")
        if os.path.exists(src_rels_path):
            with open(src_rels_path, "rb") as f_src:
                with open(dst_rels_path, "wb") as f_dst:
                    f_dst.write(f_src.read())
    
    # 复制 media
    os.makedirs(os.path.join(temp_dir, "ppt", "media"), exist_ok=True)
    for media_file in os.listdir(os.path.join(template_dir, "ppt", "media")):
        src_media_path = os.path.join(template_dir, "ppt", "media", media_file)
        dst_media_path = os.path.join(temp_dir, "ppt", "media", media_file)
        with open(src_media_path, "rb") as f_src:
            with open(dst_media_path, "wb") as f_dst:
                f_dst.write(f_src.read())
    
    # 创建 pptx 文件
    pptx_path = "/home/lmguo/桌面/郭黎明-面试答辩.pptx"
    with zipfile.ZipFile(pptx_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, arcname)
    
    print(f"PPT文件已成功创建：{pptx_path}")

if __name__ == "__main__":
    create_ppt_simple()
