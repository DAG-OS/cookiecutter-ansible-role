import subprocess

# Create an initial commit using emojis from https://gitmoji.dev/
subprocess.run(["git", "init"])
subprocess.run(["git", "add", "LICENSE"])
subprocess.run(["git", "commit", "-m", "🎉 Initial commit"])

# Initialize Ansible role via Molecule.
ansible_role = "{{ cookiecutter.role_namespace }}.{{ cookiecutter.role_name }}"
subprocess.run(
    [
        "molecule",
        "init",
        "role",
        ansible_role,
        "--driver-name",
        "{{ cookiecutter.molecule_driver }}",
    ]
)
subprocess.run(
    [
        "rm",
        "-rf",
        f"{ansible_role}/README.md",
        f"{ansible_role}/molecule/default/molecule.yml",
        f"{ansible_role}/tests",
    ]
)
subprocess.run(f"cp -r {ansible_role}/* {ansible_role}/.[!.]* .", shell=True)
subprocess.run(["rm", "-rf", ansible_role])
subprocess.run(["rm", ".travis.yml"])

# Install pre-commit hooks
subprocess.run(["pre-commit", "install"])
