# Testing the Flatpak runner inside Lutris Flatpak

Download the `lutris-flatpak-runner-tests-x86_64` artifact from the Build Flatpak runner test workflow and extract its ZIP.

```sh
flatpak install --user ./Lutris-runner-tests-x86_64.flatpak
flatpak run --branch=runner-tests net.lutris.Lutris -d
```

This uses the separate `runner-tests` branch of `net.lutris.Lutris`, built from the integration test sources. It shares that application's user configuration with other branches. Close other Lutris instances before starting it.

The build explicitly includes `flatpak-spawn`, keeps `--talk-name=org.freedesktop.Flatpak` and the existing home/Games access, and stamps the source revision. It reuses the pinned Flathub packaging and the prior packaging compatibility adjustments from the Ultris fork. Source archives and SDKs are downloaded before compilation; diagnostics are uploaded on failure.

To check access to the host Flatpak installation:

```sh
flatpak run --branch=runner-tests --command=flatpak-spawn net.lutris.Lutris --host flatpak --version
```

Then load the YUNO YAML installer in this Lutris instance and test user installation, extraction progress, font/data access, launch and the independent package/data removal choices. Games installed by the runner are host user Flatpaks, visible with `flatpak list --user`.

Remove only this test branch with:

```sh
flatpak uninstall --user net.lutris.Lutris//runner-tests
```

Do not add `--delete-data` if you want to retain the shared Lutris configuration.
