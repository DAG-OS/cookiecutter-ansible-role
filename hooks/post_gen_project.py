import subprocess
import io

#######################################
# Create an initial commit using emojis from https://gitmoji.dev/
subprocess.run(["git", "init"])
subprocess.run(["git", "add", "LICENSE"])
subprocess.run(["git", "commit", "-m", "🎉 Initial commit"])

#######################################
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
# Install pre-commit hooks
subprocess.run(["pre-commit", "install"])
