import os
import subprocess
import html
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def generate_docx():
    doc = docx.Document()
    
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # Header
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("Department of Computer Engineering (Software Engineering)\n")
    r_dept.font.size = Pt(14)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_dept.add_run("Web Technology Laboratory — Academic Year 2026-27\n")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Practical No. 04: Server-Side Web Application using Core Node.js HTTP Module")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(37, 99, 235)

    # Metadata Table
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        [("Name:", "Sarthak Bhosale"), ("PRN:", "202401100051")],
        [("Batch:", "TY SE-A2"), ("Roll No:", "A50")]
    ]
    for row_idx, row in enumerate(meta_data):
        col_offset = 0
        for label, val in row:
            cell_lbl = meta_table.cell(row_idx, col_offset)
            cell_val = meta_table.cell(row_idx, col_offset + 1)
            cell_lbl.text = label
            cell_lbl.paragraphs[0].runs[0].font.bold = True
            cell_lbl.paragraphs[0].runs[0].font.color.rgb = RGBColor(71, 85, 105)
            cell_val.text = val
            cell_val.paragraphs[0].runs[0].font.bold = True
            cell_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(15, 23, 42)
            set_cell_bg(cell_lbl, "F1F5F9")
            set_cell_bg(cell_val, "FFFFFF")
            set_cell_margins(cell_lbl, 80, 80, 100, 100)
            set_cell_margins(cell_val, 80, 80, 100, 100)
            col_offset += 2

    doc.add_paragraph()

    def add_section_heading(num_str, title_str):
        h = doc.add_paragraph()
        r = h.add_run(f"{num_str}. {title_str}")
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        return h

    def add_code_block(title, code_str):
        p_t = doc.add_paragraph()
        r_t = p_t.add_run(title)
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(37, 99, 235)
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_bg(cell, "0F172A")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        r = p.add_run(code_str)
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(241, 245, 249)
        doc.add_paragraph()

    # 1. Aim
    add_section_heading("1", "Aim")
    doc.add_paragraph(
        "To design, develop, test, and deploy a high-performance server-side web application for the TaskGravity system "
        "using core Node.js built-in modules (http, url, path, fs), implementing asynchronous non-blocking I/O, custom HTTP "
        "route dispatching, streaming request body parsing, in-memory data persistence, and static asset serving."
    )

    # 2. Problem Statement
    add_section_heading("2", "Problem Statement")
    doc.add_paragraph(
        "While modern web frameworks abstract low-level HTTP handling, mastering core server-side networking fundamentals "
        "is critical for building resilient distributed systems. Implement a server application without external web frameworks "
        "capable of handling REST API routes (GET, POST, PUT, DELETE for tasks, and GET /health), parsing chunked HTTP request "
        "buffers into JSON objects, validating task input fields, and serving static frontend dashboard assets with correct MIME types."
    )

    # 3. Theory & Concept Review
    add_section_heading("3", "Theory & Concept Review")
    doc.add_paragraph(
        "3.1 Node.js Event-Driven Architecture & Event Loop\n"
        "Node.js runs on the V8 JavaScript engine and utilizes a single-threaded event loop paired with libuv worker threads. "
        "This allows high-concurrency I/O operations without multi-threading overhead by dispatching asynchronous system calls "
        "and invoking callbacks upon completion."
    )
    doc.add_paragraph(
        "3.2 Core HTTP Server & Streams\n"
        "In Node's http module, http.createServer((req, res) => {...}) receives IncomingMessage and ServerResponse streams. "
        "Incoming POST/PUT payloads arrive as streamed chunks via req.on('data', chunk) and req.on('end', callback), "
        "requiring manual buffer concatenation and JSON parsing."
    )
    doc.add_paragraph(
        "3.3 MIME Type Resolution & Static File Serving\n"
        "Static file delivery uses fs.readFile / fs.createReadStream alongside path.extname to match file extensions "
        "(.html, .css, .js, .json) to their IANA standard Content-Type headers, returning 404 Not Found on missing assets."
    )

    # 4. Software & Hardware Requirements
    add_section_heading("4", "Software & Hardware Requirements")
    req_table = doc.add_table(rows=5, cols=2)
    req_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    req_data = [
        ("Operating System", "Microsoft Windows 11 x64 / Linux x64 (Render Cloud)"),
        ("Runtime & Package Manager", "Node.js v20.x, npm v10.x"),
        ("Core Modules Used", "http, fs, path, url (zero external web framework dependencies)"),
        ("Testing Tools", "Google Chrome, Postman, PowerShell Invoke-RestMethod"),
        ("Cloud Hosting & Version Control", "Render Web Service (PaaS), Git, GitHub")
    ]
    for idx, (lbl, val) in enumerate(req_data):
        c1, c2 = req_table.cell(idx, 0), req_table.cell(idx, 1)
        c1.text = lbl
        c1.paragraphs[0].runs[0].font.bold = True
        c2.text = val
        set_cell_bg(c1, "F8FAFC")
        set_cell_bg(c2, "FFFFFF")
        set_cell_margins(c1, 80, 80, 100, 100)
        set_cell_margins(c2, 80, 80, 100, 100)
    doc.add_paragraph()

    # 5. Design & Architectural Implementation
    add_section_heading("5", "Design & Architectural Implementation")
    doc.add_paragraph(
        "1. Server Initialization: Create HTTP server listening on process.env.PORT || 5000.\n"
        "2. Route Dispatcher: Inspect req.method and req.url parsed via url.parse.\n"
        "3. Body Buffer Aggregator: Helper parseBody(req) returns a Promise resolving parsed JSON from data/end stream events.\n"
        "4. Validation Layer: validator.js ensures title (min 3 chars), priority (Low/Medium/High), and status (todo/in-progress/done).\n"
        "5. In-Memory Store: Dynamic task repository supporting initial seed tasks, ID generation, and thread-safe CRUD mutations.\n"
        "6. Static Delivery: URLs starting with '/' and not matching '/api' are routed to the public/ folder with MIME headers."
    )

    # 6. Source Code
    add_section_heading("6", "Source Code Implementation")
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical4"
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    server_js = read_code("server.js")
    validator_js = read_code("validator.js")
    app_js = read_code(r"public\app.js")
    index_html = read_code(r"public\index.html")

    add_code_block("6.1 server.js (Core Node.js HTTP Server, Router & Static Handler)", server_js)
    add_code_block("6.2 validator.js (Payload Validation Module)", validator_js)
    add_code_block("6.3 public/app.js (Client-Side API Integration Controller)", app_js)
    add_code_block("6.4 public/index.html (TaskGravity Minimalist UI Dashboard)", index_html)

    # 7. Verification & Test Results
    add_section_heading("7", "Verification & Test Results")
    test_table = doc.add_table(rows=6, cols=3)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Test Case / Endpoint", "Observed Behavior & Response", "Status"]
    for c_idx, h in enumerate(test_headers):
        cell = test_table.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 100, 100)
    
    tests = [
        ("GET /api/tasks", "Returns HTTP 200 OK with JSON array of active tasks and Content-Type: application/json.", "Passed"),
        ("POST /api/tasks", "Buffers incoming stream, validates schema, assigns UUID/ID, returns HTTP 201 Created.", "Passed"),
        ("Validation Failure", "Submitting empty title or invalid priority returns HTTP 400 Bad Request with field error message.", "Passed"),
        ("PUT /api/tasks/:id", "Updates existing task fields and timestamp, returns HTTP 200 OK with updated record.", "Passed"),
        ("DELETE /api/tasks/:id", "Removes task by ID from memory, returns HTTP 200 OK confirmation.", "Passed")
    ]
    for r_idx, row in enumerate(tests, start=1):
        for c_idx, val in enumerate(row):
            cell = test_table.cell(r_idx, c_idx)
            cell.text = val
            if c_idx == 2:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_bg(cell, "DCFCE7")
            else:
                set_cell_bg(cell, "FFFFFF")
            set_cell_margins(cell, 80, 80, 100, 100)
    doc.add_paragraph()

    # 8. Conclusion
    add_section_heading("8", "Conclusion")
    doc.add_paragraph(
        "Practical 04 successfully demonstrates the fundamentals of server-side web engineering using core Node.js built-in modules. "
        "By constructing a complete REST server without third-party frameworks, key concepts including event-driven stream parsing, "
        "manual route dispatching, MIME header synthesis, and asynchronous validation were thoroughly verified. The application "
        "operates efficiently with zero external web dependencies and has been deployed to Render Cloud as a live web service."
    )

    # Links Box
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(14)
    tbl_links = doc.add_table(rows=1, cols=1)
    tbl_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_links = tbl_links.cell(0, 0)
    set_cell_bg(c_links, "F8FAFC")
    set_cell_margins(c_links, 120, 120, 150, 150)
    p_l = c_links.paragraphs[0]
    r_lh = p_l.add_run("Project Links & Deployment Information:\n")
    r_lh.font.bold = True
    r_lh.font.size = Pt(11)
    r_lh.font.color.rgb = RGBColor(15, 23, 42)

    r_gh = p_l.add_run("GitHub Link / Code Link: ")
    r_gh.font.bold = True
    p_l.add_run("https://github.com/Sarthak-1229/taskgravity-practical-04\n")

    r_live = p_l.add_run("Live Deployment Link: ")
    r_live.font.bold = True
    p_l.add_run("https://taskgravity-practical-04.onrender.com")

    docx_path = r"D:\_TY\Web-Tech\Practicals\Practical4\Practical_04_Report.docx"
    doc.save(docx_path)
    print(f"Generated DOCX: {docx_path}")

def generate_pdf():
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical4"
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    server_js = html.escape(read_code("server.js"))
    validator_js = html.escape(read_code("validator.js"))
    app_js = html.escape(read_code(r"public\app.js"))
    index_html = html.escape(read_code(r"public\index.html"))

    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Practical 04 Report - Sarthak Bhosale</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}
  .header {{
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }}
  .dept-title {{
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.2px;
    text-transform: uppercase;
  }}
  .sub-title {{
    font-size: 10pt;
    font-weight: 600;
    color: #64748b;
    margin-top: 2px;
  }}
  .prac-title {{
    font-size: 14pt;
    font-weight: 800;
    color: #2563eb;
    margin-top: 8px;
  }}
  .meta-grid {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 9.5pt;
  }}
  .meta-grid td {{
    border: 1px solid #cbd5e1;
    padding: 6px 10px;
  }}
  .meta-grid .lbl {{
    background-color: #f1f5f9;
    font-weight: 700;
    color: #475569;
    width: 15%;
  }}
  .meta-grid .val {{
    font-weight: 700;
    color: #0f172a;
    width: 35%;
  }}
  h2.sec-title {{
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  h3.subsec-title {{
    font-size: 10pt;
    font-weight: 700;
    color: #2563eb;
    margin-top: 14px;
    margin-bottom: 4px;
  }}
  p, li {{
    font-size: 9.5pt;
    color: #334155;
    text-align: justify;
    margin-top: 4px;
    margin-bottom: 6px;
  }}
  ul, ol {{
    padding-left: 20px;
    margin-top: 4px;
    margin-bottom: 8px;
  }}
  .code-block {{
    background-color: #0f172a;
    color: #f8fafc;
    font-family: "Consolas", "Fira Code", monospace;
    font-size: 8pt;
    line-height: 1.4;
    padding: 10px 14px;
    border-radius: 4px;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 8px 0 14px 0;
  }}
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9pt;
  }}
  .data-table th, .data-table td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }}
  .data-table th {{
    background-color: #f8fafc;
    font-weight: 700;
    color: #0f172a;
  }}
  .badge-pass {{
    color: #15803d;
    font-weight: 700;
    background-color: #dcfce7;
    padding: 2px 6px;
    border-radius: 3px;
    display: inline-block;
  }}
  .links-box {{
    margin-top: 20px;
    padding: 12px 14px;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #2563eb;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  .links-box a {{
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="dept-title">Department of Computer Engineering (Software Engineering)</div>
  <div class="sub-title">Web Technology Laboratory — Academic Year 2026-27</div>
  <div class="prac-title">Practical No. 04: Server-Side Web Application using Core Node.js HTTP Module</div>
</div>

<table class="meta-grid">
  <tr>
    <td class="lbl">Name:</td>
    <td class="val">Sarthak Bhosale</td>
    <td class="lbl">PRN:</td>
    <td class="val">202401100051</td>
  </tr>
  <tr>
    <td class="lbl">Batch:</td>
    <td class="val">TY SE-A2</td>
    <td class="lbl">Roll No:</td>
    <td class="val">A50</td>
  </tr>
</table>

<h2 class="sec-title">1. Aim</h2>
<p>
To design, develop, test, and deploy a high-performance server-side web application for the TaskGravity system using core Node.js built-in modules (<code>http</code>, <code>url</code>, <code>path</code>, <code>fs</code>), implementing asynchronous non-blocking I/O, custom HTTP route dispatching, streaming request body parsing, in-memory data persistence, and static asset serving.
</p>

<h2 class="sec-title">2. Problem Statement</h2>
<p>
While modern web frameworks abstract low-level HTTP handling, mastering core server-side networking fundamentals is critical for building resilient distributed systems. Implement a server application without external web frameworks capable of handling REST API routes (GET, POST, PUT, DELETE for tasks, and GET /health), parsing chunked HTTP request buffers into JSON objects, validating task input fields, and serving static frontend dashboard assets with correct MIME types.
</p>

<h2 class="sec-title">3. Theory & Concept Review</h2>
<p>
<strong>3.1 Node.js Event-Driven Architecture & Event Loop:</strong> Node.js operates on the V8 engine and libuv, executing a single-threaded non-blocking event loop. Asynchronous I/O handles multiple client requests concurrently without per-thread memory overhead.
</p>
<p>
<strong>3.2 Core HTTP Server & Stream Handling:</strong> <code>http.createServer</code> receives readable request and writable response streams. POST and PUT request bodies arrive as streamed buffer chunks, handled via <code>req.on('data')</code> and assembled on <code>req.on('end')</code>.
</p>
<p>
<strong>3.3 Static File Serving & MIME Resolution:</strong> Static file serving maps URL paths to files on disk using <code>path.join</code>, preventing directory traversal vulnerabilities, and assigns proper Content-Type headers based on extensions.
</p>

<h2 class="sec-title">4. Software & Hardware Requirements</h2>
<table class="data-table">
  <tr><th style="width: 30%;">Component</th><th>Specification</th></tr>
  <tr><td>Operating System</td><td>Microsoft Windows 11 x64 / Linux x64 (Render PaaS)</td></tr>
  <tr><td>Runtime & Dependencies</td><td>Node.js v20.x, npm v10.x (Zero external web dependencies)</td></tr>
  <tr><td>Core Built-in Modules</td><td><code>http</code>, <code>fs</code>, <code>path</code>, <code>url</code></td></tr>
  <tr><td>Diagnostics & API Clients</td><td>Google Chrome DevTools, Postman, cURL</td></tr>
  <tr><td>Version Control & Cloud</td><td>Git, GitHub, Render Web Services</td></tr>
</table>

<h2 class="sec-title">5. Design & Architectural Implementation</h2>
<ol>
  <li>Initialize core HTTP server on dynamic port (<code>process.env.PORT || 5000</code>).</li>
  <li>Create asynchronous stream parser <code>parseBody(req)</code> to accumulate data buffers into structured JSON.</li>
  <li>Implement routing switch inspecting <code>req.method</code> and pathname for <code>/api/tasks</code> and <code>/api/health</code>.</li>
  <li>Construct standalone validator module enforcing business rules (title length, valid priority, recognized status).</li>
  <li>Maintain thread-safe in-memory task array supporting all CRUD operations.</li>
  <li>Serve HTML/CSS/JS frontend files from <code>public/</code> with proper MIME header mappings.</li>
</ol>

<h2 class="sec-title">6. Source Code Implementation</h2>

<h3 class="subsec-title">6.1 server.js (Core Node.js HTTP Server, Router & Static Handler)</h3>
<pre class="code-block">{server_js}</pre>

<h3 class="subsec-title">6.2 validator.js (Payload Validation Module)</h3>
<pre class="code-block">{validator_js}</pre>

<h3 class="subsec-title">6.3 public/app.js (Client-Side API Integration Controller)</h3>
<pre class="code-block">{app_js}</pre>

<h3 class="subsec-title">6.4 public/index.html (TaskGravity Minimalist UI Dashboard)</h3>
<pre class="code-block">{index_html}</pre>

<h2 class="sec-title">7. Verification & Test Results</h2>
<table class="data-table">
  <thead>
    <tr>
      <th>Test Case / Endpoint</th>
      <th>Observed Behavior & Criteria</th>
      <th>Verification Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>GET /api/tasks</strong></td>
      <td>Returns HTTP 200 OK with JSON array of active tasks and Content-Type: application/json.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>POST /api/tasks</strong></td>
      <td>Buffers incoming stream, validates schema, assigns UUID, returns HTTP 201 Created.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>Validation Failure</strong></td>
      <td>Submitting empty title or invalid priority returns HTTP 400 Bad Request with field error message.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>PUT /api/tasks/:id</strong></td>
      <td>Updates existing task fields and timestamp, returns HTTP 200 OK with updated record.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>DELETE /api/tasks/:id</strong></td>
      <td>Removes task by ID from memory, returns HTTP 200 OK confirmation.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
  </tbody>
</table>

<h2 class="sec-title">8. Conclusion</h2>
<p>
Practical 04 successfully demonstrates the fundamentals of server-side web engineering using core Node.js built-in modules. By constructing a complete REST server without third-party frameworks, key concepts including event-driven stream parsing, manual route dispatching, MIME header synthesis, and asynchronous validation were thoroughly verified. The application operates efficiently with zero external web dependencies and has been deployed to Render Cloud as a live web service.
</p>

<div class="links-box">
  <div style="font-weight: 700; font-size: 11pt; margin-bottom: 6px; color: #0f172a;">Project Links & Deployment Information</div>
  <div><strong>GitHub Link / Code Link:</strong> <a href="https://github.com/Sarthak-1229/taskgravity-practical-04" target="_blank">https://github.com/Sarthak-1229/taskgravity-practical-04</a></div>
  <div style="margin-top: 4px;"><strong>Live Deployment Link:</strong> <a href="https://taskgravity-practical-04.onrender.com" target="_blank">https://taskgravity-practical-04.onrender.com</a></div>
</div>

</body>
</html>
"""
    html_report_path = r"D:\_TY\Web-Tech\Practicals\Practical4\report_temp.html"
    pdf_report_path = r"D:\_TY\Web-Tech\Practicals\Practical4\Practical_04_Report.pdf"

    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    chrome_cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_report_path}",
        html_report_path
    ]
    subprocess.run(chrome_cmd, check=True)
    
    if os.path.exists(html_report_path):
        os.remove(html_report_path)
    
    print(f"Generated PDF: {pdf_report_path}")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()
