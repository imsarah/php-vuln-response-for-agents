# WordPress: patching it properly

WordPress sites are the majority of what this playbook gets pointed at, and "patch it" means three different jobs that get confused with each other:

1. **Patch PHP** (the branch the site runs on) — Phase 6 / Phase 9 of the main guide.
2. **Patch WordPress itself** — core, plugins, themes.
3. **Harden the site** — settings and files, so a plugin compromise does not become a shell.

Do them in that order unless the site is already compromised. Everything below is from a real response; commands are `wp-cli` unless noted.

## 0. Pre-flight (do not skip)

```bash
wp core version                      # WP version
wp core verify-checksums             # Integrity: files that do not match the release
wp plugin list --update=available    # What is actually outdated
wp theme list --update=available
wp user list --role=administrator    # Who can install code
wp db size --tables --human          # Before you dump
```

- **Backup first**: files + database, outside the webroot. A dump in the docroot is a public file.
- **Staging is not optional for plugin updates.** Clone docroot (rsync) and import the dump. If the account cannot create a database, import into the *same* database under a prefix (`stg_`) and point the staging `wp-config.php` at it, then set `siteurl`/`home` to the staging hostname. Undo it afterwards by dropping the prefixed tables.
- Check the PHP branch against the plugins **before** switching: `wp plugin list` plus the plugin's "requires PHP" header. A plugin that declares `Requires PHP: 7.4` may still break on 8.3.

## 1. Patch PHP for a WordPress site

The mechanics live in the main guide (Phase 5–9). WordPress-specific traps:

- **Extensions vanish on a version switch.** A missing `mysqli` shows as *"Your PHP installation appears to be missing the MySQL extension which is required by WordPress."* Enable `mysqli` (or `nd_mysqli` on CloudLinux) **before** the switch, not after.
- **`memory_limit` and upload limits reset.** Elementor, page builders and imports fail at 128M; record the old values and restore them.
- **Pending DB upgrades surface in wp-admin**, not on the front end: Elementor, LearnPress, WooCommerce. `wp core update-db` does core; plugin upgrades usually happen on the next admin visit — sign in once and complete them, or the site limps.
- **Purge every cache layer** after the switch: plugin cache, LiteSpeed/`x-litespeed-cache`, SureCache, Cloudflare. A stale `HIT` hides both fixes and breakage.
- **Verify by text, not by status**: compare rendered text against staging (`difflib`/`diff <(curl … ) <(curl …)`), check `wp-login.php` renders, check one form's AJAX endpoint answers, and confirm no `Warning:`/`Fatal error` in the HTML of any page.

## 2. Patch WordPress core, plugins, themes

On staging first, always:

```bash
wp plugin update --all --dry-run          # What would change
wp plugin update --all --exclude=<slug>   # The real run (see below)
wp theme update --all
wp core update && wp core update-db
```

- **Read the version jumps, not just the count.** A major-version plugin update is a rewrite. In the response this guide came from, one plugin's 5.x → 6.x update deleted a file that the theme required, and every page — including `wp-login.php` — threw a warning. The fix was one plugin pinned back:

  ```bash
  wp plugin install <slug> --version=5.1.0 --force
  ```

  Production then ran `--exclude=<slug>` so the breakage could never land.
- **Pin what breaks, and write down why** (plugin, version, symptom, date) so the next person does not "just update everything".
- **Inactive plugins are still attack surface.** Delete unused ones (`wp plugin delete <slug>`), which also removes their update burden.
- **Auto-updates:** enabling them for minor/core security releases is usually right; do not enable them for plugins you have not tested.

## 3. Harden the site (after the patches land)

```bash
wp config set DISALLOW_FILE_EDIT true --raw       # No plugin/theme editor in wp-admin
wp config set DISALLOW_FILE_MODS false --raw      # keep installs working; true locks them
```

- **No PHP in `uploads/`.** If the host allows a `.htaccess`:
  ```apache
  <Directory "…/wp-content/uploads">
    <FilesMatch "\.php$">
      Require all denied
    </FilesMatch>
  </Directory>
  ```
  On nginx this is a server config change — ask the host rather than shipping a `.htaccess` that does nothing (Phase 5 of the main guide).
- **Audit administrators**, remove dormant ones, rotate their passwords; add 2FA (a plugin is acceptable).
- **XML-RPC**: block only if you have confirmed nothing uses it (some apps and Jetpack do).
- **After any suspected compromise**: rotate DB credentials, all salts (`wp config shuffle-salts`), admin passwords and hosting-panel credentials, then re-run the compromise check in Phase 4.
- **Keep the WordPress `.htaccess` block intact** (`# BEGIN WordPress … # END WordPress`). Add your rules outside it, or the next permalink save wipes them.

## 4. Failure modes you will actually hit

| Symptom | Real meaning | Do this |
|---|---|---|
| *"missing the MySQL extension"* | New PHP branch has `mysqli` disabled | Enable the extension, or switch back immediately |
| Every page, including `wp-login.php`, shows a warning | A plugin/theme major update removed a file another one requires | `wp plugin list`, then pin the offender back to its last working version |
| *"Briefly unavailable for scheduled maintenance"* | A core/plugin update left `.maintenance` behind | Delete `wp-content/.maintenance` once the update is finished |
| Admin requires a database update and the front end looks broken | Elementor/LearnPress/WooCommerce DB migration pending | Sign in to wp-admin once, run the upgrade, then purge caches |
| Front end fine, admin blank/500 | `memory_limit` too low after the switch | Restore the previous limit (256M is a sane floor for page builders) |
| `.htaccess` block vanished | LiteSpeed Cache / Wordfence / permalink save rewrote it | Move the rule out of plugin-owned scope; re-verify by hash |
| 200 everywhere but the page content is old | Page cache or object cache | Purge plugin + server cache, re-request with a cache-busting query string |

## 5. What "done" looks like

- `wp core verify-checksums` clean, `wp plugin list --update=available` empty (or every remaining pin documented).
- Front end, `wp-login.php`, REST index and one form all answer 200 with no PHP warnings; rendered text matches staging.
- PHP branch at a patched release, with the advisory cited in the report.
- A restore point exists, and the report says which of the four states each site is in.
