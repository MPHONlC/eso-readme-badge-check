# ESO Addon README Badge Check

Checks that shields.io badges in your GitHub README (`![Version](https://img.shields.io/badge/version-X.X.X-...)`, `![ESO API](https://img.shields.io/badge/ESO%20API-XXXXX%20%7C%20XXXXX-...)`) still match your `.addon` manifest's real current `## Version:` / `## APIVersion:`. These badges are hand-typed text, not a live query - they silently go stale the moment you bump a version and forget to edit the README too.

## Usage

```yaml
name: README Badge Check

on:
  push:
    branches: [main]
    paths:
      - 'README.md'
      - '*.addon'
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: MPHONlC/eso-readme-badge-check@Version-0.0.1
        with:
          manifest_file: 'YourAddon.addon'
```

To auto-fix instead of just failing:

```yaml
      - uses: MPHONlC/eso-readme-badge-check@Version-0.0.1
        with:
          manifest_file: 'YourAddon.addon'
          fix: true
      # then commit README.md yourself if it changed - this action only writes the file
```

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `readme_file` | No | `README.md` | GitHub README containing the badges. |
| `manifest_file` | Yes | - | `.addon` manifest to compare against. |
| `fix` | No | `false` | Rewrite stale badge values in place instead of failing. |

> [!NOTE]
> Badges are matched against the exact shields.io URL shape shown at the top of this README (`.../badge/version-...` and `.../badge/ESO%20API-...`). A badge in a different shape or from a different service isn't recognized - the check silently reports "no badge found" and skips it rather than failing, so a typo'd badge URL won't be caught by this action.

## License

MIT - see [LICENSE](LICENSE).
