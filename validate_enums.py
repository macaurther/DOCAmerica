#!/usr/bin/env python3
"""
validate_enums.py
Checks that CvEnums.h and the mod's XML definition files agree on the order
and count of every entity type tracked by the mod, and flags mismatches
against Python Consts.py counts.

Usage:
    python validate_enums.py [mod_root_directory]

If mod_root_directory is omitted the directory containing this script is used.

Exit code: 0 if no ORDER mismatches found, 1 otherwise.
Count-only differences (e.g. Python tracking a subset) are printed as warnings,
not errors.
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# Color output — disabled when stdout is not a terminal
# ---------------------------------------------------------------------------

_USE_COLOR = sys.stdout.isatty()

def _c(code, text):
    return '\033[%sm%s\033[0m' % (code, text) if _USE_COLOR else text

def _red(t):    return _c('91', t)
def _yellow(t): return _c('93', t)
def _green(t):  return _c('92', t)

def cprint(msg):
    """Print msg with ANSI color based on its tag."""
    if '[FAIL]' in msg or '[ORDER]' in msg:
        print(_red(msg))
    elif '[WARN]' in msg or '[SKIP]' in msg:
        print(_yellow(msg))
    elif '[OK]' in msg:
        print(_green(msg))
    else:
        print(msg)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

MOD_ROOT   = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
CONSTS_PY  = os.path.join(MOD_ROOT, 'Assets', 'Python', 'Consts.py')
CVENUMS_H  = os.path.join(MOD_ROOT, 'CvGameCoreDLL', 'CvEnums.h')
XML_ROOT   = os.path.join(MOD_ROOT, 'Assets', 'XML')

# ---------------------------------------------------------------------------
# Check definitions
#   label         - human-readable category name
#   enum_name     - C++ enum name in CvEnums.h
#   enum_prefix   - prefix shared by all real constants in that enum
#   xml_rel       - path to XML file relative to Assets/XML/
#   xml_prefix    - prefix used in <Type> tags in that XML file
#   py_count_var  - Python variable in Consts.py whose value should equal
#                   the number of enum entries (None = skip check)
#   py_tuple_var  - same variable name whose (...) = range(...) tuple to use
#                   for order comparison (None = skip order check)
#   py_count_note - optional string appended to count mismatch messages to
#                   explain expected differences (e.g. plague/pagan entries)
# ---------------------------------------------------------------------------

CHECKS = [
    dict(
        label='BuildingClass',
        enum_name='BuildingClassTypes', enum_prefix='BUILDINGCLASS_',
        xml_rel='Buildings/CIV4BuildingClassInfos.xml', xml_prefix='BUILDINGCLASS_',
        py_count_var=None, py_tuple_var=None,
        civ_prefix_aware=True,
    ),
    dict(
        label='Building',
        enum_name='BuildingTypes', enum_prefix='BUILDING_',
        xml_rel='Buildings/CIV4BuildingInfos.xml', xml_prefix='BUILDING_',
        py_count_var='iNumBuildings', py_tuple_var='iNumBuildings',
        py_count_note='plague not tracked in Python; pagan shrines are XML-only',
        py_count_enum_offset=1,   # plague is in CvEnums.h but not tracked in Python
        count_gap_expected=12,    # pagan shrines are XML-only (not in CvEnums.h)
        civ_prefix_aware=True,
        py_tuple_name_aliases={'BUILDING_FORT_MC_HENRY': 'BUILDING_FORT_MCHENRY'},
    ),
    dict(
        label='UnitClass',
        enum_name='UnitClassTypes', enum_prefix='UNITCLASS_',
        xml_rel='Units/CIV4UnitClassInfos.xml', xml_prefix='UNITCLASS_',
        py_count_var=None, py_tuple_var=None,
    ),
    dict(
        label='Unit',
        enum_name='UnitTypes', enum_prefix='UNIT_',
        xml_rel='Units/CIV4UnitInfos.xml', xml_prefix='UNIT_',
        py_count_var='iNumUnits', py_tuple_var='iNumUnits',
        py_tuple_civ_prefix_aware=True,
        py_tuple_name_aliases={
            'UNIT_ORTHODOX_MISS':        'UNIT_ORTHODOX_MISSIONARY',
            'UNIT_CATHOLIC_MISS':        'UNIT_CATHOLIC_MISSIONARY',
            'UNIT_PROTESTANT_MISS':      'UNIT_PROTESTANT_MISSIONARY',
            'UNIT_FA_RS':                'UNIT_CUBAN_FARS',
            'UNIT_ANTI_TANK':            'UNIT_AT_INFANTRY',
            'UNIT_GRENADIER_CAVALRY':    'UNIT_ARGENTINE_MOUNTED_GRENADIER',
            'UNIT_WORKBOAT':             'UNIT_WORK_BOAT',
            'UNIT_FE_GREAT_PROPHET':     'UNIT_FEMALE_GREAT_PROPHET',
            'UNIT_FE_GREAT_ARTIST':      'UNIT_FEMALE_GREAT_ARTIST',
            'UNIT_FE_GREAT_SCIENTIST':   'UNIT_FEMALE_GREAT_SCIENTIST',
            'UNIT_FE_GREAT_MERCHANT':    'UNIT_FEMALE_GREAT_MERCHANT',
            'UNIT_FE_GREAT_ENGINEER':    'UNIT_FEMALE_GREAT_ENGINEER',
            'UNIT_FE_GREAT_STATESMAN':   'UNIT_FEMALE_GREAT_STATESMAN',
            'UNIT_FE_GREAT_GENERAL':     'UNIT_FEMALE_GREAT_GENERAL',
            'UNIT_FE_GREAT_SPY':         'UNIT_FEMALE_GREAT_SPY',
        },
    ),
    dict(
        label='Tech',
        enum_name='TechTypes', enum_prefix='',
        xml_rel='Technologies/CIV4TechInfos.xml', xml_prefix='TECH_',
        py_count_var='iNumTechs', py_tuple_var='iNumTechs',
        bare_enum=True,  # CvEnums.h TechTypes uses bare names (no TECH_ prefix)
        py_tuple_suffix_drops=['_TECH'],  # e.g. iCurrencyTech -> CURRENCY_TECH -> CURRENCY
        name_aliases={'CURRENCY_TECH': 'CURRENCY'},
        py_tuple_name_aliases={'CURRENCY': 'CURRENCY_TECH'},
    ),
    dict(
        label='Promotion',
        enum_name='PromotionTypes', enum_prefix='PROMOTION_',
        xml_rel='Units/CIV4PromotionInfos.xml', xml_prefix='PROMOTION_',
        py_count_var='iNumPromotions', py_tuple_var='iNumPromotions',
        py_tuple_suffix_drops=['_PROMO'],  # e.g. iShockPromo -> PROMOTION_SHOCK_PROMO -> PROMOTION_SHOCK
    ),
    dict(
        label='Bonus',
        enum_name='BonusTypes', enum_prefix='BONUS_',
        xml_rel='Terrain/CIV4BonusInfos.xml', xml_prefix='BONUS_',
        py_count_var='iNumBonuses', py_tuple_var='iNumBonuses',
        py_count_note='iNumBonuses counts base bonuses; bonus varieties share the same enum',
        xml_graphical_only_filter=True,
    ),
    dict(
        label='Civic',
        enum_name='CivicTypes', enum_prefix='CIVIC_',
        xml_rel='GameInfo/CIV4CivicInfos.xml', xml_prefix='CIVIC_',
        py_count_var='iNumCivics', py_tuple_var='iNumCivics',
        py_tuple_suffix_drops=['_CIVIC'],  # e.g. iFactoryCivic -> CIVIC_FACTORY_CIVIC -> CIVIC_FACTORY
    ),
    dict(
        label='CivicOption',
        enum_name='CivicOptionTypes', enum_prefix='CIVICOPTION_',
        xml_rel='GameInfo/CIV4CivicOptionInfos.xml', xml_prefix='CIVICOPTION_',
        py_count_var=None, py_tuple_var=None,
    ),
    dict(
        label='Feature',
        enum_name='FeatureTypes', enum_prefix='FEATURE_',
        xml_rel='Terrain/CIV4FeatureInfos.xml', xml_prefix='FEATURE_',
        py_count_var=None, py_tuple_var=None,
    ),
    dict(
        label='Improvement',
        enum_name='ImprovementTypes', enum_prefix='IMPROVEMENT_',
        xml_rel='Terrain/CIV4ImprovementInfos.xml', xml_prefix='IMPROVEMENT_',
        py_count_var=None, py_tuple_var=None,
    ),
    dict(
        label='Terrain',
        enum_name='TerrainTypes', enum_prefix='TERRAIN_',
        xml_rel='Terrain/CIV4TerrainInfos.xml', xml_prefix='TERRAIN_',
        py_count_var=None, py_tuple_var=None,
    ),
    dict(
        label='Civilization',
        enum_name='CivilizationTypes', enum_prefix='',
        xml_rel='Civilizations/CIV4CivilizationInfos.xml', xml_prefix='CIVILIZATION_',
        py_count_var='iNumCivs', py_tuple_var=None,
        bare_enum=True,
        name_aliases={'MINOR_CIV': 'MINOR', 'BARBARIAN_CIV': 'BARBARIAN'},
    ),
]

# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def read_file(path):
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def parse_cvenums(text, enum_name, prefix):
    """
    Extract the ordered list of <prefix>* constants from the named C++ enum.
    Skips sentinel values (those whose suffix starts with NUM_, FIRST_, LAST_).
    Returns (entries, error_string).
    """
    pattern = r'\benum\s+' + re.escape(enum_name) + r'\b[^{]*\{([^}]*)\}'
    m = re.search(pattern, text, re.DOTALL)
    if not m:
        return None, "enum %s not found in CvEnums.h" % enum_name

    entries = []
    for line in m.group(1).splitlines():
        line = re.sub(r'//.*', '', line).strip().rstrip(',').strip()
        if not line:
            continue
        m2 = re.match(r'(\w+)', line)
        if not m2:
            continue
        name = m2.group(1)
        if prefix:
            if not name.startswith(prefix):
                continue
            suffix = name[len(prefix):]
            # Skip sentinel entries (NUM_ENUMTYPES, LAST_ENUMTYPE).
            # FIRST_ is intentionally excluded to avoid skipping real names like CIVIC_FIRST_NATION.
            if re.match(r'^(NUM|LAST)(_|$)', suffix):
                continue
        else:
            # Bare-name enum (e.g. TechTypes): skip NO_* sentinels and count/last markers
            if re.match(r'^(NO|NUM|LAST)_', name):
                continue
        entries.append(name)

    return entries, None


def parse_xml(path, prefix, graphical_only_filter=False):
    """
    Extract all <Type>PREFIX*</Type> values from an XML file in document order.
    When graphical_only_filter=True, skips entries whose record contains
    <bGraphicalOnly>1</bGraphicalOnly> (e.g. bonus variety entries).
    Returns (entries, error_string).
    """
    if not os.path.exists(path):
        return None, "file not found: %s" % path
    content = read_file(path)
    if graphical_only_filter:
        entries = []
        type_re = re.compile(r'<Type>(%s[^<]+)</Type>' % re.escape(prefix))
        graphical_re = re.compile(r'<bGraphicalOnly>\s*1\s*</bGraphicalOnly>')
        matches = list(type_re.finditer(content))
        for i, m in enumerate(matches):
            seg_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            if not graphical_re.search(content[m.start():seg_end]):
                entries.append(m.group(1))
        return entries, None
    pattern = r'<Type>(%s[^<]+)</Type>' % re.escape(prefix)
    return re.findall(pattern, content), None


def get_python_count(text, var_name):
    """Return the integer value of a simple assignment in Consts.py, or None."""
    m = re.search(r'\b' + re.escape(var_name) + r'\s*=\s*(\d+)', text)
    return int(m.group(1)) if m else None


def extract_python_tuple(text, count_var):
    """
    Locate the tuple assigned via (...) = range(count_var) in Consts.py and
    return the list of camelCase identifiers, in order.
    Identifiers must contain at least one uppercase letter (filters out keywords).
    Returns None if the pattern is not found.
    """
    end_re = r'\)\s*=\s*range\s*\(\s*' + re.escape(count_var) + r'\s*\)'
    m = re.search(end_re, text)
    if not m:
        return None
    end_pos = m.start()

    # Walk backward from end_pos to find the matching open paren.
    depth = 0
    start_pos = 0
    for i in range(end_pos, -1, -1):
        if text[i] == ')':
            depth += 1
        elif text[i] == '(':
            depth -= 1
            if depth == 0:
                start_pos = i
                break

    raw = re.sub(r'#[^\n]*', '', text[start_pos:end_pos + 1])  # strip comments
    names = re.findall(r'\b([a-z][a-zA-Z0-9]+)\b', raw)
    return [n for n in names if any(c.isupper() for c in n)]


def python_name_to_enum(py_name, prefix):
    """
    Convert a Python camelCase constant (e.g. 'iKalasasaya') to an enum-style
    name (e.g. 'BUILDINGCLASS_KALASASAYA') using the given prefix.
    This is best-effort; some names may not normalise cleanly.
    """
    name = py_name
    # Strip single lower-case type prefix (i, e, b …) when followed by uppercase
    if len(name) > 1 and name[0].islower() and name[1].isupper():
        name = name[1:]
    elif name.startswith('i'):
        name = name[1:]

    # CamelCase -> UPPER_SNAKE
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    return prefix + name.upper()

# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------

MAX_REPORT = 15   # maximum mismatches to print per category

def compare_ordered(enum_entries, xml_entries, match_fn=None):
    """
    Return (errors, warnings, messages) comparing two ordered name lists.
    match_fn(e, x) -> bool  when provided, used instead of e == x for equality
    (e.g. to treat BUILDING_KUNA and BUILDING_MAYA_KUNA as the same position).
    errors   - count of order mismatches (DLL will use wrong integer)
    warnings - count of entries only in one source
    """
    if match_fn is None:
        match_fn = lambda e, x: e == x
    errors   = 0
    warnings = 0
    msgs     = []
    n_civ    = 0   # same-position civ-prefix name variants — not order errors

    n_e = len(enum_entries)
    n_x = len(xml_entries)

    if n_e != n_x:
        msgs.append("  COUNT: CvEnums.h=%d  XML=%d" % (n_e, n_x))
        # report names present in only one source, using match_fn to exclude civ-prefix pairs
        xml_set  = set(xml_entries)
        enum_set = set(enum_entries)
        only_e = sorted(e for e in enum_entries
                        if e not in xml_set and not any(match_fn(e, x) for x in xml_entries))
        only_x = sorted(x for x in xml_entries
                        if x not in enum_set and not any(match_fn(e, x) for e in enum_entries))
        if only_e:
            msgs.append("  Only in CvEnums.h (%d): %s%s" % (
                len(only_e), ', '.join(only_e[:8]),
                ' …' if len(only_e) > 8 else ''))
        if only_x:
            msgs.append("  Only in XML       (%d): %s%s" % (
                len(only_x), ', '.join(only_x[:8]),
                ' …' if len(only_x) > 8 else ''))
        warnings += 1

    reported = 0
    for i, (e, x) in enumerate(zip(enum_entries, xml_entries)):
        if e == x:
            continue
        if match_fn(e, x):
            n_civ += 1
            continue
        msgs.append("  [ORDER] pos %4d: CvEnums.h=%-50s XML=%s" % (i, e, x))
        errors += 1
        reported += 1
        if reported >= MAX_REPORT:
            msgs.append("  … (further mismatches suppressed)")
            break

    if n_civ:
        msgs.append("  (%d name variant(s) at same position — integers align)" % n_civ)

    return errors, warnings, msgs


def compare_python_order(py_names, enum_entries, enum_prefix, suffix_drops=None,
                         civ_prefix_aware=False, py_name_aliases=None):
    """
    Normalise py_names and compare with enum_entries.
    Returns (n_name_mismatches, messages).
    Name mismatches are printed as warnings (the integers may still be right).
    """
    msgs = []
    n = min(len(py_names), len(enum_entries))
    mismatches = []
    for i in range(n):
        norm = python_name_to_enum(py_names[i], enum_prefix)
        ev = enum_entries[i]
        match = norm == ev
        if not match and suffix_drops:
            match = any(norm.endswith(s) and norm[:-len(s)] == ev for s in suffix_drops)
        if not match and civ_prefix_aware and enum_prefix:
            match = ev.endswith('_' + norm[len(enum_prefix):])
        if not match and py_name_aliases:
            match = py_name_aliases.get(norm) == ev
        if not match:
            mismatches.append((i, py_names[i], norm, enum_entries[i]))

    if mismatches:
        msgs.append("  Python tuple vs CvEnums.h name mismatches (may be naming differences):")
        for i, py_raw, py_norm, ev in mismatches[:MAX_REPORT]:
            msgs.append("    pos %4d: Python %-30s -> %-50s  CvEnums.h: %s"
                        % (i, py_raw, py_norm, ev))
        if len(mismatches) > MAX_REPORT:
            msgs.append("    … (%d more suppressed)" % (len(mismatches) - MAX_REPORT))

    return len(mismatches), msgs

# ---------------------------------------------------------------------------
# Per-check runner
# ---------------------------------------------------------------------------

def run_check(chk, cvenums_text, consts_text):
    label      = chk['label']
    prefix     = chk['enum_prefix']
    bare_enum  = chk.get('bare_enum', False)
    civ_aware  = chk.get('civ_prefix_aware', False)
    xml_path   = os.path.join(XML_ROOT, chk['xml_rel'])
    py_count_v = chk.get('py_count_var')
    py_tuple_v = chk.get('py_tuple_var')
    py_note        = chk.get('py_count_note', '')
    py_enum_offset = chk.get('py_count_enum_offset', 0)
    count_gap_exp  = chk.get('count_gap_expected', 0)

    print("\n=== %s ===" % label)

    # --- CvEnums.h ---
    enum_entries, err = parse_cvenums(cvenums_text, chk['enum_name'], prefix)
    if err:
        cprint("  [SKIP] %s" % err)
        return {'label': label, 'errors': 0, 'warnings': 1}

    # --- XML ---
    graphical_only = chk.get('xml_graphical_only_filter', False)
    xml_entries, err = parse_xml(xml_path, chk['xml_prefix'], graphical_only_filter=graphical_only)
    if err:
        cprint("  [SKIP] %s" % err)
        return {'label': label, 'errors': 0, 'warnings': 1}

    # Build match function for civ-qualified XML name variants (e.g. BUILDING_KUNA vs BUILDING_MAYA_KUNA)
    if civ_aware:
        _ep = prefix
        _xp = chk['xml_prefix']
        def _match_fn(e, x, ep=_ep, xp=_xp):
            e_suf = e[len(ep):]
            x_suf = x[len(xp):]
            return x_suf.endswith('_' + e_suf)
        match_fn = _match_fn
    else:
        match_fn = None

    aliases = chk.get('name_aliases', {})
    if aliases:
        _rev = {v: k for k, v in aliases.items()}
        def _alias_fn(e, x, a=aliases, r=_rev):
            return a.get(e) == x or r.get(e) == x
        prev_fn = match_fn
        if prev_fn is None:
            match_fn = _alias_fn
        else:
            def match_fn(e, x, _a=_alias_fn, _p=prev_fn):
                return _a(e, x) or _p(e, x)

    # --- Primary: order comparison (this is the crash-risk check) ---
    if bare_enum:
        # Strip xml_prefix from XML names so they match bare CvEnums.h names
        xml_strip = chk['xml_prefix']
        xml_cmp = [e[len(xml_strip):] if e.startswith(xml_strip) else e for e in xml_entries]
    else:
        xml_cmp = xml_entries
    errors, warnings, msgs = compare_ordered(enum_entries, xml_cmp, match_fn=match_fn)
    count_gap_ok = count_gap_exp > 0 and (len(xml_entries) - len(enum_entries)) == count_gap_exp
    if errors == 0 and (warnings == 0 or count_gap_ok):
        gap_note = (' (%d XML-only entries expected)' % count_gap_exp) if count_gap_ok else ''
        cprint("  [OK] %d entries — CvEnums.h and XML in sync%s" % (len(enum_entries), gap_note))
        for msg in msgs:
            if 'COUNT' not in msg and 'Only in' not in msg:
                print(msg)   # still print civ-qualified note
    elif errors == 0:
        cprint("  [WARN] Order is consistent but counts differ (%d entries in CvEnums.h, %d in XML)"
               % (len(enum_entries), len(xml_entries)))
        for msg in msgs:
            cprint(msg)
    else:
        cprint("  [FAIL] %d order mismatch(es) — DLL will use wrong integers!" % errors)
        for msg in msgs:
            cprint(msg)

    # --- Python count check ---
    if py_count_v and consts_text:
        py_val = get_python_count(consts_text, py_count_v)
        if py_val is None:
            cprint("  [WARN] %s not found in Consts.py" % py_count_v)
        else:
            n_xml = len(xml_entries)
            n_ev  = len(enum_entries)
            if py_val == n_ev:
                cprint("  [OK] Python %s=%d matches CvEnums.h count" % (py_count_v, py_val))
            elif py_enum_offset and py_val == n_ev - py_enum_offset:
                cprint("  [OK] Python %s=%d = CvEnums.h %d - %d (expected: plague excluded)"
                       % (py_count_v, py_val, n_ev, py_enum_offset))
            elif py_val == n_xml:
                cprint("  [OK] Python %s=%d matches XML count" % (py_count_v, py_val))
            else:
                diff_ev  = n_ev  - py_val
                diff_xml = n_xml - py_val
                note = ("  (%s)" % py_note) if py_note else ''
                cprint("  [WARN] Python %s=%d, CvEnums.h=%d (+%d), XML=%d (+%d)%s"
                       % (py_count_v, py_val, n_ev, diff_ev, n_xml, diff_xml, note))

    # --- Python tuple order check (best-effort) ---
    if py_tuple_v and consts_text:
        py_names = extract_python_tuple(consts_text, py_tuple_v)
        if py_names is None:
            cprint("  [WARN] Tuple for %s not found in Consts.py" % py_tuple_v)
        else:
            civ_tuple_aware = chk.get('py_tuple_civ_prefix_aware', False)
            py_name_aliases = chk.get('py_tuple_name_aliases', {})
            suffix_drops = chk.get('py_tuple_suffix_drops', [])
            n_miss, msgs2 = compare_python_order(py_names, enum_entries, prefix, suffix_drops,
                                                 civ_tuple_aware, py_name_aliases)
            if n_miss == 0:
                cprint("  [OK] Python tuple order matches CvEnums.h (via name normalisation)")
            else:
                cprint("  [WARN] %d Python name(s) did not normalise to the CvEnums.h name at the same position" % n_miss)
                print("         (Could be intentional naming differences — check if integers still align)")
                for msg in msgs2:
                    print(msg)

    return {'label': label, 'errors': errors,
            'warnings': 0 if (errors == 0 and count_gap_ok) else warnings}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    print("validate_enums.py")
    print("Mod root : %s" % MOD_ROOT)
    print("CvEnums.h: %s" % CVENUMS_H)
    print("Consts.py: %s" % CONSTS_PY)

    cvenums_text = read_file(CVENUMS_H)
    if not cvenums_text:
        print("ERROR: Cannot read CvEnums.h")
        sys.exit(1)

    consts_text = read_file(CONSTS_PY)
    if not consts_text:
        print("WARNING: Cannot read Consts.py — Python count/order checks skipped")

    total_errors = 0
    results = []
    for chk in CHECKS:
        r = run_check(chk, cvenums_text, consts_text)
        results.append(r)
        total_errors += r['errors']

    # --- File-level recap ---
    print("\n" + "=" * 60)
    print("RECAP")
    w = max(len(r['label']) for r in results)
    for r in results:
        if r['errors']:
            line = "  %-*s  [FAIL] %d order mismatch(es)" % (w, r['label'], r['errors'])
            print(_red(line))
        elif r['warnings']:
            line = "  %-*s  [WARN] count or name differences" % (w, r['label'])
            print(_yellow(line))
        else:
            line = "  %-*s  [OK]" % (w, r['label'])
            print(_green(line))

    print("=" * 60)
    if total_errors == 0:
        cprint("All order checks passed.  [OK]")
    else:
        cprint("%d order mismatch(es) found — these cause wrong DLL integers.  [FAIL]" % total_errors)

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == '__main__':
    main()
