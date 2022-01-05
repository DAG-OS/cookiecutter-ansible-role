import io
import os
import subprocess

#######################################
# Create an initial commit using emojis from https://gitmoji.dev/
subprocess.run(["git", "init"])
subprocess.run(["git", "add", "LICENSE"])
subprocess.run(["git", "commit", "-m", "🎉 Initial commit"])

#######################################
# Initialize Ansible role via Molecule.
subprocess.run(
    [
        "molecule",
        "init",
        "role",
        "{{ cookiecutter.role }}",
        "--driver-name",
        "{{ cookiecutter.molecule_driver }}",
    ]
)
subprocess.run(
    [
        "rm",
        "-rf",
        "{{ cookiecutter.role }}/README.md",
        "{{ cookiecutter.role }}/molecule/default/molecule.yml",
        "{{ cookiecutter.role }}/tests",
    ]
)
subprocess.run(
    "cp -r {{ cookiecutter.role }}/* {{ cookiecutter.role }}/.[!.]* .", shell=True
)
subprocess.run(["rm", "-rf", "{{ cookiecutter.role }}"])
subprocess.run(["rm", ".travis.yml"])

#######################################
# Modify Ansible role meta information
sed = io.StringIO()
sed.write("sed -i ")
sed.write("-e 's/author:.*/author: {{ cookiecutter.full_name }}/' ")
sed.write("-e 's/description:.*/description: {{ cookiecutter.role_description }}/' ")
# Follow molecule min ansible version for now
sed.write("-e 's/min_ansible_version:.*/min_ansible_version: 2.8/' ")
# Delete redundant lines between company and license
sed.write("-e '/company: /,/license: /{//!d}' ")
sed.write("-e '/company: /d' ")
sed.write("-e 's/license:.*/license: MIT/' ")
sed.write("meta/main.yml")
subprocess.run(sed.getvalue(), shell=True, check=True)

#######################################
# Create symbolic links used in Antora documentation
#
# As of now this cannot be done natively with cookiecutter.
# See: https://github.com/cookiecutter/cookiecutter/pull/934
def create_symbolic_link(to, link_file):
    relative_path = os.path.relpath(to, link_file)
    # HACK: For some reason the relative path is off by one
    relative_path = relative_path[3:]
    os.symlink(relative_path, link_file)


module_dir = "docs/antora/modules/ROOT"
example_dir = f"{module_dir}/examples"
pages_dir = f"{module_dir}/pages"
create_symbolic_link(
    "molecule/default/converge.yml",
    f"{example_dir}/converge.yml",
)
create_symbolic_link(
    "defaults/main.yml",
    f"{example_dir}/defaults-main.yml",
)
create_symbolic_link(
    "CHANGELOG.adoc",
    f"{pages_dir}/CHANGELOG.adoc"
)

#######################################
# Install pre-commit hooks
subprocess.run(["pre-commit", "install"])
