import re
import os
import sys

def empty_dmi_table(path, table_name):
    if not os.path.exists(path):
        print("NOT FOUND: " + path)
        return
    with open(path, 'r', errors='replace') as f:
        lines = f.readlines()
    start = None
    depth = 0
    end = None
    for i, line in enumerate(lines):
        if table_name in line and start is None:
            start = i
            print("Found " + table_name + " at line " + str(i+1) + " in " + path)
        if start is not None:
            depth += line.count('{') - line.count('}')
            if depth <= 0 and i > start:
                end = i
                break
    if start is None:
        print("NOT FOUND: " + table_name + " in " + path)
        return
    if end is None:
        print("NO END: " + table_name)
        return
    decl = lines[start]
    brace = decl.rfind('{')
    if brace != -1:
        new_line = decl[:brace] + '= { {0} };\n'
    else:
        new_line = decl.rstrip() + ' { {0} };\n'
    lines[start:end+1] = [new_line]
    with open(path, 'w') as f:
        f.writelines(lines)
    print("PATCHED: " + table_name + " in " + path)

os.chdir('linux-6.6')

empty_dmi_table('arch/x86/kernel/reboot.c',     'reboot_dmi_table')
empty_dmi_table('arch/x86/kernel/cpu/match.c',  'intel_early_ids')
empty_dmi_table('drivers/acpi/acpi_osi.c',      'acpi_osi_dmi_table')
empty_dmi_table('arch/x86/pci/acpi.c',          'pciprobe_dmi_table')
empty_dmi_table('drivers/video/fbdev/efifb.c',  'efifb_dmi_system_table')
empty_dmi_table('drivers/acpi/acpi_lpss.c',     'override_status_ids')

print("Done")
