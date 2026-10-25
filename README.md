# BDD Forms Assignment

Behavior-Driven Development test automation for the Login and Registration
forms at [QA Practice Hub](https://qapracticehub.com/#forms). The project uses
Python, Behave, Selenium WebDriver, Page Objects, and explicit waits.

## Project structure

```text
bdd_forms_assignment/
├── features/
│   ├── form_submission.feature
│   ├── steps/
│   │   └── form_steps.py
│   └── environment.py
├── pages/
│   └── forms_page.py
├── utils/
│   └── config.py
├── reports/
├── requirements.txt
└── README.md
```

## Requirements and setup

- Python 3.10 or later
- Chrome, Firefox, or Microsoft Edge
- Internet access to the target website

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Selenium Manager locates the matching driver for the installed browser.

## Run the tests and report

Run the scenarios:

```powershell
python -m behave
```

Generate an HTML report in `reports/`:

```powershell
python -m behave -f behave_html_formatter:HTMLFormatter -o reports/behave-report.html
```

Run selected scenarios using their tags:

```powershell
python -m behave --tags=@smoke
python -m behave --tags=@regression
```

Failed steps capture a screenshot under `reports/screenshots/`.

## Configuration

Configuration is provided through environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `BASE_URL` | `https://qapracticehub.com/#forms` | Absolute HTTP(S) target URL |
| `BROWSER` | `chrome` | `chrome`, `firefox`, or `edge` |
| `HEADLESS` | `true` | Headless mode (`true`/`false`, `1`/`0`, `yes`/`no`, `on`/`off`) |
| `WAIT_TIMEOUT` | `10` | Positive explicit-wait timeout in seconds |
| `LOG_LEVEL` | `INFO` | Python logging level |

For example, use a visible Chrome browser in PowerShell:

```powershell
$env:HEADLESS = "false"
$env:BROWSER = "chrome"
python -m behave
```

Invalid configuration values fail with an explanatory error.

## Scenarios

The feature covers successful login with the practice credentials, invalid and
empty login attempts, successful registration, missing required registration
details, and clearing the registration form. The target is a client-side
practice application; these scenarios verify UI behavior and do not create
persistent accounts.

## Reusable form steps

Use the same table-driven steps with different values instead of adding
scenario-specific step definitions:

```gherkin
When I fill the login form with:
  | field    | value      |
  | username | tester     |
  | password | password123 |
And I submit the login form
```

Registration uses the same pattern with `first_name`, `last_name`, `email`,
and `country` fields. Use an empty value to cover missing-field cases. Unknown,
duplicate, or omitted field names are reported as step errors.
