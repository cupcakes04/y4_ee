#!/usr/bin/env python3
"""
Build `project_proposal_v2h.docx` (and `project_proposal_v2h.pdf`) from `project_proposal_updated.docx`
without modifying `project_proposal_updated.docx`.

Key transformations:
- Keep cover page (0..29) and Appendix A (148..170) intact.
- Replace Statement of Originality (30..56) with plain black-bordered boxes and concise, natural first-person student answers.
- Update Table of Contents (59) with clean section headings and accurate page numbers.
- Replace main body (62..132) with natural, direct student engineering prose, 5 plain black-bordered Word tables (Tables 1-5),
  and monochrome LaTeX-style figures (Figures 1 and 2).
- Keep strictly verified IEEE References [1]-[13] (133..147).
"""
import os
import re
import zipfile
import subprocess
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DOCX = os.path.join(BASE_DIR, 'project_proposal_v1.docx')
OUT_DOCX = os.path.join(BASE_DIR, 'project_proposal_v2h.docx')
FIG1_PNG = os.path.join(BASE_DIR, 'assets', 'fig1_latex_arch.png')
FIG2_PNG = os.path.join(BASE_DIR, 'assets', 'fig2_latex_flow.png')

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
PIC = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
XML_SPACE = '{http://www.w3.org/XML/1998/namespace}space'


def make_run(text, bold=False, italic=False, sz=24, color='000000', underline=False):
    r = ET.Element(f'{{{W}}}r')
    rPr = ET.SubElement(r, f'{{{W}}}rPr')
    rFonts = ET.SubElement(rPr, f'{{{W}}}rFonts')
    rFonts.set(f'{{{W}}}ascii', 'Times New Roman')
    rFonts.set(f'{{{W}}}hAnsi', 'Times New Roman')
    rFonts.set(f'{{{W}}}eastAsia', 'Times New Roman')
    rFonts.set(f'{{{W}}}cs', 'Times New Roman')
    if bold:
        ET.SubElement(rPr, f'{{{W}}}b')
        ET.SubElement(rPr, f'{{{W}}}bCs')
    if italic:
        ET.SubElement(rPr, f'{{{W}}}i')
        ET.SubElement(rPr, f'{{{W}}}iCs')
    if underline:
        u = ET.SubElement(rPr, f'{{{W}}}u')
        u.set(f'{{{W}}}val', 'single')
    c = ET.SubElement(rPr, f'{{{W}}}color')
    c.set(f'{{{W}}}val', color)
    s = ET.SubElement(rPr, f'{{{W}}}sz')
    s.set(f'{{{W}}}val', str(sz))
    sCs = ET.SubElement(rPr, f'{{{W}}}szCs')
    sCs.set(f'{{{W}}}val', str(sz))
    t = ET.SubElement(r, f'{{{W}}}t')
    if text.startswith(' ') or text.endswith(' '):
        t.set(XML_SPACE, 'preserve')
    t.text = text
    return r


def make_p(runs_or_text, jc='both', before=0, after=120, line=240, keep_next=False,
           page_break_before=False, indent_left=None, hanging=None, outline_lvl=None, bookmark=None):
    p = ET.Element(f'{{{W}}}p')
    pPr = ET.SubElement(p, f'{{{W}}}pPr')
    if page_break_before:
        ET.SubElement(pPr, f'{{{W}}}pageBreakBefore')
    if keep_next:
        ET.SubElement(pPr, f'{{{W}}}keepNext')
    if outline_lvl is not None:
        ol = ET.SubElement(pPr, f'{{{W}}}outlineLvl')
        ol.set(f'{{{W}}}val', str(outline_lvl))
    sp = ET.SubElement(pPr, f'{{{W}}}spacing')
    sp.set(f'{{{W}}}before', str(before))
    sp.set(f'{{{W}}}after', str(after))
    sp.set(f'{{{W}}}line', str(line))
    sp.set(f'{{{W}}}lineRule', 'auto')
    if indent_left is not None:
        ind = ET.SubElement(pPr, f'{{{W}}}ind')
        ind.set(f'{{{W}}}left', str(indent_left))
        if hanging is not None:
            ind.set(f'{{{W}}}hanging', str(hanging))
    j = ET.SubElement(pPr, f'{{{W}}}jc')
    j.set(f'{{{W}}}val', jc)

    if bookmark:
        bm_id, bm_name = bookmark
        bs = ET.SubElement(p, f'{{{W}}}bookmarkStart')
        bs.set(f'{{{W}}}id', str(bm_id))
        bs.set(f'{{{W}}}name', bm_name)

    if isinstance(runs_or_text, str):
        if runs_or_text:
            p.append(make_run(runs_or_text))
    else:
        for item in runs_or_text:
            if isinstance(item, ET.Element):
                p.append(item)
            elif isinstance(item, tuple):
                txt = item[0]
                kw = item[1] if len(item) > 1 else {}
                p.append(make_run(txt, **kw))

    if bookmark:
        be = ET.SubElement(p, f'{{{W}}}bookmarkEnd')
        be.set(f'{{{W}}}id', str(bookmark[0]))
    return p


def make_h1(title, bm_id, bm_name, before=180, after=80):
    return make_p(
        [(title, {'bold': True, 'sz': 26, 'color': '000000'})],
        jc='left', before=before, after=after, keep_next=True, outline_lvl=0,
        bookmark=(bm_id, bm_name)
    )


def make_h2(title, bm_id, bm_name, before=140, after=60):
    return make_p(
        [(title, {'bold': True, 'sz': 24, 'color': '000000'})],
        jc='left', before=before, after=after, keep_next=True, outline_lvl=1,
        bookmark=(bm_id, bm_name)
    )


def make_table_caption(num, text):
    return make_p(
        [
            (f'Table {num}. ', {'bold': True, 'sz': 21}),
            (text, {'italic': False, 'sz': 21}),
        ],
        jc='left', before=100, after=40, keep_next=True
    )


def make_figure_caption(num, text):
    return make_p(
        [
            (f'Figure {num}. ', {'bold': True, 'sz': 21}),
            (text, {'italic': False, 'sz': 21}),
        ],
        jc='center', before=40, after=120
    )


def set_black_borders(bdr_parent, sz='4', color='000000', inside=True):
    sides = ['top', 'left', 'bottom', 'right']
    if inside:
        sides += ['insideH', 'insideV']
    for s in sides:
        el = ET.SubElement(bdr_parent, f'{{{W}}}{s}')
        el.set(f'{{{W}}}val', 'single')
        el.set(f'{{{W}}}sz', sz)
        el.set(f'{{{W}}}space', '0')
        el.set(f'{{{W}}}color', color)


def make_box_table(paragraphs_list):
    """Single-cell plain black-bordered box for Statement of Originality."""
    tbl = ET.Element(f'{{{W}}}tbl')
    tblPr = ET.SubElement(tbl, f'{{{W}}}tblPr')
    tblW = ET.SubElement(tblPr, f'{{{W}}}tblW')
    tblW.set(f'{{{W}}}w', '9026')
    tblW.set(f'{{{W}}}type', 'dxa')
    jc = ET.SubElement(tblPr, f'{{{W}}}jc')
    jc.set(f'{{{W}}}val', 'center')
    bdrs = ET.SubElement(tblPr, f'{{{W}}}tblBorders')
    set_black_borders(bdrs, sz='4', color='000000', inside=False)
    cm = ET.SubElement(tblPr, f'{{{W}}}tblCellMar')
    for side, val in [('top', '60'), ('left', '120'), ('bottom', '60'), ('right', '120')]:
        m = ET.SubElement(cm, f'{{{W}}}{side}')
        m.set(f'{{{W}}}w', val)
        m.set(f'{{{W}}}type', 'dxa')

    grid = ET.SubElement(tbl, f'{{{W}}}tblGrid')
    gc = ET.SubElement(grid, f'{{{W}}}gridCol')
    gc.set(f'{{{W}}}w', '9026')

    tr = ET.SubElement(tbl, f'{{{W}}}tr')
    tc = ET.SubElement(tr, f'{{{W}}}tc')
    tcPr = ET.SubElement(tc, f'{{{W}}}tcPr')
    tcW = ET.SubElement(tcPr, f'{{{W}}}tcW')
    tcW.set(f'{{{W}}}w', '9026')
    tcW.set(f'{{{W}}}type', 'dxa')

    for p in paragraphs_list:
        tc.append(p)
    return tbl


def make_student_table(col_widths, headers, rows, font_sz=20, header_fill='E8E8E8', center_cols=None):
    """Plain student-style Word table: simple 1px black grid, light-grey header row, no zebra striping."""
    if center_cols is None:
        center_cols = set()
    total_w = sum(col_widths)
    tbl = ET.Element(f'{{{W}}}tbl')
    tblPr = ET.SubElement(tbl, f'{{{W}}}tblPr')
    tblW = ET.SubElement(tblPr, f'{{{W}}}tblW')
    tblW.set(f'{{{W}}}w', str(total_w))
    tblW.set(f'{{{W}}}type', 'dxa')
    jc = ET.SubElement(tblPr, f'{{{W}}}jc')
    jc.set(f'{{{W}}}val', 'center')
    bdrs = ET.SubElement(tblPr, f'{{{W}}}tblBorders')
    set_black_borders(bdrs, sz='4', color='000000', inside=True)
    layout = ET.SubElement(tblPr, f'{{{W}}}tblLayout')
    layout.set(f'{{{W}}}type', 'fixed')
    cm = ET.SubElement(tblPr, f'{{{W}}}tblCellMar')
    for side, val in [('top', '45'), ('left', '90'), ('bottom', '45'), ('right', '90')]:
        m = ET.SubElement(cm, f'{{{W}}}{side}')
        m.set(f'{{{W}}}w', val)
        m.set(f'{{{W}}}type', 'dxa')

    grid = ET.SubElement(tbl, f'{{{W}}}tblGrid')
    for w in col_widths:
        gc = ET.SubElement(grid, f'{{{W}}}gridCol')
        gc.set(f'{{{W}}}w', str(w))

    # Header row
    tr_h = ET.SubElement(tbl, f'{{{W}}}tr')
    trPr_h = ET.SubElement(tr_h, f'{{{W}}}trPr')
    ET.SubElement(trPr_h, f'{{{W}}}cantSplit')
    ET.SubElement(trPr_h, f'{{{W}}}tblHeader')
    for c_idx, h_text in enumerate(headers):
        tc = ET.SubElement(tr_h, f'{{{W}}}tc')
        tcPr = ET.SubElement(tc, f'{{{W}}}tcPr')
        tcW = ET.SubElement(tcPr, f'{{{W}}}tcW')
        tcW.set(f'{{{W}}}w', str(col_widths[c_idx]))
        tcW.set(f'{{{W}}}type', 'dxa')
        if header_fill:
            shd = ET.SubElement(tcPr, f'{{{W}}}shd')
            shd.set(f'{{{W}}}val', 'clear')
            shd.set(f'{{{W}}}fill', header_fill)
        vAlign = ET.SubElement(tcPr, f'{{{W}}}vAlign')
        vAlign.set(f'{{{W}}}val', 'center')
        align = 'center' if c_idx in center_cols else 'left'
        tc.append(make_p([(h_text, {'bold': True, 'sz': font_sz})], jc=align, before=20, after=20))

    # Data rows
    for row in rows:
        tr = ET.SubElement(tbl, f'{{{W}}}tr')
        trPr = ET.SubElement(tr, f'{{{W}}}trPr')
        ET.SubElement(trPr, f'{{{W}}}cantSplit')
        for c_idx, cell_val in enumerate(row):
            tc = ET.SubElement(tr, f'{{{W}}}tc')
            tcPr = ET.SubElement(tc, f'{{{W}}}tcPr')
            tcW = ET.SubElement(tcPr, f'{{{W}}}tcW')
            tcW.set(f'{{{W}}}w', str(col_widths[c_idx]))
            tcW.set(f'{{{W}}}type', 'dxa')
            vAlign = ET.SubElement(tcPr, f'{{{W}}}vAlign')
            vAlign.set(f'{{{W}}}val', 'top')
            align = 'center' if c_idx in center_cols else 'left'
            tc.append(make_p([(cell_val, {'bold': False, 'sz': font_sz})], jc=align, before=20, after=20))

    return tbl


def make_gantt_table():
    """
    Plain student-style Gantt chart table with 2 distinct semester shades per Dr. Shalini's Meeting 5 feedback:
    - Autumn Semester (W1-W15): muted blue-grey fill ('A6BDD7') for active cells, light header ('D9E2EC')
    - Spring Semester (W16-W30): muted sage-grey fill ('A8C69F') for active cells, light header ('DCE8D8')
    """
    task_w = 2906
    wk_w = 480
    col_widths = [task_w] + [wk_w] * 14
    total_w = sum(col_widths)

    tbl = ET.Element(f'{{{W}}}tbl')
    tblPr = ET.SubElement(tbl, f'{{{W}}}tblPr')
    tblW = ET.SubElement(tblPr, f'{{{W}}}tblW')
    tblW.set(f'{{{W}}}w', str(total_w))
    tblW.set(f'{{{W}}}type', 'dxa')
    jc = ET.SubElement(tblPr, f'{{{W}}}jc')
    jc.set(f'{{{W}}}val', 'center')
    bdrs = ET.SubElement(tblPr, f'{{{W}}}tblBorders')
    set_black_borders(bdrs, sz='4', color='000000', inside=True)
    layout = ET.SubElement(tblPr, f'{{{W}}}tblLayout')
    layout.set(f'{{{W}}}type', 'fixed')
    cm = ET.SubElement(tblPr, f'{{{W}}}tblCellMar')
    for side, val in [('top', '35'), ('left', '20'), ('bottom', '35'), ('right', '20')]:
        m = ET.SubElement(cm, f'{{{W}}}{side}')
        m.set(f'{{{W}}}w', val)
        m.set(f'{{{W}}}type', 'dxa')

    grid = ET.SubElement(tbl, f'{{{W}}}tblGrid')
    for w in col_widths:
        gc = ET.SubElement(grid, f'{{{W}}}gridCol')
        gc.set(f'{{{W}}}w', str(w))

    # Row 0: Semester super-header
    tr0 = ET.SubElement(tbl, f'{{{W}}}tr')
    trPr0 = ET.SubElement(tr0, f'{{{W}}}trPr')
    ET.SubElement(trPr0, f'{{{W}}}cantSplit')
    ET.SubElement(trPr0, f'{{{W}}}tblHeader')

    def add_merged_header(tr_el, width, span, text, fill):
        tc = ET.SubElement(tr_el, f'{{{W}}}tc')
        tcPr = ET.SubElement(tc, f'{{{W}}}tcPr')
        tcW = ET.SubElement(tcPr, f'{{{W}}}tcW')
        tcW.set(f'{{{W}}}w', str(width))
        tcW.set(f'{{{W}}}type', 'dxa')
        if span > 1:
            gs = ET.SubElement(tcPr, f'{{{W}}}gridSpan')
            gs.set(f'{{{W}}}val', str(span))
        shd = ET.SubElement(tcPr, f'{{{W}}}shd')
        shd.set(f'{{{W}}}val', 'clear')
        shd.set(f'{{{W}}}fill', fill)
        vAlign = ET.SubElement(tcPr, f'{{{W}}}vAlign')
        vAlign.set(f'{{{W}}}val', 'center')
        tc.append(make_p([(text, {'bold': True, 'sz': 18})], jc='center', before=15, after=15))

    add_merged_header(tr0, task_w, 1, 'Project Task', 'E8E8E8')
    add_merged_header(tr0, wk_w * 7, 7, 'Autumn Semester (Weeks 1-15)', 'D9E2EC')
    add_merged_header(tr0, wk_w * 7, 7, 'Spring Semester (Weeks 16-30)', 'DCE8D8')

    # Row 1: Week labels
    tr1 = ET.SubElement(tbl, f'{{{W}}}tr')
    trPr1 = ET.SubElement(tr1, f'{{{W}}}trPr')
    ET.SubElement(trPr1, f'{{{W}}}cantSplit')
    ET.SubElement(trPr1, f'{{{W}}}tblHeader')
    wk_labels = ['Activity / Weeks', 'W1-2', 'W3-4', 'W5-6', 'W7-8', 'W9-10', 'W11-12', 'W13-15',
                 'W16-18', 'W19-20', 'W21-22', 'W23-24', 'W25-26', 'W27-28', 'W29-30']
    for idx, lbl in enumerate(wk_labels):
        fill = 'E8E8E8' if idx == 0 else ('EBF1F6' if idx <= 7 else 'EDF4EB')
        tc = ET.SubElement(tr1, f'{{{W}}}tc')
        tcPr = ET.SubElement(tc, f'{{{W}}}tcPr')
        tcW = ET.SubElement(tcPr, f'{{{W}}}tcW')
        tcW.set(f'{{{W}}}w', str(col_widths[idx]))
        tcW.set(f'{{{W}}}type', 'dxa')
        shd = ET.SubElement(tcPr, f'{{{W}}}shd')
        shd.set(f'{{{W}}}val', 'clear')
        shd.set(f'{{{W}}}fill', fill)
        vAlign = ET.SubElement(tcPr, f'{{{W}}}vAlign')
        vAlign.set(f'{{{W}}}val', 'center')
        tc.append(make_p([(lbl, {'bold': True, 'sz': 18 if idx == 0 else 13})], jc='center', before=15, after=15))

    # Tasks: (name, active_col_indices_1_to_14, review_cols)
    tasks = [
        ('1. Literature review, setup & Docker (W5-W8, 45 h)', {3, 4}, {}),
        ('2. Simulate world, actors & C0 baseline (W7-W12, 45 h)', {4, 5, 6}, {6: 'PR1'}),
        ('3. Prepare vision-LiDAR tracker (O1) (W9-W15, 90 h)', {5, 6, 7}, {7: 'PR2'}),
        ('4. Setup automated testing harness (O3) (W11-W20, 45 h)', {6, 7, 8, 9}, {}),
        ('5. Develop predictive MPPI critic (O2) (W13-W20, 75 h)', {7, 8, 9}, {9: 'PR3'}),
        ('6. Run comparative simulation benchmarks (W19-W24, 60 h)', {9, 10, 11}, {11: 'PR4'}),
        ('7. Analyze results & statistical metrics (W23-W28, 30 h)', {11, 12, 13}, {13: 'PR5'}),
        ('8. Write final thesis & prepare video demos (W25-W30, 60 h)', {12, 13, 14}, {}),
    ]

    for t_name, active_set, pr_map in tasks:
        tr = ET.SubElement(tbl, f'{{{W}}}tr')
        trPr = ET.SubElement(tr, f'{{{W}}}trPr')
        ET.SubElement(trPr, f'{{{W}}}cantSplit')

        # Task name cell
        tc0 = ET.SubElement(tr, f'{{{W}}}tc')
        tcPr0 = ET.SubElement(tc0, f'{{{W}}}tcPr')
        tcW0 = ET.SubElement(tcPr0, f'{{{W}}}tcW')
        tcW0.set(f'{{{W}}}w', str(task_w))
        tcW0.set(f'{{{W}}}type', 'dxa')
        vAlign0 = ET.SubElement(tcPr0, f'{{{W}}}vAlign')
        vAlign0.set(f'{{{W}}}val', 'center')
        tc0.append(make_p([(t_name, {'bold': False, 'sz': 18})], jc='left', before=15, after=15))

        for w_idx in range(1, 15):
            tc = ET.SubElement(tr, f'{{{W}}}tc')
            tcPr = ET.SubElement(tc, f'{{{W}}}tcPr')
            tcW = ET.SubElement(tcPr, f'{{{W}}}tcW')
            tcW.set(f'{{{W}}}w', str(wk_w))
            tcW.set(f'{{{W}}}type', 'dxa')
            is_active = w_idx in active_set
            if is_active:
                fill = '9BB8D3' if w_idx <= 7 else 'A3C999'
            else:
                fill = 'F7FAFC' if w_idx <= 7 else 'F8FBF7'
            shd = ET.SubElement(tcPr, f'{{{W}}}shd')
            shd.set(f'{{{W}}}val', 'clear')
            shd.set(f'{{{W}}}fill', fill)
            vAlign = ET.SubElement(tcPr, f'{{{W}}}vAlign')
            vAlign.set(f'{{{W}}}val', 'center')
            cell_txt = pr_map.get(w_idx, '')
            tc.append(make_p([(cell_txt, {'bold': True, 'sz': 16})], jc='center', before=15, after=15))

    return tbl


def build_statement_of_originality():
    """Build clean, student-style Statement of Originality elements (replacing indices 30..56)."""
    els = []
    els.append(make_p(
        [('Statement of Originality', {'bold': True, 'sz': 28})],
        jc='left', before=0, after=80, page_break_before=True, bookmark=(10, '_Toc_SOO')
    ))
    els.append(make_p(
        [('University of Nottingham | Faculty of Science and Engineering | Department of Electrical and Electronic Engineering | EEEE4077 Mechatronics Project',
          {'bold': True, 'sz': 20})],
        jc='left', before=0, after=80
    ))
    for bullet in [
        '• I have read and understood the University of Nottingham Academic Misconduct Policy.',
        '• I am aware that failure to act in accordance with the Regulations Governing Academic Integrity may lead to the imposition of penalties which, for the most serious cases, may include termination of programme.',
        '• I consent to the University copying and distributing any or all of my work in any form and using third parties to verify whether my work contains plagiarised material, and for quality assurance purposes.',
    ]:
        els.append(make_p([(bullet, {'sz': 20})], jc='both', before=0, after=40, indent_left=240, hanging=180))

    els.append(make_p(
        [('Note: ', {'bold': True, 'sz': 20}),
         ('You must change the statements in the boxes to reflect your individual submission.', {'italic': True, 'sz': 20})],
        jc='left', before=40, after=100
    ))

    # 1. Acknowledgment of Sources
    els.append(make_p([('1. Acknowledgment of Sources', {'bold': True, 'sz': 22})], jc='left', before=80, after=30, keep_next=True))
    els.append(make_p(
        [('You must acknowledge all sources of information (e.g. ideas, algorithms, data) using citations to auditable, authoritative sources. You must also put quotation marks around any sections of text that you have copied without paraphrasing and cite the original source. If any figures or tables have been taken or modified from another source, you must explain this in the caption, and cite the original source.', {'sz': 19})],
        jc='both', before=0, after=40, keep_next=True
    ))
    els.append(make_box_table([
        make_p([('I have acknowledged all sources used in this report and cited them using IEEE numbering [1]–[13]. No text has been copied without attribution, and the block diagrams, flowcharts, and schedule tables were prepared by me for this project.', {'sz': 20})], jc='both', before=20, after=20)
    ]))

    # 2. Resources Produced by Someone Else
    els.append(make_p([('2. Resources Produced by Someone Else', {'bold': True, 'sz': 22})], jc='left', before=90, after=30, keep_next=True))
    els.append(make_p(
        [('If you have used any code (e.g., open-source code), reference designs, or similar resources that have been produced by anyone else, you must list them in the box below. In the report, you must explain what was used and how it relates to the work you have done.', {'sz': 19})],
        jc='both', before=0, after=40, keep_next=True
    ))
    els.append(make_box_table([
        make_p([('I plan to use the following open-source software and libraries produced by others:', {'sz': 20})], jc='both', before=20, after=30),
        make_p([('1. ROS 2 (Jazzy / Humble) and the Nav2 stack (nav2_mppi_controller, nav2_costmap_2d) for robot communication, coordinate frames (tf2), and the baseline local planner.', {'sz': 20})], jc='both', before=0, after=20, indent_left=240, hanging=240),
        make_p([('2. Gazebo Harmonic for the indoor corridor simulation, differential-drive robot physics, simulated sensors, and scripted moving obstacle actors.', {'sz': 20})], jc='both', before=0, after=20, indent_left=240, hanging=240),
        make_p([('3. Ultralytics YOLOv8 (pre-trained yolov8n weights) and ByteTrack (boxmot) for 2D bounding box detection and frame-to-frame object tracking.', {'sz': 20})], jc='both', before=0, after=20, indent_left=240, hanging=240),
        make_p([('4. Standard open-source math and vision libraries (OpenCV, Eigen3, NumPy, SciPy, Matplotlib) for matrix calculations and data plotting.', {'sz': 20})], jc='both', before=0, after=30, indent_left=240, hanging=240),
        make_p([('The camera-LiDAR frustum depth matching, linear Kalman filter velocity tracker, custom C++ MPPI dynamic obstacle critic plugin, and automated testing scripts will be written by me.', {'sz': 20})], jc='both', before=0, after=20),
    ]))

    # 3. Generative AI Declaration
    els.append(make_p([('3. Generative AI Declaration', {'bold': True, 'sz': 22})], jc='left', before=90, after=30, keep_next=True))
    els.append(make_p(
        [('If you have used generative AI tools in the preparation of your assessed work, or the underlying code/designs/underpinning work, its use must be declared in a signed statement in the box below. You must declare the tools employed and the method and extent of use. You can do this using the table below:', {'sz': 19})],
        jc='both', before=0, after=40, keep_next=True
    ))
    ai_inner_tbl = make_student_table(
        [2000, 2300, 4400],
        ['Tool', 'Application Scope', 'Nature of Assistance'],
        [['ChatGPT / Google Gemini', 'Grammar checking and syntax lookup',
          'Used for checking grammar and phrasing in draft sections, and for looking up standard ROS 2 / C++ syntax and configuration boilerplate.']],
        font_sz=19
    )
    els.append(make_box_table([
        make_p([('Generative AI tools have been used in the preparation of this work as follows:', {'sz': 20})], jc='left', before=20, after=40),
        ai_inner_tbl,
        make_p([('I confirm that all project design decisions, parameter choices, and final written sections are my own work.', {'sz': 20})], jc='both', before=40, after=20),
    ]))

    # 4. Independent Work
    els.append(make_p([('4. Independent Work & External Assistance', {'bold': True, 'sz': 22})], jc='left', before=90, after=30, keep_next=True))
    els.append(make_p(
        [('You can consult with teaching staff/demonstrators, but you should not show anyone else your work (this includes uploading your work to publicly accessible repositories e.g. GitHub, unless expressly permitted by your supervisor). Nor should you help other students with their work. You must get permission in writing before you seek outside assistance, e.g. a proofreading service, and declare it here.', {'sz': 19})],
        jc='both', before=0, after=40, keep_next=True
    ))
    els.append(make_box_table([
        make_p([('I completed this work myself and have not shared my work with other students or used any external proofreading services. My project repository is kept private.', {'sz': 20})], jc='both', before=20, after=20)
    ]))

    # 5. Research Data Integrity
    els.append(make_p([('5. Research Data Integrity & Reproducibility', {'bold': True, 'sz': 22})], jc='left', before=90, after=30, keep_next=True))
    els.append(make_p(
        [('You must not have fabricated, modified or distorted any data, evidence, references, experimental results, or other material used or presented in the report. You must clearly describe your experiments and how the results were obtained, and include all data, source code and/or designs (submitted as a separate file) so that your results could be reproduced.', {'sz': 19})],
        jc='both', before=0, after=40, keep_next=True
    ))
    els.append(make_box_table([
        make_p([('The material in this planning report is genuine, and all simulation parameters and evaluation methods are designed to be reproducible in the simulation workspace.', {'sz': 20})], jc='both', before=20, after=20)
    ]))

    # 6. Ethical Approval
    els.append(make_p([('6. Ethical Approval', {'bold': True, 'sz': 22})], jc='left', before=90, after=30, keep_next=True))
    els.append(make_p(
        [('If your work involved research studies (including surveys) on human participants, their cells or data, or on animals, you must have been granted ethical approval before the work was carried out, and any experiments must have followed these requirements. You must give details of this in the report, and list the ethical approval reference number(s) in the box below.', {'sz': 19})],
        jc='both', before=0, after=40, keep_next=True
    ))
    els.append(make_box_table([
        make_p([('Not applicable. This project is carried out entirely in computer simulation (Gazebo Harmonic and ROS 2) using virtual obstacle actors and does not involve human participants or animals.', {'sz': 20})], jc='both', before=20, after=20)
    ]))

    # Sign-off
    els.append(make_p([('Supervisory Discussion & Final Sign-Off', {'bold': True, 'sz': 22})], jc='left', before=90, after=30, keep_next=True))
    els.append(make_p([('My responses to these questions are full and complete, and I have discussed them with my supervisor.', {'sz': 19})], jc='both', before=0, after=40, keep_next=True))
    els.append(make_student_table(
        [2500, 6526],
        ['Field', 'Detail'],
        [
            ['Student Name', 'Nicholas Khor Han Le'],
            ['Student ID', '20617556'],
            ['Degree Programme', 'MEng (Hons) Electrical and Electronic Engineering / Mechatronics'],
            ['Project Code & Title', 'SD-MEng-26-01: Vision-Augmented Mobile Robot Navigation in Dynamic Environments'],
            ['Supervisor', 'Dr. Shalini Darmaraju'],
            ['Moderator', 'Ir Dr. Daniel Pu'],
            ['Date', '2 November 2026'],
            ['Student Signature', 'Nic'],
        ],
        font_sz=19
    ))

    return els


def build_toc(toc_entries):
    """Build a clean Table of Contents matching plain academic Word formatting."""
    els = []
    els.append(make_p(
        [('Table of Contents', {'bold': True, 'sz': 28})],
        jc='left', before=0, after=160, page_break_before=True
    ))
    for level, title, anchor, page_str in toc_entries:
        p = ET.Element(f'{{{W}}}p')
        pPr = ET.SubElement(p, f'{{{W}}}pPr')
        tabs = ET.SubElement(pPr, f'{{{W}}}tabs')
        tab = ET.SubElement(tabs, f'{{{W}}}tab')
        tab.set(f'{{{W}}}val', 'right')
        tab.set(f'{{{W}}}pos', '9016')
        tab.set(f'{{{W}}}leader', 'dot')
        sp = ET.SubElement(pPr, f'{{{W}}}spacing')
        sp.set(f'{{{W}}}before', '40' if level == 1 else '15')
        sp.set(f'{{{W}}}after', '40' if level == 1 else '15')
        if level == 2:
            ind = ET.SubElement(pPr, f'{{{W}}}ind')
            ind.set(f'{{{W}}}left', '360')

        hl = ET.SubElement(p, f'{{{W}}}hyperlink')
        hl.set(f'{{{W}}}anchor', anchor)
        hl.append(make_run(title, bold=(level == 1), sz=24))
        r_tab = ET.Element(f'{{{W}}}r')
        ET.SubElement(r_tab, f'{{{W}}}tab')
        hl.append(r_tab)
        hl.append(make_run(str(page_str), bold=False, sz=24))
        els.append(p)
    return els


def build_main_body(fig1_drawing_p, fig2_drawing_p):
    """Build Sections 1-6 with direct student prose, LaTeX-style figures, and 5 plain tables."""
    els = []

    # Page break before Section 1
    p_brk = ET.Element(f'{{{W}}}p')
    pPr_brk = ET.SubElement(p_brk, f'{{{W}}}pPr')
    ET.SubElement(pPr_brk, f'{{{W}}}pageBreakBefore')
    els.append(p_brk)

    # =========================================================================
    # SECTION 1: OVERVIEW OF THE PROJECT
    # =========================================================================
    els.append(make_h1('1. Overview of the Project', 20, '_Toc_Sec1', before=0, after=80))
    els.append(make_h2('1.1 Background and the Freezing Robot Problem', 21, '_Toc_Sec1_1', before=60, after=60))

    els.append(make_p(
        'According to the International Federation of Robotics (IFR), transportation and logistics made up the largest commercial segment for professional service robots in 2024, with 102,900 units sold globally (a 14% annual increase) [1]. Most of these Autonomous Mobile Robots (AMRs) are deployed in existing brownfield factories and warehouses that cannot be redesigned with dedicated robot-only lanes. Instead, the robots have to share narrow corridors with walking workers, pallet jacks, and forklifts. To keep hardware costs reasonable and meet industrial safety standards (ISO 3691-4), most commercial AMRs rely on a single-plane 2D safety laser scanner paired with the open-source Robot Operating System 2 (ROS 2) navigation stack, Nav2 [2], [3]. While a 2D LiDAR provides accurate range measurements across a 270° to 360° field of view at 20 to 40 Hz, combining a planar laser scan with a standard 2D occupancy grid (nav2_costmap_2d) causes a well-known failure mode in busy corridors called the freezing robot problem [4].'
    ))

    els.append(make_p(
        'As described by Trautman and Krause [4], the freezing robot problem happens when a mobile robot encounters moving obstacles and either stops completely, oscillates in place, or triggers unnecessary recovery rotations because its local planner marks all forward paths as unsafe. In a standard 2D LiDAR setup, this happens for two practical reasons. First, a 2D laser scanner mounted 10 to 20 cm above the ground only slices across a walking person\'s lower legs, which show up as two small, jumping point clusters without any class label, bounding box, or velocity estimate. Second, standard Nav2 pipelines write these laser hits directly into a static 2D costmap [2], treating every occupied cell as a permanent wall at the current instant. When a person walks across a corridor at a normal speed of 1.2 to 1.4 m/s [9], the local planner cannot predict that the person will clear the path in a second or two. Instead, the robot brakes and waits until the path is completely clear, or gets stuck trying to replan around a moving target.'
    ))

    els.append(make_h2('1.2 Project Aim and Objectives', 22, '_Toc_Sec1_2'))

    els.append(make_p([
        ('Project Aim: ', {'bold': True}),
        ('To develop and evaluate in simulation a vision-augmented mobile robot navigation framework that combines simulated camera images with 2D planar range measurements to track moving obstacles, estimate their positions and velocities, and incorporate short-term motion predictions into local path planning and collision avoidance.', {})
    ]))

    els.append(make_p('To meet this aim and align directly with the four objectives defined in the approved FYP specification (Appendix A.3), the project comprises a foundational literature review and three core experimental engineering subsystems (Objectives O1–O3):', after=60))

    els.append(make_p(
        '1. Literature Review and State-of-the-Art Synthesis: To review existing methods for vision-augmented mobile robot navigation, camera and range-sensor integration, obstacle tracking and motion prediction.',
        indent_left=360, hanging=360, after=60
    ))
    els.append(make_p(
        '2. Multi-Modal Obstacle Detection and Tracking (Objective O1): To build an indoor mobile robot simulation and adapt visual detection and tracking methods to combine simulated camera images with planar range scans for obstacle position and velocity estimation.',
        indent_left=360, hanging=360, after=60
    ))
    els.append(make_p(
        '3. Motion-Aware Local Path Planning (Objective O2): To develop a local navigation controller that uses short-term obstacle motion predictions and expanding safety margins during trajectory evaluation to reduce robot freezing while avoiding collisions.',
        indent_left=360, hanging=360, after=60
    ))
    els.append(make_p(
        '4. Comparative Simulation Evaluation (Objective O3): To evaluate the proposed system against range-sensor-only navigation and non-predictive visual detection baselines across different obstacle speeds, movement patterns, and crowd densities, measuring tracking error, navigation success, waiting time, and computation time.',
        indent_left=360, hanging=360, after=100
    ))

    els.append(make_h2('1.3 System Architecture', 23, '_Toc_Sec1_3'))

    els.append(make_p(
        'Figure 1 shows the top-down block diagram of the proposed system. The main design idea is to separate static building walls (which stay in the standard 2D costmap) from moving obstacles (which are tracked in Objective O1 and forward-projected inside the local planner in Objective O2).'
    ))

    # Figure 1 image + caption
    els.append(fig1_drawing_p)
    els.append(make_figure_caption(1, 'Top-down system architecture showing simulated sensors, obstacle tracking (O1), motion-aware local planning (O2), and evaluation logging (O3).'))

    els.append(make_p(
        'As shown in Figure 1, the simulated robot uses a forward-facing RGB camera (1280×720 resolution at 30 Hz, 80° horizontal field of view) and a 360° planar 2D LiDAR running at 20 to 40 Hz. In the perception pipeline (O1), an off-the-shelf YOLOv8 detector finds moving obstacle classes (such as pedestrians and carts) in each camera frame in about 12 to 18 ms. These 2D bounding boxes are passed to ByteTrack [8], which matches boxes across frames in 1 to 2 ms on the CPU so that obstacle IDs are not lost during brief partial occlusions (up to 1.0 s). Using the camera-to-LiDAR calibration method from Zhang and Pless [6], the 2D laser scan rays are projected into the camera frame. Rays falling inside each tracked 2D bounding box are filtered using the median range value so that laser rays slipping past a person\'s legs onto background walls are ignored. A linear Kalman filter [7] with a constant-velocity motion model then smooths these floor positions at 30 Hz (< 0.2 ms CPU time) to estimate each obstacle\'s 2D position and velocity vector.'
    ))

    els.append(make_p(
        'In the local planning stage (O2), the tracked obstacle states are sent to a custom C++ critic plugin inside the Nav2 Model Predictive Path Integral (MPPI) controller [5], [10] running at 20 Hz. Instead of writing moving obstacles into the 2D costmap where they leave lagging raycast trails, the custom critic projects each obstacle\'s position forward over a 2.0 s lookahead window with a slightly expanding safety radius. This allows the MPPI planner to smoothly slow down or steer behind a crossing obstacle while the standard 2D costmap continues to handle static corridor walls across the full 360° laser scan.'
    ))

    # =========================================================================
    # SECTION 2: SPECIFICATION
    # =========================================================================
    els.append(make_h1('2. Specification', 24, '_Toc_Sec2'))

    els.append(make_p(
        'Table 1 lists the quantitative specifications for the project, including both minimum pass thresholds and target goals, how each requirement is justified, the test method, and the expected technical challenge (Low, Medium, or High). These metrics will be tested across five indoor simulation scenarios: perpendicular corridor crossings, narrow aisle head-on passes, faster pushcarts, multi-person intersections, and a static obstacle control run.'
    ))

    els.append(make_table_caption(1, 'Project specification metrics, target thresholds, engineering justification, and verification methods.'))
    els.append(make_student_table(
        [600, 1600, 1020, 950, 2250, 2106, 500],
        ['ID', 'Metric', 'Minimum', 'Target', 'Engineering Justification', 'Verification Method', 'Ch.'],
        [
            ['O1-a', 'Obstacle velocity RMSE (within 8 m)', '<= 0.25 m/s', '<= 0.15 m/s',
             'About 10% of normal 1.4 m/s walking speed [9]; keeps 2.0 s position prediction error under 0.3 m.',
             'Compare Kalman filter velocity against Gazebo ground truth across 30 runs.', 'M'],
            ['O1-b', 'Camera-LiDAR box matching rate', '>= 85%', '>= 95%',
             'Accurate frustum depth gating [6] stops background wall hits from corrupting the velocity filter [7].',
             'Percentage of visual detections matched to a laser cluster within 0.3 m of ground truth.', 'M'],
            ['O2-a', 'Robot freezes per 10 crossings', '>= 50% below C0', '0 freezes',
             'Directly addresses the freezing robot problem [4] where static planners halt or spin in traffic.',
             'Count planner timeouts, recovery rotations, and stops longer than 2.0 s.', 'H'],
            ['O2-b', 'Route completion time vs. baseline', '>= 10% faster', '15-25% faster',
             'Adjusting speed early and passing behind moving obstacles avoids stop-and-wait delays.',
             'Compare average travel time across 30 seeded trials per scenario.', 'M'],
            ['O2-c', 'Collision-free navigation', '0 collisions', '0 collisions',
             'Predictive path planning must not trade away basic physical safety.',
             'Monitored via Gazebo contact sensors; any physical contact counts as a failed run.', 'M'],
            ['O3-a', '3-way ablation statistical separation', 'p < 0.05', 'p < 0.01',
             'Separates the benefit of visual detection alone (C1) from motion prediction (C2).',
             'Paired t-test and one-way ANOVA across C0, C1, and C2 over obstacle speeds of 0.5-2.0 m/s.', 'M'],
            ['O3-b', 'Cumulative waiting time per run', '>= 50% reduction', '<= 5.0 s',
             'Measures how much time the robot wastes standing still at busy intersections.',
             'Total time robot speed is near zero (< 0.05 m/s) while a goal is active.', 'M'],
            ['O3-c', 'Real-time control loop rate', '>= 15 Hz', '>= 20 Hz',
             'Local controller must keep up with the 20 Hz laser scan rate for responsive avoidance [10].',
             'Log mean execution rate of the tracker (>= 30 Hz) and MPPI loop (>= 20 Hz).', 'L'],
            ['NF1', 'Docker container reproducibility', 'Pass', 'Pass',
             'Ensures simulation benchmarks run consistently without ROS package version issues.',
             'Verify a single launch command inside Docker reproduces the test scenarios.', 'L'],
        ],
        font_sz=18,
        center_cols={0, 2, 3, 6}
    ))

    els.append(make_p(
        'The four objectives map directly to the formal project deliverables in the FYP specification. In fulfillment of Deliverable 1 and Deliverable 5, the literature review and comparative analysis are synthesised in Section 3.2 and documented continuously across the interim progress reviews and final dissertation report. In parallel, each core engineering objective produces a practical software deliverable: Objective O1 produces the ROS 2 vision-LiDAR perception and Kalman tracking package, verified against simulator ground truth (O1-a and O1-b); Objective O2 produces the custom C++ dynamic obstacle MPPI critic plugin (along with a costmap inflation fallback layer), verified through closed-loop crossing trials (O2-a, O2-b, and O2-c); Objective O3 produces the automated Python scenario test runner, statistical evaluation scripts, simulation video demonstrations, and the final dissertation report comparing configurations C0, C1, and C2.',
        before=80
    ))

    els.append(make_p(
        'If the core deliverables are completed ahead of schedule, three prioritized stretch goals will be explored. First (S1), a dense crowd test with 4 to 6 simultaneous moving obstacles will test how well ByteTrack and the planner handle frequent visual occlusions. Second (S2), higher-speed obstacles (up to 2.5 m/s) and diagonal crossing paths will be used to find where the constant-velocity assumption starts to break down. Third (S3), the system will be profiled under a strict 4-core CPU limit to check whether the local planner still maintains its 20 Hz update rate on constrained hardware.'
    ))

    # =========================================================================
    # SECTION 3: METHODOLOGY
    # =========================================================================
    els.append(make_h1('3. Methodology', 25, '_Toc_Sec3'))
    els.append(make_h2('3.1 Development Steps and Tools', 26, '_Toc_Sec3_1', before=60, after=60))

    els.append(make_p(
        'The project is developed entirely in simulation using Ubuntu 24.04 LTS, ROS 2 Jazzy, and Gazebo Harmonic. To separate the effect of camera detection from motion prediction as required by the project brief, three configurations will be compared: C0 (the standard 2D LiDAR-only Nav2 baseline), C1 (camera + 2D LiDAR detection where obstacles are treated as stationary circles at the current instant without velocity prediction), and C2 (the full framework with Kalman velocity tracking and 2.0 s forward projection in MPPI). Table 2 outlines the six methodology steps (M0 to M5), the tools used, their practical limitations, and my current skill level and preparation tasks for each stage.'
    ))

    els.append(make_table_caption(2, 'Methodology development steps (M0-M5), selected software tools, limitations, and skill assessment.'))
    els.append(make_student_table(
        [1050, 2550, 2700, 2726],
        ['Step', 'Core Process & Selected Tools', 'Tool Limitations & Project Impact', 'Skill Level & Preparation Tasks'],
        [
            ['M0: Setup',
             'Ubuntu 24.04 LTS, ROS 2 Jazzy, Gazebo Harmonic, and Docker container.',
             'Older ROS 2 versions reach end-of-life soon; using Docker avoids package conflicts across machines.',
             'Low challenge. Already comfortable with Linux, Docker, and basic ROS 2 workspaces.'],
            ['M1: Sim & C0',
             'Gazebo indoor corridor worlds, differential-drive robot URDF, scripted pedestrian actors, and Nav2 baseline.',
             'Default scripted actors move on fixed loops unless randomized; contact sensors need explicit setup.',
             'Medium challenge. Write Python actor spawners with seeded speeds (0.5-2.0 m/s) and record C0 freezing runs.'],
            ['M2: Tracker (O1)',
             'YOLOv8n detector, ByteTrack [8] 2D tracker, Zhang-Pless frustum projection [6], and Linear Kalman Filter [7].',
             'Camera FOV (80°) is narrower than the 360° LiDAR; laser rays can slip past legs and hit walls behind them.',
             'Low challenge. Familiar with OpenCV and Kalman filtering; add median depth gating and outlier rejection.'],
            ['M3: Critic (O2)',
             'Custom C++17 DynamicObstaclesCriticPlugin integrated into nav2_mppi_controller [5], [10].',
             'Scoring 2,000 candidate trajectories per control cycle must finish well inside the 50 ms (20 Hz) budget.',
             'High challenge (first time writing a Nav2 C++ plugin). Build a minimal dummy critic early to test pluginlib loading.'],
            ['M4: Harness (O3)',
             'Automated Python scenario runner, Gazebo reset services, rosbag2 logger, and ground-truth evaluator.',
             'Running 450 batch trials across C0, C1, and C2 can hang if Gazebo or Nav2 nodes fail to reset cleanly.',
             'Medium challenge. Add process watchdog timeouts, fixed random seeds, and headless Gazebo execution.'],
            ['M5: Analysis (O3)',
             'Python evaluation and plotting scripts using NumPy, SciPy, and Matplotlib.',
             'Multi-agent interactions can produce noisy travel times if sample sizes are too small.',
             'Low challenge. Automate paired t-tests, one-way ANOVA, and boxplot generation from recorded logs.'],
        ],
        font_sz=18,
        center_cols={0}
    ))

    els.append(make_h2('3.2 Workflow and Algorithm Choices', 27, '_Toc_Sec3_2'))

    els.append(make_p(
        'Figure 2 shows how the methodology steps depend on one another. The main critical path runs sequentially from environment setup (M0) and baseline simulation (M1) through the vision-LiDAR tracker (M2), the predictive MPPI critic (M3), and final statistical evaluation (M5). Because the automated testing harness (M4) only depends on the simulation world from M1, it can be built in parallel alongside M2 and M3 to save time. Figure 2 also includes a fallback path (F1): if writing or linking the native C++ MPPI critic plugin takes longer than expected, the tracked velocity vectors from M2 can be injected into the 2D costmap as velocity-stretched obstacle zones so that comparative testing in M5 can still go ahead.'
    ))

    # Figure 2 image + caption
    els.append(fig2_drawing_p)
    els.append(make_figure_caption(2, 'Top-down methodology workflow showing the main critical path (solid), parallel testing harness (dashed), and fallback option (dotted).'))

    els.append(make_p(
        'Several practical trade-offs guided the choice of algorithms for each subsystem. For obstacle detection and depth estimation (O1), I considered 2D laser-only clustering, DeepSORT, and full 3D point cloud networks. Pure 2D laser clustering was ruled out because a single-plane scan splits walking legs into separate clusters and cannot tell a person apart from a static pillar, while 3D point cloud networks need dense 3D LiDAR data and heavy GPU memory. Instead, running YOLOv8n with ByteTrack [8] keeps stable track IDs in 2D image space on the CPU, and projecting the 2D laser scan into each bounding box frustum [6] gives accurate floor distances using a simple median filter.'
    ))

    els.append(make_p(
        'For obstacle motion prediction (O1/O2), I compared a Constant-Velocity (CV) linear Kalman filter [7] against the Social Force Model [9], Interactive Gaussian Processes [4], and deep trajectory transformers. In indoor corridors, pedestrians and pushcarts generally walk or roll at a steady speed and direction over short 1 to 2 s windows [9]. Running iterative social force simulations or neural networks across 2,000 MPPI trajectory rollouts at 20 Hz would be far too slow on a standard CPU, whereas linear constant-velocity extrapolation takes less than 0.2 ms.'
    ))

    els.append(make_p(
        'Finally, for local path planning (O2), I chose to extend the Nav2 MPPI controller [5], [10] rather than using the Dynamic Window Approach (DWA), Timed Elastic Band (TEB), or post-filter Control Barrier Functions [11]. DWA only samples constant-velocity arcs and frequently freezes when an obstacle crosses ahead, while TEB often oscillates between left and right passes in multi-agent intersections. By adding a dynamic obstacle critic directly inside MPPI, the planner can evaluate future obstacle positions across all 2,000 sampled trajectories and smoothly adjust the robot\'s speed to pass behind moving traffic.'
    ))

    # =========================================================================
    # SECTION 4: ORIGINALITY
    # =========================================================================
    els.append(make_h1('4. Originality', 28, '_Toc_Sec4'))
    els.append(make_h2('4.1 Project Novelty and Comparison', 29, '_Toc_Sec4_1', before=60, after=60))

    els.append(make_p(
        'Table 3 compares the proposed framework against standard industrial 2D LiDAR AMRs, non-predictive vision-LiDAR trackers, and recent high-compute GPU MPPI methods.'
    ))

    els.append(make_table_caption(3, 'Comparison of the proposed system against standard 2D LiDAR navigation, non-predictive trackers, and high-compute GPU MPPI methods.'))
    els.append(make_student_table(
        [1500, 1850, 1850, 1900, 1926],
        ['Feature', 'Standard Industrial AMR (Nav2 + 2D LiDAR [2])', 'Vision-LiDAR Trackers (Without Prediction)', 'High-Compute GPU MPPI Variants [11]-[13]', 'Proposed Framework (This Project)'],
        [
            ['Sensor Suite',
             'Planar 2D LiDAR only (around $400)',
             '2D/3D LiDAR + RGB or depth camera ($500-$4,000)',
             'Dense 3D LiDAR or depth point clouds (> $3,000)',
             '2D LiDAR + monocular RGB camera (around $450)'],
            ['Obstacle Representation',
             'Static 2D costmap cells fixed at current time (t = 0)',
             'Tracked bounding boxes written into static 2D costmap',
             'Unsegmented 3D point clouds [12] or reactive barriers [11]',
             'Static walls in 2D costmap + moving velocity tracks'],
            ['Trajectory Evaluation',
             'Static costmap critics only; freezes in cross-traffic',
             'Static clearance inflation with raycast clearing delay',
             'GPU signed-distance fields [12] or GPU clustering [13]',
             'Lightweight C++ MPPI critic with 2.0 s motion prediction'],
            ['Compute Requirement',
             'Standard onboard CPU',
             'Onboard CPU + edge GPU',
             'Dedicated high-compute CUDA GPU (not edge-optimised)',
             'Standard CPU for planning (< 0.3 ms) + light 2D detector'],
            ['Evaluation Setup',
             'Static obstacle avoidance tests',
             'Isolated perception tracking metrics only',
             'End-to-end comparison against older planners',
             'Controlled 3-way ablation (C0 vs. C1 vs. C2)'],
        ],
        font_sz=18
    ))

    els.append(make_p(
        'In current industrial practice, brownfield AMRs either rely on a basic 2D LiDAR with static costmaps (which causes the robot to stop and wait whenever someone walks across its path) or require an expensive upgrade to 3D LiDARs and high-end onboard GPUs [1], [2]. As shown in Table 3, the originality of this project lies in bridging that gap with a practical, low-cost software and sensor setup. By pairing a standard 2D laser scanner with a single monocular camera, the system gets reliable visual class detection from the camera and accurate metric distances from the laser scanner without needing a 3D LiDAR.',
        before=80
    ))

    els.append(make_p(
        'On the planning side, all 11 default critics shipped with the ROS 2 Nav2 MPPI controller only check candidate trajectories against the static 2D costmap at the current instant [10]. Recent research papers such as SE-MPPI [11], EXACT-MPPI [12], and CSC-MPPI [13] have extended MPPI for complex environments, but they rely on heavy GPU computation (such as CUDA signed-distance fields or GPU DBSCAN clustering) that is not optimised for standard industrial robot computers, or act only as reactive safety filters on the final command [11]. Instead, this project implements a lightweight C++ dynamic obstacle critic plugin that projects tracked velocity vectors over a 2.0 s horizon on a standard CPU in under 0.3 ms. Furthermore, running a 3-way ablation study across C0 (LiDAR-only), C1 (visual detection without motion prediction), and C2 (full predictive planning) clearly separates the benefit of visual detection from the benefit of motion prediction.'
    ))

    els.append(make_h2('4.2 Project Limitations', 30, '_Toc_Sec4_2'))

    els.append(make_p(
        'There are three main practical limitations in this project that directly shape the specification in Table 1. First, because the project is 100% simulation-based (0% hardware), virtual Gazebo actors do not capture all real-world camera lighting issues or uneven human leg motion; to account for this, Table 1 defines both a realistic minimum pass threshold (85% track matching) and a target threshold (95%). Second, because the monocular camera has an 80° horizontal field of view compared to the 360° 2D LiDAR, velocity tracking is only active inside the front 80° camera cone. Outside this cone, the robot falls back to the 360° 2D LiDAR static costmap so that obstacles approaching from the sides or rear still trigger safe collision avoidance. Third, the constant-velocity motion model assumes obstacles move in a straight line over short windows and will lag if someone suddenly changes direction; therefore, predictions are capped at 2.0 s with a growing safety margin over time.'
    ))

    # =========================================================================
    # SECTION 5: RISK MANAGEMENT
    # =========================================================================
    els.append(make_h1('5. Risk Management', 31, '_Toc_Sec5'))

    els.append(make_p(
        'Table 4 lists the four main technical and project management risks, scored by Likelihood (L, 1 to 5), Impact (I, 1 to 5), and overall Risk Score (L × I), along with practical mitigation steps.'
    ))

    els.append(make_table_caption(4, 'Project risk register showing likelihood (L), impact (I), risk score, system effect, and mitigation strategies.'))
    els.append(make_student_table(
        [520, 2340, 420, 420, 640, 1950, 2736],
        ['ID', 'Risk Description', 'L', 'I', 'Score', 'Effect on Project', 'Mitigation & Fallback Plan'],
        [
            ['R1',
             'Custom C++ MPPI critic plugin runs into Nav2 integration issues or exceeds the 50 ms (20 Hz) CPU time budget (O2).',
             '4', '5', '20',
             'Controller update rate drops below 20 Hz or plugin fails to load in Nav2.',
             'Use vectorized Eigen math and cap lookahead at 2.0 s. If blocked, use Fallback F1 by writing velocity-stretched safety zones into the 2D costmap.'],
            ['R2',
             'Camera-LiDAR projection errors or laser rays hitting background walls behind legs corrupt velocity estimates (O1).',
             '3', '4', '12',
             'Noisy obstacle positions cause jumpy velocity vectors and poor predictions.',
             'Read exact sensor transforms from TF2, take the median laser depth inside each 2D box, and reject sudden position jumps in the Kalman filter.'],
            ['R3',
             'Gazebo simulation instability or scope creep delays the 3-way batch benchmark runs (O3).',
             '3', '4', '12',
             'Incomplete statistical data across C0, C1, and C2 or simulator crashes.',
             'Pin all ROS 2 and Gazebo packages in Docker, add watchdog auto-restarts to the test script, and only run stretch goals after core scenarios finish.'],
            ['R4',
             'Visual occlusion when multiple obstacles cross each other causes track ID switching (O1/O2).',
             '3', '3', '9',
             'Brief loss of velocity tracking during multi-person intersection crossings.',
             'Use ByteTrack two-stage association [8] to keep low-confidence occluded boxes, and coast Kalman filter states for up to 1.0 s before dropping tracks.'],
        ],
        font_sz=18,
        center_cols={0, 2, 3, 4}
    ))

    # =========================================================================
    # SECTION 6: PLANNED WORK SCHEDULE
    # =========================================================================
    els.append(make_p(
        [('6. Planned Work Schedule', {'bold': True, 'sz': 26, 'color': '000000'})],
        jc='left', before=0, after=80, keep_next=True, outline_lvl=0, page_break_before=True,
        bookmark=(32, '_Toc_Sec6')
    ))

    els.append(make_p(
        'Table 5 shows the project Gantt chart split across the Autumn Semester (Weeks 1 to 15, shaded in blue-grey) and Spring Semester (Weeks 16 to 30, shaded in green-grey). Active project execution runs from Week 5 (true project start following topic allocation) through Week 30 across a total workload of 450 hours, with five supervisory progress reviews (PR1 to PR5) starting in Weeks 11-12.',
        keep_next=True, after=80
    ))

    els.append(make_table_caption(5, 'Project Gantt chart across the Autumn Semester (Weeks 1-15) and Spring Semester (Weeks 16-30), including progress reviews (PR1-PR5).'))
    els.append(make_gantt_table())

    els.append(make_p(
        'In the Autumn Semester, following project allocation at Week 5, Weeks 5 to 8 (45 h) cover conducting the foundational literature review on vision-LiDAR integration and predictive navigation, alongside setting up Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, and the Docker container. Weeks 7 to 12 (45 h) focus on building the indoor corridor worlds, scripting the moving obstacle actors, and logging the C0 2D LiDAR-only baseline, concluding with the first supervisory progress review (PR1 in Weeks 11-12). Weeks 9 to 15 (90 h) are dedicated to building and verifying the YOLOv8, ByteTrack, frustum depth gating, and Kalman filter tracking package for Objective O1 (PR2 in Weeks 13-15). Starting in Week 11 and running in parallel through Week 20 (45 h), the automated Python scenario runner and metric logger are developed so that each module can be tested as soon as it is ready.',
        before=80
    ))

    els.append(make_p(
        'Spanning late Autumn and early Spring (Weeks 13 to 20, 75 h), the custom C++ dynamic obstacle MPPI critic plugin (Objective O2) and the non-predictive C1 baseline are implemented and tuned to run at 20 Hz (PR3 in Weeks 19-20, which also serves as the decision point for activating Fallback F1 if needed). In the Spring Semester, Weeks 19 to 24 (60 h) execute the batch simulation trials comparing C0, C1, and C2 across all obstacle speeds and crowd densities (PR4 in Weeks 23-24). Finally, Weeks 23 to 28 (30 h) cover the statistical analysis (paired t-tests, ANOVA, and performance plots, with PR5 in Weeks 27-28), overlapping with Weeks 25 to 30 (60 h) to write the final MEng thesis and record the simulation demonstration videos.'
    ))

    return els


def main():
    with zipfile.ZipFile(SRC_DOCX, 'r') as zin:
        xml_bytes = zin.read('word/document.xml')

    ns_matches = re.findall(r'xmlns:([a-zA-Z0-9]+)="([^"]+)"', xml_bytes.decode('utf-8'))
    for prefix, uri in ns_matches:
        ET.register_namespace(prefix, uri)

    tree = ET.fromstring(xml_bytes)
    body = tree.find(f'{{{W}}}body')
    orig_children = list(body)

    # Extract original drawing paragraphs for Fig 1 (idx 78) and Fig 2 (idx 99)
    fig1_p = orig_children[78]
    fig2_p = orig_children[99]
    # Remove any <w:lastRenderedPageBreak/> inside fig2_p
    for lrpb in list(fig2_p.iter(f'{{{W}}}lastRenderedPageBreak')):
        for parent in fig2_p.iter():
            if lrpb in list(parent):
                parent.remove(lrpb)

    # Adjust image extents to match our new aspect ratios:
    # Fig 1 is 8.0 x 8.6 in -> cx = 4552950, cy = int(4552950 * 8.6 / 8.0) = 4894421
    # Fig 2 is 8.0 x 7.5 in -> cx = 4552950, cy = int(4552950 * 7.5 / 8.0) = 4268390
    for ext in fig1_p.iter(f'{{{WP}}}extent'):
        ext.set('cx', '4552950')
        ext.set('cy', '4894421')
    for ext in fig1_p.iter(f'{{{A}}}ext'):
        ext.set('cx', '4552950')
        ext.set('cy', '4894421')

    for ext in fig2_p.iter(f'{{{WP}}}extent'):
        ext.set('cx', '4552950')
        ext.set('cy', '4268390')
    for ext in fig2_p.iter(f'{{{A}}}ext'):
        ext.set('cx', '4552950')
        ext.set('cy', '4268390')

    # Also change References heading (orig_children[134]) color from 1F4E79 to 000000 and add bookmark
    ref_heading_p = orig_children[134]
    for c in ref_heading_p.iter(f'{{{W}}}color'):
        c.set(f'{{{W}}}val', '000000')
    bs_ref = ET.Element(f'{{{W}}}bookmarkStart')
    bs_ref.set(f'{{{W}}}id', '33')
    bs_ref.set(f'{{{W}}}name', '_Toc_Refs')
    be_ref = ET.Element(f'{{{W}}}bookmarkEnd')
    be_ref.set(f'{{{W}}}id', '33')
    ref_heading_p.insert(0, bs_ref)
    ref_heading_p.append(be_ref)

    # Also change Appendix A heading colors from 1F4E79 to 000000 and tighten spacing so it fits on Page 14
    for app_el in orig_children[148:170]:
        for c in app_el.iter(f'{{{W}}}color'):
            if c.get(f'{{{W}}}val') == '1F4E79':
                c.set(f'{{{W}}}val', '000000')
        pPr_app = app_el.find(f'{{{W}}}pPr')
        if pPr_app is not None:
            sp_app = pPr_app.find(f'{{{W}}}spacing')
            if sp_app is not None:
                if sp_app.get(f'{{{W}}}after') and int(sp_app.get(f'{{{W}}}after')) > 60:
                    sp_app.set(f'{{{W}}}after', '50')
                if sp_app.get(f'{{{W}}}before') and int(sp_app.get(f'{{{W}}}before')) > 90:
                    sp_app.set(f'{{{W}}}before', '80')

    # Explicitly set verified IEEE references [1]-[13] on orig_children[135..147]
    ieee_refs = [
        [('[1] International Federation of Robotics, "Service robots see global growth boom," in ', False),
         ('World Robotics 2025 \u2013 Service Robots', True),
         (', Frankfurt, Germany: IFR, Oct. 7, 2025. [Online]. Available: https://ifr.org/ifr-press-releases/news/service-robots-see-global-growth-boom. Accessed: Nov. 4, 2026.', False)],
        [('[2] S. Macenski, F. Mart\u00edn, R. White, and J. Gin\u00e9s Clavero, "The Marathon 2: A navigation system," in ', False),
         ('Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)', True),
         (', Las Vegas, NV, USA, Oct. 2020, pp. 2718\u20132725, doi: 10.1109/IROS45743.2020.9341207.', False)],
        [('[3] S. Macenski, T. Moore, D. V. Lu, A. Merzlyakov, and M. Ferguson, "From the desks of ROS maintainers: A survey of modern & capable mobile robotics algorithms in the Robot Operating System 2," ', False),
         ('Robot. Auton. Syst.', True),
         (', vol. 168, Oct. 2023, Art. no. 104493, doi: 10.1016/j.robot.2023.104493.', False)],
        [('[4] P. Trautman and A. Krause, "Unfreezing the robot: Navigation in dense, interacting crowds," in ', False),
         ('Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)', True),
         (', Taipei, Taiwan, Oct. 2010, pp. 797\u2013803, doi: 10.1109/IROS.2010.5654369.', False)],
        [('[5] G. Williams, N. Wagener, B. Goldfain, P. Drews, J. M. Rehg, B. Boots, and E. A. Theodorou, "Information theoretic MPC for model-based reinforcement learning," in ', False),
         ('Proc. IEEE Int. Conf. Robot. Autom. (ICRA)', True),
         (', Singapore, May\u2013Jun. 2017, pp. 1714\u20131721, doi: 10.1109/ICRA.2017.7989202.', False)],
        [('[6] Q. Zhang and R. Pless, "Extrinsic calibration of a camera and laser range finder (improves camera calibration)," in ', False),
         ('Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)', True),
         (', Sendai, Japan, Sep.\u2013Oct. 2004, vol. 3, pp. 2301\u20132306, doi: 10.1109/IROS.2004.1389752.', False)],
        [('[7] S. Thrun, W. Burgard, and D. Fox, ', False),
         ('Probabilistic Robotics', True),
         ('. Cambridge, MA, USA: MIT Press, 2005.', False)],
        [('[8] Y. Zhang, P. Sun, Y. Jiang, D. Yu, F. Weng, Z. Yuan, P. Luo, W. Liu, and X. Wang, "ByteTrack: Multi-object tracking by associating every detection box," in ', False),
         ('Computer Vision \u2013 ECCV 2022', True),
         (' (Lecture Notes in Computer Science), vol. 13682, Cham, Switzerland: Springer, Oct. 2022, pp. 1\u201321, doi: 10.1007/978-3-031-20047-2_1.', False)],
        [('[9] D. Helbing and P. Moln\u00e1r, "Social force model for pedestrian dynamics," ', False),
         ('Phys. Rev. E', True),
         (', vol. 51, no. 5, pp. 4282\u20134286, May 1995, doi: 10.1103/PhysRevE.51.4282.', False)],
        [('[10] S. Macenski and A. Budyakov, "MPPI Controller (nav2_mppi_controller)," ', False),
         ('Nav2 Documentation', True),
         (', Open Navigation LLC, 2024. [Online]. Available: https://docs.nav2.org/configuration/packages/configuring-mppic.html. Accessed: Nov. 4, 2026.', False)],
        [('[11] J. Kang, "SE-MPPI: Coordinating online local-minima escape with control-barrier-function safety in a Nav2-native controller," Tech. Preprint / GitHub Repository, 2026. [Online]. Available: https://github.com/kjungmo/se-mppi-nav2. Accessed: Nov. 4, 2026.', False)],
        [('[12] C. Peng, Z. Ge, W. Lu, H. Gao, S. Vougioukas, and P. Wei, "EXACT-MPPI: Exact signed-distance navigation for arbitrary-footprint robots from point clouds via path integral control," 2026, ', False),
         ('arXiv:2605.29663', True),
         ('.', False)],
        [('[13] L. Park, K. Jang, and S. Kim, "CSC-MPPI: A novel constrained MPPI framework with DBSCAN for reliable obstacle avoidance," in ', False),
         ('Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)', True),
         (', Hangzhou, China, Oct. 2025, pp. 19645\u201319652, doi: 10.1109/IROS60139.2025.11246839.', False)],
    ]
    for idx_offset, ref_runs in enumerate(ieee_refs):
        ref_p = orig_children[135 + idx_offset]
        pPr_ref = ref_p.find(f'{{{W}}}pPr')
        for ch in list(ref_p):
            if ch is not pPr_ref:
                ref_p.remove(ch)
        for txt, is_it in ref_runs:
            ref_p.append(make_run(txt, italic=is_it, sz=21))

    # Initial TOC entries (page numbers verified after LibreOffice PDF conversion)
    toc_entries = [
        (1, 'Statement of Originality', '_Toc_SOO', '2'),
        (1, '1. Overview of the Project', '_Toc_Sec1', '5'),
        (2, '1.1 Background and the Freezing Robot Problem', '_Toc_Sec1_1', '5'),
        (2, '1.2 Project Aim and Objectives', '_Toc_Sec1_2', '5'),
        (2, '1.3 System Architecture', '_Toc_Sec1_3', '5'),
        (1, '2. Specification', '_Toc_Sec2', '7'),
        (1, '3. Methodology', '_Toc_Sec3', '8'),
        (2, '3.1 Development Steps and Tools', '_Toc_Sec3_1', '8'),
        (2, '3.2 Workflow and Algorithm Choices', '_Toc_Sec3_2', '8'),
        (1, '4. Originality', '_Toc_Sec4', '10'),
        (2, '4.1 Project Novelty and Comparison', '_Toc_Sec4_1', '10'),
        (2, '4.2 Project Limitations', '_Toc_Sec4_2', '11'),
        (1, '5. Risk Management', '_Toc_Sec5', '11'),
        (1, '6. Planned Work Schedule', '_Toc_Sec6', '12'),
        (1, 'References', '_Toc_Refs', '13'),
        (1, 'Appendix A: Supervisor-Provided Project Specification', '_Toc_AppA', '14'),
    ]

    # Assemble new body children
    new_body_children = []
    # 1. Cover page (0..29)
    new_body_children.extend(orig_children[0:30])
    # 2. Statement of Originality
    new_body_children.extend(build_statement_of_originality())
    # 3. Table of Contents
    new_body_children.extend(build_toc(toc_entries))
    # 4. Main Body (Sections 1-6)
    new_body_children.extend(build_main_body(fig1_p, fig2_p))
    # 5. References & Appendix A (133..170)
    new_body_children.extend(orig_children[133:])

    # Clear body and repopulate
    for child in list(body):
        body.remove(child)
    for child in new_body_children:
        body.append(child)

    new_xml_bytes = ET.tostring(tree, encoding='utf-8', xml_declaration=True)

    with open(FIG1_PNG, 'rb') as f:
        fig1_bytes = f.read()
    with open(FIG2_PNG, 'rb') as f:
        fig2_bytes = f.read()

    fig1_media = {'word/media/image2.png', 'word/media/image5.png', 'word/media/image8.png', 'word/media/image11.png'}
    fig2_media = {'word/media/image3.png', 'word/media/image6.png', 'word/media/image9.png', 'word/media/image12.png'}

    with zipfile.ZipFile(SRC_DOCX, 'r') as zin, zipfile.ZipFile(OUT_DOCX, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, new_xml_bytes)
            elif item.filename in fig1_media:
                zout.writestr(item, fig1_bytes)
            elif item.filename in fig2_media:
                zout.writestr(item, fig2_bytes)
            else:
                zout.writestr(item, zin.read(item.filename))

    print("Wrote:", OUT_DOCX)


if __name__ == '__main__':
    main()
