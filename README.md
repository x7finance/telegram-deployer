<p align="center">
  <img src="https://assets.x7finance.org/images/svgs/x7.svg" alt="X7 Banner Logo" />
</p>

<br />
<div align="center"><strong>X7 Finance</strong></div>
<div align="center">Trust No One. Trust Code. Long Live DeFi</div>
<div align="center">X7 is a completely decentralized exchange - complete with it's innovative lending protocols.</div>
<br />
<div align="center">
<a href="https://www.x7finance.org/">Website</a> 
<span> · </span>
<a href="https://t.me/X7m105portal">Telegram</a> 
<span> · </span>
<a href="https://twitter.com/X7_Finance">Twitter</a>
</div>

## About

This is a repo is maintained and deployed by the X7DAO.

Please feel free to contact the author of this repo directly with improvements

<br />

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The project requires Python 3.8 and above. You can check your Python version with the following command:

```bash
python --version
```

The project also requires several Python packages. You can install them with the following command:

```bash
pip install -r requirements.txt
```

### Installation

#### **For Contributors (Fork First)**
If you plan to contribute to the project, **fork the repository first** and then clone your fork:

```bash
git clone https://github.com/your-username/telegram-bot
```

#### **For Maintainers (Direct Clone)**
If you're an internal maintainer, you can **clone the repository directly**:

```bash
git clone https://github.com/x7finance/telegram-deployer
```

Next, navigate to the project folder:

```bash
cd your-project-name
```

Then, set up a Python virtual environment to manage your project's dependencies. First, create the virtual environment:

```bash
python -m venv myenv
```

Next, activate the virtual environment:

- For bash/zsh:

```bash
source myenv/bin/activate
```

- For fish:

```fish
source myenv/bin/activate.fish
```

- For Windows (PowerShell):
```powershell
myenv\Scripts\Activate
```

- For Windows (Command Prompt - cmd):
```cmd
myenv\Scripts\activate.bat
```

After activating the virtual environment, install the project's dependencies:

```bash
pip install -r requirements.txt
```

### Setting Up Environment Variables

Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

Fill in the required values in `.env`

### Running the Project

With the virtual environment activated and all dependencies installed, you can now run your project with:

```bash
python app/main.py
```