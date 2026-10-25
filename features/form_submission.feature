Feature: Login and registration forms
  As a QA engineer
  I want to submit login and registration forms
  So that I can verify successful and invalid form submissions

  Background:
    Given I open the Forms section

  @smoke
  Scenario: Login succeeds with the published practice credentials
    When I fill the login form with:
      | field    | value      |
      | username | tester     |
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
      | field    | value      |
      | username | not-a-user |
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
