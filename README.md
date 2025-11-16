# 🧩 HENNGE Backend Challenge — Mission 1 & 3

This repository contains my solution for the **HENNGE Backend Challenge**. It includes:

- ✅ **Mission 1** — Core logic problem (`main.py`)
- 🚀 **Mission 3** — Automated submission with TOTP authentication (`main_submit.py`)

---

## 🎯 Mission 1: Core Logic Solution (`main.py`)

The file **`main.py`** implements the recursive solution for Mission 1.

### ✔️ Requirements Fulfilled

- **Input Handling**  
  Reads `N` test cases and then reads exactly `X` integers for each test case.

- **Calculation Logic**  
  Computes the sum of the **fourth power**:  
  \[
  \sum{Y_n^4}
  \]  
  but **ignores any positive `Y_n` values** (i.e., only non-positive values are considered).

- **Constraint Satisfaction**  
  Implements the logic **without loops or list comprehensions**.  
  Uses **recursion**, `map`, and `functools.reduce`.


  
---

## 🚀 Mission 3: Automated Submission (`main_submit.py`)

The file **`main_submit.py`** automates the authenticated submission of the Gist URL to the challenge API.

### 🛠️ Technical Details

- **Endpoint:**  
`https://api.challenge.hennge.com/challenges/backend-recursion/004`

- **Authentication:**  
Uses **HTTP Basic Auth** with:
- `USER_EMAIL`
- A **10-digit TOTP**

### 🔐 TOTP Generation

The script generates the TOTP based on:

| Parameter       | Value                |
|----------------|----------------------|
| Algorithm       | HMAC-SHA-512         |
| Time Step (X)   | 30 seconds           |
| Standard        | RFC 6238 & RFC 4226 |

The script ensures the TOTP is generated at runtime to avoid timing issues and ensure valid authentication.

---

## ⚙️ Setup and Execution

### 📦 Prerequisites

Make sure Python 3 is installed.

Install the required package:

```bash
pip install requests


- **Error Handling**  
  If the number of integers provided does **not match the expected count `X`**, the program prints:
