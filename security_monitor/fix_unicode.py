#!/usr/bin/env python3
"""Fix Unicode characters in advanced_analyzer.py"""

import re

# Read the file
with open('advanced_analyzer.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace unicode characters with ASCII equivalents
replacements = {
    '✓': '[OK]',
    '✗': '[X]',
    '→': '->',
    '⚠️': '[!]',
    '🔐': '',
    '🔍': '[*]',
    '💾': '[*]',
    '📋': '[*]',
    '⚡': '[*]'
}

for old, new in replacements.items():
    content = content.replace(old, new)

# Write back
with open('advanced_analyzer.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✓ Fixed Unicode characters in advanced_analyzer.py')
