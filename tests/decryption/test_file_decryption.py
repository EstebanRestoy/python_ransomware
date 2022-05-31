from os.path import split, exists

import pytest

from modules.cryptography.file_decryption import decrypt_file_name, decrypt_file_content
from modules.cryptography.file_encryption import encrypt_file_name, encrypt_file_content


@pytest.mark.asyncio
async def test_encrypt_file_name(create_file, get_fernet):
    path_to_file, file_name = split(create_file)
    encrypted_name = await encrypt_file_name(create_file, get_fernet)
    await decrypt_file_name(path_to_file + '/' + encrypted_name, get_fernet)
    assert exists(path_to_file + '/' + file_name)


@pytest.mark.asyncio
async def test_encrypt_file_content(create_file, get_fernet):
    old_content = create_file.open().read()
    await encrypt_file_content(create_file, get_fernet)
    await decrypt_file_content(create_file, get_fernet)
    assert old_content == create_file.open().read()
