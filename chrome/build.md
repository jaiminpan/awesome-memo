## 获取和编译chromium

Linux：[chromium.googlesource.com/chromium/sr…](https://link.juejin.cn?target=https%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%2F%2B%2Frefs%2Fheads%2Fmain%2Fdocs%2Flinux%2Fbuild_instructions.md)

Windows：[chromium.googlesource.com/chromium/sr…](https://link.juejin.cn?target=https%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%2F%2B%2Frefs%2Fheads%2Fmain%2Fdocs%2Fwindows_build_instructions.md)

Mac：[chromium.googlesource.com/chromium/sr…](https://link.juejin.cn?target=https%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%2F%2B%2Frefs%2Fheads%2Fmain%2Fdocs%2Fmac_build_instructions.md)

## 重要文档

headless模式：[chromium.googlesource.com/chromium/sr…](https://link.juejin.cn?target=https%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%2F%2B%2Flkgr%2Fheadless)

Vscode配置：[chromium.googlesource.com/chromium/sr…](https://link.juejin.cn?target=https%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%2F%2B%2Frefs%2Fheads%2Fmain%2Fdocs%2Fvscode.md)

源码查看：[source.chromium.org/chromium/ch…](https://link.juejin.cn?target=https%3A%2F%2Fsource.chromium.org%2Fchromium%2Fchromium%2Fsrc)

GN构建参数：[www.chromium.org/developers/…](https://link.juejin.cn?target=https%3A%2F%2Fwww.chromium.org%2Fdevelopers%2Fgn-build-configuration)

## Linux安装依赖

安装上依赖，不安装会有缺库等问题。

```r
yum install git python bzip2 tar pkgconfig atk-devel alsa-lib-devel \
bison binutils brlapi-devel bluez-libs-devel bzip2-devel cairo-devel \
cups-devel dbus-devel dbus-glib-devel expat-devel fontconfig-devel \
freetype-devel gcc-c++ glib2-devel glibc.i686 gperf glib2-devel gtk2-devel \
gtk3-devel java-1.*.0-openjdk-devel libatomic libcap-devel libffi-devel \
libgcc.i686 libgnome-keyring-devel libjpeg-devel libstdc++.i686 libX11-devel \
libXScrnSaver-devel libXtst-devel libxkbcommon-x11-devel ncurses-compat-libs \
nspr-devel nss-devel pam-devel pango-devel pciutils-devel \
pulseaudio-libs-devel zlib.i686 httpd mod_ssl php php-cli python-psutil wdiff \
xorg-x11-server-Xvfb
```

## 设置代理获取chromium代码

git 设置代理：

```lua
git config --global http.proxy http://127.0.0.1:1080
git config --global https.proxy https://127.0.0.1:1080

git config --global --unset http.proxy
git config --global --unset https.proxy 
```

全局代理：

```ini
export http_proxy="http://127.0.0.1:1080"
export https_proxy="https://127.0.0.1:1080"
```

Boto代理设置：

```ini
[Boto文件]
proxy=127.0.0.1
proxy_port = 1080

然后设置：
export NO_AUTH_BOTO_CONFIG=/usr/local/dev/chromium/chromium_src/http_proxy.boto（linux）
set NO_AUTH_BOTO_CONFIG=E:\chromium_src\httpproxy.boto (windows)
```

参考文章： Windows源码下载编译：[blog.berd.moe/archives/ge…](https://link.juejin.cn?target=https%3A%2F%2Fblog.berd.moe%2Farchives%2Fget-code-and-compile-chromium%2F)

代理使用心得：[blog.csdn.net/Vincent95/a…](https://link.juejin.cn?target=https%3A%2F%2Fblog.csdn.net%2FVincent95%2Farticle%2Fdetails%2F79828480)

## Chromium默认编译不支持音视频的播放

为了避免授权和专利的问题，在 Chromium 中是不能直接内置音频以及视频解码器的，所以就造成了默认编译出来的 Chromium 不能播放音视频。

解决方法是，在args.gn文件中增加编译参数

```ini
proprietary_codecs = true
ffmpeg_branding = "Chrome"
```

chromium官方文档中对此说明

```vbnet
GN Flags
There are a few GN flags which can alter the behaviour of Chromium's HTML5 audio/video implementation.

ffmpeg_branding
  Overrides which version of FFmpeg to use
  Default: $(branding)
  Values:
    Chrome - includes additional proprietary codecs (MP3, etc..) for use with Google Chrome
    Chromium - builds default set of codecs

proprietary_codecs
  Alters the list of codecs Chromium claims to support, which affects <source> and canPlayType() behaviour
  Default: 0(gyp)/false(gn)
  Values:
    0/false - <source> and canPlayType() assume the default set of codecs
    1/true - <source> and canPlayType() assume they support additional proprietary codecs
```

## 加速编译

Chromium官方文档中提供了一些可以加速编译的GN编译项。

```ini
symbol_level = 0
blink_symbol_level= 0
enable_nacl = false
```

## 一些重要的编译参数介绍

- is_debug。这个选项值可以为true或者false。当为true时编译debug版本，false时编译release版本。
- is_component_build。这个选项值可以为true或者false。当为true时将chromium代码编译成多个小的dll，false时代码编译成单个dll。一般我们编译debug版本时，设置is_component_build = true，这样每次改动编译链接花费的时间就会减少很多。编译release版本时，设置is_component_build = false，这样就可以把所有代码编译到一个dll里面。
- target_cpu。这个选项值为字符串，控制我们编译出的程序所匹配的cpu。编译32位x86版本设置成target_cpu =”x86″，编译64位x64版本设置成target_cpu =”x64″。如果我们没有显式指定target_cpu的值，那么target_cpu的值为编译它的电脑所用的cpu类型。通常target_cpu的值为x86会比x64编译速度更快，并且支持增量编译。另外如果设置了target_cpu =”x86″，也必须设置enable_nacl = false，否则编译速度会慢很多。
- enable_nacl。这个选项值可以为true或者false。控制是否启用Native Client，通常我们并不需要。所以把其值设置成enable_nacl = false。
- is_clang。这个选项值可以为true或者false。控制是否启用clang进行编译。目前m63 clang编译还不稳定，所以这个选项设置成is_clang = false。m64开始支持clang编译。
- ffmpeg_branding=”Chrome” proprietary_codecs=true。这个两个选项是控制代码编译支持的多媒体格式跟chrome一样，支持mp4等格式。
- symbol_level。其值为整数。当值为0时，不生成调试符号，可以加快代码编译链接速度。当值为1时，生成的调试符号中不包含源代码信息，无法进行源代码级调试，但是可以加快代码编译链接速度。当值为2时，生成完整的调试符号，编译链接时间比较长。
- is_official_build。这个选项值可以为true或者false。控制是否启用official编译模式。official编译模式会进行代码编译优化，非常耗时。仅发布的时候设置成is_official_build = true开启优化。

## GN编译命令

```csharp
# 生成编译目录
gn gen out/Default

# 设置编译目录的编译参数
gn args out/Default

# 查看编译目录的编译参数
gn args --list out/Default


# 启动编译
autoninja -C out/Default chrome
// ninja -C out/Default  区别？

# headless_shell编译
ninja -C out/Default headless_shell
```

## headless_shell编译参数

```ini
##### debug

import("//build/args/headless.gn")
is_component_build = true
is_debug = true
symbol_level = 0
blink_symbol_level= 0
enable_nacl = false
proprietary_codecs = true
ffmpeg_branding = "Chrome"

#### release

import("//build/args/headless.gn")
is_component_build = false
is_debug = false
symbol_level = 0
blink_symbol_level= 0
enable_nacl = false
proprietary_codecs = true
ffmpeg_branding = "Chrome"
```

## Chromium中视频不自动播放

chromuim 66 版本以后的内核，在默认情况下和标签已经不能自动播放了。需要用户点击触发后才播放，或者要把播放设置为静音模式才可自动播放。

解决方法是，启动参数中增加--autoplay-policy=no-user-gesture-required来关闭这个默认策略。

## 启动参数

chrome：

```scss
./out/Default/chrome --headless --no-sandbox --ignore-certificate-errors --ignore-ssl-errors --disable-gpu --disable-software-rasterizer --remote-debugging-port=9222 https://www.baidu.com
```

headless_shell：

```css
./out/Release/headless_shell --no-sandbox --ignore-certificate-errors --ignore-ssl-errors --disable-gpu --disable-software-rasterizer --remote-debugging-address=0.0.0.0 --remote-debugging-port=9222 https://www.baidu.com
```

## headless_shell进程指令

查看headless_shell进程是否存在

```perl
ps -ef | grep headless_shell
```

关闭headless_shell进程

```scss
pkill -f '(chrome)?(--headless)'
```

## VirtualBox虚拟机远程调试

1. 启动参数增加--remote-debugging-address=0.0.0.0 --remote-debugging-port=9222。
2. 关闭虚拟机中操作系统的防火墙，或者开放9222端口。
3. VirtualBox设置端口转发，从子系统9222到主机任意可用端口。
4. 浏览器打开chrome://inspect/#devices开始调试。

## 调试相关

调试地址：chrome://inspect/#devices

一些调试接口：

1. [http://127.0.0.1:9222/json](https://link.juejin.cn?target=http%3A%2F%2F127.0.0.1%3A9222%2Fjson) 查看已经打开的Tab列表
2. [http://127.0.0.1:9222/json/version](https://link.juejin.cn?target=http%3A%2F%2F127.0.0.1%3A9222%2Fjson%2Fversion) : 查看浏览器版本信息
3. [http://127.0.0.1:9222/json/new?http://www.baidu.com](https://link.juejin.cn?target=http%3A%2F%2F127.0.0.1%3A9222%2Fjson%2Fnew%3Fhttp%3A%2F%2Fwww.baidu.com) : 新开Tab打开指定地址
4. [http://127.0.0.1:9222/json/close/8795FFF09B01BD41B1F2931110475A67](https://link.juejin.cn?target=http%3A%2F%2F127.0.0.1%3A9222%2Fjson%2Fclose%2F8795FFF09B01BD41B1F2931110475A67) :关闭指定Tab,close后为tab页面的id
5. [http://127.0.0.1:9222/json/activate/5C7774203404DC082182AF4563CC7256](https://link.juejin.cn?target=http%3A%2F%2F127.0.0.1%3A9222%2Fjson%2Factivate%2F5C7774203404DC082182AF4563CC7256) : 切换到目标Ta

## chromium C++与javascript互操作

- 仿照extensions_v8::LoadTimesExtension

- 在ChromeContentRendererClient的函数RenderThreadStarted()中注册

  thread->RegisterExtension(extensions_v8::XXXXExtension::Get());