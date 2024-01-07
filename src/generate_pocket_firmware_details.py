#!/usr/bin/env python3
# Copyright (c) 2024 José Manuel Barroso Galindo <theypsilon@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You can download the latest version of this tool from:
# https://github.com/theypsilon/Update_All_MiSTer

import requests
from update_all.analogue_pocket.firmware_update import FirmwareInfo
from pathlib import Path
import json


def generate_pocket_firmware_details():
    details_url = 'https://www.analogue.co/support/pocket/firmware/latest/details'
    details = requests.get(details_url).json()
    print(f'Querying {details_url}...')
    print(json.dumps(details, indent=4))
    print()

    assert isinstance(details['download_url'], str) and len(details['download_url']) > 0, 'download_url is not a string'
    assert details['download_url'].startswith('https://') and details['download_url'].endswith('.bin'), 'download_url is not a valid URL'
    assert isinstance(details['version'], str) and len(details['version']) > 0, 'version is not a string'
    assert isinstance(details['file_size'], str) and len(details['file_size']) > 0, 'file_size is not a string'
    assert isinstance(details['md5'], str) and len(details['md5']) == 32, 'md5 is not a string or is not 32 chars long'

    firmware_info: FirmwareInfo = {
        'url': details['download_url'],
        'version': details['version'],
        'file': parse_file(details['download_url']),
        'md5': details['md5'].lower(),
        'size': parse_size(details['file_size'])
    }

    print('Generated firmware_info:')
    print(json.dumps(firmware_info, indent=4))
    print()

    with open(Path(__file__).parent / 'update_all/analogue_pocket/pocket_firmware_details.py', 'w+') as f:
        f.write(
            '# File auto-generated by src/generate_pocket_firmware_details.py\n'
            f'def pocket_firmware_details(): return {json.dumps(firmware_info, indent=4)}\n'
        )

    print('pocket_firmware_details.py generated successfully!')


def parse_size(size_str: str) -> float:
    assert size_str.endswith('MB'), 'size is not in MB'
    result = float(size_str[:-2])
    assert result > 0, 'size is not a positive number'
    assert result < 1000, 'size is too big'
    return result


def parse_file(url: str) -> str:
    return Path(url).name


if __name__ == '__main__':
    generate_pocket_firmware_details()
