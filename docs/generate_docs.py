import subprocess
import platform
import pathlib

file = pathlib.Path(__file__)

if platform.system() == "Windows":
    subprocess.call(
        f"sphinx-apidoc -d 2 -f -e -P -o .\\docs\\backend .\\src\\backend\\ /*/tests/*"
    )

    make = file.parent.joinpath("backend", "make.bat")
    print(make)
    subprocess.call(f"{make.resolve().as_posix()} clean")
    subprocess.call(f"{make.resolve().as_posix()} html")
else:
    subprocess.call(
        f"sphinx-apidoc -d 2 -f -e -P -o docs/backend src/backend/ /*/tests/*"
    )
    subprocess.call("make clean")
    subprocess.call("make html")
