"""This module provides functionality to format file names for finished songs
based on a template."""


def format_file_name(
    template: str, title: str = "", artist: str = "", album: str = "", year: str = ""
):
    """Format a file name with the given template and parameters.
    Templates may contain "{{TITLE}}", "{{ARTIST}}", "{{ALBUM}}" and "{{YEAR}}" as placeholders.
    At least one of the placeholder should be in the template to avoid overwriting files.
    The placeholders will be replaced with the provided metadata.
    :param template: The template to replace metadata into.
    :param title: The song title.
    :param artist: The artist.
    :param album: The album.
    :param year: The song's release year.
    """
    return replace_all(
        template,
        {
            "{{TITLE}}": title,
            "{{ARTIST}}": artist,
            "{{ALBUM}}": album,
            "{{YEAR}}": year,
        },
    )


def replace_all(text: str, replacements: dict):
    """Replace all occurences of the given dict keys with the given dict values.
    NOTE: Do not use this function if the order in which keys are replaced is relevant.
    For example, if you have a ``replacements`` dict like ``{"house": "home", "om": "em"}``,
    the resulting example for ``"house om"`` will not be ``"home em"`` but ``"heme em"``.
    :param text: The haystack to find and replace in.
    :param replacements: A dict of items to replace, formatted as {"find": "replace"}
    :returns: `str` containing the text after replacing.
    """
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return text
