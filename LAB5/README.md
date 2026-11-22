# Lab 5: Static Code Analysis – Income Tax Calculator

## Overview

This project demonstrates the use of static code analysis tools to identify and fix code quality issues, coding standard violations, and potential security vulnerabilities in a Python-based income tax calculator.

## Objectives

- Perform static code analysis on a Python application.
- Identify coding errors, style violations, and security vulnerabilities.
- Improve code readability, maintainability, and security.
- Apply recommended fixes based on analysis reports.
- Compare the results before and after code improvements.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application implementation |
| Pylint | Code quality and maintainability analysis |
| Flake8 | PEP 8 style and formatting checks |
| Bandit | Security vulnerability scanning |
| Cryptography | AES-GCM encryption and RSA key generation |
| DefusedXML | Secure XML parsing |

## Application Features

The income tax calculator demonstrates:

- Simplified new-regime and old-regime tax calculations.
- Comparison of both regimes to identify the lower calculated tax.
- PAN format validation using regular expressions.
- PAN encryption using AES-GCM.
- RSA private key generation with a 2048-bit key.
- Form 16 XML parsing using `defusedxml`.

## Issues Identified and Fixes Applied

The original code contained several issues identified through static analysis and manual review.

| Category | Identified Issue | Fix Applied |
|---|---|---|
| Security | AES-ECB encryption | Replaced with AES-GCM authenticated encryption |
| Security | RSA 1024-bit key | Increased key size to 2048 bits |
| Security | Unsafe XML parsing using minidom | Replaced with defusedxml |
| Security | CGIHandler usage | Removed unnecessary CGI functionality |
| Functional | Incorrect progressive tax calculation | Implemented slab-wise tax calculation |
| Functional | PAN validation accepted extra characters | Used `re.fullmatch()` |
| Code Quality | Unused imports and variables | Removed unnecessary declarations |
| Code Quality | CamelCase naming | Converted functions and variables to snake_case |
| Code Quality | Missing docstrings | Added module and function documentation |
| Code Quality | Bare exception handling | Added specific exception handling |
| Code Quality | Unused function parameters | Removed unnecessary parameters |

For a detailed list of identified issues, refer to [`issues.md`](issues.md).

## Before and After Analysis

The following results are based on the reports stored in the repository.

| Static Analysis Tool | Before Fixes | After Fixes |
|---|---:|---:|
| Pylint | 4.57/10 | 10.00/10 |
| Flake8 | 22 violations | 2 violations |
| Bandit | 6 findings | 0 findings |

### Pylint

Pylint initially reported issues involving naming conventions, missing documentation, unused variables, unnecessary statements, and code structure.

After improvements, the recorded score increased from **4.57/10 to 10.00/10**.

### Flake8

Flake8 initially reported 22 violations, including unused imports, formatting problems, long lines, and bare exception handling.

The AFTER report contains only two remaining line-length violations (`E501`). These should be corrected in a subsequent cleanup.

### Bandit

Bandit initially identified six security findings:

- Use of `minidom` for XML parsing.
- Use of `CGIHandler`.
- Insecure AES-ECB encryption.
- Weak 1024-bit RSA key generation.

After applying the security improvements, Bandit reported **no issues identified**.

## Project Structure

```text
L5_53_income-tax-calculator/
│
├── BEFORE/
│   ├── bandit_report.txt
│   ├── flake8_report.txt
│   └── pylint_report.txt
│
├── AFTER/
│   ├── corrected_tax_calc.py
│   ├── bandit_report.txt
│   ├── flake8_report.txt
│   └── pylint_report.txt
│
├── tax_calculator.py
├── issues.md
└── README.md
```

- `tax_calculator.py`: Original implementation.
- `BEFORE/`: Static analysis reports generated for the original code.
- `AFTER/`: Corrected implementation and its static analysis reports.
- `issues.md`: Detailed documentation of the identified issues and their fixes.

## Setup and Execution

### Prerequisites

- Python 3.9 or later.
- pip package manager.

### 1. Clone the repository

```bash
git clone https://github.com/Janavi88/L5_53_income-tax-calculator.git
cd L5_53_income-tax-calculator
```

### 2. Install dependencies

```bash
pip install cryptography defusedxml pylint flake8 bandit
```

### 3. Configure the encryption key

For Windows PowerShell:

```powershell
$key = python -c "import secrets; print(secrets.token_hex(32))"
$env:PAN_KEY = $key
```

The environment variable stores a randomly generated 256-bit AES key in hexadecimal format.

### 4. Execute the corrected program

```powershell
python .\AFTER\corrected_tax_calc.py
```

### 5. Run static analysis

```powershell
pylint .\AFTER\corrected_tax_calc.py

flake8 .\AFTER\corrected_tax_calc.py

bandit .\AFTER\corrected_tax_calc.py
```

## Conclusion


By applying the recommended fixes, the project achieved:

- An improvement in Pylint score from 4.57/10 to 10.00/10.
- A reduction in Flake8 violations from 22 to 2.
- A reduction in Bandit security findings from 6 to 0.


