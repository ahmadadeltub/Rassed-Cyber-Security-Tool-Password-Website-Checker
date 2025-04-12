# 🛡️ RASSED – Personal Cybersecurity Assistant

**Haseen** is a Python-based graphical application designed as part of Qatar’s *Cyber Eco* initiative by the National Cyber Security Agency. The project aims to raise cybersecurity awareness among individuals by providing simple tools to test and improve their online safety practices.

## 📌 Features

- **Password Strength Checker**

  - Checks for password length, digit, uppercase, lowercase, and special character.
  - Provides feedback to improve weak passwords.

- **Data Breach Checker**

  - Verifies if the entered password has been exposed in any known data breaches using the [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3).

- **Website Safety Checker**

  - Tests whether a website is reachable and returns its HTTP status.
  - Helps users identify potentially dangerous or fake links.

- **Password Visibility Toggle**

  - Allows users to show/hide their input for better UX.

- **Simple GUI Interface**

  - Built using Python's `tkinter` for ease of use, especially for students and non-technical users.

## 💡 Objectives

- Enhance digital safety awareness in schools and communities.
- Encourage users to adopt strong password habits.
- Provide a hands-on learning tool for understanding basic cybersecurity practices.

## 🛠️ Technologies Used

- Python 3
- Tkinter (GUI)
- Requests (HTTP requests)
- re (Regex for validation)
- hashlib (for SHA1 encryption)
- threading (for async API calls)
- PIL (for potential image support)

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.x installed. You can install the required libraries using:

```bash
pip install requests pillow
```
