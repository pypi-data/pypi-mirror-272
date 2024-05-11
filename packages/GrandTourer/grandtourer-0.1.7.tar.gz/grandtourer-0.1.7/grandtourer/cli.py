"""A CLI tool for easily launching GUI applications on MacOS with a two letter command: `gt`"""

# Standard library imports
import os
import subprocess
from collections import Counter

# Third party imports
import click


def get_applications_dict() -> dict[str, str]:
    """Retrieves a dictionary mapping lowercase application names to their full names by searching the default folders on MacOS.

    Returns:
        A dictionary in which keys are lowercase, with spaces and `.app` removed. This enables easy string matching with user input back in main. Values have `.app` removed. This is so that the `open_application` function can use `open -a` on them. Applications with common prefixes (e.g., "Microsoft", "Adobe") are also included with these prefixes removed.
    """
    applications_list = set()
    folders = [
        "/Applications",
        "/System/Applications",
        "/System/Applications/Utilities",
    ]
    for folder in folders:
        applications_list.update(os.listdir(folder))

    # Builds a set of common prefix words, converted to lowercase
    first_words = Counter(app.split()[0] for app in applications_list)
    common_first_words = {
        item.lower() for item, count in first_words.items() if count > 1
    }

    # Lowercase and spaces-removed keys mean easier string-matching back in the caller. Values need `.app` removed to work with `open -a`
    applications_dict = {}
    for application in applications_list:
        key = application.replace(" ", "").replace(".app", "").lower()
        value = application.replace(".app", "")
        applications_dict[key] = value

    # Also adds items with de-common-prefixed keys to applications_dict, so `Microsoft Word` can be accessed by just `word`
    to_add = {}
    for key, value in applications_dict.items():
        for word in common_first_words:
            if key.startswith(word):
                stripped_key = key[len(word) :].lstrip()
                to_add[stripped_key] = value
                break
    applications_dict.update(to_add)

    return applications_dict


def open_application(application_name: str) -> None:
    """Open a macOS application by its name using the `open -a` command.

    Args:
        application_name: The name of the application to open, in a format suitable for "open -a".

    Raises:
        Subprocess error, if the application fails to open.
    """
    try:
        subprocess.run(["open", "-a", application_name], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(f"Error opening application: {application_name}")
        click.echo(e)


@click.command(options_metavar="")
@click.argument("application", metavar="APPLICATION...", nargs=-1)
def app(application):
    """Launches your APPLICATION.

    You only need to enter the first few letters.
    Don't worry about capitals or spaces.
    You can also miss out common first words like "Microsoft" or "Adobe".
    String matching will find your application.
    """

    target_application = "".join(application).lower()
    possible_applications = get_applications_dict()

    # Finds all normalised keys in the applications_dict which start with the user's target string
    results = {
        key: value
        for key, value in possible_applications.items()
        if key.startswith(target_application)
    }

    if len(results) == 0:
        click.echo("No applications found with that name :(")
    elif len(results) == 1:
        value = next(iter(results.values()))
        open_application(value)
    else:
        click.echo("Did you mean one of the following?")
        options = list(results.values())
        for i, value in enumerate(options, start=1):
            click.echo(f"{i}. {value}")


        selected_option = click.prompt(
            "Enter the number you want. Enter anything else to exit"
        )

        try:
            selected_option = int(selected_option)
            if 1 <= selected_option <= len(options):
                open_application(options[selected_option - 1])
        except:
            pass

if __name__ == "__main__":
    app()
