import json
import os


def save_detailed_output(final_results, output_dir="output"):

    os.makedirs(output_dir, exist_ok=True)

    # Save per flow
    for flow_id, data in final_results["flows"].items():

        file_path = f"{output_dir}/{flow_id}_report.json"

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

    # Save per server (optional)
    for server_id, data in final_results["servers"].items():

        file_path = f"{output_dir}/{server_id}_report.json"

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

def generate_html_report(final_results, output_dir="output"):

    os.makedirs(output_dir, exist_ok=True)

    for flow_id, data in final_results["flows"].items():

        html = []

        # ======================================================
        # HTML HEADER
        # ======================================================
        html.append(f"""
        <html>
        <head>
            <title>RCA Report - {flow_id}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                }}
                h2 {{
                    color: #34495e;
                }}
                .section {{
                    margin-bottom: 25px;
                    padding: 15px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }}
                .bottleneck {{
                    color: red;
                    font-weight: bold;
                }}
                .risk {{
                    color: orange;
                }}
                .action {{
                    color: green;
                }}
                .box {{
                    margin: 5px 0;
                }}
            </style>
        </head>
        <body>
        """)

        # ======================================================
        # ✅ TITLE
        # ======================================================
        html.append(f"<h1>Flow Report: {flow_id}</h1>")

        # ======================================================
        # ✅ SECTION 1: SUMMARY (SHORT OUTPUT)
        # ======================================================
        summary = data.get("summary", {})
        layers = data.get("layer_breakdown", {})
        recommendations = data.get("recommendations", [])

        html.append("<div class='section'>")
        html.append("<h2>1. Summary (Actionable View)</h2>")

        html.append(f"<p><b>Primary Bottleneck:</b> {summary.get('primary_bottleneck')}</p>")
        html.append(f"<p><b>Confidence:</b> {summary.get('confidence')}</p>")

        # ------------------------------
        # BOTTLENECKS
        # ------------------------------
        html.append("<h3>🚨 Bottlenecks</h3><ul>")
        for layer, issues in layers.items():
            for i in issues:
                if i["severity"] == "HIGH":
                    html.append(
                        f"<li class='bottleneck'>{i['issue']} ({layer})</li>"
                    )
        html.append("</ul>")

        # ------------------------------
        # RISKS
        # ------------------------------
        html.append("<h3>⚠️ Risks</h3><ul>")
        for layer, issues in layers.items():
            for i in issues:
                if i["severity"] == "MEDIUM":
                    html.append(
                        f"<li class='risk'>{i['issue']} ({layer})</li>"
                    )
        html.append("</ul>")

        # ------------------------------
        # ACTION ITEMS
        # ------------------------------
        html.append("<h3>✅ Action Items</h3><ul>")
        for r in recommendations:
            html.append(f"<li class='action'>{r}</li>")
        html.append("</ul>")

        html.append("</div>")

        # ======================================================
        # ✅ SECTION 2: DETAILED REPORT
        # ======================================================
        html.append("<div class='section'>")
        html.append("<h2>2. Detailed RCA Report</h2>")

        # ------------------------------
        # ROOT CAUSE CHAIN
        # ------------------------------
        chain = data.get("root_cause_chain", [])
        html.append("<h3>🔁 Root Cause Chain</h3>")
        html.append(f"<p>{' → '.join(chain) if chain else 'Not available'}</p>")

        # ------------------------------
        # LAYER BREAKDOWN
        # ------------------------------
        html.append("<h3>📊 Layer-wise Breakdown</h3>")

        for layer, issues in layers.items():
            html.append(f"<h4>{layer}</h4><ul>")
            if not issues:
                html.append("<li>No major issues</li>")
            else:
                for i in issues:
                    html.append(
                        f"<li><b>{i['issue']}</b> ({i['severity']}) "
                        f"<br/> {i['detail']}</li>"
                    )
            html.append("</ul>")

        # ------------------------------
        # EVIDENCE
        # ------------------------------
        evidence = data.get("evidence", [])
        html.append("<h3>📌 Supporting Evidence</h3><ul>")

        for e in evidence:
            html.append(
                f"<li><b>{e['cause']}</b> - {e['justification']} "
                f"(Score: {e['score']})</li>"
            )

        html.append("</ul>")

        # ------------------------------
        # RECOMMENDATIONS
        # ------------------------------
        html.append("<h3>✅ Recommendations</h3><ul>")

        for r in recommendations:
            html.append(f"<li>{r}</li>")

        html.append("</ul>")

        html.append("</div>")

        # ======================================================
        # HTML FOOTER
        # ======================================================
        html.append("</body></html>")

        # ======================================================
        # WRITE FILE
        # ======================================================
        file_path = f"{output_dir}/{flow_id}_report.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html))
        print(f"✅ HTML report generated: {file_path}")
