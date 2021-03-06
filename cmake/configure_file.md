# configure_file
[Offical Page](https://cmake.org/cmake/help/latest/command/configure_file.html)

Copy a file to another location and modify its contents.
```
configure_file(<input> <output>
               [COPYONLY] [ESCAPE_QUOTES] [@ONLY]
               [NEWLINE_STYLE [UNIX|DOS|WIN32|LF|CRLF] ])
```
Copies an <input> file to an <output> file and substitutes variable values referenced as @VAR@ or ${VAR} in the input file content. Each variable reference will be replaced with the current value of the variable, or the empty string if the variable is not defined. Furthermore, input lines of the form:
```
#cmakedefine VAR ...
```
will be replaced with either:
```
#define VAR ...
```
or:
```
/* #undef VAR */
```
depending on whether VAR is set in CMake to any value not considered a false constant by the if() command.
The ”...” content on the line after the variable name, if any, is processed as above.
Input file lines of the form `#cmakedefine VAR` will be replaced with either `#define VAR 1` or `#define VAR 0` similarly.

If the input file is modified the build system will re-run CMake to re-configure the file and generate the build system again.

The arguments are:

#### <input>
Path to the input file. A relative path is treated with respect to the value of CMAKE_CURRENT_SOURCE_DIR. The input path must be a file, not a directory.
#### <output>
Path to the output file or directory. A relative path is treated with respect to the value of CMAKE_CURRENT_BINARY_DIR. If the path names an existing directory the output file is placed in that directory with the same file name as the input file.
#### COPYONLY
Copy the file without replacing any variable references or other content. This option may not be used with NEWLINE_STYLE.
#### ESCAPE_QUOTES
Escape any substituted quotes with backslashes (C-style).
#### @ONLY
Restrict variable replacement to references of the form `@VAR@`. This is useful for configuring scripts that use `${VAR}` syntax.
#### NEWLINE_STYLE <style>
Specify the newline style for the output file.
Specify `UNIX` or `LF` for `\n` newlines, or specify `DOS`, `WIN32`, or `CRLF` for `\r\n` newlines.
This option may not be used with `COPYONLY`.

# Example
Consider a source tree containing a `foo.h.in` file:
```
#cmakedefine FOO_ENABLE
#cmakedefine FOO_STRING "@FOO_STRING@"
```
An adjacent `CMakeLists.txt` may use `configure_file` to configure the header:
```
option(FOO_ENABLE "Enable Foo" ON)
if(FOO_ENABLE)
  set(FOO_STRING "foo")
endif()
configure_file(foo.h.in foo.h @ONLY)
```
This creates a `foo.h` in the build directory corresponding to this source directory.
If the `FOO_ENABLE` option is on, the configured file will contain:
```
#define FOO_ENABLE
#define FOO_STRING "foo"
```
Otherwise it will contain:
```
/* #undef FOO_ENABLE */
/* #undef FOO_STRING */
```
One may then use the `include_directories()` command to specify the output directory as an include directory:
```
include_directories(${CMAKE_CURRENT_BINARY_DIR})
```
so that sources may include the header as `#include <foo.h>`.
