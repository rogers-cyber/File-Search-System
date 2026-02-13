# File Search System v1.0.1

## Overview
**File Search System** is a professional Python-based tool that allows you to search files and their contents across multiple formats including `.txt`, `.csv`, `.xlsx`, `.pdf`, and `.xml`. It provides an ultra-fast search with regex support, file type filters, folder exclusions, and preview of exact matches including line, cell, page, or XML tag context.

---

## Features
- Search by **File Name** or **Content**.
- Support for **regex and multi-term searches**.
- Filter by file types and exclude specific folders.
- Real-time **progress, ETA, and speed metrics**.
- Results displayed in a **treeview with clickable paths**.
- **Preview column** shows exact line/cell/page/tag match.
- **Export results** to CSV including preview context.
- Double-click a result to **open the file**.

---

## Supported File Types
- **Text**: `.txt`  
- **CSV**: `.csv`  
- **Excel**: `.xlsx`  
- **PDF**: `.pdf`  
- **XML**: `.xml`  

---

## Installation

1. Clone or download the project folder.
2. Make sure you have **Python 3.9+** installed.
3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## How to Use

1. Run the application:
```bash
python file_search_system.py
```
2. Choose a **root folder** to scan.
3. Enter a **search term** (you can enable regex if needed).
4. Optionally, specify **file types** and **folders to exclude**.
5. Click **SEARCH** to start scanning.
6. Matches appear in the **treeview** with preview context.
7. **Click** a result to copy the path, **double-click** to open the file.
8. Click **Export Results** to save results to a CSV file.

---

## Notes
- Excel matches show **sheet, row, column**.
- PDF matches show **page number and snippet**.
- XML matches show **tag name and snippet**.
- Large directories may take longer depending on the number of files.

---

## Requirements

See `requirements.txt` for Python package dependencies:

```
ttkbootstrap>=0.8.0
pandas>=2.0.0
PyPDF2>=3.0.0
openpyxl>=3.1.0
```

---

## Developer Info
Developed by Mate Technologies.  
Professional, Upwork-ready Python tool for file searching and content inspection.

