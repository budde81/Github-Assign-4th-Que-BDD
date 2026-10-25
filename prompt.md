# Reusable Prompt: Build the QA Practice Hub BDD Forms Framework

Copy the prompt below into an AI coding assistant to generate or recreate this
BDD test automation project.

---

## Prompt

Act as a senior Python test-automation engineer. Build a complete, runnable
Behavior-Driven Development (BDD) automation framework for the Login and
Registration forms on:

**Target URL:** <https://qapracticehub.com/#forms>

Use **Python, Behave, Selenium WebDriver, Gherkin, and the Page Object Model
(POM)**. Respect the requested project structure exactly:

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

### Requirements

1. **Inspect before implementing.** Inspect the target page and existing
   workspace before choosing locators or making changes. Preserve existing
   files; do not overwrite unrelated work. If the workspace already has
   framework files, adapt them to the requested layout instead of making
   duplicate implementations.
2. **Keep responsibilities separated.**
   - Gherkin scenarios describe behavior, not Selenium implementation.
   - `features/steps/form_steps.py` maps reusable steps to page-object methods;
     it must not contain direct Selenium element interactions.
   - `pages/forms_page.py` owns locators and all browser interactions for the
     Forms page.
   - `features/environment.py` owns Behave hooks, WebDriver lifecycle, and
     failure diagnostics.
   - `utils/config.py` owns validated environment-based settings.
3. Use Selenium **explicit waits** for elements and messages. Disable implicit
   waits so the framework does not mix wait strategies. Avoid fixed sleeps.
4. Create a fresh WebDriver per scenario, close it reliably, and support Chrome,
   Firefox, and Edge. Run headless by default; allow headless mode to be
   configured.
5. Handle the cookie banner if it is displayed. Capture a timestamped
   screenshot under `reports/screenshots/` when a step fails. Log screenshot or
   browser teardown errors; do not silently swallow unexpected errors.
6. Make the settings configurable through `BASE_URL`, `BROWSER`, `HEADLESS`,
   `WAIT_TIMEOUT`, and `LOG_LEVEL`. Validate supported browsers, boolean
   spellings, positive integer timeout, absolute HTTP(S) URL, and log level.
   Invalid values must raise clear errors instead of silently falling back.
7. Generate an HTML report with Behave's `behave-html-formatter` plugin and
   write it into `reports/`. Document installation, configuration, running
   scenarios, tags, and report generation in `README.md`.
8. Use stable, inspected element IDs from the Forms page where available.
   The target practice login credentials are `tester` / `password123`.
   The practice site is client-side; do not claim registration persists.
9. Use table-driven, reusable Gherkin steps for entering login and registration
   values. Validate that each table contains exactly the supported fields:
   reject unknown fields, duplicates, and missing keys with explicit errors.
   Empty cell values must be supported for negative tests.
10. Keep scenario names readable and tag core happy paths `@smoke`; tag
    negative and auxiliary flows `@regression`.

### Gherkin coverage

Create scenarios covering:

- Successful login with the published practice credentials, success feedback,
  and cleared login inputs.
- Rejected login for an unknown username, incorrect password, both invalid
  values, and empty credentials.
- Successful registration with valid sample details, success feedback, and
  reset fields.
- Rejected registration when all required fields are empty and when each
  required field (first name, last name, email) is missing individually.
- Clearing a populated registration form and hiding its feedback message.

Prefer one reusable login-table step and one reusable registration-table step,
followed by explicit submit steps. For example:

```gherkin
When I fill the login form with:
  | field    | value      |
  | username | tester     |
  | password | password123 |
And I submit the login form
```

Use registration keys `first_name`, `last_name`, `email`, and `country`.
Represent a missing value with a blank table cell.

### Gherkin test cases (copy-ready)

Include these scenarios in `features/form_submission.feature`:

```gherkin
Feature: Login and registration forms
  As a QA engineer
  I want to submit login and registration forms
  So that I can verify successful and invalid form submissions

  Background:
    Given I open the Forms section

  @smoke
  Scenario: Login succeeds with the published practice credentials
    When I fill the login form with:
      | field    | value       |
      | username | tester      |
      | password | password123 |
    And I submit the login form
    Then the login message should contain "Login successful"
    And the login form should be cleared

  @regression
  Scenario: Login rejects invalid credentials
    When I fill the login form with:
      | field    | value      |
      | username | not-a-user |
      | password | incorrect  |
    And I submit the login form
    Then the login message should contain "Invalid credentials"

  @regression
  Scenario: Login rejects an unknown username with the valid password
    When I fill the login form with:
      | field    | value       |
      | username | not-a-user  |
      | password | password123 |
    And I submit the login form
    Then the login message should contain "Invalid credentials"

  @regression
  Scenario: Login rejects the valid username with an incorrect password
    When I fill the login form with:
      | field    | value     |
      | username | tester    |
      | password | incorrect |
    And I submit the login form
    Then the login message should contain "Invalid credentials"

  @regression
  Scenario: Login rejects empty credentials
    When I fill the login form with:
      | field    | value |
      | username |       |
      | password |       |
    And I submit the login form
    Then the login message should contain "Invalid credentials"

  @smoke
  Scenario: Registration succeeds with valid details
    When I fill the registration form with:
      | field      | value                     |
      | first_name | Taylor                    |
      | last_name  | Tester                    |
      | email      | taylor.tester@example.com |
      | country    | us                        |
    And I submit the registration form
    Then the registration message should contain "Registration successful for Taylor Tester"
    And the registration form should be cleared

  @regression
  Scenario: Registration rejects missing required details
    When I fill the registration form with:
      | field      | value |
      | first_name |       |
      | last_name  |       |
      | email      |       |
      | country    |       |
    And I submit the registration form
    Then the registration message should contain "Please fill in all required fields"

  @regression
  Scenario: Registration rejects a missing first name
    When I fill the registration form with:
      | field      | value                     |
      | first_name |                           |
      | last_name  | Tester                    |
      | email      | taylor.tester@example.com |
      | country    | us                        |
    And I submit the registration form
    Then the registration message should contain "Please fill in all required fields"

  @regression
  Scenario: Registration rejects a missing last name
    When I fill the registration form with:
      | field      | value                     |
      | first_name | Taylor                    |
      | last_name  |                           |
      | email      | taylor.tester@example.com |
      | country    | us                        |
    And I submit the registration form
    Then the registration message should contain "Please fill in all required fields"

  @regression
  Scenario: Registration rejects a missing email address
    When I fill the registration form with:
      | field      | value                     |
      | first_name | Taylor                    |
      | last_name  | Tester                    |
      | email      |                           |
      | country    | us                        |
    And I submit the registration form
    Then the registration message should contain "Please fill in all required fields"

  @regression
  Scenario: Registration form can be cleared
    When I fill the registration form with:
      | field      | value                     |
      | first_name | Taylor                    |
      | last_name  | Tester                    |
      | email      | taylor.tester@example.com |
      | country    | us                        |
    And I clear the registration form
    Then the registration form should be cleared
    And the registration message should be hidden
```

### Completion and verification

- Provide complete contents for every file in the requested structure.
- Ensure Behave discovers all scenarios without undefined steps.
- Run Python syntax validation and Behave dry-run/discovery.
- When browser and network access are available, run the complete browser
  suite and generate the HTML report. Clearly state if a browser test cannot be
  executed.
- Summarize the created files, test coverage, run commands, and verification
  results. Do not report tests as passing unless they were actually run.
