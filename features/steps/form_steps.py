"""Step definitions for the QA Practice Hub form scenarios."""

from behave import given, then, when


def _fields_from_table(table, expected_fields: set[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    for row in table:
        field = row["field"].strip()
        if field not in expected_fields:
            raise ValueError(f"Unsupported form field: {field!r}")
        if field in fields:
            raise ValueError(f"Form field was provided more than once: {field!r}")
        fields[field] = row["value"]

    missing_fields = expected_fields - fields.keys()
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Missing required table fields: {missing}")
    return fields


@given("I open the Forms section")
def open_forms_section(context) -> None:
    context.forms_page.open(context.settings.base_url)


@when("I fill the login form with:")
def fill_login_form(context) -> None:
    fields = _fields_from_table(context.table, {"username", "password"})
    context.forms_page.fill_login(fields["username"], fields["password"])


@when("I submit the login form")
def submit_login_form(context) -> None:
    context.forms_page.submit_login()


@then('the login message should contain "{expected_message}"')
def verify_login_message(context, expected_message: str) -> None:
    assert context.forms_page.login_message_contains(expected_message), (
        f"Login message did not contain {expected_message!r}"
    )


@then("the login form should be cleared")
def verify_login_form_cleared(context) -> None:
    assert context.forms_page.login_values() == ("", ""), (
        "Expected successful login to clear the username and password fields"
    )


@when("I fill the registration form with:")
def fill_registration_form(context) -> None:
    fields = _fields_from_table(
        context.table, {"first_name", "last_name", "email", "country"}
    )
    context.forms_page.fill_registration(
        first_name=fields["first_name"],
        last_name=fields["last_name"],
        email=fields["email"],
        country=fields["country"],
    )


@when("I submit the registration form")
def submit_registration_form(context) -> None:
    context.forms_page.submit_registration()


@when("I clear the registration form")
def clear_registration_form(context) -> None:
    context.forms_page.clear_registration()


@then('the registration message should contain "{expected_message}"')
def verify_registration_message(context, expected_message: str) -> None:
    assert context.forms_page.registration_message_contains(expected_message), (
        f"Registration message did not contain {expected_message!r}"
    )


@then("the registration form should be cleared")
def verify_registration_form_cleared(context) -> None:
    assert context.forms_page.registration_values() == ("", "", "", ""), (
        "Expected successful registration to clear all fields and reset the country"
    )


@then("the registration message should be hidden")
def verify_registration_message_hidden(context) -> None:
    assert not context.forms_page.registration_message_is_visible(), (
        "Expected the registration message to be hidden"
    )
