# File Search System v1.0.1 – Advanced File & Content Search Tool (Source Code + EXE)

File Search System v1.0.1 is a professional, high-performance desktop application for searching files and inspecting their contents across large directory trees.  
It is designed for speed, accuracy, and usability, with real-time feedback and detailed match previews.

This repository includes:
- Full Python source code
- Prebuilt Windows executable available under the Releases section
- Portable desktop utility for daily and professional workflows

------------------------------------------------------------
WINDOWS DOWNLOAD (EXE)
------------------------------------------------------------

Download the latest Windows executable from GitHub Releases:

https://github.com/rogers-cyber/File-Search-System/releases

- No Python required
- Portable executable
- Ready-to-run on Windows

------------------------------------------------------------
FEATURES
------------------------------------------------------------

- Recursive Folder Scanning — Search entire directory trees
- File Content Search — Inspect text inside supported file formats
- Regex Support — Advanced pattern matching
- Multi-Keyword Matching — All terms must be present
- File Type Filters — Glob patterns (e.g. *.txt *.pdf)
- Folder Exclusion Rules — Skip unwanted directories
- Real-Time Progress Tracking
  - Progress bar
  - Estimated time remaining (ETA)
  - Files-per-second speed indicator
- Threaded Background Search — UI remains responsive
- Match Preview Column
  - Line number (TXT / CSV)
  - Sheet, row, and column (Excel)
  - Page and snippet (PDF)
  - XML tag and snippet
- Click to Copy File Path
- Double-Click to Open Files
- Export Results to CSV (includes preview context)
- Modern Dark UI — Built with Tkinter + ttkbootstrap
- Cross-Platform Python Source (Windows EXE provided)

------------------------------------------------------------
SUPPORTED FILE TYPES
------------------------------------------------------------

- Text Files: .txt
- CSV Files: .csv
- Excel Files: .xlsx
- PDF Documents: .pdf
- XML Files: .xml

------------------------------------------------------------
REPOSITORY STRUCTURE
------------------------------------------------------------

File-Search-System/
├── file_search_system.py
├── dist/
│   └── (empty or .gitkeep)
├── logo.ico
├── requirements.txt
├── README.md
└── LICENSE

------------------------------------------------------------
INSTALLATION (SOURCE CODE)
------------------------------------------------------------

1. Clone the repository:

git clone https://github.com/rogers-cyber/File-Search-System.git
cd File-Search-System

2. Install dependencies:

pip install -r requirements.txt

(Tkinter is included with standard Python installations.)

3. Run the application:

python file_search_system.py

------------------------------------------------------------
HOW TO USE
------------------------------------------------------------

1. Select Root Folder
   - Choose the main directory to scan

2. Enter Search Term
   - Enable Regex if required

3. Configure Filters
   - File type patterns (e.g. *.txt *.pdf)
   - Excluded folders (e.g. .git node_modules)

4. Start Search
   - Click SEARCH
   - Monitor progress, speed, and ETA in real time

5. Review Results
   - Matches appear in the treeview
   - Preview column shows exact match context

6. Interact with Results
   - Single click → copy file path
   - Double click → open file

7. Export
   - Click Export Results to save a CSV report

------------------------------------------------------------
DEPENDENCIES
------------------------------------------------------------

- Python 3.9+
- ttkbootstrap
- PyPDF2 (or compatible PDF reader)
- Excel reading library (implementation dependent)
- Tkinter
- threading / regex / standard Python libraries

See requirements.txt for exact versions.

------------------------------------------------------------
NOTES
------------------------------------------------------------

- Excel matches include sheet name, row, and column
- PDF matches include page number and text snippet
- XML matches include tag name and snippet
- Performance depends on file count and disk speed
- Designed for large directory structures

------------------------------------------------------------
ABOUT
------------------------------------------------------------

File Search System is a professional desktop utility created for fast, accurate file discovery and content inspection.

It is suitable for:
- Developers
- IT professionals
- Analysts
- Power users
- Internal enterprise tooling

------------------------------------------------------------
LICENSE
------------------------------------------------------------

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software,
including the source code and compiled executable,
with attribution.

See the LICENSE file for full details.
