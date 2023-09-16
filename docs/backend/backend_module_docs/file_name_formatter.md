# File Name Formatter

This class provides functionality to format file names for finished songs based on a template.

## Contents

Public functions:

- [``format_file_name``](#format_file_name)
- [``replace_all``](#replace_all)

## Public functions

### format_file_name

Format a file name based on the given template and metadata. The template should contain at least one of the placeholders ``{{TITLE}}``, ``{{ARTIST}}``, ``{{ALBUM}}``, ``{{YEAR}}``, which will be replaced with the provided metadata.

#### format_file_name:Arguments

- ``template: str``: The template to replace metadata into.
- ``title: str``: The song title.
- ``artist: str``: The artist name.
- ``album: str``: The album name.
- ``year: str``: The song's release year.

#### format_file_name:Returns

``str`` containing the formatted text.

### replace_all

Replace all occurences of the given dict keys with the given dict values.

NOTE: Do not use this function if the order in which keys are replaced is relevant. For example, if you have a ``replacements`` dict like ``{"house": "home", "om": "em"}``, the resulting example for ``"house om"`` will not be ``"home em"`` but ``"heme em"``.

#### replace_all:Arguments

- ``text: str``: The haystack to find and replace in.
- ``replacements: dict``: The keys and values to replace, formatted as ``{"find": "replace"}``

#### replace_all:Returns

``str`` containing the text after replacing.
