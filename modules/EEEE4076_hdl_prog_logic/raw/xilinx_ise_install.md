# Xilinx ISE Installation Manual
> **How to install Xilinx ISE 14.7 on New Linux Distro (Ubuntu 22.04 LTS Example)**
https://gist.github.com/aliemo/ce58ea570ee6ffa6dedfa569f87f1c1e

![Xilinx ISE on UBUNTU 2022.4](https://githubraw.com/alimpk/raw/main/images/XilinxISEInstallUbuntu.png)

## Preinstallation Requarements
Install Essential Libraries (curses5 stdc++5 motif-dev fonts-75dpi fonts-100dpi)
```bash
sudo apt install \
    libncurses5 \
    libstdc++5 \
    libmotif-dev \
    xfonts-75dpi \
    xfonts-100dpi
```
## Download Installation file from Xilinx Design Tools Archive

1. Download **Full Installer for Linux** file from xilinx site. [Xilinx_ISE_DS_Lin_14.7_1015_1.tar](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vivado-design-tools/archive-ise.html)
2. Extract installation file:
```bash
tar -xvf Xilinx_ISE_DS_Lin_14.7_1015_1.tar
```
3. goto directory and run installation file:
```bash
cd Xilinx_ISE_DS_Lin_14.7_1015_1
./xsetup
```
4. Choose installation directory and install ISE

**Note:** Installation is not works with Noto font series in KDE or Gnome. Before running `./xsetup` it is required to change font family to Ubuntu series. issue error is : `.xsetup: line 21:  6514 Segmentation fault ...` 

## Create Gui Luncher
See my other gist [https://gist.github.com/aliemo/27d7c04a9e000e138a12320519fc749a](https://gist.github.com/aliemo/27d7c04a9e000e138a12320519fc749a)

## Post-installation fixes

After installation, a few manual fixes are required to work around problems caused by running the Xilinx tools on a Linux distribution that is not officially supported by Xilinx.

**1. Dynamic library fix (libstdc++.so)**

The ISE tools supply an outdated version of the libstdc++.so library, which may cause segfaults when using the Xilinx Microprocessor Debugger and prevents the usage of the oxygen-gtk theme. This outdated version is located in two directories within the installation tree:  `<installation-path>/ISE_DS/ISE/lib/lin64/ and <installation-path>/ISE_DS/common/lib/lin64`

To use newer version of libstdc++, rename or delete the original files and replace them with symlinks:
```bash
cd <installation-path->ISE_DS/ISE/lib/lin64/
mv libstdc++.so libstdc++.so.orig
mv libstdc++.so.6 libstdc++.so.6.orig
mv libstdc++.so.6.0.8 libstdc++.so.6.0.8.orig
ln -s /usr/lib/libstdc++.so
ln -s libstdc++.so libstdc++.so.6
ln -s libstdc++.so libstdc++.so.6.0.8
```
Next, repeat this process in the `<installation-path>/ISE_DS/common/lib/lin64`

**2. Locale issues**
PlanAhead does not like locales using other literals than '.' as the decimal point (e.g. German, which uses ','). Run the following command before launching PlanAhead:

```unset LANG```

**3. Running Xilinx tools from within KDE**
KDE by default defines the `QT_PLUGIN_PATH` shell variable. Some of the Xilinx ISE tools (ISE, Impact, XPS) are Qt applications, which means that they will search for Qt plugins in the locations defined by this shell variable.

Because the Xilinx tools are compiled against and ship with an older version of the Qt framework which cannot use these plugins, they will crash when launched with this environment variable present.

To fix this issue, run the following command before launching the tools:

```unset QT_PLUGIN_PATH```

**4. Segmentation fault on PlanAhead**
When launching PlanAhead to generate a .ucf file, a segmentation fault may occur. The issue seems unrelated to the previous topic. The ISE console will show:

`<installation-path->/ISE_DS/PlanAhead/bin/rdiArgs.sh: line 64: 14275 Segmentation fault      $RDI_PROG $*`

The problem seems to come from the bundled JRE as described here. To fix the issue, symlink the OpenJDK libjvm.so into the ISE  installation directory.

```bash
sudo apt install jre8-openjdk-headless
cd <installation-path>/14.7/ISE_DS/PlanAhead/tps/lnx64/jre/lib/amd64/server
mv libjvm.so{,-orig}
ln -s /usr/lib/jvm/java-8-openjdk/jre/lib/amd64/server/libjvm.so
```
**Remember!:** newer version of jre such as jre-openjdk-headless (version 17) is not suitable (can lead to error)

**5. GNU make**
XSDK looks for the gmake executable, which is not present in Arch Linux by default. Create a symlink somewhere in your path, e.g.

```ln -s /usr/bin/make /home/<user>/bin/gmake```

**Note:** Make sure this directory (`~/bin`) is in your PATH variable.


    