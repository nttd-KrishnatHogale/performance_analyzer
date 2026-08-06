# # from pathlib import Path


# # class HTMLGenerator:

# #     def generate(
# #         self,
# #         output_file,
# #         report,
# #         timeline,
# #         correlations
# #     ):

# #         html = f"""
# # <!DOCTYPE html>

# # <html>

# # <head>

# # <meta charset="utf-8">

# # <title>Performance RCA Report</title>

# # <style>

# # body{{
# # font-family:Arial;
# # margin:30px;
# # background:#f8f8f8;
# # }}

# # h1{{
# # color:#0b5394;
# # }}

# # table{{
# # border-collapse:collapse;
# # width:100%;
# # }}

# # th,td{{
# # border:1px solid #ddd;
# # padding:8px;
# # }}

# # th{{
# # background:#0b5394;
# # color:white;
# # }}

# # .section{{
# # background:white;
# # padding:20px;
# # margin-bottom:20px;
# # border-radius:10px;
# # box-shadow:0 0 5px gray;
# # }}

# # .high{{
# # color:red;
# # font-weight:bold;
# # }}

# # .medium{{
# # color:orange;
# # font-weight:bold;
# # }}

# # .low{{
# # color:green;
# # }}

# # </style>

# # </head>

# # <body>

# # <h1>Performance Root Cause Analysis Report</h1>

# # <div class="section">

# # <h2>Executive Summary</h2>

# # <p>{report.get("summary", "No summary generated")}</p>

# # </div>

# # <div class="section">

# # <h2>Primary Root Cause</h2>

# # <p>{report.get("root_cause", "Not available")}</p>

# # </div>

# # <div class="section">

# # <h2>Confidence</h2>

# # <h3>{report.get("confidence", "UNKNOWN")}</h3>

# # </div>

# # <div class="section">

# # <h2>Timeline</h2>

# # <table>

# # <tr>

# # <th>Start</th>

# # <th>Peak</th>

# # <th>Recovery</th>

# # <th>Component</th>

# # <th>Issue</th>

# # </tr>
# # """

# #         for e in timeline:

# #             html += f"""

# # <tr>

# # <td>{e.start_time}</td>

# # <td>{e.peak_time}</td>

# # <td>{e.recovery_time}</td>

# # <td>{e.component}</td>

# # <td>{e.metric}</td>

# # </tr>

# # """

# #         html += """

# # </table>

# # </div>

# # <div class="section">

# # <h2>Correlation Chain</h2>

# # <table>

# # <tr>

# # <th>Source</th>

# # <th>Target</th>

# # <th>Relation</th>

# # <th>Confidence</th>

# # </tr>

# # """

# #         for c in correlations:

# #             html += f"""

# # <tr>

# # <td>{c["source"]}</td>

# # <td>{c["target"]}</td>

# # <td>{c["relation"]}</td>

# # <td>{c["confidence"]}</td>

# # </tr>

# # """

# #         html += """

# # </table>

# # </div>

# # <div class="section">

# # <h2>Bottlenecks</h2>

# # <ul>

# # """

# #         for b in report.get("bottlenecks", []):

# #             html += f"<li>{b}</li>"

# #         html += """

# # </ul>

# # </div>

# # <div class="section">

# # <h2>Recommendations</h2>

# # <ul>

# # """

# #         for r in report.get("recommendations", []):

# #             html += f"<li>{r}</li>"

# #         html += """

# # </ul>

# # </div>

# # <div class="section">

# # <h2>Detailed Narrative</h2>

# # <p>

# # """

# #         html += report.get("timeline", "Timeline not available.")

# #         html += """

# # </p>

# # </div>

# # </body>

# # </html>

# # """

# #         Path(output_file).write_text(
# #             html,
# #             encoding="utf-8"
# #         )


# from pathlib import Path


# class HTMLGenerator:

#     def generate(
#         self,
#         output_file,
#         report,
#         timeline,
#         correlations
#     ):

#         confidence = report.get("confidence", "UNKNOWN").upper()

#         if confidence == "HIGH":
#             confidence_class = "high"
#         elif confidence == "MEDIUM":
#             confidence_class = "medium"
#         else:
#             confidence_class = "low"

#         html = f"""
# <!DOCTYPE html>
# <html>

# <head>

# <meta charset="utf-8">

# <title>Performance RCA Report</title>

# <style>

# body {{
#     font-family: Arial;
#     margin: 30px;
#     background: #f5f5f5;
# }}

# h1 {{
#     color: #0b5394;
# }}

# table {{
#     width:100%;
#     border-collapse:collapse;
# }}

# th,td {{
#     border:1px solid #ccc;
#     padding:8px;
#     text-align:left;
# }}

# th {{
#     background:#0b5394;
#     color:white;
# }}

# .section {{
#     background:white;
#     padding:20px;
#     margin-bottom:25px;
#     border-radius:8px;
#     box-shadow:0 0 6px rgba(0,0,0,.15);
# }}

# .high {{
#     color:red;
#     font-weight:bold;
# }}

# .medium {{
#     color:orange;
#     font-weight:bold;
# }}

# .low {{
#     color:green;
#     font-weight:bold;
# }}

# li {{
#     margin-bottom:8px;
# }}

# </style>

# </head>

# <body>

# <h1>Performance Root Cause Analysis Report</h1>

# <div class="section">

# <h2>Executive Summary</h2>

# <p>{report.get("summary","Not Available")}</p>

# </div>

# <div class="section">

# <h2>Executive Analysis</h2>

# <table>

# <tr>
# <th>Primary Root Cause</th>
# <td>{report.get("root_cause","Not Available")}</td>
# </tr>

# <tr>
# <th>Primary Bottleneck</th>
# <td>{report.get("primary_bottleneck","Not Available")}</td>
# </tr>

# <tr>
# <th>Confidence</th>
# <td class="{confidence_class}">
# {confidence}
# </td>
# </tr>

# </table>

# </div>

# <div class="section">

# <h2>Timeline Summary</h2>

# <p>

# {report.get("timeline","Timeline not available.")}

# </p>

# </div>

# <div class="section">

# <h2>Detected Timeline Events</h2>

# <table>

# <tr>

# <th>Start</th>
# <th>Peak</th>
# <th>Recovery</th>
# <th>Component</th>
# <th>Metric</th>

# </tr>

# """

#         for e in timeline:

#             html += f"""

# <tr>

# <td>{e.start_time}</td>
# <td>{e.peak_time}</td>
# <td>{e.recovery_time}</td>
# <td>{e.component}</td>
# <td>{e.metric}</td>

# </tr>

# """

#         html += """

# </table>

# </div>

# <div class="section">

# <h2>Correlation Chain</h2>

# <table>

# <tr>

# <th>Source</th>
# <th>Target</th>
# <th>Relation</th>
# <th>Confidence</th>

# </tr>

# """

#         for c in correlations:

#             html += f"""

# <tr>

# <td>{c.get("source","")}</td>
# <td>{c.get("target","")}</td>
# <td>{c.get("relation","")}</td>
# <td>{c.get("confidence","")}</td>

# </tr>

# """

#         html += """

# </table>

# </div>

# <div class="section">

# <h2>Supporting Evidence</h2>

# <ul>

# """

#         for evidence in report.get("supporting_evidence", []):

#             html += f"<li>{evidence}</li>"

#         html += """

# </ul>

# </div>

# <div class="section">

# <h2>Rejected Hypotheses</h2>

# <ul>

# """

#         for hypothesis in report.get("rejected_hypotheses", []):

#             html += f"<li>{hypothesis}</li>"

#         html += """

# </ul>

# </div>

# <div class="section">

# <h2>Detected Bottlenecks</h2>

# <ul>

# """

#         for bottleneck in report.get("bottlenecks", []):

#             if isinstance(bottleneck, dict):

#                 html += f"""
# <li>

# <b>{bottleneck.get("name","")}</b><br>

# Reason : {bottleneck.get("reason","")}

# </li>
# """

#             else:

#                 html += f"<li>{bottleneck}</li>"

#         html += """

# </ul>

# </div>

# <div class="section">

# <h2>Recommendations</h2>

# <ul>

# """

#         for recommendation in report.get("recommendations", []):

#             if isinstance(recommendation, dict):

#                 html += f"""

# <li>

# <b>Action</b><br>

# {recommendation.get("action","")}<br><br>

# <b>Purpose</b><br>

# {recommendation.get("purpose","")}<br><br>

# <b>Expected Benefit</b><br>

# {recommendation.get("expected_benefit","")}<br><br>

# <b>Risk</b><br>

# {recommendation.get("risk","")}<br><br>

# <b>Restart Required</b><br>

# {recommendation.get("restart_required","")}<br><br>

# <b>Validation</b><br>

# {recommendation.get("validation","")}

# </li>

# """

#             else:

#                 html += f"<li>{recommendation}</li>"

#         html += """

# </ul>

# </div>

# </body>

# </html>

# """

#         Path(output_file).write_text(
#             html,
#             encoding="utf-8"
#         )


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

<h2>Detected Timeline Events</h2>

<table>

<tr>

<th>Start</th>
<th>Peak</th>
<th>Recovery</th>
<th>Component</th>
<th>Metric</th>

</tr>

"""

        for e in timeline:

            html += f"""
<tr>

<td>{e.start_time}</td>
<td>{e.peak_time}</td>
<td>{e.recovery_time}</td>
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

        if correlations:

            for c in correlations:

                html += f"""

<tr>

<td>{c.get("source","")}</td>
<td>{c.get("target","")}</td>
<td>{c.get("relation","")}</td>
<td>{c.get("confidence","")}</td>

</tr>

"""

        else:

            html += """
<tr>

<td colspan="4">
No correlation detected.
</td>

</tr>
"""

        html += """

</table>

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

                html += f"""

<div class="card">

<b>Hypothesis</b><br>

{h.get("hypothesis","")}<br><br>

<b>Status</b><br>

{h.get("status","")}<br><br>

<b>Reason</b><br>

{h.get("reason","")}

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

                html += f"""

<div class="card">

<b>Component</b><br>

{b.get("component","")}<br><br>

<b>Type</b><br>

{b.get("type","")}<br><br>

<b>Classification</b><br>

{b.get("classification","")}<br><br>

<b>Evidence</b><br>

{b.get("evidence","")}

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

                html += f"""

<div class="card">

<b>Action</b><br>

{r.get("action","")}<br><br>

<b>Details</b><br>

{r.get("details","")}<br><br>

<b>Expected Benefit</b><br>

{r.get("expected_benefit","")}<br><br>

<b>Risk</b><br>

{r.get("risk","")}<br><br>

<b>Restart Required</b><br>

{r.get("restart_required","")}<br><br>

<b>Validation</b><br>

{r.get("validation","")}

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