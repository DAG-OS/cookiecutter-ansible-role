# Ansible role: {{ cookiecutter.role }}

[![CI](https://github.com/DAG-OS/ansible-role-{{ cookiecutter.role_name }}/actions/workflows/ci.yml/badge.svg?branch=trunk)](https://github.com/DAG-OS/ansible-role-{{ cookiecutter.role_name }}/actions/workflows/ci.yml)
[![Release](https://github.com/DAG-OS/ansible-role-{{ cookiecutter.role_name }}/actions/workflows/release.yml/badge.svg)](https://github.com/DAG-OS/ansible-role-{{ cookiecutter.role_name }}/actions/workflows/release.yml)
<!--
TODO: Add ansible role ID to badges once it is released
Use following command:
    ansible-galaxy info {{ cookiecutter.role }} | grep -E 'id: [0-9]' | awk {'print $2'}
[![Quality](https://img.shields.io/ansible/quality/<ansible-role-id>?logo=ansible)](https://galaxy.ansible.com/dagos/{{ cookiecutter.role_name }})
[![Downloads](https://img.shields.io/ansible/role/d/<ansible-role-id>?logo=ansible)](https://galaxy.ansible.com/dagos/{{ cookiecutter.role_name }})
-->

{{ cookiecutter.role_description }}

Find the documentation at: <https://dag-os.github.io/pages/{{ cookiecutter.role }}/trunk>
