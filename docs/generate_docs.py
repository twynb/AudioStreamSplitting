import platform
import pathlib
import os

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

os.remove(file.parent.joinpath("backend", "modules.rst").resolve().as_posix())
os.system(f"{make} clean")
os.system(f"{make} html")
os.system(f"{make} markdown")
