#!/usr/bin/env python3
# Run from kernel_platform/common/drivers/kernelsu/

import re

def fix(path, old, new, label):
    with open(path, 'r') as f:
        s = f.read()
    if old not in s:
        print(f"⚠️  {label}: context not found — already applied or source changed")
        return
    with open(path, 'w') as f:
        f.write(s.replace(old, new, 1))
    print(f"✅ {label}")

# Fix 1: core/init.c — remove ksu_late_loaded (rejected by 10_enable patch)
path = 'core/init.c'
with open(path, 'r') as f:
    s = f.read()
original = s
s = s.replace('bool ksu_late_loaded;\n\n', '')
s = s.replace('bool ksu_late_loaded;\n', '')
s = re.sub(
    r'#if defined\(__x86_64__\)\n.*?#endif\n\n#ifdef MODULE\n\tksu_late_loaded = \(current->pid != 1\);\n#else\n\tksu_late_loaded = false;\n#endif\n\n',
    '',
    s,
    flags=re.DOTALL
)
if s == original:
    print("⚠️  init.c: nothing to remove — already clean or source changed")
else:
    with open(path, 'w') as f:
        f.write(s)
    print("✅ core/init.c cleaned")

# Fix 2: supercall/supercall.c — ksys_close undeclared on kernel < 5.11
fix('supercall/supercall.c',
    '#include <linux/version.h>',
    '#include <linux/version.h>\n#include <linux/syscalls.h>',
    'supercall.c ksys_close header')

# Fix 3: selinux/selinux.c — define fake_state and ksu_selinux_hide_running
# These are referenced by security/selinux/hooks.c and selinuxfs.c
# but not defined anywhere in KernelSU-Next
fix('selinux/selinux.c',
    '#include "ksu.h"',
    '#include "ksu.h"\n#include "security.h"\n\nbool ksu_selinux_hide_running __read_mostly = false;\nstruct selinux_state fake_state;',
    'selinux/selinux.c fake_state + ksu_selinux_hide_running')

print("\n✅ All ksun fixes done")
