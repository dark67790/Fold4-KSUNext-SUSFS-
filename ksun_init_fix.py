#!/usr/bin/env python3
# Removes code that the ksun_susfs patch tries to delete but fails due to offset
# Run from kernel_platform/common/drivers/kernelsu/

import re

path = 'core/init.c'

with open(path, 'r') as f:
    s = f.read()

original = s

# Remove ksu_late_loaded declaration
s = s.replace('bool ksu_late_loaded;\n\n', '')
s = s.replace('bool ksu_late_loaded;\n', '')

# Remove x86_64 INDIRECT_SAFE block + ksu_late_loaded init
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
