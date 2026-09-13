import re
import sys
import argparse

VERSION_BADGE_RE = re.compile(
    r'(!\[[^\]]*\]\(https://img\.shields\.io/badge/version-)([^-]+)(-[^)]*\))'
)
API_BADGE_RE = re.compile(
    r'(!\[[^\]]*\]\(https://img\.shields\.io/badge/ESO%20API-)(\d+)%20%7C%20(\d+)(-[^)]*\))'
)


def read(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--readme-file', default='README.md')
    parser.add_argument('--manifest-file', required=True)
    parser.add_argument('--fix', action='store_true')
    args = parser.parse_args()

    readme = read(args.readme_file)
    manifest = read(args.manifest_file)
    out = ["## README badge freshness check", ""]

    if readme is None:
        print(f"::error::Could not read {args.readme_file}")
        sys.exit(1)
    if manifest is None:
        print(f"::error::Could not read {args.manifest_file}")
        sys.exit(1)

    version_m = re.search(r'^##\s*Version:\s*(\S+)', manifest, re.M)
    api_m = re.search(r'^##\s*APIVersion:\s*(\d+)\s+(\d+)', manifest, re.M)

    problems = []
    changed = False
    new_readme = readme

    badge_m = VERSION_BADGE_RE.search(readme)
    if badge_m and version_m:
        badge_version = badge_m.group(2)
        real_version = version_m.group(1)
        if badge_version != real_version:
            problems.append(f"Version badge says `{badge_version}`, manifest says `{real_version}`")
            if args.fix:
                new_readme = VERSION_BADGE_RE.sub(lambda m: m.group(1) + real_version + m.group(3), new_readme, count=1)
                changed = True
        out.append(f"Version badge: `{badge_version}` (manifest: `{real_version}`)")
    elif badge_m:
        out.append(f"Version badge found (`{badge_m.group(2)}`) but manifest has no '## Version:' field to compare against.")
    else:
        out.append("No version badge found - skipping that check.")

    badge_api_m = API_BADGE_RE.search(readme)
    if badge_api_m and api_m:
        badge_api = (badge_api_m.group(2), badge_api_m.group(3))
        real_api = (api_m.group(1), api_m.group(2))
        if badge_api != real_api:
            problems.append(f"API badge says `{badge_api[0]} | {badge_api[1]}`, manifest says `{real_api[0]} | {real_api[1]}`")
            if args.fix:
                new_readme = API_BADGE_RE.sub(
                    lambda m: m.group(1) + real_api[0] + '%20%7C%20' + real_api[1] + m.group(4),
                    new_readme, count=1
                )
                changed = True
        out.append(f"API badge: `{badge_api[0]} | {badge_api[1]}` (manifest: `{real_api[0]} | {real_api[1]}`)")
    elif badge_api_m:
        out.append("API badge found but manifest has no '## APIVersion:' field to compare against.")
    else:
        out.append("No API badge found - skipping that check.")

    out.append("")

    if changed:
        with open(args.readme_file, 'w') as f:
            f.write(new_readme)
        out.append(f"Fixed: rewrote stale badge value(s) in {args.readme_file}.")
        print('\n'.join(out))
        return

    if problems:
        out.append("**Stale badge(s) found:**")
        for p in problems:
            out.append(f"- {p}")
            print(f"::error::{p}")
        print('\n'.join(out))
        sys.exit(1)
    else:
        out.append("All badges match the manifest.")
        print('\n'.join(out))


if __name__ == '__main__':
    main()
