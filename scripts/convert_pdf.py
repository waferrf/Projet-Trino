import os
import re
import sys
import subprocess

# Custom SVG representing the architecture diagram
BEAUTIFUL_SVG = """
<svg width="100%" height="320" viewBox="0 0 960 360" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#A0AEC0" flood-opacity="0.3"/>
    </filter>
    <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#2B6CB0"/>
      <stop offset="100%" stop-color="#1A365D"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#319795"/>
      <stop offset="100%" stop-color="#234E52"/>
    </linearGradient>
    <linearGradient id="purpleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#805AD5"/>
      <stop offset="100%" stop-color="#44337A"/>
    </linearGradient>
    <linearGradient id="orangeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#DD6B20"/>
      <stop offset="100%" stop-color="#7B341E"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38A169"/>
      <stop offset="100%" stop-color="#1C4532"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#718096"/>
    </marker>
  </defs>

  <!-- Nodes -->
  <!-- A: CSV Sales -->
  <rect x="20" y="40" width="180" height="60" rx="8" fill="url(#greenGrad)" filter="url(#shadow)"/>
  <text x="110" y="65" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">CSV Ventes</text>
  <text x="110" y="82" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">manju_bhai_sales.csv</text>

  <!-- B: MinIO -->
  <rect x="270" y="40" width="110" height="60" rx="8" fill="url(#blueGrad)" filter="url(#shadow)"/>
  <text x="325" y="65" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">MinIO</text>
  <text x="325" y="82" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">Stockage Objet</text>

  <!-- E: Hive Metastore -->
  <rect x="440" y="40" width="140" height="60" rx="8" fill="url(#purpleGrad)" filter="url(#shadow)"/>
  <text x="510" y="65" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">Hive Metastore</text>
  <text x="510" y="82" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">Catalogue Metadata</text>

  <!-- F: Apache Iceberg -->
  <rect x="640" y="40" width="140" height="60" rx="8" fill="url(#purpleGrad)" filter="url(#shadow)"/>
  <text x="710" y="65" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">Apache Iceberg</text>
  <text x="710" y="82" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">Tables Lakehouse</text>

  <!-- C: CSV Products -->
  <rect x="20" y="260" width="180" height="60" rx="8" fill="url(#greenGrad)" filter="url(#shadow)"/>
  <text x="110" y="285" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">CSV Produits</text>
  <text x="110" y="302" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">products.csv</text>

  <!-- D: ClickHouse -->
  <rect x="270" y="260" width="110" height="60" rx="8" fill="url(#blueGrad)" filter="url(#shadow)"/>
  <text x="325" y="285" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">ClickHouse</text>
  <text x="325" y="302" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">Base Colonne</text>

  <!-- G: Trino -->
  <rect x="455" y="150" width="110" height="60" rx="8" fill="url(#orangeGrad)" filter="url(#shadow)"/>
  <text x="510" y="175" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">Trino</text>
  <text x="510" y="192" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">Moteur SQL Fédéré</text>

  <!-- H: Streamlit -->
  <rect x="655" y="150" width="110" height="60" rx="8" fill="url(#tealGrad)" filter="url(#shadow)"/>
  <text x="710" y="175" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">Streamlit</text>
  <text x="710" y="192" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">Interface Data</text>

  <!-- I: Ollama -->
  <rect x="820" y="95" width="110" height="60" rx="8" fill="url(#tealGrad)" filter="url(#shadow)"/>
  <text x="875" y="120" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">Ollama</text>
  <text x="875" y="137" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">LLM Local</text>

  <!-- J: Power BI -->
  <rect x="655" y="260" width="110" height="60" rx="8" fill="url(#tealGrad)" filter="url(#shadow)"/>
  <text x="710" y="285" fill="white" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold" text-anchor="middle">Power BI</text>
  <text x="710" y="302" fill="#E2E8F0" font-family="Segoe UI, sans-serif" font-size="10" text-anchor="middle">Dashboard</text>

  <!-- Connections -->
  <!-- A -> B -->
  <path d="M 200 70 L 262 70" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  <!-- C -> D -->
  <path d="M 200 290 L 262 290" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  <!-- B -> E -->
  <path d="M 380 70 L 432 70" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  <!-- E -> F -->
  <path d="M 580 70 L 632 70" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  
  <!-- F -> G -->
  <path d="M 710 100 L 710 120 L 510 120 L 510 142" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  <!-- D -> G -->
  <path d="M 380 290 L 510 290 L 510 218" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  <!-- D -> J -->
  <path d="M 380 290 L 647 290" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  
  <!-- G -> H & H -> G (Bidirectional) -->
  <path d="M 565 170 L 647 170" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 655 190 L 573 190" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
  
  <!-- I -> H -->
  <path d="M 820 125 L 710 125 L 710 142" fill="none" stroke="#718096" stroke-width="2" marker-end="url(#arrow)"/>
</svg>
"""

def markdown_to_html(md_text):
    lines = md_text.splitlines()
    html_blocks = []
    
    in_code_block = False
    code_block_lang = ""
    code_block_lines = []
    
    in_table = False
    table_lines = []
    
    in_list = False
    list_lines = []
    
    paragraph_lines = []
    
    def flush_paragraph():
        if paragraph_lines:
            text = " ".join(paragraph_lines)
            html_blocks.append(f"<p>{parse_inline(text)}</p>")
            paragraph_lines.clear()
            
    def flush_list():
        if list_lines:
            html_blocks.append("<ul>")
            for item in list_lines:
                html_blocks.append(f"  <li>{parse_inline(item)}</li>")
            html_blocks.append("</ul>")
            list_lines.clear()
            
    def flush_table():
        if table_lines:
            headers = []
            rows = []
            for i, line in enumerate(table_lines):
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if i == 0:
                    headers = cells
                elif i == 1:
                    continue
                else:
                    rows.append(cells)
            
            html_table = ["<table>", "  <thead>", "    <tr>"]
            for h in headers:
                html_table.append(f"      <th>{parse_inline(h)}</th>")
            html_table.append("    </tr>")
            html_table.append("  </thead>")
            html_table.append("  <tbody>")
            for r in rows:
                html_table.append("    <tr>")
                for cell in r:
                    html_table.append(f"      <td>{parse_inline(cell)}</td>")
                html_table.append("    </tr>")
            html_table.append("  </tbody>")
            html_table.append("</table>")
            html_blocks.append("\n".join(html_table))
            table_lines.clear()
            
    def parse_inline(text):
        # Escape HTML characters first
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Bold **text**
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        # Italic *text*
        text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
        # Inline code `code`
        text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
        # HTTP Links
        text = re.sub(r'(https?://[a-zA-Z0-9\.\-\/:]+)', r'<a href="\1">\1</a>', text)
        return text

    for line in lines:
        stripped = line.strip()
        
        # Code block logic
        if stripped.startswith('```'):
            if in_code_block:
                content = "\n".join(code_block_lines)
                if code_block_lang == 'mermaid':
                    html_blocks.append(f'<div class="diagram-container">{BEAUTIFUL_SVG}</div>')
                else:
                    content_escaped = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                    html_blocks.append(f'<pre><code class="language-{code_block_lang}">{content_escaped}</code></pre>')
                in_code_block = False
                code_block_lines.clear()
            else:
                flush_paragraph()
                flush_list()
                flush_table()
                in_code_block = True
                code_block_lang = stripped[3:].strip()
            continue
            
        if in_code_block:
            code_block_lines.append(line)
            continue
            
        # Table logic
        if stripped.startswith('|'):
            flush_paragraph()
            flush_list()
            in_table = True
            table_lines.append(line)
            continue
        elif in_table:
            flush_table()
            in_table = False
            
        # List logic
        if stripped.startswith('- ') or stripped.startswith('* '):
            flush_paragraph()
            flush_table()
            in_list = True
            list_lines.append(stripped[2:])
            continue
        elif in_list:
            if line.startswith('  ') and len(list_lines) > 0:
                list_lines[-1] += " " + stripped
                continue
            else:
                flush_list()
                in_list = False
                
        # Headings
        if stripped.startswith('# '):
            flush_paragraph()
            html_blocks.append(f"<h1>{parse_inline(stripped[2:])}</h1>")
        elif stripped.startswith('## '):
            flush_paragraph()
            html_blocks.append(f"<h2>{parse_inline(stripped[3:])}</h2>")
        elif stripped.startswith('### '):
            flush_paragraph()
            html_blocks.append(f"<h3>{parse_inline(stripped[4:])}</h3>")
        elif stripped == '':
            flush_paragraph()
        else:
            paragraph_lines.append(line)
            
    # Flush remaining
    flush_paragraph()
    flush_list()
    flush_table()
    
    return "\n\n".join(html_blocks)

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Rapport de Projet</title>
<style>
  @page {
    size: A4;
    margin: 2cm;
  }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #2D3748;
    line-height: 1.6;
    font-size: 10.5pt;
  }
  
  /* Cover page container */
  .cover-page {
    position: relative;
    height: 25.7cm; /* Full height of page area inside margins (29.7cm - 4cm) */
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
  }
  
  .cover-content {
    margin-top: 5cm;
  }
  
  .cover-decor {
    width: 80px;
    height: 8px;
    background: linear-gradient(90deg, #2B6CB0, #319795);
    margin-bottom: 30px;
    border-radius: 4px;
  }
  
  .cover-title {
    font-size: 32pt;
    font-weight: 800;
    line-height: 1.2;
    color: #1A365D;
    margin-bottom: 20px;
    letter-spacing: -0.5px;
  }
  
  .cover-subtitle {
    font-size: 14pt;
    color: #4A5568;
    line-height: 1.6;
    margin-bottom: 40px;
    max-width: 90%;
  }
  
  .cover-footer {
    font-size: 11pt;
    color: #718096;
    border-top: 2px solid #EDF2F7;
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
  }
  
  /* Core content styling */
  h1 {
    display: none; /* Already on cover page */
  }
  
  h2 {
    page-break-before: always;
    font-size: 16pt;
    font-weight: 700;
    color: #1A365D;
    margin-top: 0;
    margin-bottom: 15px;
    border-bottom: 2px solid #EDF2F7;
    padding-bottom: 6px;
  }
  
  h2:first-of-type {
    page-break-before: avoid !important;
  }
  
  h3 {
    font-size: 12pt;
    font-weight: 700;
    color: #2C5282;
    margin-top: 22px;
    margin-bottom: 8px;
  }
  
  p {
    margin-top: 0;
    margin-bottom: 12px;
    text-align: justify;
  }
  
  ul {
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 20px;
  }
  
  li {
    margin-bottom: 6px;
  }
  
  code {
    font-family: Consolas, "Liberation Mono", Courier, monospace;
    font-size: 9pt;
    background-color: #EDF2F7;
    padding: 2px 5px;
    border-radius: 3px;
    color: #2B6CB0;
  }
  
  pre {
    font-family: Consolas, "Liberation Mono", Courier, monospace;
    background-color: #F7FAFC;
    border: 1px solid #E2E8F0;
    padding: 12px;
    border-radius: 5px;
    margin-top: 0;
    margin-bottom: 15px;
    overflow-x: auto;
    page-break-inside: avoid;
  }
  
  pre code {
    background-color: transparent;
    padding: 0;
    border-radius: 0;
    color: #2D3748;
    font-size: 8.5pt;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
    margin-bottom: 20px;
    page-break-inside: avoid;
  }
  
  th {
    background-color: #2B6CB0;
    color: white;
    font-weight: 600;
    font-size: 9.5pt;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #2B6CB0;
  }
  
  td {
    padding: 8px 10px;
    border: 1px solid #E2E8F0;
    font-size: 9pt;
    vertical-align: top;
  }
  
  tr:nth-child(even) {
    background-color: #F7FAFC;
  }
  
  .diagram-container {
    margin: 25px 0;
    text-align: center;
    page-break-inside: avoid;
  }
  
  a {
    color: #2B6CB0;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
</style>
</head>
<body>

<!-- Cover Page -->
<div class="cover-page">
  <div class="cover-content">
    <div class="cover-decor"></div>
    <div class="cover-title">Rapport de Projet<br>Data Lakehouse & GenAI</div>
    <div class="cover-subtitle">Mise en place d'une architecture moderne de données locale intégrant Trino, Apache Iceberg, MinIO, ClickHouse, Streamlit, Ollama et Power BI.</div>
  </div>
  
  <div class="cover-footer">
    <div>
      <strong>Auteur :</strong> Projet-Trino
    </div>
  </div>
</div>

<!-- Main Content -->
{content}

</body>
</html>
"""

def main():
    workspace_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    md_path = os.path.join(workspace_dir, "RAPPORT_PROJET.md")
    html_path = os.path.join(workspace_dir, "scripts", "temp_report.html")
    pdf_path = os.path.join(workspace_dir, "Rapport_Projet.pdf")
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        sys.exit(1)
        
    print(f"Reading {md_path}...")
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    print("Converting Markdown to HTML...")
    body_content = markdown_to_html(md_text)
    full_html = HTML_TEMPLATE.replace("{content}", body_content)
    
    print(f"Saving temporary HTML to {html_path}...")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    # Standard installation paths for MS Edge
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        # Check PATH as fallback
        "msedge.exe"
    ]
    
    edge_executable = None
    for path in edge_paths:
        if os.path.exists(path) or path == "msedge.exe":
            edge_executable = path
            break
            
    if not edge_executable:
        print("Error: Microsoft Edge could not be located in standard paths.")
        sys.exit(1)
        
    print(f"Found Edge: {edge_executable}")
    print(f"Generating PDF to {pdf_path}...")
    
    # Run Edge headless to print to PDF
    # Using --no-margins to let CSS control layout and margins
    # Using --print-to-pdf-no-header to disable Edge's own default header/footer
    cmd = [
        edge_executable,
        "--headless",
        "--disable-gpu",
        "--no-margins",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    
    try:
        # Check if we need to call it as shell
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("PDF generated successfully!")
        
        # Cleanup temp HTML
        if os.path.exists(html_path):
            os.remove(html_path)
            print("Temporary HTML file removed.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error executing Edge: {e}")
        print(f"Stderr: {e.stderr.decode(errors='ignore')}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
