import pathlib

PACKAGE_ROOT = pathlib.Path(__file__).parent.parent.absolute()
DATA_DIR = PACKAGE_ROOT.joinpath("./data")
OUTPUT_DIR = PACKAGE_ROOT.joinpath("./output")
