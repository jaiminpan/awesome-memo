# GDB on MacOS

In recent versions of macOS and Xcode, Apple's GDB is not provided by default.
It's **recommended to use LLDB** instead.

#### Install GDB
```sh
brew install gdb
```

#### Using a Certificate
+ Launch *Keychain Access* application: Applications > Utilities > Keychain Access.
+ From the Keychains list on the left, right-click on the System item and select *Unlock* Keychain “*System*”.
+ In menu, open Keychain Access > Certificate Assistant > Create a Certificate.
    + Choose a name (e.g. `gdbcert`)
    + Identity type: Self Signed Root
    + Certificate type: Code Signing
    + Check: Let Me Override Defaults
    + Continue with default options until *Specify a Location For*. Set Keychain location to *System*. Then Create.
+ Find the certificate(e.g. `gdbcert`) in System keychain.
    + Double click certificate.
    + Expand Trust, set Code signing to *Always Trust*
+ Restart taskgated in terminal: `sudo killall taskgated` or possibily  `ps aux | grep taskgated` then  `kill -9 <pid>`

+ Enable *root account* by following the steps given below
    + Open System Preferences
    + Go to User & Groups > Unlock
    + Login Options > Join (next to Network Account Server)
    + Click Open Directory Utility
    + In menu Edit > Enable Root User

+ Codesign gdb using your certificate
    + `codesign -fs gdbcert /usr/local/bin/gdb`
    + OR `sudo killall taskgated && codesign -fs gdbcert /usr/local/bin/gdb`
    + Codesign authenticate as root user
+ Shut down your mac and restart in recovery mode (hold down command-R until Apple logo appears)
    + Open terminal window
    + Modify System Integrity Protection to allow debugging: `csrutil enable --without debug`
+ Reboot your Mac. Debugging with gdb should now work as expected.

#### Q&A
Q: Still Error
```
Error message from debugger back end:
Unable to find Mach task port for process-id 39847: (os/kern) failure (0x5).\n (please check gdb is codesigned - see taskgated(8))
Unable to find Mach task port for process-id 39847: (os/kern) failure (0x5).\n (please check gdb is codesigned - see taskgated(8))
```
A:
This is related to codesign entitlements. you must add "com.apple.security.cs.debugger" key in signing process.

for example you must change `codesign -fs gdbcert /usr/local/bin/gdb` to `codesign --entitlements gdb.xml -fs gdbcert /usr/local/bin/gdb`.

`gdb.xml` content must something like following code.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.debugger</key>
    <true/>
</dict>
</plist>
```