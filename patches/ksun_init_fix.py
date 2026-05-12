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

# Fix 1: core/init.c - remove ksu_late_loaded (rejected by ksun_susfs patch)
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
    print("⚠️  ksun_init_fix: nothing to remove — already clean or source changed")
else:
    with open(path, 'w') as f:
        f.write(s)
    print("✅ ksun_init_fix: core/init.c cleaned")

# Fix 2: supercall/supercall.c - ksys_close undeclared on kernel < 5.11
fix(
    'supercall/supercall.c',
    '#include <linux/version.h>',
    '#include <linux/version.h>\n#include <linux/syscalls.h>',
    'supercall.c ksys_close header'
)
