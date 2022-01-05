import io
import os
import subprocess


def create_symbolic_link(to, link_file):
    """
    Create a symbolic link to a file relative to provided link_file.
    As of now this cannot be done natively with cookiecutter.
    See: https://github.com/cookiecutter/cookiecutter/pull/934
    """
    relative_path = os.path.relpath(to, link_file)
    # HACK: For some reason the relative path is off by one
    relative_path = relative_path[3:]
    os.symlink(relative_path, link_file)


def modify_with_sed(file, patterns):
    """
    Modify provided file with provided sed patterns.
    """
    sed = io.StringIO()
    sed.write("sed -i ")
    for pattern in patterns:
        sed.write(f"-e '{pattern}' ")
    sed.write(file)
    subprocess.run(sed.getvalue(), shell=True, check=True)


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
modify_with_sed(
    "meta/main.yml",
    patterns=[
        "s/author:.*/author: {{ cookiecutter.full_name }}/",
        "s/description:.*/description: {{ cookiecutter.role_description }}/",
        # Follow molecule min ansible version for now
        "s/min_ansible_version:.*/min_ansible_version: 2.8/",
        # Delete redundant lines between company and license
        "/company: /,/license: /{//!d}",
        "/company: /d",
        "s/license:.*/license: MIT/",
    ],
)
#######################################
# Modify CHANGELOG
initial_commit_id = subprocess.run(
    "git log --oneline --reverse | head -n 1 | awk '{ print $1 }'",
    shell=True,
    check=True,
    capture_output=True,
).stdout.strip().decode("utf-8")
modify_with_sed(
    "CHANGELOG.adoc",
    patterns=[f"s/#initial_commit_id#/{initial_commit_id}/g"],
)

#######################################
# Create symbolic links used in Antora documentation
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
create_symbolic_link("CHANGELOG.adoc", f"{pages_dir}/CHANGELOG.adoc")

#######################################
# Install pre-commit hooks
subprocess.run(["pre-commit", "install"])
