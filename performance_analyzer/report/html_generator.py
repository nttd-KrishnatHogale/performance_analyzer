from pathlib import Path


class HTMLGenerator:

    def generate(
        self,
        output_file,
        report,
        timeline,
        correlations
    ):

        html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>Performance RCA Report</title>

<style>

body{{
font-family:Arial;
margin:30px;
background:#f8f8f8;
}}

h1{{
color:#0b5394;
}}

table{{
border-collapse:collapse;
width:100%;
}}

th,td{{
border:1px solid #ddd;
padding:8px;
}}

th{{
background:#0b5394;
color:white;
}}

.section{{
background:white;
padding:20px;
margin-bottom:20px;
border-radius:10px;
box-shadow:0 0 5px gray;
}}

.high{{
color:red;
font-weight:bold;
}}

.medium{{
color:orange;
font-weight:bold;
}}

.low{{
color:green;
}}

</style>

</head>

<body>

<h1>Performance Root Cause Analysis Report</h1>

<div class="section">

<h2>Executive Summary</h2>

<p>{report["summary"]}</p>

</div>

<div class="section">

<h2>Primary Root Cause</h2>

<p>{report["root_cause"]}</p>

</div>

<div class="section">

<h2>Confidence</h2>

<h3>{report["confidence"]}</h3>

</div>

<div class="section">

<h2>Timeline</h2>

<table>

<tr>

<th>Start</th>

<th>Peak</th>

<th>Recovery</th>

<th>Component</th>

<th>Issue</th>

</tr>
"""

        for e in timeline:

            html += f"""

<tr>

<td>{e.start_time}</td>

<td>{e.peak_time}</td>

<td>{e.end_time}</td>

<td>{e.component}</td>

<td>{e.metric}</td>

</tr>

"""

        html += """

</table>

</div>

<div class="section">

<h2>Correlation Chain</h2>

<table>

<tr>

<th>Source</th>

<th>Target</th>

<th>Relation</th>

<th>Confidence</th>

</tr>

"""

        for c in correlations:

            html += f"""

<tr>

<td>{c["source"]}</td>

<td>{c["target"]}</td>

<td>{c["relation"]}</td>

<td>{c["confidence"]}</td>

</tr>

"""

        html += """

</table>

</div>

<div class="section">

<h2>Bottlenecks</h2>

<ul>

"""

        for b in report["bottlenecks"]:

            html += f"<li>{b}</li>"

        html += """

</ul>

</div>

<div class="section">

<h2>Recommendations</h2>

<ul>

"""

        for r in report["recommendations"]:

            html += f"<li>{r}</li>"

        html += """

</ul>

</div>

<div class="section">

<h2>Detailed Narrative</h2>

<p>

"""

        html += report["timeline"]

        html += """

</p>

</div>

</body>

</html>

"""

        Path(output_file).write_text(
            html,
            encoding="utf-8"
        )