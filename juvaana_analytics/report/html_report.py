import json


class HTMLReport:

    def __init__(self, title="Juvaana Interactive EDA"):
        self.title = title
        self.data = []
        self.columns = []
        self.overview = {}
        self.summary = {}
        self.missing = {}
        self.correlations = []
        self.column_types = {}

    # -----------------------------------
    # SET DATA
    # -----------------------------------
    def set_data(self, data, columns):
        self.data = data
        self.columns = columns

    # -----------------------------------
    # SET OVERVIEW
    # -----------------------------------
    def set_overview(self, overview):
        self.overview = overview

    # -----------------------------------
    # SET SUMMARY
    # -----------------------------------
    def set_summary(self, summary):
        self.summary = summary

    # -----------------------------------
    # SET MISSING
    # -----------------------------------
    def set_missing(self, missing):
        self.missing = missing

    # -----------------------------------
    # SET CORRELATIONS
    # -----------------------------------
    def set_correlations(self, correlations):
        self.correlations = correlations

    # -----------------------------------
    # SET COLUMN TYPES
    # -----------------------------------
    def set_column_types(self, column_types):
        self.column_types = column_types

    # -----------------------------------
    # GENERATE REPORT
    # -----------------------------------
    def generate(self, output_file="report.html"):

        # -----------------------------------
        # SUMMARY TABLE ROWS
        # -----------------------------------
        summary_rows = ""
        for col, stats in self.summary.items():
            summary_rows += f"""
            <tr>
                <td>{col}</td>
                <td>{stats['mean']:.2f}</td>
                <td>{stats['median']:.2f}</td>
                <td>{stats['std']:.2f}</td>
                <td>{stats['min']:.2f}</td>
                <td>{stats['max']:.2f}</td>
                <td>{stats['missing']}</td>
                <td>{stats['skewness']:.2f}</td>
            </tr>
            """

        # -----------------------------------
        # MISSING TABLE ROWS
        # -----------------------------------
        missing_rows = ""
        for col, m in self.missing.items():
            missing_rows += f"""
            <tr>
                <td>{col}</td>
                <td>{m['missing_count']}</td>
                <td>{m['missing_percent']}%</td>
            </tr>
            """

        # -----------------------------------
        # CORRELATION TABLE ROWS
        # -----------------------------------
        corr_rows = ""
        for c in self.correlations:
            corr_rows += f"""
            <tr>
                <td>{c['x']}</td>
                <td>{c['y']}</td>
                <td>{c['corr']}</td>
            </tr>
            """

        # -----------------------------------
        # SAFE JSON — injected directly, no JSON.parse() needed
        # -----------------------------------
        data_json    = json.dumps(self.data,    ensure_ascii=False)
        columns_json = json.dumps(self.columns, ensure_ascii=False)

        # -----------------------------------
        # HTML
        # -----------------------------------
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{self.title}</title>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet" />

    <style>
        :root {{
            --bg:       #0a0a0b;
            --surface:  #111113;
            --border:   #222226;
            --accent:   #ff7a00;
            --accent2:  #ff3c00;
            --text:     #e8e8e8;
            --muted:    #888;
            --radius:   10px;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: 'DM Mono', monospace;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
        }}

        /* ---- NAVBAR ---- */
        .navbar {{
            background: var(--surface);
            border-bottom: 2px solid var(--accent);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }}

        .navbar-brand {{
            font-family: 'Syne', sans-serif;
            font-weight: 800;
            font-size: 1.3rem;
            color: var(--accent);
            letter-spacing: -0.5px;
        }}

        .navbar-links a {{
            color: var(--muted);
            text-decoration: none;
            margin-left: 20px;
            font-size: 0.75rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            transition: color 0.2s;
        }}

        .navbar-links a:hover {{ color: var(--accent); }}

        /* ---- LAYOUT ---- */
        .container {{ max-width: 1200px; margin: 0 auto; padding: 28px 20px; }}

        .box {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 24px;
            margin-bottom: 24px;
        }}

        .box h2 {{
            font-family: 'Syne', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
        }}

        /* ---- OVERVIEW GRID ---- */
        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px;
            margin-top: 8px;
        }}

        .stat-card {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }}

        .stat-card .value {{
            font-family: 'Syne', sans-serif;
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--accent);
        }}

        .stat-card .label {{
            font-size: 0.7rem;
            color: var(--muted);
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: 4px;
        }}

        /* ---- TYPE BADGES ---- */
        .badge-list {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 4px; }}

        .badge {{
            font-size: 0.7rem;
            padding: 3px 10px;
            border-radius: 20px;
            border: 1px solid var(--border);
            color: var(--text);
            background: var(--bg);
        }}

        .badge.numeric  {{ border-color: var(--accent);  color: var(--accent); }}
        .badge.categoric {{ border-color: #5599ff; color: #5599ff; }}

        /* ---- CONTROLS ---- */
        .controls {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: flex-end;
            margin-bottom: 16px;
        }}

        .control-group {{ display: flex; flex-direction: column; gap: 4px; }}

        .control-group label {{
            font-size: 0.68rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        select {{
            padding: 8px 12px;
            background: var(--bg);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 6px;
            font-family: 'DM Mono', monospace;
            font-size: 0.8rem;
            outline: none;
            cursor: pointer;
        }}

        select:focus {{ border-color: var(--accent); }}

        button {{
            padding: 9px 22px;
            background: var(--accent);
            color: #000;
            border: none;
            border-radius: 6px;
            font-family: 'Syne', sans-serif;
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 0.5px;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
            align-self: flex-end;
        }}

        button:hover  {{ background: #ff9433; }}
        button:active {{ transform: scale(0.97); }}

        /* ---- TABLE ---- */
        .table-wrap {{ overflow-x: auto; }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.78rem;
        }}

        thead th {{
            background: var(--bg);
            color: var(--accent);
            padding: 10px 12px;
            text-align: left;
            font-family: 'Syne', sans-serif;
            font-size: 0.7rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            border-bottom: 1px solid var(--border);
        }}

        tbody tr {{ border-bottom: 1px solid var(--border); transition: background 0.15s; }}
        tbody tr:hover {{ background: rgba(255,122,0,0.05); }}
        tbody td {{ padding: 9px 12px; color: var(--text); }}

        /* ---- PROFILES ---- */
        .profiles-list {{ display: flex; flex-direction: column; gap: 20px; }}

        .profile-card {{
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }}

        .profile-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 14px 18px;
            background: var(--surface);
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            user-select: none;
        }}

        .profile-header h3 {{
            font-family: 'Syne', sans-serif;
            font-size: 0.95rem;
            color: var(--accent);
        }}

        .profile-header .type-pill {{
            font-size: 0.65rem;
            padding: 3px 10px;
            border-radius: 20px;
            border: 1px solid var(--border);
        }}

        .type-pill.numeric  {{ border-color: var(--accent); color: var(--accent); }}
        .type-pill.categoric {{ border-color: #5599ff; color: #5599ff; }}

        .profile-body {{ padding: 18px; display: none; }}
        .profile-body.open {{ display: block; }}

        .profile-body .stats-row {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 10px;
            margin-bottom: 16px;
        }}

        .mini-stat {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 10px;
            text-align: center;
        }}

        .mini-stat .ms-val {{
            font-family: 'Syne', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            color: var(--text);
        }}

        .mini-stat .ms-label {{
            font-size: 0.62rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 3px;
        }}

        .profile-chart {{ width: 100%; margin-bottom: 16px; }}

        .profile-tabs {{
            display: flex;
            gap: 6px;
            margin-bottom: 12px;
        }}

        .tab-btn {{
            padding: 5px 14px;
            font-size: 0.7rem;
            font-family: 'DM Mono', monospace;
            background: var(--surface);
            color: var(--muted);
            border: 1px solid var(--border);
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.15s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .tab-btn.active, .tab-btn:hover {{
            background: var(--accent);
            color: #000;
            border-color: var(--accent);
        }}

        .tab-panel {{ display: none; }}
        .tab-panel.active {{ display: block; }}

        .small-table {{ font-size: 0.72rem; width: 100%; border-collapse: collapse; }}
        .small-table th {{
            background: var(--surface);
            color: var(--accent);
            padding: 7px 10px;
            text-align: left;
            font-size: 0.65rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            border-bottom: 1px solid var(--border);
        }}
        .small-table td {{
            padding: 6px 10px;
            border-bottom: 1px solid var(--border);
            color: var(--text);
            font-size: 0.72rem;
        }}
        .small-table tr:last-child td {{ border-bottom: none; }}
        .small-table tr:hover td {{ background: rgba(255,122,0,0.04); }}

        /* ---- EMPTY STATE ---- */
        .empty {{ color: var(--muted); font-size: 0.8rem; padding: 12px 0; }}
    </style>
</head>

<body>

    <!-- NAVBAR -->
    <nav class="navbar">
        <div class="navbar-brand">⬡ Juvaana EDA</div>
        <div class="navbar-links">
            <a href="#overview">Overview</a>
            <a href="#graphs">Graphs</a>
            <a href="#summary">Summary</a>
            <a href="#missing">Missing</a>
            <a href="#heatmap">Heatmap</a>
            <a href="#datatable">Preview</a>
            <a href="#variables">Variables</a>
        </div>
    </nav>

    <div class="container">

        <!-- OVERVIEW -->
        <div class="box" id="overview">
            <h2>Dataset Overview</h2>
            <div class="overview-grid">
                <div class="stat-card">
                    <div class="value">{self.overview.get('rows', 0)}</div>
                    <div class="label">Rows</div>
                </div>
                <div class="stat-card">
                    <div class="value">{self.overview.get('columns', 0)}</div>
                    <div class="label">Columns</div>
                </div>
                <div class="stat-card">
                    <div class="value">{self.overview.get('missing_values', 0)}</div>
                    <div class="label">Missing</div>
                </div>
                <div class="stat-card">
                    <div class="value">{self.overview.get('duplicates', 0)}</div>
                    <div class="label">Duplicates</div>
                </div>
            </div>
        </div>

        <!-- COLUMN TYPES -->
        <div class="box">
            <h2>Column Types</h2>
            <p style="font-size:0.75rem;color:var(--muted);margin-bottom:8px;">NUMERIC</p>
            <div class="badge-list">
                {"".join(f'<span class="badge numeric">{c}</span>' for c in self.column_types.get('numeric', []))}
            </div>
            <p style="font-size:0.75rem;color:var(--muted);margin:14px 0 8px;">CATEGORICAL</p>
            <div class="badge-list">
                {"".join(f'<span class="badge categoric">{c}</span>' for c in self.column_types.get('categorical', []))}
            </div>
        </div>

        <!-- GRAPH BUILDER -->
        <div class="box" id="graphs">
            <h2>Interactive Graph Builder</h2>
            <div class="controls">
                <div class="control-group">
                    <label>X Axis</label>
                    <select id="x"></select>
                </div>
                <div class="control-group">
                    <label>Y Axis</label>
                    <select id="y"></select>
                </div>
                <div class="control-group">
                    <label>Chart Type</label>
                    <select id="type">
                        <option value="scatter">Scatter</option>
                        <option value="line">Line</option>
                        <option value="bar">Bar</option>
                        <option value="histogram">Histogram</option>
                        <option value="box">Box Plot</option>
                    </select>
                </div>
                <button onclick="draw()">Generate</button>
            </div>
            <div id="chart"></div>
        </div>

        <!-- SUMMARY -->
        <div class="box" id="summary">
            <h2>Numeric Summary</h2>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Column</th><th>Mean</th><th>Median</th><th>Std</th>
                            <th>Min</th><th>Max</th><th>Missing</th><th>Skewness</th>
                        </tr>
                    </thead>
                    <tbody>{summary_rows}</tbody>
                </table>
            </div>
        </div>

        <!-- MISSING -->
        <div class="box" id="missing">
            <h2>Missing Values</h2>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr><th>Column</th><th>Missing Count</th><th>Missing %</th></tr>
                    </thead>
                    <tbody>{missing_rows}</tbody>
                </table>
            </div>
        </div>

        <!-- CORRELATIONS -->
        <div class="box">
            <h2>Top Correlations</h2>
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr><th>X</th><th>Y</th><th>Correlation</th></tr>
                    </thead>
                    <tbody>{corr_rows}</tbody>
                </table>
            </div>
        </div>

        <!-- HEATMAP -->
        <div class="box" id="heatmap">
            <h2>Correlation Heatmap</h2>
            <div id="heatmapChart"></div>
        </div>

        <!-- DATA HEAD / TAIL -->
        <div class="box" id="datatable">
            <h2>Data Preview</h2>
            <div class="profile-tabs">
                <button class="tab-btn active" onclick="switchPreview('head', this)">Head (5)</button>
                <button class="tab-btn" onclick="switchPreview('tail', this)">Tail (5)</button>
            </div>
            <div class="table-wrap">
                <table class="small-table" id="previewTable"></table>
            </div>
        </div>

        <!-- VARIABLE PROFILES -->
        <div class="box" id="variables">
            <h2>Variable Profiles</h2>
            <div class="profiles-list" id="profiles"></div>
        </div>

    </div>

<script>
    // -------------------------------------------------------
    // DATA — injected directly from Python (no JSON.parse)
    // -------------------------------------------------------
    const data    = {data_json};
    const columns = {columns_json};

    console.log("DATA sample:", Array.isArray(data) ? data.slice(0,2) : data);
    console.log("COLUMNS:", columns);

    // -------------------------------------------------------
    // PLOTLY LAYOUT DEFAULTS
    // -------------------------------------------------------
    const layout = {{
        paper_bgcolor: "#111113",
        plot_bgcolor:  "#0a0a0b",
        font: {{ color: "#e8e8e8", family: "DM Mono, monospace" }},
        margin: {{ t: 30, r: 20, b: 60, l: 60 }},
        xaxis: {{ gridcolor: "#222226", zerolinecolor: "#222226" }},
        yaxis: {{ gridcolor: "#222226", zerolinecolor: "#222226" }}
    }};

    const config = {{ responsive: true, displaylogo: false }};

    // -------------------------------------------------------
    // POPULATE DROPDOWNS
    // -------------------------------------------------------
    const xSel = document.getElementById("x");
    const ySel = document.getElementById("y");

    columns.forEach(col => {{
        const o1 = new Option(col, col);
        const o2 = new Option(col, col);
        xSel.appendChild(o1);
        ySel.appendChild(o2);
    }});

    // -------------------------------------------------------
    // CLEAN — extract numeric values for a column
    // -------------------------------------------------------
    function clean(col) {{
        if (!Array.isArray(data)) {{
            console.error("data is not an array:", data);
            return [];
        }}
        return data
            .map(row => parseFloat(row[col]))
            .filter(v => !isNaN(v));
    }}

    // -------------------------------------------------------
    // DRAW GRAPH
    // -------------------------------------------------------
    function draw() {{
        const x    = xSel.value;
        const y    = ySel.value;
        const type = document.getElementById("type").value;

        const xData = clean(x);
        const yData = clean(y);

        let trace;

        if (type === "scatter") {{
            trace = {{ x: xData, y: yData, mode: "markers", type: "scatter",
                       marker: {{ color: "#ff7a00", opacity: 0.7 }} }};
        }} else if (type === "line") {{
            trace = {{ x: xData, y: yData, mode: "lines", type: "scatter",
                       line: {{ color: "#ff7a00" }} }};
        }} else if (type === "bar") {{
            trace = {{ x: xData, y: yData, type: "bar",
                       marker: {{ color: "#ff7a00" }} }};
        }} else if (type === "histogram") {{
            trace = {{ x: xData, type: "histogram",
                       marker: {{ color: "#ff7a00" }} }};
        }} else {{
            trace = {{ y: yData, type: "box",
                       marker: {{ color: "#ff7a00" }} }};
        }}

        Plotly.newPlot("chart", [trace], {{
            ...layout,
            xaxis: {{ ...layout.xaxis, title: x }},
            yaxis: {{ ...layout.yaxis, title: y }}
        }}, config);
    }}

    // -------------------------------------------------------
    // PEARSON CORRELATION
    // -------------------------------------------------------
    function pearson(a, b) {{
        const n = Math.min(a.length, b.length);
        if (n === 0) return 0;
        const avgA = a.slice(0, n).reduce((s, v) => s + v, 0) / n;
        const avgB = b.slice(0, n).reduce((s, v) => s + v, 0) / n;
        let num = 0, d1 = 0, d2 = 0;
        for (let i = 0; i < n; i++) {{
            const da = a[i] - avgA, db = b[i] - avgB;
            num += da * db;
            d1  += da * da;
            d2  += db * db;
        }}
        const denom = Math.sqrt(d1 * d2);
        return denom === 0 ? 0 : num / denom;
    }}

    // -------------------------------------------------------
    // HEATMAP
    // -------------------------------------------------------
    function drawHeatmap() {{
        const numCols = columns.filter(c => clean(c).length > 0);
        if (numCols.length === 0) return;

        const z = numCols.map(c1 => {{
            const a = clean(c1);
            return numCols.map(c2 => pearson(a, clean(c2)));
        }});

        Plotly.newPlot("heatmapChart", [{{
            z, x: numCols, y: numCols,
            type: "heatmap",
            colorscale: [[0, "#003080"], [0.5, "#111113"], [1, "#ff7a00"]],
            zmin: -1, zmax: 1
        }}], {{
            ...layout,
            margin: {{ t: 40, r: 40, b: 120, l: 120 }}
        }}, config);
    }}

    // -------------------------------------------------------
    // DATA PREVIEW — head / tail
    // -------------------------------------------------------
    function renderPreview(slice) {{
        const table = document.getElementById("previewTable");
        if (!Array.isArray(data) || data.length === 0) {{ table.innerHTML = "<tr><td>No data</td></tr>"; return; }}
        const rows  = slice === "head" ? data.slice(0, 5) : data.slice(-5);
        let html = "<thead><tr><th>#</th>" + columns.map(c => `<th>${{c}}</th>`).join("") + "</tr></thead><tbody>";
        const startIdx = slice === "tail" ? data.length - rows.length : 0;
        rows.forEach((row, i) => {{
            html += `<tr><td style="color:var(--muted)">${{startIdx + i}}</td>` +
                columns.map(c => `<td>${{row[c] === null || row[c] === undefined ? '<span style="color:var(--muted)">NaN</span>' : row[c]}}</td>`).join("") +
                "</tr>";
        }});
        html += "</tbody>";
        table.innerHTML = html;
    }}

    function switchPreview(slice, btn) {{
        document.querySelectorAll(".profile-tabs .tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        renderPreview(slice);
    }}

    renderPreview("head");

    // -------------------------------------------------------
    // VARIABLE PROFILES — with charts, stats, head/tail tabs
    // -------------------------------------------------------
    function buildProfiles() {{
        const container = document.getElementById("profiles");

        columns.forEach((col, idx) => {{
            const vals   = clean(col);
            const isNum  = vals.length > 0;
            const allVals = Array.isArray(data) ? data.map(r => r[col]) : [];

            // --- card shell ---
            const card = document.createElement("div");
            card.className = "profile-card";

            const typePill = isNum
                ? `<span class="type-pill numeric">Numeric</span>`
                : `<span class="type-pill categoric">Categorical</span>`;

            card.innerHTML = `
                <div class="profile-header" onclick="toggleProfile(this)">
                    <h3>${{col}}</h3>
                    ${{typePill}}
                </div>
                <div class="profile-body" id="body-${{idx}}">
                    ${{isNum ? buildNumericBody(col, vals, idx) : buildCatBody(col, allVals, idx)}}
                </div>
            `;

            container.appendChild(card);

            // auto-open first card
            if (idx === 0) {{
                card.querySelector(".profile-body").classList.add("open");
                setTimeout(() => drawProfileChart(col, vals, allVals, isNum, idx), 100);
            }}
        }});
    }}

    function toggleProfile(header) {{
        const body = header.nextElementSibling;
        const wasOpen = body.classList.contains("open");
        body.classList.toggle("open");
        if (!wasOpen) {{
            const idx = header.parentElement.querySelector(".profile-body").id.split("-")[1];
            const col = columns[parseInt(idx)];
            const vals = clean(col);
            const allVals = Array.isArray(data) ? data.map(r => r[col]) : [];
            drawProfileChart(col, vals, allVals, vals.length > 0, parseInt(idx));
        }}
    }}

    // -------------------------------------------------------
    // NUMERIC BODY HTML
    // -------------------------------------------------------
    function buildNumericBody(col, vals, idx) {{
        const sorted = [...vals].sort((a,b) => a - b);
        const n      = sorted.length;
        const mean   = vals.reduce((a,b)=>a+b,0) / n;
        const median = n % 2 === 0 ? (sorted[n/2-1]+sorted[n/2])/2 : sorted[Math.floor(n/2)];
        const variance = vals.reduce((s,v)=>s+(v-mean)**2,0)/n;
        const std    = Math.sqrt(variance);
        const q1     = sorted[Math.floor(n*0.25)];
        const q3     = sorted[Math.floor(n*0.75)];
        const missing = Array.isArray(data) ? data.filter(r => r[col]===null||r[col]===undefined||r[col]==="").length : 0;

        return `
            <div class="stats-row">
                <div class="mini-stat"><div class="ms-val">${{n}}</div><div class="ms-label">Count</div></div>
                <div class="mini-stat"><div class="ms-val">${{mean.toFixed(2)}}</div><div class="ms-label">Mean</div></div>
                <div class="mini-stat"><div class="ms-val">${{median.toFixed(2)}}</div><div class="ms-label">Median</div></div>
                <div class="mini-stat"><div class="ms-val">${{std.toFixed(2)}}</div><div class="ms-label">Std Dev</div></div>
                <div class="mini-stat"><div class="ms-val">${{sorted[0]}}</div><div class="ms-label">Min</div></div>
                <div class="mini-stat"><div class="ms-val">${{sorted[n-1]}}</div><div class="ms-label">Max</div></div>
                <div class="mini-stat"><div class="ms-val">${{q1}}</div><div class="ms-label">Q1 (25%)</div></div>
                <div class="mini-stat"><div class="ms-val">${{q3}}</div><div class="ms-label">Q3 (75%)</div></div>
                <div class="mini-stat"><div class="ms-val">${{missing}}</div><div class="ms-label">Missing</div></div>
                <div class="mini-stat"><div class="ms-val">${{(q3-q1).toFixed(2)}}</div><div class="ms-label">IQR</div></div>
            </div>
            <div class="profile-tabs">
                <button class="tab-btn active" onclick="switchTab(${{idx}},'hist',this)">Histogram</button>
                <button class="tab-btn" onclick="switchTab(${{idx}},'box',this)">Box Plot</button>
                <button class="tab-btn" onclick="switchTab(${{idx}},'head',this)">Head</button>
                <button class="tab-btn" onclick="switchTab(${{idx}},'tail',this)">Tail</button>
                <button class="tab-btn" onclick="switchTab(${{idx}},'quantiles',this)">Quantiles</button>
            </div>
            <div class="tab-panel active" id="tab-${{idx}}-hist">
                <div class="profile-chart" id="chart-hist-${{idx}}"></div>
            </div>
            <div class="tab-panel" id="tab-${{idx}}-box">
                <div class="profile-chart" id="chart-box-${{idx}}"></div>
            </div>
            <div class="tab-panel" id="tab-${{idx}}-head">
                <div class="table-wrap" id="tbl-head-${{idx}}"></div>
            </div>
            <div class="tab-panel" id="tab-${{idx}}-tail">
                <div class="table-wrap" id="tbl-tail-${{idx}}"></div>
            </div>
            <div class="tab-panel" id="tab-${{idx}}-quantiles">
                <div class="table-wrap" id="tbl-q-${{idx}}"></div>
            </div>
        `;
    }}

    // -------------------------------------------------------
    // CATEGORICAL BODY HTML
    // -------------------------------------------------------
    function buildCatBody(col, allVals, idx) {{
        const nonNull = allVals.filter(v => v !== null && v !== undefined && v !== "");
        const unique  = [...new Set(nonNull)];
        const missing = allVals.length - nonNull.length;
        return `
            <div class="stats-row">
                <div class="mini-stat"><div class="ms-val">${{nonNull.length}}</div><div class="ms-label">Count</div></div>
                <div class="mini-stat"><div class="ms-val">${{unique.length}}</div><div class="ms-label">Unique</div></div>
                <div class="mini-stat"><div class="ms-val">${{missing}}</div><div class="ms-label">Missing</div></div>
            </div>
            <div class="profile-tabs">
                <button class="tab-btn active" onclick="switchTab(${{idx}},'bar',this)">Bar Chart</button>
                <button class="tab-btn" onclick="switchTab(${{idx}},'head',this)">Head</button>
                <button class="tab-btn" onclick="switchTab(${{idx}},'tail',this)">Tail</button>
                <button class="tab-btn" onclick="switchTab(${{idx}},'counts',this)">Value Counts</button>
            </div>
            <div class="tab-panel active" id="tab-${{idx}}-bar">
                <div class="profile-chart" id="chart-bar-${{idx}}"></div>
            </div>
            <div class="tab-panel" id="tab-${{idx}}-head">
                <div class="table-wrap" id="tbl-head-${{idx}}"></div>
            </div>
            <div class="tab-panel" id="tab-${{idx}}-tail">
                <div class="table-wrap" id="tbl-tail-${{idx}}"></div>
            </div>
            <div class="tab-panel" id="tab-${{idx}}-counts">
                <div class="table-wrap" id="tbl-counts-${{idx}}"></div>
            </div>
        `;
    }}

    // -------------------------------------------------------
    // DRAW PROFILE CHART
    // -------------------------------------------------------
    function drawProfileChart(col, vals, allVals, isNum, idx) {{
        const miniLayout = {{
            paper_bgcolor: "#0a0a0b",
            plot_bgcolor:  "#0a0a0b",
            font: {{ color: "#e8e8e8", family: "DM Mono, monospace", size: 10 }},
            margin: {{ t: 10, r: 10, b: 40, l: 50 }},
            height: 220,
            xaxis: {{ gridcolor: "#222226", zerolinecolor: "#222226" }},
            yaxis: {{ gridcolor: "#222226", zerolinecolor: "#222226" }}
        }};

        if (isNum) {{
            // histogram
            const hEl = document.getElementById(`chart-hist-${{idx}}`);
            if (hEl) Plotly.newPlot(hEl, [{{
                x: vals, type: "histogram",
                marker: {{ color: "#ff7a00", opacity: 0.85 }},
                nbinsx: 30
            }}], miniLayout, config);

            // box
            const bEl = document.getElementById(`chart-box-${{idx}}`);
            if (bEl) Plotly.newPlot(bEl, [{{
                x: vals, type: "box",
                marker: {{ color: "#ff7a00" }},
                line: {{ color: "#ff7a00" }},
                fillcolor: "rgba(255,122,0,0.15)",
                orientation: "h"
            }}], miniLayout, config);

            // quantile table
            const sorted = [...vals].sort((a,b)=>a-b);
            const n = sorted.length;
            const pcts = [0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100];
            const qRows = pcts.map(p => {{
                const v = sorted[Math.min(Math.floor(n * p/100), n-1)];
                return `<tr><td>${{p}}%</td><td>${{v}}</td></tr>`;
            }}).join("");
            const qEl = document.getElementById(`tbl-q-${{idx}}`);
            if (qEl) qEl.innerHTML = `<table class="small-table"><thead><tr><th>Percentile</th><th>Value</th></tr></thead><tbody>${{qRows}}</tbody></table>`;

        }} else {{
            // value counts bar
            const counts = {{}};
            allVals.forEach(v => {{ if (v !== null && v !== undefined && v !== "") counts[v] = (counts[v]||0)+1; }});
            const sorted = Object.entries(counts).sort((a,b)=>b[1]-a[1]).slice(0,20);
            const bEl = document.getElementById(`chart-bar-${{idx}}`);
            if (bEl) Plotly.newPlot(bEl, [{{
                x: sorted.map(e=>e[0]),
                y: sorted.map(e=>e[1]),
                type: "bar",
                marker: {{ color: "#5599ff" }}
            }}], miniLayout, config);

            // value counts table
            const cEl = document.getElementById(`tbl-counts-${{idx}}`);
            if (cEl) {{
                const rows = sorted.map(([v,c]) =>
                    `<tr><td>${{v}}</td><td>${{c}}</td><td>${{((c/allVals.length)*100).toFixed(1)}}%</td></tr>`
                ).join("");
                cEl.innerHTML = `<table class="small-table"><thead><tr><th>Value</th><th>Count</th><th>%</th></tr></thead><tbody>${{rows}}</tbody></table>`;
            }}
        }}

        // head table
        buildRowTable(col, idx, "head", data.slice(0, 10));
        // tail table
        buildRowTable(col, idx, "tail", data.slice(-10));
    }}

    function buildRowTable(col, idx, which, rows) {{
        const el = document.getElementById(`tbl-${{which}}-${{idx}}`);
        if (!el) return;
        const startIdx = which === "tail" ? data.length - rows.length : 0;
        let html = `<table class="small-table"><thead><tr><th>#</th><th>${{col}}</th></tr></thead><tbody>`;
        rows.forEach((row, i) => {{
            const v = row[col];
            const display = (v === null || v === undefined || v === "")
                ? `<span style="color:var(--muted)">NaN</span>` : v;
            html += `<tr><td style="color:var(--muted)">${{startIdx+i}}</td><td>${{display}}</td></tr>`;
        }});
        html += "</tbody></table>";
        el.innerHTML = html;
    }}

    // -------------------------------------------------------
    // TAB SWITCHING PER PROFILE CARD
    // -------------------------------------------------------
    function switchTab(idx, panel, btn) {{
        // deactivate all tab btns in this card
        btn.closest(".profile-body").querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        // hide all panels in this card
        btn.closest(".profile-body").querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

        const target = document.getElementById(`tab-${{idx}}-${{panel}}`);
        if (target) target.classList.add("active");
    }}

    // -------------------------------------------------------
    // INIT
    // -------------------------------------------------------
    drawHeatmap();
    buildProfiles();

</script>
</body>
</html>"""

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[SUCCESS] Report generated → {output_file}")