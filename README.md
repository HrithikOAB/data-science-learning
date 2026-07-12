# 🚀 Data Science Learning & Generative AI

A comprehensive collection of **Data Science**, **Machine Learning**, and **Generative AI** learning notebooks built using **Python**, **Jupyter Notebook**, and **uv**.

This repository is designed for beginners as well as intermediate learners who want hands-on practice with real-world datasets and modern AI frameworks.

---

# 📚 Repository Contents

```
.
├── Complete_Data_Science_Course.ipynb
├── Data_Cleaning_and_Preprocessing_Course.ipynb
├── Important_Data_Science_Topics.ipynb
├── LangChain_RAG_Pipeline_with_100_Page_PDF.ipynb
├── student_performance_test_dataset.csv
├── Python_Django_Session1.ipynb
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# 📖 Notebooks

## 1. Complete_Data_Science_Course.ipynb

An end-to-end Data Science workflow covering:

- Data Loading
- Exploratory Data Analysis (EDA)
- Data Visualization
- Feature Engineering
- Feature Selection
- Model Building
- Model Evaluation
- Hyperparameter Tuning
- Model Comparison
- Saving Models

Dataset Used:

- Student Performance Dataset

---

## 2. Data_Cleaning_and_Preprocessing_Course.ipynb

Learn how to prepare data before machine learning.

Topics include:

- Missing Values
- Duplicate Records
- Outlier Detection
- Categorical Encoding
- Feature Scaling
- Normalization
- Standardization
- Data Transformation
- Pipelines
- Train/Test Split
- Data Leakage Prevention

---

## 3. Important_Data_Science_Topics.ipynb

Theory + Practical concepts including:

- Statistics
- Probability
- Sampling Techniques
- Bias vs Variance
- Cross Validation
- Evaluation Metrics
- Feature Importance
- Explainable AI
- Ethics in AI
- Project Checklist

---

## 4. LangChain_RAG_Pipeline_with_100_Page_PDF.ipynb

Build a complete Retrieval-Augmented Generation (RAG) pipeline using LangChain.

Topics:

- Document Loading
- Text Chunking
- Embedding Models
- Vector Databases
- Similarity Search
- Retrieval
- Prompt Engineering
- LLM Integration
- Question Answering
- End-to-End PDF Chat

---

## Dataset

`student_performance_test_dataset.csv`

Dataset used throughout the notebooks for practical implementation.

---

# 🐍 Python Version

Recommended:

```
Python 3.12+
```

---

# ⚡ Why use uv?

**uv** is an extremely fast Python package manager and project manager written in Rust.

Compared to pip, uv provides:

- 🚀 Much faster package installation
- 🔒 Deterministic dependency locking
- 📦 Built-in virtual environment management
- ⚡ Faster dependency resolution
- 🛠️ Modern Python project workflow

---

# 🛠 Installing uv

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify installation:

```bash
uv --version
```

---

# 📦 Clone Repository

```bash
git clone https://github.com/your-username/data-science-learning.git

cd data-science-learning
```

---

# ⚙️ Create Virtual Environment

Create a virtual environment:

```bash
uv venv
```

This creates:

```
.venv/
```

Create with a specific Python version:

```bash
uv venv --python 3.12
```

---

# ▶️ Activate Virtual Environment

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

# 📥 Install Dependencies

If the project contains a `pyproject.toml` file:

```bash
uv sync
```

`uv sync`:

- Reads `pyproject.toml`
- Installs all dependencies
- Creates/updates `uv.lock`
- Ensures everyone gets the same package versions

---

# ➕ Install a Package

Example:

```bash
uv add pandas
```

Another example:

```bash
uv add scikit-learn
```

This command:

- Installs the package
- Updates `pyproject.toml`
- Updates `uv.lock`

---

# ➕ Install Development Dependencies

```bash
uv add --dev pytest
```

Useful for:

- Testing
- Linting
- Formatting
- Development tools

---

# ❌ Remove a Package

```bash
uv remove pandas
```

Removes the dependency from:

- pyproject.toml
- uv.lock

---

# 🔄 Update Dependencies

Update everything:

```bash
uv sync --upgrade
```

Update a specific package:

```bash
uv add pandas@latest
```

---

# 📄 View Installed Packages

```bash
uv pip list
```

---

# 🔍 Show Package Information

```bash
uv pip show pandas
```

---

# 📦 Install from requirements.txt

If needed:

```bash
uv pip install -r requirements.txt
```

---

# 📤 Export requirements.txt

Generate a traditional requirements file:

```bash
uv export --format requirements-txt > requirements.txt
```

Useful when deploying to platforms that expect `requirements.txt`.

---

# ▶️ Run Python Scripts

Instead of activating the environment:

```bash
uv run main.py
```

Or:

```bash
uv run app.py
```

`uv run` automatically uses the project's virtual environment.

---

# 📒 Launch Jupyter Notebook

```bash
uv run jupyter notebook
```

Or use JupyterLab:

```bash
uv run jupyter lab
```

---

# 📥 Install Jupyter

```bash
uv add jupyter
```

or

```bash
uv add jupyterlab
```

---

# 🔒 Lock Dependencies

Generate/update the lock file:

```bash
uv lock
```

This ensures every contributor installs identical dependency versions.

---

# 🔄 Synchronize Environment

```bash
uv sync
```

This command:

- Reads `uv.lock`
- Installs missing packages
- Removes unnecessary packages
- Keeps the environment identical across machines

---

# 🧹 Remove Virtual Environment

Simply delete:

```
.venv/
```

Then recreate:

```bash
uv venv

uv sync
```

---

# 📁 Typical Project Structure

```
project/
│
├── .venv/
├── notebooks/
├── datasets/
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

---

# 📌 Common uv Commands

| Command | Description |
|----------|-------------|
| `uv venv` | Create a virtual environment |
| `uv sync` | Install dependencies from `pyproject.toml`/`uv.lock` |
| `uv add package` | Add a new dependency |
| `uv remove package` | Remove a dependency |
| `uv lock` | Generate or update the lock file |
| `uv run file.py` | Run a Python script inside the project environment |
| `uv run jupyter notebook` | Launch Jupyter Notebook |
| `uv run jupyter lab` | Launch JupyterLab |
| `uv pip list` | List installed packages |
| `uv pip show package` | Display package details |
| `uv export --format requirements-txt > requirements.txt` | Export dependencies to `requirements.txt` |
| `uv sync --upgrade` | Upgrade installed dependencies |

---

# 💡 Recommended Learning Order

1. Complete Data Science Course
2. Data Cleaning & Preprocessing
3. Important Data Science Topics
4. LangChain RAG Pipeline
5. Build your own ML and GenAI projects

---

# 🤝 Contributing

Contributions are welcome!

You can contribute by:

- Improving notebooks
- Fixing bugs
- Adding datasets
- Creating new tutorials
- Improving documentation

---

# ⭐ Support

If you found this repository helpful:

- ⭐ Star the repository
- 🍴 Fork it
- 🛠️ Contribute
- 📢 Share it with others

Happy Learning! 🚀