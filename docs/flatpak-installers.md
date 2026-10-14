# Installing Flatpak applications from YAML

Use the `flatpak` runner and its `install_flatpak` task. Flatpak must already be
installed on the host. Installations created by this task are always per-user;
system installations are neither reused nor removed.

## Flathub

The application ID is the only required application setting. Flathub is the
default remote. If the user has no user-scoped Flathub remote, Lutris asks before
adding the official Flathub repository. Other remotes must already be configured.

```yaml
name: Brief
game_slug: brief
slug: brief-flathub
version: Flathub
runner: flatpak
script:
  game:
    appid: io.github.shonebinu.Brief
  installer:
    - task:
        name: install_flatpak
```

If you load a script in a format where Lutris already supplies its installer
metadata, `game`, `files` and `installer` are the contents of the `script` section.
Optional `remote`, `arch` and `branch` parameters can be set on the task. The
application ID, architecture and branch default to the `game` section.

## A downloaded GitHub release

Let Lutris download the package using `files`, then reference its file alias in
the task. Use a direct asset URL, not the GitHub release page or a ZIP containing
an asset. The declared application ID must match the package.

```yaml
name: Example application
game_slug: example-application
slug: example-application-github
version: '1.0'
runner: flatpak
script:
  game:
    appid: io.github.author.Application
  files:
    - package: https://github.com/author/project/releases/download/v1.0/application.flatpak
  installer:
    - task:
        name: install_flatpak
        file: package
```

The same task accepts a `.flatpakref`. Lutris checks its application ID and asks
for confirmation because the reference can add repositories and download
runtimes. Flatpak manages runtime dependencies; failures such as an unavailable
runtime or missing bundle origin are reported by the installer.

## Running Lutris as a Flatpak

Commands use `flatpak-spawn --host flatpak`, so the host installation is used.
Lutris needs `flatpak-spawn` and permission to talk to
`org.freedesktop.Flatpak`; access errors are reported separately from a missing
application. Downloaded local packages are copied temporarily into Lutris's
shared per-application cache so the host can read them, even if the original
file was in sandbox-private `/tmp`.

## Launching and removing applications

After successful installation Lutris saves the actual application reference,
sets `install_type: user`, and launches it with `flatpak run --user`. An already
installed user application is reused without reinstalling or updating it.

The uninstall dialog has a separate **Uninstall Flatpak application** checkbox,
independent of removing the Lutris library entry. It is initially selected only
for applications installed by this task. Explicit confirmation is required,
because the same application may be used outside Lutris. Personal data and
unrelated dependencies are retained; system installations are never removed.

If uninstalling an application fails, its Lutris entry is retained. When removing
multiple applications, some earlier removals may already have succeeded before
a later one fails; retrying skips applications that are no longer installed.

## Flatpak packaging requirements

The Lutris Flatpak manifest must provide `flatpak-spawn` and allow host-command
access through this finish argument:

```yaml
finish-args:
  - --talk-name=org.freedesktop.Flatpak
```

The default per-application cache is already shared with the host by Flatpak;
keep that mapping available for temporary package staging. No broad filesystem
permission is required solely for this staging step. These manifest changes
belong to the Lutris Flatpak packaging project and are not included in this PR.

If native Flatpak is missing, the installer shows an explanatory **Flatpak is
required** dialog, with an **OK** button and instructions to install it using the
distribution package manager. Missing `flatpak-spawn` or a failed host-access
check instead shows **Flatpak is inaccessible**. These are expected errors;
technical diagnostics stay in the logs, not in a traceback presented to users.
