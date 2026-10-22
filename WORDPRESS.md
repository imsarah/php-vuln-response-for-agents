# WordPress: patching it properly

WordPress sites are the majority of what this playbook gets pointed at, and "patch it" means three different jobs that get confused with each other:

1. **Patch PHP** (the branch the site runs on) — Phase 6 / Phase 9 of the main guide.
2. **Patch WordPress itself** — core, plugins, themes.
3. **Harden the site** — settings and files, so a plugin compromise does not become a shell.

Do them in that order unless the site is already compromised. Everything below is from a real response unless marked otherwise; commands are `wp-cli` unless noted.

## 0. Pre-flight (do not skip)

```bash
wp core version                      # WP version
wp core verify-checksums             # Integrity: files that do not match the release
wp plugin list --update=available    # What is actually outdated
wp theme list --update=available
wp user list --role=administrator    # Who can install code
wp db size --tables --human-readable # Before you dump
```

- **Backup first**: files + database, outside the webroot. A dump in the docroot is a public file.
- **Staging is not optional for plugin updates.** Clone docroot (rsync) and import the dump. If the account cannot create a database, import into the *same* database under a prefix (`stg_`) and point the staging `wp-config.php` at it, then set `siteurl`/`home` to the staging hostname. Undo it afterwards by dropping the prefixed tables.
- Check the PHP branch against the plugins **before** switching: `wp plugin list` plus the plugin's "requires PHP" header. A plugin that declares `Requires PHP: 7.4` may still break on 8.3.

## 0b. When there is no wp-cli (shared hosting, no SSH, official Docker image)

Plenty of WordPress sites cannot run `wp` at all — including the **official `wordpress` Docker image**, which ships WordPress, Apache and PHP but no wp-cli. The procedure survives without it, but you lose the dry run and the precise rollback — so compensate with the stash and the staging copy.

- **Installing wp-cli is itself a write.** Downloading a phar into the container changes the system you were asked to inspect; it needs the same approval as any other change, and on a container without a mounted volume it disappears on recreate anyway.
- **Reading the database without a client**: a PHP one-liner over stdin is enough (`docker exec -i <name> php -r '…'`), and it keeps credentials out of the transcript if you read them from `wp-config.php` inside that same process.

- **Backup from the panel first**: files (or at least `wp-content`) *and* the database export. A dashboard update cannot be undone by the host.
- **Stash a copy of the plugin folder and its version** before updating it (`wp-content/plugins/<slug>` → download via File Manager). This is your rollback: re-upload the old folder, or use **Plugins → Add New → Upload Plugin** with the previous zip.
- **Update one group at a time**, starting with the plugins nobody can live without (security, commerce, forms). Refresh the dashboard between batches and look for the "Briefly unavailable for scheduled maintenance" screen or a leftover `.maintenance` file in the WordPress root (next to `wp-config.php`) — delete it once the batch finished.
- **Core update** the same way: Dashboard → Updates, or the panel's WordPress installer if it bundles one. Never update core and a page builder in the same sitting.
- **No dry run means staging is the dry run.** Use the prefixed-copy trick from the pre-flight section, run the dashboard updates there first, then repeat on production.
- If a batch dies mid-way, **do not immediately retry the whole batch**: refresh, note which plugin's row still shows an update, and do that one alone.

*The dashboard steps in this section are written from the WordPress interface, not from a live run on a host without `wp-cli` (the two Docker bullets are from a live run); treat the timings as guidance and the backups as mandatory.*

## 1. Patch PHP for a WordPress site

The mechanics live in the main guide (Phase 5–9). WordPress-specific traps:

- **Extensions vanish on a version switch.** A missing `mysqli` shows as *"Your PHP installation appears to be missing the MySQL extension which is required by WordPress."* Enable `mysqli` (or `nd_mysqli` on CloudLinux) **before** the switch, not after, and confirm it is listed as loaded for the new branch.
- **`memory_limit` and upload limits reset.** Elementor, page builders and imports fail at 128M; record the old values and restore them, then read the effective values back as the web server sees them (the CLI often loads a different `php.ini`).
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
- **Update in dependency groups, not alphabetically.** Page builders ship an addon pack, WooCommerce ships gateway extensions, and some plugins declare nothing while still requiring a companion. Updating one half and not the other is a common way to break a site that "only had two updates". Update the pair in the same batch, or neither.
- **When an update will not download**, that is a different failure from a broken update. Premium plugins and themes check a licence against a vendor server: a lapsed licence, a migrated site or a dead endpoint shows as `401`/`403`/timeout in the update log, while the dashboard just says "update failed". Renew or re-attach the licence, or upload the new zip manually — do not force-reinstall from the old server, and do not assume the plugin is current because it says so.
- **Inactive plugins are still attack surface.** Delete unused ones (`wp plugin delete <slug>`), which also removes their update burden.
- **Auto-updates:** enabling them for minor/core security releases is usually right; do not enable them for plugins you have not tested. Read the setting back afterwards (`wp plugin auto-updates status --all`).

## 2b. Gates before anything destructive

Deleting a plugin, overwriting a file, dropping the prefixed staging tables — each needs the same three steps, in this order:

1. **A restore point exists** (files + database), and you have said where it is.
2. **The exact list is shown before it happens** — paths, plugin slugs, table names — not "some unused plugins".
3. **The operator confirms.** A general "go ahead and patch it" does not cover deletion.

Two specific traps:

- **Never reinstall a plugin over a modified copy without diffing first.** Customised plugin/theme files are overwritten silently; diff `wp-content/plugins/<slug>` against the version you are installing, or take the folder aside first.
- **`wp` refuses to run as root without `--allow-root`.** Adding the flag to get past the error is the wrong fix: run as the site user, or use `sudo -u <siteuser> wp …`.

## 3. Harden the site (after the patches land)

```bash
wp config set DISALLOW_FILE_EDIT true --raw       # No plugin/theme editor in wp-admin
wp config set DISALLOW_FILE_MODS false --raw      # keep installs working; true locks them
```

Read both back with `wp config get DISALLOW_FILE_EDIT` / `wp config get DISALLOW_FILE_MODS` — a mistyped name is added silently and does nothing.

- **No PHP in `uploads/`.** If the host allows a `.htaccess`, put this in `wp-content/uploads/.htaccess`:
  ```apache
  <FilesMatch "(?i)\.(php[0-9]?|phtml|phar)$">
    Require all denied
  </FilesMatch>
  ```
  On nginx this is a server config change — ask the host rather than shipping a `.htaccess` that does nothing (Phase 5 of the main guide); either way, verify by fetching a harmless test `.php` placed in `uploads/` (expect 403/404, then delete it) rather than assuming the rule applies.

  An extension list is never complete — under some handler configurations a double extension like `shell.php.jpg` still executes — so treat the `.htaccess` rule as best-effort. The only real guarantee is turning the PHP handler off for that directory at the server level (Apache: `RemoveHandler` / `SetHandler none`; nginx: a `location` block denying `.php` under `uploads/`), which is a host change, not something you can do from a file on shared hosting.
- **Audit administrators**, remove dormant ones, rotate their passwords; add 2FA (a plugin is acceptable).
- **XML-RPC**: block only if you have confirmed nothing uses it (some apps and Jetpack do). If you block it, request `/xmlrpc.php` afterwards and confirm it is refused.
- **After any suspected compromise**: rotate DB credentials, all salts (`wp config shuffle-salts`), admin passwords and hosting-panel credentials, then re-run the compromise check in Phase 4.
- **Keep the WordPress `.htaccess` block intact** (`# BEGIN WordPress … # END WordPress`). Add your rules outside it, or the next permalink save wipes them.

## 4. Failure modes you will actually hit

| Symptom | Real meaning | Do this |
|---|---|---|
| *"missing the MySQL extension"* | New PHP branch has `mysqli` disabled | Enable the extension, or switch back immediately |
| Every page, including `wp-login.php`, shows a warning | A plugin/theme major update removed a file another one requires | `wp plugin list`, then pin the offender back to its last working version |
| *"Briefly unavailable for scheduled maintenance"* | A core/plugin update left `.maintenance` behind | Delete `.maintenance` in the WordPress root once the update is finished |
| Admin requires a database update and the front end looks broken | Elementor/LearnPress/WooCommerce DB migration pending | Sign in to wp-admin once, run the upgrade, then purge caches |
| Front end fine, admin blank/500 | `memory_limit` too low after the switch | Restore the previous limit (256M is a sane floor for page builders) and read the effective value back |
| `.htaccess` block vanished | LiteSpeed Cache / Wordfence / permalink save rewrote it | Move the rule out of plugin-owned scope; re-verify by hash |
| 200 everywhere but the page content is old | Page cache or object cache | Purge plugin + server cache, re-request with a cache-busting query string |
| Update available, download fails (`401`/`403`/timeout) | Licence lapsed or the vendor's update server is gone | Renew/re-attach the licence, or upload the zip manually; never force-reinstall from the old server |
| Stale options or missing tables after an update, HTTP cache already purged | Redis/Memcached object cache still holding serialized data from the old version | Flush the object cache too (`wp cache flush`, or the panel's cache tool) — a different layer from page cache |
| Two plugins break when updated separately | They ship together (builder + addon, commerce + gateway) | Update the pair in one batch, or roll both back together |

**Multisite:** out of scope for this document. Network-activated plugins update from the Network Admin and apply to every site; a single-site rollback does not undo a network-wide one. Get explicit approval before touching a network, and take a full database dump first.

## 5. What "done" looks like

- `wp core verify-checksums` clean, `wp plugin list --update=available` empty (or every remaining pin documented).
- Front end, `wp-login.php`, REST index and one form all answer 200 with no PHP warnings; rendered text matches staging.
- PHP branch at a patched release, with the advisory cited in the report.
- A restore point exists, and the report says which of the four states each site is in.
