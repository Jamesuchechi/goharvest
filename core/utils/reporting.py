def generate_markdown_report(result) -> str:
    lines = [
        f"# GOharveST Report: {result.job.url}",
        "",
        "## Summary",
        "",
        f"- Content length: {len(result.content)}",
        f"- Total assets: {result.total_assets}",
        "",
    ]
    return "\n".join(lines)
