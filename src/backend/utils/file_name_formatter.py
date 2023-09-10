def format_file_name(
    template: str, title: str = "", artist: str = "", album: str = "", year: str = ""
):
    """Format a file name with the given template and parameters.
    Templates may contain "{{TITLE}}", "{{ARTIST}}", "{{ALBUM}}" and "{{YEAR}}" as placeholders.
    :param template: The name template.
    :param title: The song title.
    :param artist: The artist.
    :param album: The album.
    :param year: The year.
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
    """Replace several items in a text at once.
    :param text: The haystack.
    :param replacements: A dict of items to replace, formatted as {"search": "replace"}
    :returns: The text with replacements applied.
    """
    for search, replace in replacements.items():
        text = text.replace(search, replace)
    return text
