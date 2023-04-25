#! /usr/bin/env python
import argparse
import getpass
import os
import subprocess
import tarfile

REL_GNOME_EXTENSIONS_DIR = '/.local/share/gnome-shell/extensions/'
REL_GNOME_BGS_DIR = '/.local/share/backgrounds/'
REL_GNOME_ICONS_DIR = '/.icons/'
REL_GNOME_THEMES_DIR = '/.themes/'
REL_FIREFOX_SETTINGS_DIR = '/.mozilla/'

GNOME_EXTENSIONS_DIR = os.path.expanduser('~') + REL_GNOME_EXTENSIONS_DIR
GNOME_BGS_DIR = os.path.expanduser('~') + REL_GNOME_BGS_DIR
GNOME_ICONS_DIR = os.path.expanduser('~') + REL_GNOME_ICONS_DIR
GNOME_THEMES_DIR = os.path.expanduser('~') + REL_GNOME_THEMES_DIR

DCONF_SETTINGS_FILENAME = os.path.join(os.path.expanduser('~'), 'dconf-extensions-settings.dump')
TAR_FILENAME = os.path.join(os.getcwd(), 'gnome_settings.tar.gz')


def export_settings():
    print('>>>> Starting to export settings...')
    dconf_settings = subprocess.run(['dconf', 'dump', '/'], capture_output=True, check=False).stdout
    clean_dconf_settings = dconf_settings.replace(getpass.getuser().encode('utf8'), b'%%USER%%')
    dconf_settings_dump = open(DCONF_SETTINGS_FILENAME, 'wb')
    dconf_settings_dump.write(clean_dconf_settings)

    with tarfile.open(TAR_FILENAME, "w:gz") as tar:
        if os.path.exists(GNOME_ICONS_DIR):
            print('>>>> Exporting icons...')
            tar.add(GNOME_ICONS_DIR, arcname=REL_GNOME_ICONS_DIR)

        if os.path.exists(GNOME_THEMES_DIR):
            print('>>>> Exporting themes...')
            tar.add(GNOME_THEMES_DIR, arcname=REL_GNOME_THEMES_DIR)

        if os.path.exists(GNOME_EXTENSIONS_DIR):
            print('>>>> Exporting extensions...')
            tar.add(GNOME_EXTENSIONS_DIR, arcname=REL_GNOME_EXTENSIONS_DIR)

        if os.path.exists(GNOME_BGS_DIR):
            print('>>>> Exporting wallpapers...')
            tar.add(GNOME_BGS_DIR, arcname=REL_GNOME_BGS_DIR)


        print('>>>> Exporting dconf extension settings...')
        tar.add(DCONF_SETTINGS_FILENAME, arcname='dconf-extensions-settings.dump')

    subprocess.run(['rm', DCONF_SETTINGS_FILENAME], check=False)
    print(f'>>>> Done! Check the tar created at {TAR_FILENAME}!')

def import_settings():
    print('>>>> Starting to import settings...')

    if os.path.exists(TAR_FILENAME):
        print('>>>> Unpacking static files...')
        subprocess.run(['tar', '-xzf', TAR_FILENAME, '-C', os.path.expanduser('~')], check=True)

        print('>>>> Importing dconf extension settings...')
        dconf_settings = open(DCONF_SETTINGS_FILENAME, 'rb').read()
        subprocess.run(
            ['dconf', 'load', '-f', '/'],
            input=dconf_settings.replace(b'%%USER%%', getpass.getuser().encode('utf8')),
            check=False
        )

        subprocess.run(['rm', DCONF_SETTINGS_FILENAME], check=False)
        print('>>>> Done! You may need to restart your Gnome session for settings to load (logout and login).')
    else:
        print('>>>> Please copy file to destination location first: %s\n' % TAR_FILENAME)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This is a simple script to export and \
            import all settings and extensions from and for a Gnome user.'
    )
    parser.add_argument(
        '--export-settings',
        action="store_true",
        help="Exports a tar file with all settings and extensions."
    )
    parser.add_argument(
        '--import-settings',
        action="store_true",
        help='''Imports all settings and extensions from a previously exported tar file.
        This file should be located at your user\'s home directory.'''
    )

    args = parser.parse_args()
 
    if args.export_settings:
        export_settings()
    if args.import_settings:
        import_settings()
