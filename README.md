# Player-Evaluation-Engine ⚽
Player Evaluation Engine is a user-friendly desktop application designed for evaluating football players based on statistical data extracted from Football Manager.
Ideal for football analytics enthusiast or anyone passionate about making data-driven transfer decisions!

## ⚠️ WARNING

> **For large HTML files, data cleaning may take up to 20 minutes.**  
> Please be patient and avoid interrupting the process.

---

## 🚀 Features

- **🔄 Load & Clean Data**  
  Import HTML file extracted from Football Manager (use the upload Evalution Engine Scout View.fmf) and automatically clean and prepare the dataset.

- **🔍 Set UP Filters**  
  Filter players based on nationality, division, age range, salary, and playing positions using an intuitive GUI.

- **⚙️ Select Stats & Weights**  
  Select from a wide array of player stats and assign custom weights to prioritize what's important for your analysis.

- **📊 Evaluate Players**  
  Score and rank players by position based on your custom stat configuration and view the results instantly.

---

## 📦 Installation

### Option 1: Run the Standalone `.exe`

1. Download `Evaluation_Engine.exe` from the [Releases] [Evaluation Engine.exe](https://github.com/AKoronaios/Player-Evaluation-Engine/releases/download/v1.0.0/Evaluation.Engine.exe) section.
2. Double-click to launch the app.
3. No Python or dependencies required.

### Option 2: Run from Source (Python)

1. Clone this repo:
   ```bash
   git clone https://github.com/AKoronaios/Player-Evaluation-Engine.git
   cd football-analytics-tool
   pip install -r requirements.txt
   python evalution_engine_app.py

## ⚙ Technology Stack
- **Python** (Pandas, Tkinter)
- **Data Processing with Pandas**
- **Tkinter GUI Components** (for user-friendly interaction)
- **PyInstaller** (for executable packaging)


