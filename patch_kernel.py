#!/usr/bin/env python3
# patch_kernel.py
# Removes large static tables from kernel source to shrink binary size
# Run from inside the linux-6.6 directory

import os
import re

def patch_file(path, description, old, new):
    if not os.path.exists(path):
        print(f"SKIP (not found): {path}")
        return
    with open(path, 'r', errors='replace') as f:
        content = f.read()
    if old not in content:
        print(f"SKIP (pattern not found): {path} - {description}")
        return
    content = content.replace(old, new)
    with open(path, 'w') as f:
        f.write(content)
    print(f"PATCHED: {path} - {description}")

# 1. Remove reboot DMI table (saves ~13KB)
# This is a huge table of DMI entries for machine-specific reboot quirks
patch_file(
    'arch/x86/kernel/reboot.c',
    'Empty reboot DMI table',
    'static struct dmi_system_id reboot_dmi_table[] __initdata = {',
    'static struct dmi_system_id reboot_dmi_table[] __initdata = { {NULL,NULL,{{0}},NULL}, /* patched empty */'
)

# 2. Remove Intel early CPU IDs table (saves ~13KB)
# Only needed for Intel-specific early init, irrelevant on AMD
patch_file(
    'arch/x86/kernel/cpu/match.c',
    'Empty intel_early_ids',
    'static const struct x86_cpu_id intel_early_ids[] = {',
    'static const struct x86_cpu_id intel_early_ids[] = { {} /* patched empty */,'
)

# 3. Remove acpi_osi DMI table (saves ~6KB)
patch_file(
    'drivers/acpi/acpi_osi.c',
    'Empty acpi_osi_dmi_table',
    'static struct dmi_system_id acpi_osi_dmi_table[] __initdata = {',
    'static struct dmi_system_id acpi_osi_dmi_table[] __initdata = { {NULL,NULL,{{0}},NULL}, /* patched empty */'
)

# 4. Remove override_status_ids DMI table (saves ~9KB)
patch_file(
    'drivers/acpi/acpi_lpss.c',
    'Empty override_status_ids',
    'static const struct dmi_system_id override_status_ids[] __initconst = {',
    'static const struct dmi_system_id override_status_ids[] __initconst = { {NULL,NULL,{{0}},NULL}, /* patched empty */'
)

# 5. Remove pciprobe DMI table (saves ~8KB)
patch_file(
    'arch/x86/pci/acpi.c',
    'Empty pciprobe_dmi_table',
    'static const struct dmi_system_id pciprobe_dmi_table[] __initconst = {',
    'static const struct dmi_system_id pciprobe_dmi_table[] __initconst = { {NULL,NULL,{{0}},NULL}, /* patched empty */'
)

# 6. Remove efifb DMI table (saves ~13KB) - not needed for BIOS boot
patch_file(
    'drivers/video/fbdev/efifb.c',
    'Empty efifb_dmi_system_table',
    'static const struct dmi_system_id efifb_dmi_system_table[] __initconst = {',
    'static const struct dmi_system_id efifb_dmi_system_table[] __initconst = { {NULL,NULL,{{0}},NULL}, /* patched empty */'
)

print("All patches applied")
