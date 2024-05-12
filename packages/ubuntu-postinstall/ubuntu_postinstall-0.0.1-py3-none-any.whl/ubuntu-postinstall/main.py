from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow
from models.action import Action
from models.command_function import CommandFunction
from models.command_line import CommandLine
from models.system_action import SystemAction

import os
import sys
from utils.gnome_utils import set_custom_shortcut

location = os.path.dirname(os.path.realpath(__file__))

actions = {
    'installBrave': SystemAction('Installing Brave...', [
        CommandLine('apt install curl -y'),
        CommandLine("curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg " +
                    'https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg'),
        CommandLine('echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] ' +
                    'https://brave-browser-apt-release.s3.brave.com/ stable main" ' +
                    '| tee /etc/apt/sources.list.d/brave-browser-release.list'),
        CommandLine('apt update'),
        CommandLine('apt install brave-browser -y')
    ]),
    'installChrome': SystemAction('Installing Google Chrome...', [
        CommandLine('apt install wget -y'),
        CommandLine('wget "https://dl.google.com/linux/direct/' +
                    'google-chrome-stable_current_amd64.deb"'),
        CommandLine('dpkg -i google-chrome-stable_current_amd64.deb'),
        CommandLine('rm google-chrome-stable_current_amd64.deb')
    ]),
    'installVsCode': SystemAction('Installing Visual Studio Code...', [
        CommandLine('apt install wget gpg -y'),
        CommandLine('wget -qO- https://packages.microsoft.com/keys/microsoft.asc |' +
                    'gpg --dearmor > packages.microsoft.gpg'),
        CommandLine('install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg'),
        CommandLine('sudo sh -c "echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list"'),
        CommandLine('rm -f packages.microsoft.gpg'),
        CommandLine('apt install apt-transport-https -y'),
        CommandLine('apt update'),
        CommandLine('apt install code -y')
    ]),
    'installAudacity': SystemAction('Installing Audacity...', [
        CommandLine('apt install audacity -y')
    ]),
    'installDiscord': SystemAction('Installing Discord...', [
        CommandLine('wget "https://discord.com/api/download?platform=linux&format=deb" -O discord.deb'),
        CommandLine('dpkg -i discord.deb'),
        CommandLine('rm discord.deb')
    ]),
    'installVlc': SystemAction('Installing VLC Media Player...', [
        CommandLine('apt install vlc -y')
    ]),
    'installSteam': SystemAction('Installing Steam...', [
        CommandLine('wget "https://cdn.akamai.steamstatic.com/client/installer/steam.deb" -O steam.deb'),
        CommandLine('dpkg -i steam.deb'),
        CommandLine('rm steam.deb')
    ]),
    'installGnomeConsole': SystemAction('Installing GNOME Console...', [
        CommandLine('apt remove gnome-terminal -y'),
        CommandLine('apt install gnome-console -y')
    ]),
    'installGnomeTweaks': SystemAction('Installing GNOME Tweaks...', [
        CommandLine('apt install gnome-tweaks -y')
    ]),
    'installDconfEditor': SystemAction('Installing dconf Editor...', [
        CommandLine("apt install dconf-editor -y")
    ]),
    'installVirtualBox': SystemAction('Installing VirtualBox...', [
        CommandLine('apt install virtualbox-qt virtualbox-guest-utils virtualbox-guest-additions-iso -y'),
        CommandLine('usermod -aG vboxusers $USER')
    ]),
    'installExtensionManager': SystemAction('Installing Extension Manager...', [
        CommandLine('apt install gnome-shell-extension-manager -y')
    ]),
    'setupDock': Action('Setting up Dock...', [
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock click-action "cycle-windows"'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock customize-alphas true'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock custom-theme-customize-running-dots true'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock dock-fixed false'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock dock-position "BOTTOM"'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock extend-height false'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock hotkeys-overlay false'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock isolate-monitors true'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock isolate-workspaces true'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock max-alpha 0.75'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock min-alpha 0.25'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock multi-monitor true'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock show-mounts false'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock show-mounts-network false'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock show-trash false'),
        CommandLine('gsettings set org.gnome.shell.extensions.dash-to-dock transparency-mode "DYNAMIC"')
    ]),
    'setupOverview': Action('Setting up Overview improvements...', [
        CommandLine('gsettings --schemadir "$HOME/.local/share/gnome-shell/extensions/gnome-ui-tune@itstime.tech/schemas" set org.gnome.shell.extensions.gnome-ui-tune hide-search false')
    ]),
    'setupSmallTweaks': Action('Setting up small tweaks...', [
        CommandLine('gsettings --schemadir "$HOME/.local/share/gnome-shell/extensions/' +
                    'just-perfection-desktop@just-perfection/schemas"' +
                    'set org.gnome.shell.extensions.just-perfection osd-position 2'),
        CommandLine('gsettings --schemadir "$HOME/.local/share/gnome-shell/extensions/' +
                    'just-perfection-desktop@just-perfection/schemas"' +
                    'set org.gnome.shell.extensions.just-perfection switcher-popup-delay false'),
        CommandLine('gsettings --schemadir "$HOME/.local/share/gnome-shell/extensions/' +
                    'just-perfection-desktop@just-perfection/schemas"' +
                    'set org.gnome.shell.extensions.just-perfection window-demands-attention-focus true'),
        CommandLine('gsettings --schemadir "$HOME/.local/share/gnome-shell/extensions/' +
                    'just-perfection-desktop@just-perfection/schemas"' +
                    'set org.gnome.shell.extensions.just-perfection workspace-popup false')
    ]),
    'dynamicTouchpad': Action('Disabling touchpad when mouse is connected...', [
        CommandLine('gsettings set org.gnome.desktop.peripherals.touchpad send-events "disabled-on-external-mouse"')
    ]),
    'detachModals': Action('Disabling modal dialog attachment...', [
        CommandLine('gsettings set org.gnome.mutter attach-modal-dialogs false')
    ]),
    'flatMouseProfile': Action('Setting mouse profile to flat...', [
       CommandLine('gsettings set org.gnome.desktop.peripherals.mouse accel-profile "flat"')
    ]),
    'shortcutNautilus': Action('Setting shortcut for Nautilus...', [
        CommandFunction(set_custom_shortcut, 'New Nautilus Window', 'nautilus -w', '<Super>e')
    ]),
    "shortcutSysMon": Action('Setting shortcut for System Monitor...', [
        CommandFunction(set_custom_shortcut, 'Open System Monitor', 'gnome-system-monitor', '<Primary><Shift>Escape')
    ]),
    'shortcutMinimize': Action('Setting shortcut for Minimize...', [
        CommandLine('gsettings set org.gnome.desktop.wm.keybindings minimize ["<Super>d"]')
    ]),
    'shortcutWorkspaceSwitch': Action('Setting shortcut for workspace switching...', [
        CommandLine('gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-left ["<Control><Super>Left"]'),
        CommandLine('gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-right ["<Control><Super>Right"]')
    ]),
}


def main():
    app = QApplication(sys.argv)

    window = MainWindow(actions)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
