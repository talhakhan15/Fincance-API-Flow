# Fincance API Automation Script

This repository contains a Python automation script that simulates a complete **Islamic Finance application flow** through API calls using mock Nafath user data.
---

## 📁 Structure

- `nafath_loan_flow.py`  
  Contains the full Nafath-to-loan-application simulation, broken into steps.
  
---

## 🚀 Features

- 🔐 Registers a mock user via `nafath` data
- 🧾 Submits required loan steps like:
  - Register user
  - Update Nafath
  - Accept Terms
  - Finance submission
  - Verification with salary info
  - Simmah Consent
  - Risk Counter input
  - Contract OTP extraction
  - OTP Verification
  - IVR Callback Simulation

---

## 🛠 Requirements

Install dependencies with:

```bash
pip install requests
