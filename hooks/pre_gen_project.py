import shutil

#######################################
# Check required dependencies are installed.
class DependencyException(Exception):
    pass

def assert_installed(program):
    if shutil.which(program) is None:
        raise DependencyException(f"'{program}' is required but not found!")

assert_installed("molecule")
assert_installed("pre-commit")
