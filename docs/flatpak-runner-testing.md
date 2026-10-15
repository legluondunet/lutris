# Testing the Flatpak runner inside Lutris Flatpak

This test build reuses the **precompiled stable Lutris application from Flathub** as its base. Only the modified Lutris client and flatpak-spawn are rebuilt. The application runtime and SDK branch are read from the installed base metadata, and its exact commit is recorded in the diagnostics artifact. It does not rebuild Qt, VLC, DOSBox, Mesa or the other bundled dependencies.

Download the `lutris-flatpak-runner-tests-x86_64` artifact from the Build Flatpak runner test workflow and extract its ZIP.

```sh
flatpak install --user ./Lutris-runner-tests-x86_64.flatpak
flatpak run --branch=runner-tests net.lutris.Lutris -d
```

This uses the separate runner-tests branch of net.lutris.Lutris, built from the integration test sources. It shares user configuration with other branches of that application. Close other Lutris instances first.

The generated manifest retains Flathub permissions, explicitly includes flatpak-spawn, allows host commands through org.freedesktop.Flatpak, grants access to ~/Games, and inherits the installed base's extension points. The build checks Pillow imports and lutris --version before exporting the bundle.

Check access to host Flatpak:

```sh
flatpak run --branch=runner-tests --command=flatpak-spawn net.lutris.Lutris --host flatpak --version
```

Then load the YUNO YAML installer and test installation, extraction progress, data/font access, launch, and independent package/data removal. Installed games are host user Flatpaks visible with flatpak list --user.

Remove only the test branch:

```sh
flatpak uninstall --user net.lutris.Lutris//runner-tests
```

Do not add --delete-data if you want to retain shared Lutris configuration. This is a test overlay over Flathub's dependency set, not a full dependency rebuild.
