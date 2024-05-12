import subprocess
import os


def get(cmd: str):
    return subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")


def set_custom_shortcut(name, command, shortcut):
    key = "org.gnome.settings-daemon.plugins.media-keys custom-keybindings"
    subkey1 = key.replace(" ", ".")[:-1]+":"
    item_s = f"/{key.replace(' ', '/').replace('.', '/')}/"
    firstname = "custom"

    array_str = get("gsettings get " + key)

    command_result = array_str.lstrip("@as")
    current = eval(command_result)

    n = 1
    while True:
        new = item_s+firstname+str(n)+"/"
        if new in current:
            n = n+1
        else:
            break

    current.append(new)
    cmd0 = f'gsettings set {key} "{str(current)}"'
    cmd1 = f'gsettings set {subkey1}{new} name "{name}"'
    cmd2 = f'gsettings set {subkey1}{new} command "{command}"'
    cmd3 = f'gsettings set {subkey1}{new} binding "{shortcut}"'

    for cmd in [cmd0, cmd1, cmd2, cmd3]:
        subprocess.call(["/bin/bash", "-c", cmd])


def install_extension(extension: str):
    os.system(f'busctl --user call org.gnome.Shell.Extensions /org/gnome/Shell/Extensions org.gnome.Shell.Extensions InstallRemoteExtension s {extension}')
