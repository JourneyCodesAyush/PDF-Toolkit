# Contributing to PDF Toolkit

Thank you for considering contributing to **PDF Toolkit**! Whether you're fixing bugs, suggesting features, or improving the documentation, we welcome all contributions.

Please follow the steps below to get started with contributing to the project.

## Code of Conduct

Please make sure to read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). It ensures a positive and respectful environment for all contributors.

---

## 📚 Table of Contents

- [Contributing to PDF Toolkit](#contributing-to-pdf-toolkit)
  - [Code of Conduct](#code-of-conduct)
  - [📚 Table of Contents](#-table-of-contents)
  - [🛠️ Getting Started](#️-getting-started)
    - [Prerequisites](#prerequisites)
  - [🚧 Making a Contribution](#-making-a-contribution)
    - [🧑‍💻 Code Style Guidelines](#-code-style-guidelines)
  - [✅ Tips for a Great Pull Request](#-tips-for-a-great-pull-request)
  - [🙋‍♂️ Need Help](#️-need-help)
  - [🙌 Thank You](#-thank-you)


---

## 🛠️ Getting Started

To contribute, you’ll need to set up the project on your local machine. Follow these steps:

### Prerequisites
1. **Python 3.9+**: Ensure you have Python 3.9 or above installed on your machine. You can check your Python version by running:
   ```bash
   python --version
   ```
2. **Clone the repository**: First, clone the repository to your local machine using the following command:
   ```bash
    git clone https://github.com/JourneyCodesAyush/pdf-toolkit.git
    cd pdf-toolkit
    ```
3. **(Recommended) Create a virtual environment**: Creating a virtual environment helps isolate dependencies without affecting your system Python setup.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4. **Install dependencies**: Use pip to install all the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. **Run the application locally**:
   ```bash
   python main.py
    ```


### Linux Quick Launch (Optional, for Linux Users)

If you're on Linux OS, you can simplify the setup process using the `launch_linux.sh` script. This script sets up the environment and installs dependencies automatically.

#### To use the script:

1. Give the script executable permissions:
   
    ```bash
    chmod +x launch_linux.sh
    ```
2. Run the script: 
   
    ```bash
    ./launch_linux.sh
    ```
---

## 🧪 Running Tests

All tests are written using [`pytest`](https://docs.pytest.org/). To run the test suite:
1. Install `pytest`
   ```bash
   pip install pytest
   ```
2. Run all tests:
   ```bash
   pytest
   ```
If `core/` is not found, run: 
   ```bash
   python -m pytest
   ```
---

## 🚧 Making a Contribution

1. Understand the Project Structure
    ``` 
    pdf-toolkit/
    │
    │
    ├── .github/
    │    ├── ISSUE_TEMPLATE/
    │    │   ├── bug_report.yml
    │    │   ├── feature_request.yml
    │    │   ├── question.yml
    │    │   └── config.yml
    │    └── PULL_REQUEST_TEMPLATE.yml
    │     
    │
    ├── assets/ 
    │   ├── PDF_file.ico
    │   ├── PDF_file.png
    │   ├── screenshot.png
    │   └── screenshot2.png 
    │   
    ├── gui/
    │   ├── __init__.py
    │   ├── error_handler_gui.py
    │   ├── merge_gui.py
    │   ├── rename_gui.py
    │   ├── split_gui.py
    │   ├── extract_page_pdf.py
    │   ├── common_ui.py
    │   ├── main_window.py
    │   └── batch/
    │       ├── __init__.py
    │       ├── batch_operations_gui.py
    │       ├── batch_merge_gui.py
    │       ├── batch_rename_gui.py
    │       └── batch_split_gui.py
    │
    ├── core/
    │   ├── __init__.py
    │   ├── pdf_merge.py
    │   ├── pdf_rename.py
    │   ├── pdf_splitter.py
    │   ├── pdf_extract_pages.py
    │   ├── utils.py
    │   ├── error_handler.py
    │   └── batch/
    │       ├── __init__.py
    │       ├── batch_merge.py
    │       ├── batch_rename.py
    │       └── batch_split.py
    │
    ├── logs/
    │   ├── errors.json
    │   └── user_activity.log
    │
    ├── tests/
    │   ├── conftest.py
    │   ├── error_handler.py
    │   └── core_tests/
    │       ├──__init__.py
    │       ├── test_pdf_merge.py
    │       ├── test_pdf_rename.py
    │       ├── test_pdf_splitter.py
    │       ├── test_pdf_extract.py
    │       └── batch/
    │           ├── __init__.py
    │           ├── test_pdf_merge.py
    │           ├── test_pdf_rename.py
    │           └── test_pdf_splitter.py
    │
    ├── config/
    │   ├── config.py
    │   ├── json_formatter.py
    │   └── preferences.py
    │
    ├── user_config/
    │   └── preferences.json
    │
    ├── main.py
    ├── README.md
    ├── CHANGELOG.md
    ├── CODE_OF_CONDUCT.md
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    ├── launch_linux.sh
    ├── LICENSE
    └── .gitignore   
    ```

2. Write Tests

    If you are adding new logic in `core/`, please add unit tests in the `tests/` directory.

3. Follow Commit Message Convention
   
    We use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)    
    ```bash
        <type>(<scope>):<short message>
    ```
    Examples:
    ```bash
        feat(split): add multi-range page support
        fix(rename): handle non-PDF files gracefully
        docs(readme): update installation instructions
    ```
    
    Common types include: `feat`, `fix`, `docs`, `style`, `refactor`, `test` and `chore`.

4. Branch Naming Convention  
    Use clear and consistent branch names to indicate the purpose of your work.  
    Examples:  
    ```bash
        feature/pdf-merge-support
        bugfix/fix-path-issue
        docs/update-contributing-guide
    ```
    Use the prefix that best matches your contribution type:
        - `feature/` for new features
        - `bugfix/` for bug fixes
        - `docs/` for documentation-only changes

---

### 🧑‍💻 Code Style Guidelines

To maintain consistency across the codebase, please follow these standards when writing or editing code:

- ✅ **Formatting**: Format all Python files using [`black`](https://github.com/psf/black)  
    Run:  
    ```bash
    black .
    ```
- ✅ Import Sorting: Keep imports organized using [`isort`](https://pycqa.github.io/isort/)
    Run:  
    ```bash
    isort .
    ```

- ✅ **Style Guide**: Follow the [PEP8](https://peps.python.org/pep-0008/) style guide.

- ✅  **Error Handling**: Use the `Result` object and the shared `handle_exception()` function for all error reporting (see examples in `core/`).

- ✅ **Modular & Testable Code**: Keep functions small, focused, and testable. Avoid deeply nested logic or monolithic functions.
- ✅ **Naming Conventions**: Use `snake_case` for variables and functions, and clear, descriptive names that reflect their purpose.

---

## ✅ Tips for a Great Pull Request

- Make sure your code follows Python formatting standards (PEP8).
- Include relevant tests if applicable.
- Keep commits small and focused.
- Provide a clear description of your changes in the PR.
- Reference relevant issues (if any), e.g. `Closes #42`.

---

## 🙋‍♂️ Need Help

If you:
- Found a bug
- Have a question
- Want to suggest a feature


    Open an [Issue](https://github.com/JourneyCodesAyush/pdf-toolkit/issues) or start a [discussion](https://github.com/JourneyCodesAyush/pdf-toolkit/discussions)

---

## 🙌 Thank You

Thanks for making **PDF Toolkit** better!  
Every line of code, every typo fix, and every suggestion makes a difference.  
We’re excited to build this project with your help — let’s create something awesome together! 🚀
