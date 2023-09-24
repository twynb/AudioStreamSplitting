import os
import pathlib
import platform
import re


def replace_dot_with_underscore(matchobj: re.Match):
    result = (
        "("
        + matchobj.group(1).replace(".", "_")
        # + ".md"
        + (matchobj.group(2) if matchobj.group(2) is not None else "")
        + ")"
    )
    return result


file = pathlib.Path(__file__)

if platform.system() == "Windows":
    os.system(
        f"sphinx-apidoc -d 2 -f -e -l -P -o .\\docs\\backend .\\src\\backend\\ /*/tests/*"
    )
    make = file.parent.joinpath("backend", "make.bat").resolve().as_posix()
else:
    os.system(
        f"sphinx-apidoc -d 2 -f -e -l -P -o ./docs/backend/ ./src/backend/ **/tests/*"
    )
    make = "make"
    os.chdir(file.parent.joinpath("backend").resolve().as_posix())

os.remove(file.parent.joinpath("backend", "modules.rst").resolve().as_posix())
os.system(f"{make} clean")
os.system(f"{make} html")
os.system(f"{make} markdown")

print(
    "Finished generating documentation, renaming and editing files so they work with vitepress..."
)

folder = file.parent.joinpath("backend", "_build", "markdown")
files = [f for f in os.listdir(folder) if f.endswith(".md")]

for file_name in files:
    file_path = os.path.join(str(folder), file_name)
    file_content = ""
    with open(file_path, mode="r", encoding="utf8") as file:
        file_content = file.read()
    os.remove(file_path)

    # no need for a regex here, we can just replace all "." and then fix the file ending
    result_file_name = file_name.replace(".", "_").replace("_md", ".md")
    result_file_path = os.path.join(str(folder), result_file_name)

    """
    match all module links. links in markdown files are formatted as
    [Display Text](module.submodule.file_name.md#section.to.access) - This will match the
    section in normal brackets, and the sub() call will replace all ``.`` in the file
    names with ``_``. The section after the # is not affected.
    The output for the above example would be ``(module_submodule_file_name.md#section.to.access)``.
    """
    content_pattern = re.compile(r"\(([A-Za-z\._]+)\.md(#[A-Za-z\.\-_]+)?\)")
    result_content = content_pattern.sub(replace_dot_with_underscore, file_content)

    with open(result_file_path, mode="w", encoding="utf8") as result_file:
        result_file.seek(0)
        result_file.write(result_content)

print("Finished renaming files!")
