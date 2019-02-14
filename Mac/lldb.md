# lldb

Since Xcode itself now uses LLDB instead of GDB, this can be a more convenient alternative for Mac users. It integrated much easier in Eclipse than GDB.

## lldb on Eclipse CDT
CDT has experimental support for LLDB starting from CDT 9.1. The minimum recommended version for LLDB is 3.8.

#### How do I install the LLDB debugger integration?

+ Go to Help > Install new Software
+ Select the CDT update site (9.1 or greater)
+ Under CDT Optional Features, select C/C++ LLDB Debugger Integration

#### How do I debug with LLDB?
Only local debug (new process) and local attach are supported right now.
First, create a debug configuration just like you would when debugging with GDB. Then you need to set the launcher to **LLDB-MI Debug Process Launcher**.

## Reference
https://wiki.eclipse.org/CDT/User/FAQ#How_do_I_get_the_LLDB_debugger.3F