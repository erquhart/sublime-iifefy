# Sublime Iifefy

A Sublime Text 3 plugin for wrapping Javascript code in immediately invoking functions.

## Installation

### Using [Package Control][pkgcontrol] (*Recommended*)

For all Sublime Text 2/3 users we recommend install via [Package Control][pkgcontrol].

1. [Install][pkgcontrol-install] Package Control if you haven't already
2. Use `cmd+shift+P` (or `ctrl+shift+P` for Windows) then select `Package Control: Install Package`
3. Search for `Iifefy` and select to install

### Manual Install

1. Click the `Preferences > Browse Packages…` menu
2. Browse up a folder and then into the `Installed Packages/` folder
3. Download the [zip archive][zip], rename it to `Iifefy.sublime-package` and copy it into the `Installed Packages/` directory
4. Restart Sublime Text

## Getting It Working

Find the new option for wrapping in IIFE's in the main menu at Edit > Wrap > Wrap selection/document
in IIFE. The option is also available in the context menu.

A keyboard shortcut can be added by going to the main menu at Preferences > Key Bindings - User and
adding the following to the file, replacing the key values with whatever you wish:

```
{ "keys": [ "ctrl+i" ], "command": "iifefy", "context":
    [{ "key": "selector", "operator": "equal", "operand": "source.js", "match_all": true }]
},
{ "keys": [ "ctrl+shift+i" ], "command": "iifefy_skip_initial_comments", "context":
    [{ "key": "selector", "operator": "equal", "operand": "source.js", "match_all": true }]
}
```

## Usage

If there are any selections, they'll be wrapped.

If there are no selections, the entire document will be wrapped.

There's a "skip_initial_comments" version of the command, which will begin wrapping at the first
non-comment, non-blank line.

Lastly, this plugin adds 'use strict' and a trailing newline to every IIFE by default. If making
this configurable would be helpful for you, open an issue.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

## License

Code copyright 2014 Professant LLC. Code released under [the MIT License][license].

[pkgcontrol]: https://sublime.wbond.net
[pkgcontrol-install]: https://sublime.wbond.net/installation
[zip]: https://github.com/professant/sublime-iifefy/archive/master.zip
[license]: https://github.com/professant/sublime-iifefy/blob/master/LICENSE