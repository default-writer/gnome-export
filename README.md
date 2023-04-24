# gnome-export

python scripting for gnome export/import

## migrate_gnome_settings.py

This script makes it easier to copy Gnome settings and extensions from one pc to the other. It supports python>=3.5.

To use it, download it, then run python3 migrate_gnome_settings.py --export-settings to create a tar.gz file with all the settings.

Then, on your new system, copy the script and the gzip to your user's home directory and run python3 migrate_gnome_settings.py --import-settings.

For now, the script migrates:

    icons;
    themes;
    wallpapers;
    extensions;
    keybindings;
    most app settings.

Note: if you choose to export firefox settings, DO NOT share your configuration with anyone, since it WILL contain private data.
