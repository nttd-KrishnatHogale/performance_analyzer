from pathlib import Path


class HTMLGenerator:

    def generate(
        self,
        output_file,
        report,
        timeline,
        correlations
    ):

        confidence = report.get("confidence", "UNKNOWN").upper()

        if confidence == "HIGH":
            confidence_class = "high"
        elif confidence == "MEDIUM":
            confidence_class = "medium"
        else:
            confidence_class = "low"

        html = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="utf-8">

<title>Performance RCA Report</title>

<style>

body {{
    font-family: Arial;
    margin: 30px;
    background: #f5f5f5;
}}

h1 {{
    color: #0b5394;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th,td {{
    border:1px solid #ccc;
    padding:8px;
    text-align:left;
}}

th {{
    background:#0b5394;
    color:white;
}}

.section {{
    background:white;
    padding:20px;
    margin-bottom:25px;
    border-radius:8px;
    box-shadow:0 0 6px rgba(0,0,0,.15);
}}

.high {{
    color:red;
    font-weight:bold;
}}

.medium {{
    color:orange;
    font-weight:bold;
}}

.low {{
    color:green;
    font-weight:bold;
}}

.card {{
    border-left:5px solid #0b5394;
    background:#fafafa;
    padding:12px;
    margin-bottom:15px;
}}

li {{
    margin-bottom:8px;
}}

</style>

</head>

<body>

<h1>Performance Root Cause Analysis Report</h1>

<div class="section">

<h2>Executive Summary</h2>

<p>{report.get("summary","Not Available")}</p>

</div>


<div class="section">

<h2>Executive Analysis</h2>

<table>

<tr>
<th width="30%">Primary Root Cause</th>
<td>{report.get("root_cause","Not Available")}</td>
</tr>

<tr>
<th>Primary Bottleneck</th>
<td>{report.get("primary_bottleneck","Not Available")}</td>
</tr>

<tr>
<th>Confidence</th>
<td class="{confidence_class}">
{confidence}
</td>
</tr>

</table>

</div>


<div class="section">

<h2>Timeline Summary</h2>

<p>

{report.get("timeline","Timeline not available.")}

</p>

</div>


<div class="section">

<h2>Supporting Evidence</h2>

<ul>

"""

        for evidence in report.get("supporting_evidence", []):

            html += f"<li>{evidence}</li>"

        html += """

</ul>

</div>


<div class="section">

<h2>Rejected Hypotheses</h2>

"""

        hypotheses = report.get("rejected_hypotheses", [])

        if hypotheses:

            for h in hypotheses:

                if isinstance(h, dict):

                    hypothesis = (
                        h.get("hypothesis")
                        or h.get("name")
                        or ""
                    )

                    reason = (
                        h.get("reason")
                        or h.get("rationale")
                        or ""
                    )

                    evidence = (
                        h.get("evidence")
                        or h.get("evidence_summary")
                        or ""
                    )

                    if isinstance(evidence, list):
                        evidence = "<br>".join(
                            f"• {e}" for e in evidence
                        )

                    html += f"""
<div style="margin-bottom:20px;">

<b>Hypothesis</b><br>
{hypothesis}<br><br>


<b>Evidence</b><br>
{evidence}

</div>
"""

                else:

                    html += f"""

<div style="margin-bottom:20px;">

{h}

</div>

"""

        else:

            html += "<p>None</p>"

        html += """

</div>


<div class="section">

<h2>Detected Bottlenecks</h2>

"""

        bottlenecks = report.get("bottlenecks", [])

        if bottlenecks:

            for b in bottlenecks:

                if isinstance(b, dict):

                    evidence = (
                        b.get("evidence")
                        or b.get("evidence_summary")
                        or ""
                    )

                    if isinstance(evidence, list):
                        evidence = "<br>".join(
                            f"• {e}" for e in evidence
                        )

                    html += f"""

<div style="margin-bottom:20px;">

<b>Classification</b><br>

{b.get("classification","")}<br><br>

<b>Evidence</b><br>

{evidence}

</div>

"""

                else:

                    html += f"""

<div style="margin-bottom:20px;">

{b}

</div>

"""

        else:

            html += "<p>No bottlenecks identified.</p>"

        html += """

</div>


<div class="section">

<h2>Recommendations</h2>

"""

        recommendations = report.get("recommendations", [])

        if recommendations:

            for r in recommendations:

                if isinstance(r, dict):

                    html += f"""

<div style="margin-bottom:25px;">

<b>Action</b><br>

{r.get("action","")}<br><br>


<b>Expected Benefit</b><br>

{r.get("expected_benefit","")}<br><br>

<b>Risk</b><br>

{r.get("risk","")}<br><br>



<b>Validation</b><br>

{r.get("validation","")}

</div>

"""

                else:

                    html += f"""

<div style="margin-bottom:20px;">

{r}

</div>

"""

        else:

            html += "<p>No recommendations generated.</p>"

        html += """

</div>

</body>

</html>

"""

        Path(output_file).write_text(
            html,
            encoding="utf-8"
        )