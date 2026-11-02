"""The audit agent: a LangGraph workflow that scans a workbook, asks the meaning model about each
formula run, verifies every flagged cell against the workbook itself, and writes the report."""
