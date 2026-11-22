# Static Analysis Issues — Income Tax Calculator

This document lists the issues identified in the original `tax_calculator.py` using Pylint, Bandit, Flake8 reports and manual code review.

**Baseline Pylint Score:** 4.57/10

**Baseline Bandit Findings:** 6 issues (2 High, 3 Medium, 1 Low)

**Baseline Flake8 Findings:** 22 violations

> Line numbers refer to the original, unmodified `tax_calculator.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| CGIHandler security concern | Security — High | 6, 92 | Bandit (B412) flags the use of `wsgiref.handlers.CGIHandler` because of potential security implications. | Remove CGIHandler if it is not required, or replace it with a safer application-serving approach. |
| Insecure AES encryption mode | Security — Medium | 77 | Bandit (B305) identifies AES in ECB mode as insecure. ECB does not provide adequate protection because identical plaintext blocks produce identical ciphertext blocks. | Replace ECB with authenticated encryption such as AES-GCM. Use a unique nonce for every encryption. |
| Weak RSA key size | Security — Medium | 83 | Bandit (B505) reports that the RSA private key uses only 1024 bits, which is considered weak. | Increase the RSA key size to at least 2048 bits. |
| Unsafe XML parsing | Security — Medium/Low | 5, 86 | Bandit (B408 and B318) warns that `xml.dom.minidom` can be vulnerable when parsing untrusted XML input. | Replace `minidom` with the equivalent parser from `defusedxml` and handle invalid XML safely. |
| Incorrect progressive tax calculation | Functional | 37–40 | The new tax regime calculation multiplies the entire taxable income by the rate returned by `slabRate()`. This is incorrect because each income slab must be taxed at its respective rate. | Calculate tax separately for each slab and add the amounts to obtain the total tax. |
| PAN validation accepts extra characters | Functional | 72 | The regular expression uses `re.match()`, which does not ensure that the entire input matches the PAN format. Extra trailing characters may be accepted. | Use `re.fullmatch()` to validate the complete PAN string. |
| Bare exception handler | Code Quality | 71–74 | Pylint (W0702) and Flake8 (E722) report the use of a bare `except:` statement. It can hide unexpected errors. | Catch only the expected exception instead of catching every exception. |
| Unused imports and variables | Code Quality | 2–4, 36 | Pylint and Flake8 report unused imports (`os`, `sys`, `json`) and unused variables (`bracket`, `checked`). | Remove unused imports and variables from the program. |
| Naming convention violations | Code Quality | Multiple | Pylint (C0103) reports that function and variable names use camelCase instead of Python's recommended snake_case convention. | Rename functions and variables using snake_case and update their references throughout the program. |
| Missing docstrings | Code Quality | Multiple | Pylint (C0114 and C0116) reports missing module and function documentation. | Add a module-level docstring and descriptive docstrings to functions. |
| Formatting and line-length violations | Code Quality | Multiple | Flake8 reports long lines, missing blank lines and multiple statements on one line. Pylint also reports formatting violations. | Follow PEP 8 guidelines by correcting indentation, adding blank lines, splitting long lines and separating statements. |
| Unused function parameters | Code Quality | 85, 91 | Pylint (W0613) reports that the `strict` parameter in `parseForm16()` and `debug` parameter in `runAsCgi()` are never used. | Remove unnecessary parameters or implement their intended functionality. |


