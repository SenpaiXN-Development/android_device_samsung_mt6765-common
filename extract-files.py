#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/mt6765-common',
    'hardware/mediatek',
    'hardware/mediatek/libmtkperf_client',
    'hardware/samsung',
    'vendor/samsung/mt6765-common',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_vendor' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libuuid',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    (
        'vendor/lib64/libkeymaster_helper.so',
        'vendor/lib64/libskeymaster4device.so',
    ): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
    (
        'vendor/lib/hw/vendor.mediatek.hardware.pq@2.11-impl.so',
        'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.11-impl.so',
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    (
        'vendor/bin/hw/camerahalserver',
    ): blob_fixup()
        .replace_needed('libbinder.so', 'libbinder-v32.so')
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so')
        .replace_needed('libutils.so', 'libutils-v32.so'),
    (
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek',
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b',
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib64/libcam.utils.sensorprovider.so',
    ): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'libsensorndkbridge-v31.so'),
    (
        'vendor/lib/lib_SoundAlive_3DPosition_ver202.so',
        'vendor/lib64/lib_SoundAlive_3DPosition_ver202.so',
    ): blob_fixup()
        .add_needed('libc++.so'),
    (
        'vendor/bin/wvkprov',
        'vendor/lib64/lib3a.flash.so',
        'vendor/lib64/libSQLiteModule_VER_ALL.so',
    ): blob_fixup()
        .add_needed('liblog.so'),
    (
        'vendor/lib64/libmnl.so',
    ): blob_fixup()
        .add_needed('libcutils.so'),
    (
        'vendor/lib/libnvram.so',
        'vendor/lib/libsysenv.so',
        'vendor/lib64/libnvram.so',
        'vendor/lib64/libsysenv.so',
    ) : blob_fixup()
        .add_needed('libbase_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'mt6765-common',
    'samsung',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
