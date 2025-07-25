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
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libhidlbase_shim.so'),
    (
        'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so')
        .replace_needed('libutils.so', 'libutils-v32.so')
        .add_needed('libhidlbase_shim.so'),
    (
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek',
        'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek-64b',
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    (
        'vendor/bin/mnld',
        'vendor/lib64/libcam.utils.sensorprovider.so',
    ): blob_fixup()
        .replace_needed('libsensorndkbridge.so', 'libshim_sensors.so'),
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
    (
        'vendor/lib/libthha.so',
        'vendor/lib/libvcodec_oal.so',
        'vendor/lib/libmp4enc_sa.ca7.so',
        'vendor/lib/libvp8dec_sa.ca7.so',
        'vendor/lib/libvp9dec_sa.ca7.so',
        'vendor/lib/libh264enc_sa.ca7.so',
        'vendor/lib/libvc1dec_sa.ca7.so',
        'vendor/lib/libmp4enc_xa.ca7.so',
    ): blob_fixup()
       .clear_symbol_version('__aeabi_memclr')
       .clear_symbol_version('__aeabi_memclr4')
       .clear_symbol_version('__aeabi_memcpy')
       .clear_symbol_version('__aeabi_memcpy4')
       .clear_symbol_version('__aeabi_memmove')
       .clear_symbol_version('__aeabi_memset')
       .clear_symbol_version('__gnu_Unwind_Find_exidx'),
    (
        'vendor/lib/hw/vulkan.mt6765.so',
        'vendor/lib64/hw/vulkan.mt6765.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_acquire')
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_createFromHandle')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_getNativeHandle')
        .clear_symbol_version('AHardwareBuffer_release'),
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
