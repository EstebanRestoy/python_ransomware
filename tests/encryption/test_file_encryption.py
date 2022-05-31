from os import listdir
from os.path import split, isfile, join

import pytest

from modules.cryptography.file_encryption import encrypt_file_name, encrypt_file_content


@pytest.mark.asyncio
async def test_encrypt_file_name(create_file, get_fernet):
    await encrypt_file_name(create_file, get_fernet)
    path_to_file, file_name = split(create_file)
    assert [join(f) for f in listdir(path_to_file) if isfile(join(path_to_file, f))] != ["test.txt"]


@pytest.mark.asyncio
async def test_encrypt_file_content(create_file, get_fernet):
    old_content = create_file.open().read()
    await encrypt_file_content(create_file, get_fernet)
    assert old_content != create_file.open().read()
