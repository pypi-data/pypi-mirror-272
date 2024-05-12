import os
from powerline.theme import requires_segment_info
import subprocess

g_env_pyenv_keys = ["PYENV_VERSION", "PYENV_DIR"]
g_env_virtualenv_key = "VIRTUAL_ENV"

# Remove ENV vars injected to powershell by pyenv
for key in g_env_pyenv_keys:
    os.unsetenv(key)

@requires_segment_info
def pyenv(pl, segment_info):
    
    global g_env_pyenv_keys, g_env_virtualenv_key
    env = segment_info["environ"]
    # Check for shell spawned by virtualenv(maybe used by pipenv) first
    if g_env_virtualenv_key in env:
        py_version = "{}(venv)".format(
            os.path.basename(env[g_env_virtualenv_key]))
    else:
        for key in g_env_pyenv_keys:
            if key in env:
                os.putenv(key, env[key])
        cwd = segment_info["getcwd"]()
        pyenv_version = subprocess.check_output(
            ["pyenv", "version-name"], cwd=cwd).decode('utf-8').strip()
        py_version = "{}(pyenv)".format(pyenv_version)

    return [{
        "name": "pyenv_version",
        "type": "string",
        "contents": " {}".format(py_version),
        "highlight_groups": ["pyenv:version"],
    }]


@requires_segment_info
def jenv(pl, segment_info):
    cwd = segment_info["getcwd"]()
    jenv_version = subprocess.check_output(
        ["jenv", "version-name"], cwd=cwd).decode('utf-8').strip()
    java_version = "{}".format(jenv_version)

    return [{
        "name": "jenv_version",
        "type": "string",
        "contents": " {}".format(java_version),
        "highlight_groups": ["jenv:version"],
    }]


@requires_segment_info
def docker_ctx(pl, segment_info):
    cwd = segment_info["getcwd"]()
    get_docker_ctx = subprocess.check_output(
        ["docker", "context", "show"], cwd=cwd).decode('utf-8').strip()
    docker_ctx = "{}".format(get_docker_ctx)

    return [{
        "name": "docker_ctx",
        "type": "string",
        "contents": "  {}".format(docker_ctx),
        "highlight_groups": ["docker_ctx"],
    }]
