#!/usr/bin/env python3
import zipfile
import os
import datetime

def create_ppt_simple():
    # 创建一个临时目录来存储 pptx 文件的内容
    temp_dir = "/tmp/ppt_simple"
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
    template_dir = "/tmp/pptx-content"
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
    
    # 创建第一张幻灯片
    slide1_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="5" name="标题 1"/>
          <p:cNvSpPr txBox="1"/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr bwMode="auto">
          <a:xfrm>
            <a:off x="2425179" y="837506"/>
            <a:ext cx="9070829" cy="954107"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
          <a:noFill/>
          <a:ln>
            <a:noFill/>
          </a:ln>
        </p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" wrap="square" lIns="0" tIns="45720" rIns="91440" bIns="45720" numCol="1" anchor="t" anchorCtr="0" compatLnSpc="1">
            <a:spAutoFit/>
          </a:bodyPr>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="0" marR="0" lvl="0" indent="0" algn="l" defTabSz="914400" rtl="0" eaLnBrk="0" fontAlgn="base" latinLnBrk="0" hangingPunct="0">
              <a:lnSpc>
                <a:spcPct val="100000"/>
              </a:lnSpc>
              <a:spcBef>
                <a:spcPct val="0"/>
              </a:spcBef>
              <a:spcAft>
                <a:spcPct val="0"/>
              </a:spcAft>
              <a:buClrTx/>
              <a:buSzTx/>
              <a:buFontTx/>
              <a:buNone/>
              <a:defRPr/>
            </a:pPr>
            <a:r>
              <a:rPr kumimoji="0" lang="zh-CN" altLang="en-US" sz="5600" b="1" i="0" u="none" strike="noStrike" kern="0" cap="none" spc="0" normalizeH="0" baseline="0" noProof="0">
                <a:ln>
                  <a:noFill/>
                </a:ln>
                <a:solidFill>
                  <a:srgbClr val="C00000"/>
                </a:solidFill>
                <a:effectLst/>
                <a:uLnTx/>
                <a:uFillTx/>
                <a:latin typeface="+mj-ea"/>
                <a:ea typeface="+mj-ea"/>
                <a:cs typeface="+mj-cs"/>
              </a:rPr>
              <a:t>工程师</a:t>
            </a:r>
            <a:r>
              <a:rPr kumimoji="0" lang="zh-CN" altLang="en-US" sz="5600" b="1" i="0" u="none" strike="noStrike" kern="0" cap="none" spc="0" normalizeH="0" baseline="0" noProof="0" dirty="0">
                <a:ln>
                  <a:noFill/>
                </a:ln>
                <a:solidFill>
                  <a:srgbClr val="C00000"/>
                </a:solidFill>
                <a:effectLst/>
                <a:uLnTx/>
                <a:uFillTx/>
                <a:latin typeface="+mj-ea"/>
                <a:ea typeface="+mj-ea"/>
                <a:cs typeface="+mj-cs"/>
              </a:rPr>
              <a:t>面试答辩</a:t>
            </a:r>
            <a:endParaRPr kumimoji="0" lang="zh-CN" altLang="en-US" sz="5600" b="1" i="0" u="none" strike="noStrike" kern="0" cap="none" spc="0" normalizeH="0" baseline="0" noProof="0" dirty="0">
              <a:ln>
                <a:noFill/>
              </a:ln>
              <a:solidFill>
                <a:srgbClr val="C00000"/>
              </a:solidFill>
              <a:effectLst/>
              <a:uLnTx/>
              <a:uFillTx/>
              <a:latin typeface="+mj-ea"/>
              <a:ea typeface="+mj-ea"/>
              <a:cs typeface="+mj-cs"/>
            </a:endParaRPr>
          </a:p>
        </p:txBody>
      </p:sp>
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="6" name="副标题 2"/>
          <p:cNvSpPr txBox="1"/>
          <p:nvPr/>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm>
            <a:off x="480963" y="1845618"/>
            <a:ext cx="10201874" cy="3888432"/>
          </a:xfrm>
          <a:prstGeom prst="rect">
            <a:avLst/>
          </a:prstGeom>
        </p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:pPr marL="342900" marR="0" lvl="0" indent="-342900" algn="l" defTabSz="914400" rtl="0" eaLnBrk="0" fontAlgn="base" latinLnBrk="0" hangingPunct="0">
              <a:lnSpc>
                <a:spcPct val="100000"/>
              </a:lnSpc>
              <a:spcBef>
                <a:spcPct val="20000"/>
              </a:spcBef>
              <a:spcAft>
                <a:spcPct val="0"/>
              </a:spcAft>
              <a:buClr>
                <a:srgbClr val="990000"/>
              </a:buClr>
              <a:buSzTx/>
              <a:defRPr/>
            </a:pPr>
            <a:r>
              <a:rPr kumimoji="0" lang="zh-CN" altLang="en-US" sz="3600" b="1" i="0" u="none" strike="noStrike" kern="0" cap="none" spc="0" normalizeH="0" baseline="0" noProof="0" dirty="0">
                <a:ln>
                  <a:noFill/>
                </a:ln>
                <a:solidFill>
                  <a:schemeClr val="tx1">
                    <a:lumMod val="75000"/>
                    <a:lumOff val="25000"/>
                  </a:schemeClr>
                </a:solidFill>
                <a:effectLst/>
                <a:uLnTx/>
                <a:uFillTx/>
                <a:latin typeface="+mj-ea"/>
                <a:ea typeface="+mj-ea"/>
                <a:cs typeface="+mn-cs"/>
              </a:rPr>
              <a:t>  姓名：郭黎明</a:t>
            </a:r>
            <a:endParaRPr kumimoji="0" lang="en-US" altLang="zh-CN" sz="3600" b="1" i="0" u="none" strike="noStrike" kern="0" cap="none" spc="0" normalizeH="0" baseline="0" noProof="0" dirty="0">
              <a:ln>
                <a:noFill/>
              </a:ln>
              <a:solidFill>
                <a:schemeClr val="tx1">
                  <a:lumMod val="75000"/>
                  <a:lumOff val="25000"/>
                </a:schemeClr>
              </a:solidFill>
              <a:effectLst/>
              <a:uLnTx/>
              <a:uFillTx/>
              <a:latin typeface="+mj-ea"/>
              <a:ea typeface="+mj-ea"/>
              <a:cs typeface="+mn-cs"/>
            </a:endParaRPr>
          </a:p>
          <a:p>
            <a:pPr marL="342900" marR="0" lvl="0" indent="-342900" algn="l" defTabSz="914400" rtl="0" eaLnBrk="0" fontAlgn="base" latinLnBrk="0" hangingPunct="0">
              <a:lnSpc>
                <a:spcPct val="100000"/>
              </a:lnSpc>
              <a:spcBef>
                <a:spcPct val="20000"/>
              </a:spcBef>
              <a:spcAft>
                <a:spcPct val="0"/>
              </a:spcAft>
              <a:buClr>
                <a:srgbClr val="990000"/>
              </a:buClr>
              <a:buSzTx/>
              <a:defRPr/>
            </a:pPr>
            <a:r>
              <a:rPr lang="en-US" altLang="zh-CN" sz="3600" b="1" kern="0" dirty="0">
                <a:solidFill>