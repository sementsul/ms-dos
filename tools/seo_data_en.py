# -*- coding: utf-8 -*-
"""English guide pages for ms-dos.su/en: eight articles, one list named ARTICLES.

Each item follows the data contract used by the site generator:
slug, cat, h1, title, desc, lead, sections, faq, howto.

Facts about MBFUTool 2.0 (four operations, .mbfu container, limits, trial)
follow the published English pages of the site. No MS-DOS files are shipped
with the program, so every article points at the licensing page.
"""


ARTICLES = [
    # ------------------------------------------------------------------ 1
    {
        "slug": "how-to-create-bootable-ms-dos-usb",
        "cat": "Guides",
        "h1": "How to create a bootable MS-DOS USB drive",
        "title": "How to create a bootable MS-DOS USB drive | ms-dos.su",
        "desc": (
            "How to write your own lawful MS-DOS image to a USB stick on Windows: "
            "what you need, how to write it, and how to prove that it boots."
        ),
        "lead": (
            "A bootable MS-DOS stick is a FAT16 partition with the system files in the "
            "right place. Here is the whole path: the hardware, a lawful image, writing it "
            "on Windows, and checking that it boots."
        ),
        "sections": [
            ("What you need", """<ul>
<li>A USB stick of up to 4 GB, or a larger stick with a FAT16 first partition; the <a href="/en/fat16-limits-and-4gb-usb-drives.html">FAT16 limits page</a> explains why.</li>
<li>Your own lawful MS-DOS image: floppies you imaged yourself, a subscription copy, or media you own.</li>
<li>A Windows x64 computer, administrator rights and a USB port the firmware will boot from. Formatting and boot-sector writes both need elevation.</li>
</ul>
<p>Writing erases the whole stick. Copy anything you need elsewhere and unplug USB disks you want to keep: the tool lists physical devices, not drive letters.</p>"""),
            ("Where to get MS-DOS lawfully", """<p>MBFUTool ships no MS-DOS files: support ended in 2001, there is no official free download, and the system files are Microsoft's. You supply an image you may lawfully use:</p>
<ul>
<li>the subscriber catalogue at my.visualstudio.com, for some subscription levels;</li>
<li>floppies or a boxed copy you own;</li>
<li>a machine that still runs MS-DOS, whose disk you image before the hardware dies.</li>
</ul>
<p>"MS-DOS 6.22 ISO" files from file-sharing sites are counterfeit whatever you paid for the tool. The rules are on the <a href="/en/ms-dos-license.html">licensing page</a>.</p>"""),
            
            ("Write the image", """<ol>
<li>Start MBFUTool as administrator; without elevation the write is refused.</li>
<li>Choose <b>Write MS-DOS image to USB flash</b>.</li>
<li>Select the image: .img, .ima or .mbfu. Paths with Cyrillic characters must be moved to a Latin-only folder first.</li>
<li>Select the target from the list of physical disks and check its size and model twice.</li>
<li>Confirm. The stick is partitioned as FAT16, the boot sector is written, the system files are copied.</li>
</ol>
<p>The program refuses to write to the system disk; that guard protects the machine, not the stick.</p>"""),
            ("Verify the boot", """<ol>
<li>Reboot and open the one-time boot menu: F12, F11, F8 or Esc.</li>
<li>Pick the USB entry without a "UEFI:" prefix. If only UEFI entries exist, see <a href="/en/secure-boot-and-csm-for-dos.html">Secure Boot and CSM</a>.</li>
<li>Expect a DOS prompt or the image's menu within seconds.</li>
<li>Run <code>dir</code> and <code>ver</code>; write a small file to check the volume is writable.</li>
</ol>"""),
            ("If it does not boot: symptom and what to check", """<p>Find the symptom, then work through the causes in the order given.</p>
<table>
<tr><th>Symptom</th><th>What to check</th></tr>
<tr><td>Black screen, the PC moves on to the next device</td><td>UEFI-only mode: enable CSM or Legacy boot and disable Secure Boot.</td></tr>
<tr><td><code>Non-System disk or disk error</code></td><td>No <code>IO.SYS</code>/<code>MSDOS.SYS</code> on the volume, or the firmware booted another device. Rewrite, then check the boot order.</td></tr>
<tr><td><code>Invalid media type</code></td><td>The active partition is NTFS or exFAT, or its boot sector is damaged. Recreate it as FAT16.</td></tr>
<tr><td><code>Missing operating system</code></td><td>No active partition: the partition table is wrong or was overwritten.</td></tr>
<tr><td>The stick is missing from the boot menu</td><td>USB boot disabled, Fast Boot on, or a port that cannot boot. Try a rear USB 2.0 port.</td></tr>
<tr><td><code>Cannot exceed 4GB for FAT16</code></td><td>The stick is larger than 4 GB. Use a smaller one or a 2 GB FAT16 first partition.</td></tr>

</table>
<p>The <a href="/en/ms-dos-boot-errors-explained.html">error guide</a> covers each message in more detail.</p>"""),
            ("What the tool does, and what it does not", """<p>MBFUTool 2.0 is a Windows x64 program with four operations: <b>Write MS-DOS image to USB flash</b>, <b>Create MBFU image from disk/floppy/USB</b>, <b>Clone MS-DOS disk/floppy/USB to USB</b>, and <b>Edit MS-DOS image with DOS commands</b>, which runs in the bundled DOSBox 0.72 with a BEN menu. The .mbfu container holds a header, zlib-compressed data and a SHA-256 digest of the raw image.</p>
<p>It does not ship, download or install MS-DOS. Images are FAT16, so a partition stops at 4 GB and 2 GB in practice; DOSBox cannot mount one above 4 GB; paths must be Latin-only. The trial runs 30 days, offline and without a key: <a href="https://ms-dos.su/#trial">trial details</a>.</p>"""),
            ("Where to go next", """<ul>
<li><a href="/en/bios-update-from-dos-usb.html">Updating the BIOS from a DOS USB drive</a></li>
<li><a href="/en/ms-dos-in-virtualbox-or-dosbox.html">DOSBox or a virtual machine</a></li>
<li><a href="/en/hard-disk-diagnostics-from-dos.html">Testing hard drives and memory from DOS</a></li>
<li><a href="/en/best-ms-dos-usb-tools.html">Tools for writing MS-DOS images to USB</a></li>
<li><a href="/en/dos-test.html">MS-DOS in the browser</a></li>
</ul>"""),
        ],
        "faq": [
            ("Do I need FreeDOS for this?",
             "No. FreeDOS is a separate operating system with its own files. It is quicker for a DOS-like command line, but it is not MS-DOS."),
            ("Does MBFUTool include MS-DOS?",
             "No. It writes, captures, clones and edits images. The system files come from your own lawful copy."),
            ("Will the stick boot on a UEFI-only laptop?",
             "No. Without CSM the firmware only runs EFI programs, and MS-DOS has no EFI version."),
        ],
        "howto": [
            ("Back up the stick", "Copy anything you need off the drive; writing replaces the partition table."),
            ("Get a lawful image", "Use your own floppy or disk image, or a copy from a Visual Studio subscription."),
            ("Run as administrator", "Choose Write MS-DOS image to USB flash as administrator, pick the image and the physical device, confirm."),
            ("Boot from the stick", "Open the boot menu, choose the entry without the UEFI prefix, check that DOS starts."),
        ],
    },

    # ------------------------------------------------------------------ 2
    {
        "slug": "ms-dos-in-virtualbox-or-dosbox",
        "cat": "Guides",
        "h1": "Running MS-DOS in DOSBox or a virtual machine",
        "title": "Running MS-DOS in DOSBox or a virtual machine | ms-dos.su",
        "desc": (
            "When DOSBox or a virtual machine is enough for MS-DOS work, when only "
            "real hardware will do, and how to edit images without a physical PC."
        ),
        "lead": (
            "Emulation covers most day-to-day DOS work and costs nothing to set up. It stops "
            "being enough the moment the task depends on firmware, a real bus or a port."
        ),
        "sections": [
            ("What emulation is good for", """<p>A DOS emulator executes the same interrupts and file-system code as the real thing, so anything that touches only DOS and its own files behaves the same:</p>
<ul>
<li>editing <code>config.sys</code> and <code>autoexec.bat</code> and seeing the effect at once;</li>
<li>learning <code>dir</code>, <code>copy</code>, <code>fdisk</code> and <code>format</code> without risking a real disk;</li>
<li>running old business software, games and QBASIC programs;</li>
<li>checking an image before it goes onto a stick, and copying files into or out of it.</li>
</ul>"""),
            ("DOSBox: the fastest route", """<p>DOSBox installs nothing, needs no driver and starts in a second: mount a folder as <code>C:</code>, mount a floppy image as <code>A:</code>, run the program. A bad setting costs a restart rather than a reinstall.</p>
<p>MBFUTool ships DOSBox 0.72 with a BEN menu and uses it for <b>Edit MS-DOS image with DOS commands</b>: the image is mounted as <code>A:</code> or <code>C:</code>, and <code>copy</code>, <code>del</code>, <code>md</code>, <code>rd</code> and <code>edit</code> work as usual. That build cannot mount an image larger than 4 GB, and paths must be Latin-only.</p>
<p>The emulation is not cycle-accurate: demos that count cycles and software that programs a sound card directly may behave differently. Adjust <code>cycles</code> to change the speed.</p>"""),
            ("When a virtual machine is better", """<p>VirtualBox, VMware, QEMU and the period emulators 86Box and PCem boot a disk image for real: partition table, boot sector, everything. That makes them the place to test whether an image is bootable and to experiment with <code>fdisk</code> before touching hardware. Snapshots undo a mistake in one click.</p>
<ul>
<li>VirtualBox and VMware need their own disk format; convert a raw image with <code>VBoxManage convertfromraw</code> or <code>qemu-img convert</code>.</li>
<li>Floppy images usually attach as they are.</li>
<li>86Box and PCem emulate period chipsets and ISA cards, which matters for software that programs hardware directly.</li>
</ul>"""),
            ("When only real hardware will do", """<p>Some jobs never leave the physical machine:</p>
<ul>
<li><b>Firmware updates.</b> A flasher writes to the SPI flash chip through the chipset; an emulator has no chipset to write to.</li>
<li><b>Industrial machines.</b> ISA cards, serial dongles and software that polls custom I/O ports have no trustworthy emulation.</li>
<li><b>The boot path.</b> Secure Boot, CSM, USB enumeration and the stick's controller are invisible to DOSBox.</li>
<li><b>Drive diagnostics.</b> MHDD talks to the storage controller directly; a virtual machine sees a virtual disk.</li>
</ul>"""),
            ("What emulation hides", """<p>A test that passes in DOSBox proves the files are right; it says nothing about whether your PC will start from the stick. Treat emulation as a check of the image and the real machine as the check of the boot.</p>"""),
            ("A practical order of work", """<ol>
<li>Build or edit the image in DOSBox.</li>
<li>Check the boot in a virtual machine.</li>
<li>Write it to the stick with <a href="/en/how-to-create-bootable-ms-dos-usb.html">the USB guide</a>.</li>
<li>Test on the real machine, keeping the emulator open for quick fixes.</li>
</ol>"""),
            ("Where MBFUTool fits", """<p>MBFUTool 2.0 is a Windows x64 utility with four operations: write an image to USB, create a .mbfu image from a disk, floppy or USB stick, clone MS-DOS media to a USB stick, and edit an image with DOS commands. Editing is where the bundled DOSBox 0.72 earns its place; the .mbfu container stores a header, a zlib-compressed payload and a SHA-256 digest of the raw image.</p>
<p>The program ships no MS-DOS files - the image is yours, as the <a href="/en/ms-dos-license.html">licensing page</a> explains. For a first look at the command line there is <a href="/en/dos-test.html">MS-DOS in the browser</a>.</p>"""),
        ],
        "faq": [
            ("Can DOSBox replace a real PC for a BIOS update?",
             "No. The flasher needs the actual chipset and flash chip; under DOSBox nothing reaches hardware."),
            ("Why does DOSBox refuse a 6 GB image?",
             "DOSBox 0.72 cannot mount images larger than 4 GB. A bigger file is almost always FAT32 or exFAT, which MS-DOS cannot read."),
            ("Is a virtual machine enough to test a bootable stick?",
             "It can boot the image file, which proves the image is bootable. It cannot tell you whether your firmware will accept that stick."),
            ("Does DOSBox run on Windows only?",
             "DOSBox runs on Windows, Linux and macOS. MBFUTool itself is a Windows x64 program."),
        ],
        "howto": [
            ("Install DOSBox or create a VM", "DOSBox needs no installation: unpack and run it. For a VM, create a machine and attach the image."),
            ("Mount the media", "Use mount for a folder and imgmount for a floppy image; in a VM convert the raw image first."),
            ("Work on the image", "Edit config.sys and autoexec.bat, copy files in, run the programs you need."),
            ("Test the boot in a VM", "Attach the image to a virtual machine and check that it reaches a DOS prompt."),
            ("Write to physical media", "Once the image is correct, write it to USB and test on the real hardware."),
        ],
    },

    # ------------------------------------------------------------------ 3
    {
        "slug": "bios-update-from-dos-usb",
        "cat": "BIOS",
        "h1": "Updating the BIOS from a DOS USB drive",
        "title": "Updating the BIOS from a DOS USB drive | ms-dos.su",
        "desc": (
            "How to update a motherboard BIOS from a DOS USB drive: identify the board, "
            "get the vendor flasher, boot in Legacy mode, run it, verify the version."
        ),
        "lead": (
            "This is the one job on this site that can leave a machine unusable if it goes "
            "wrong. The procedure is short; the preparation is what makes it safe."
        ),
        "sections": [
            ("Before you start", """<p>A BIOS update rewrites the firmware that starts the board. If the write is interrupted the board may not POST, and recovery depends on what the vendor built in: a Flashback port, a second BIOS chip, a socketed chip.</p>
<p>Update for a reason - a CPU the board does not recognise yet, a fixed bug, a security advisory. If the vendor offers a Windows utility for your board, use it: the DOS route is for boards where only a DOS flasher is published, or where Windows will not start.</p>"""),
            ("Identify the board and the current version", """<ul>
<li>Read the exact model and revision from the board or its box; vendors ship different firmware for revisions that share a name.</li>
<li><code>msinfo32</code> shows <b>BaseBoard Product</b>, <b>BaseBoard Version</b> and <b>BIOS Version/Date</b>.</li>
<li>Compare them with the vendor's support page and read the release notes.</li>
<li>Write the current version down; it is how you confirm afterwards that the flash worked.</li>
</ul>"""),
            ("Download and verify the package", """<p>Take the file only from the vendor's support page for your model. A DOS package is usually a ZIP with the flasher, the firmware file (.rom or .bin), sometimes a batch file and a readme.</p>
<ul>
<li>Compare the published checksum with the download - <code>Get-FileHash -Algorithm SHA256</code> in PowerShell.</li>
<li>Unpack the archive; do not flash from inside it.</li>
<li>Read the readme: some vendors require a cleared CMOS or a particular utility version.</li>
</ul>"""),
            ("Prepare the DOS USB drive", """<p>Use a stick of 4 GB or less, or a larger one with a FAT16 first partition. Write your MS-DOS image with MBFUTool as administrator, choose <b>Write MS-DOS image to USB flash</b>, select the image and the device, and confirm. Everything on the stick is erased; the steps are in <a href="/en/how-to-create-bootable-ms-dos-usb.html">the USB guide</a>.</p>"""),
            ("Copy the vendor files onto the stick", """<ul>
<li>Copy the flasher and the firmware file to the root of the stick.</li>
<li>Keep the vendor's file names; renaming a .rom file can make the flasher reject it.</li>
</ul>"""),
            ("Boot in Legacy/CSM mode", """<p>The DOS flasher is a real-mode program: the firmware must be in Legacy or CSM mode, Secure Boot must be off, and you must pick the USB entry without a "UEFI:" prefix. On many boards the stick appears twice, and the UEFI entry leads to a black screen. <a href="/en/secure-boot-and-csm-for-dos.html">Secure Boot and CSM</a> covers the settings per vendor.</p>"""),
            ("Run the flasher", """<ol>
<li>At the DOS prompt, find the stick's letter with <code>dir</code>; it is often not <code>C:</code>.</li>
<li>Run the vendor's executable or batch file.</li>
<li>Confirm the board model and the version before pressing the key that starts the write.</li>
<li>Do not touch the keyboard or the power button while erase and write blocks are on screen; a blank display is normal.</li>
<li>Wait for the completion message or the automatic reboot. Do not reset the machine yourself.</li>
</ol>"""),
            ("After the reboot", """<ul>
<li>Load the defaults if the vendor asks, then set the date, SATA mode and boot order.</li>
<li>Re-enable Secure Boot and the TPM if Windows 11 needs them.</li>
<li>Verify the new version on the POST screen and in setup.</li>
<li>With BitLocker on, expect a recovery-key prompt; have the key ready.</li>
</ul>"""),
            ("Safety rules", """<ul>
<li>Use a UPS, or a charged battery on a laptop: a power cut during the write is the failure that matters.</li>
<li>Verify the checksum and never flash a file from a forum or from another model's page.</li>
<li>Do not run a DOS flasher from Windows or from DOSBox.</li>
<li>If the board does not POST, stop power-cycling it and look up the vendor's recovery procedure.</li>
</ul>"""),
        ],
        "faq": [
            ("Can I flash the BIOS from a DOSBox window?",
             "No. DOSBox emulates a machine, so the flasher writes nothing to the real chip; it must run on the actual board."),
            ("What happens if the power fails during the flash?",
             "The board may not start. Recovery depends on a Flashback port, a backup BIOS chip or service reprogramming."),
            ("Will the update erase my BIOS settings?",
             "Usually yes; most updates load defaults. Note the SATA mode, boot order and overclocking settings first."),
            ("Do I need the newest version or the one for my revision?",
             "The one for your exact model and revision; newer is not always compatible with older revisions."),
        ],
        "howto": [
            ("Identify the board", "Read the model and revision from the board or box, and note the current BIOS version."),
            ("Download the package", "Get the flasher and firmware from the vendor page for that model, then compare the checksum."),
            ("Write the DOS stick", "Use a stick of 4 GB or less and write your own MS-DOS image as administrator."),
            ("Copy the files", "Put the flasher and the firmware file in the root of the stick under their original names."),
            ("Boot in Legacy mode", "Disable Secure Boot, enable CSM, choose the USB entry without the UEFI prefix."),
            ("Run the flasher and wait", "Confirm the model and version, then leave the machine alone until it reboots."),
        ],
    },

    # ------------------------------------------------------------------ 4
    {
        "slug": "secure-boot-and-csm-for-dos",
        "cat": "BIOS",
        "h1": "Secure Boot, UEFI and CSM: booting DOS on modern hardware",
        "title": "Secure Boot, UEFI and CSM for booting DOS | ms-dos.su",
        "desc": (
            "Why a modern PC refuses to boot MS-DOS from USB: Secure Boot, UEFI, CSM and "
            "Legacy mode, vendor differences, and what to change in the firmware setup."
        ),
        "lead": (
            "A modern PC boots DOS only when three independent conditions are met. Fixing one "
            "and expecting the other two to follow is why this takes an evening."
        ),
        "sections": [
            ("Three requirements, not one", """<p>A machine boots MS-DOS when the firmware can run legacy boot code, Secure Boot is not blocking it, and the stick carries a BIOS boot sector with an active FAT16 partition. These are separate switches in separate menus, and each failure looks different.</p>"""),
            ("What UEFI expects", """<p>UEFI firmware looks for an EFI System Partition - a FAT32 partition with a bootloader in <code>EFI/BOOT/BOOTX64.EFI</code> - and runs that program. An MS-DOS stick has none of this: it starts with a 512-byte master boot record, which the firmware executes in 16-bit mode and which chains to the partition boot sector and then to <code>IO.SYS</code>.</p>
<p>A UEFI-only machine has nothing to run, so it skips the stick or lists it without a bootable image. The old BIOS path survives on most desktops as CSM, the Compatibility Support Module, which provides the interrupt services DOS expects.</p>"""),
            ("What Secure Boot checks", """<p>Secure Boot verifies the signature of the next program in the boot chain against the keys stored in the firmware. DOS boot code is unsigned, so with Secure Boot on the firmware refuses it. Disabling the check does not enable legacy boot by itself.</p>
<p>Two notes. Some boards require Secure Boot off before CSM appears, so change them in that order. And Windows 11 requires Secure Boot, so put it back afterwards.</p>"""),
            ("CSM, Legacy, or Boot Mode", """<p>Vendors name the same switch differently: <b>CSM Support</b>, <b>Launch CSM</b>, <b>Legacy Boot</b>, <b>Boot Mode: Legacy</b>, <b>UEFI/Legacy Boot: Both</b>. All of them mean "let the firmware run BIOS boot code". Some boards offer <b>Other OS</b> instead of a Secure Boot toggle, which switches off the signature check.</p>
<p>Not every machine has the option: most laptops sold after roughly 2020, and several desktop chipsets, ship without CSM. Without it DOS cannot boot; the alternatives are another PC or a virtual machine.</p>"""),
            ("Vendors differ", """<p>Entry keys are consistent enough: Del or F2 on ASUS and MSI, Del on Gigabyte, F1 or F2 on Lenovo, F2 on Dell, Esc then F10 on HP. The rest is vendor-specific:</p>
<ul>
<li><b>ASUS</b> keeps it under Security or Boot as OS Type, where Other OS means unsigned; some boards hide it until an administrator password is set.</li>
<li><b>MSI</b> puts it under Settings - Security, next to a Boot Mode selector.</li>
<li><b>Gigabyte</b> often needs CSM Support enabled before Secure Boot can be changed.</li>
<li><b>Lenovo</b> uses Secure Boot plus a separate UEFI/Legacy Boot setting; BitLocker may ask for its recovery key afterwards.</li>
<li><b>Dell</b> has Secure Boot Enable and a Legacy boot option list, with a confirmation on exit.</li>
<li><b>HP</b> asks for a four-digit code when you disable Secure Boot.</li>
</ul>
<p>Wording changes between versions, so follow the labels, not a memorised path.</p>"""),
            ("The stick must be written for MBR/BIOS boot", """<p>A stick prepared for UEFI - GPT partition table, FAT32, an EFI bootloader - is invisible to CSM. MS-DOS needs the opposite: an MBR partition table, one active FAT16 partition and a DOS boot sector. That is what MBFUTool writes, and what <a href="/en/how-to-create-bootable-ms-dos-usb.html">the USB guide</a> describes. If a tool offers the choice, pick MBR/BIOS rather than GPT/UEFI.</p>"""),
            ("What to check in the boot menu", """<ul>
<li>Open the one-time boot menu (F12, F11, F8 or Esc) rather than changing the permanent order.</li>
<li>If the stick is listed twice, choose the entry without a <b>UEFI:</b> prefix.</li>
<li>No entry at all: enable USB boot, disable Fast Boot, and try a rear USB 2.0 port.</li>
<li>Still nothing: recheck CSM and Secure Boot, then try the stick on another machine.</li>
</ul>"""),
        ],
        "faq": [
            ("Can Windows 11 still boot with Secure Boot disabled?",
             "An installed system usually starts, although Windows 11 requires Secure Boot as an installation requirement. Re-enable it afterwards."),
            ("My laptop has no CSM option. Is there a workaround?",
             "Not for DOS. Without CSM the firmware only runs EFI programs, and MS-DOS has no EFI version."),
            ("Does a UEFI shell let me run DOS programs?",
             "No. It runs EFI applications; it cannot execute real-mode DOS code or load IO.SYS."),
            ("Why does the same stick boot on an old PC but not a new one?",
             "The old PC has a BIOS with CSM; the new one is UEFI-only or has Secure Boot on. The stick is fine."),
        ],
        "howto": [
            ("Open the firmware setup", "Press the vendor key: Del or F2 on most desktops, F2 on Dell, F1 or F2 on Lenovo, Esc then F10 on HP."),
            ("Disable Secure Boot", "Find Secure Boot under Security or Boot and set it to Disabled; on ASUS, OS Type: Other OS does the same."),
            ("Enable CSM or Legacy boot", "Turn on CSM Support, Launch CSM or Boot Mode: Legacy, depending on the label."),
            ("Select the stick", "Open the one-time boot menu and choose the USB entry without the UEFI prefix."),
            ("Restore the settings", "Re-enable Secure Boot and the TPM for Windows 11 once the DOS work is finished."),
        ],
    },

    # ------------------------------------------------------------------ 5
    {
        "slug": "fat16-limits-and-4gb-usb-drives",
        "cat": "Guides",
        "h1": "FAT16 limits: why a DOS USB drive stops at 2-4 GB",
        "title": "FAT16 limits: why a DOS USB drive stops at 2-4 GB | ms-dos.su",
        "desc": (
            "FAT16 limits explained: the 4 GB ceiling, the practical 2 GB figure for "
            "MS-DOS, cluster sizes, and how to use a larger USB stick anyway."
        ),
        "lead": (
            "The size limit is not a bug in the tool or in your stick. It comes from the number "
            "of clusters FAT16 can address and the largest cluster MS-DOS accepts."
        ),
        "sections": [
            ("One number: about 65,500 clusters", """<p>FAT16 stores the location of every cluster in a 16-bit field, so a volume cannot hold more than 65,524 clusters; a few values are reserved. The volume size is cluster size multiplied by that count: bigger clusters buy a bigger volume, at the cost of wasted space in every file.</p>"""),
            ("Cluster size sets the ceiling", """<ul>
<li>512 bytes per cluster - up to 32 MB;</li>
<li>2 KB - up to 128 MB;</li>
<li>4 KB - up to 256 MB;</li>
<li>8 KB - up to 512 MB;</li>
<li>16 KB - up to 1 GB;</li>
<li>32 KB - up to 2 GB, the largest cluster MS-DOS accepts;</li>
<li>64 KB - up to 4 GB, for systems that accept 64 KB clusters, which MS-DOS does not.</li>
</ul>
<p>Every file also wastes on average half a cluster: with 32 KB clusters, a thousand small files can burn tens of megabytes.</p>"""),
            ("Where the 4 GB figure comes from", """<p>Formatting tools and the Windows format dialog will create a FAT16 volume of up to 4 GB using 64 KB clusters. A DOS stick made that way can be written, mounted and checked on a modern system, and then fail on the machine it was made for, because MS-DOS cannot read 64 KB clusters.</p>
<p>That is why the documented limit is "up to 4 GB, 2 GB in practice": two gigabytes is what a DOS-compatible layout with 32 KB clusters gives you.</p>"""),
            ("What happens above that", """<p>Ask for a 16 GB FAT16 volume and one of three things happens: the tool refuses with a message such as <b>Cannot exceed 4GB for FAT16</b>, it silently formats FAT32 or exFAT, or it produces a volume DOS cannot read. The first is the honest outcome; the other two look like success until the stick is in the target machine.</p>
<p>FAT32 is no way out for MS-DOS 6.22, which cannot read it at all. Only the DOS 7.x line shipped with Windows 95 OSR2 and 98 understands FAT32.</p>"""),
            ("Using a larger stick", """<ol>
<li>Create a primary FAT16 partition of 2 GB (4 GB at most) at the start of the stick.</li>
<li>Mark it active; DOS boots from the active primary partition only.</li>
<li>Leave the rest unallocated, or use it for a second partition DOS will never see.</li>
<li>Format it as FAT16 and copy the system files, or let MBFUTool write your image to the stick.</li>
</ol>
<p>DOS addresses the first physical disk and its first partition, so extra capacity is invisible. The write itself is described in <a href="/en/how-to-create-bootable-ms-dos-usb.html">the USB guide</a>.</p>"""),
            ("Why DOSBox 0.72 stops at 4 GB", """<p>The DOSBox build that ships with MBFUTool, version 0.72, cannot mount an image larger than 4 GB. An image past that size is usually FAT32 or a raw dump of a larger disk, and the mount code does not handle it. MBFUTool's .mbfu captures of DOS media stay inside the limit, and the program reports the problem instead of producing a broken image.</p>"""),
            ("Practical checklist", """<ul>
<li>2 GB stick: the safest choice for MS-DOS 6.22.</li>
<li>4 GB stick: works with 32 KB clusters; verify that DOS reads it.</li>
<li>8 GB and larger: first partition 2 GB, active, FAT16.</li>
<li>File names: 8.3, Latin characters, shallow folder trees.</li>
<li>Volume label: Latin characters, no spaces.</li>
</ul>"""),
        ],
        "faq": [
            ("Can FAT16 hold a file larger than 2 GB?",
             "No. The file size field is 32 bits, which caps a single file at 2 GB, and the volume cap arrives first."),
            ("Does MS-DOS 6.22 read FAT32?",
             "No. FAT32 support arrived with the DOS 7.x line in Windows 95 OSR2 and Windows 98."),
            ("Is exFAT an option for a DOS stick?",
             "No. MS-DOS has no exFAT driver and cannot read the volume at all."),
            ("Why does Windows show my 16 GB stick as 2 GB?",
             "Only the first FAT16 partition is formatted; the rest is unallocated. That is the intended layout."),
        ],
        "howto": [
            ("Check the stick size", "Anything above 4 GB cannot be one FAT16 volume; decide between a smaller stick and a small first partition."),
            ("Create the first partition", "Make a primary FAT16 partition of 2 GB at the start of the disk and mark it active."),
            ("Format it for DOS", "Use 32 KB clusters; 64 KB clusters give 4 GB, but MS-DOS will not mount them."),
            ("Write and test", "Write your image, boot the stick, and confirm that DOS reads the volume."),
        ],
    },

    # ------------------------------------------------------------------ 6
    {
        "slug": "ms-dos-boot-errors-explained",
        "cat": "Guides",
        "h1": "MS-DOS boot errors explained",
        "title": "MS-DOS boot errors explained | ms-dos.su",
        "desc": (
            "Six classic MS-DOS boot and disk errors with the cause of each and what to "
            "do: Non-System disk, Invalid media type, Missing operating system and more."
        ),
        "lead": (
            "Each message names the layer that failed: the firmware, the boot sector, IO.SYS "
            "or COMMAND.COM. Read the wording carefully, because messages that look alike "
            "are fixed differently."
        ),
        "sections": [
            ("How to read these messages", """<p>A message from the firmware appears before anything else and mentions a device or a boot order. A message from <code>IO.SYS</code> means the boot sector ran but the system files were not found. A message from <code>COMMAND.COM</code> means DOS is running and only a command was wrong. If the same message returns after a rewrite, suspect the stick rather than the image.</p>"""),
            ("Non-System disk or disk error", """<p><b>Cause:</b> the boot sector ran, but <code>IO.SYS</code> and <code>MSDOS.SYS</code> are not on the volume - or the firmware booted a different device.</p>
<ul>
<li>Rewrite the stick; the write operation copies the system files as part of the image.</li>
<li>Check the boot order and choose the stick explicitly.</li>
<li>If the message appears with no stick attached, the hard disk's boot record is damaged - a different repair.</li>
</ul>"""),
            ("Invalid media type", """<p><b>Cause:</b> DOS read the partition table, but the boot sector describes a file system it does not know - usually NTFS or exFAT, sometimes a damaged FAT.</p>
<ul>
<li>Recreate the stick as FAT16; Windows formatting it as exFAT is the usual origin.</li>
<li>If it used to work, the boot sector or FAT is damaged; rewriting is faster than repairing.</li>
<li>On a hard disk, back the data up before any repair tool runs.</li>
</ul>"""),
            ("Missing operating system", """<p><b>Cause:</b> the master boot record found no active partition, or the active partition's first sector does not end with the <code>55 AA</code> signature.</p>
<ul>
<li>Check the partition table: exactly one primary partition should be active.</li>
<li>Rewriting the stick rebuilds the MBR, the partition table and the boot sector together.</li>
<li>If this follows a failed installation, the partition table may need rebuilding instead.</li>
</ul>"""),
            ("Cannot exceed 4GB for FAT16", """<p><b>Cause:</b> the formatting step refused because the target is larger than FAT16 allows. This is a message from the tool, not from DOS, and it protects you from a stick that would not boot.</p>
<ul>
<li>Use a stick of 4 GB or less.</li>
<li>Or create a FAT16 first partition of 2 GB and mark it active, as the <a href="/en/fat16-limits-and-4gb-usb-drives.html">FAT16 article</a> describes.</li>
<li>Do not work around it with FAT32: MS-DOS 6.22 cannot read the result.</li>
</ul>"""),
            ("Bad command or file name", """<p><b>Cause:</b> <code>COMMAND.COM</code> is running, so the boot worked; the command is not on the current drive, not in the path, or misspelled.</p>
<ul>
<li>Check the spelling and the current drive letter.</li>
<li>Run <code>dir</code> to see what is there, and <code>path</code> to see where DOS looks.</li>
<li>Some commands are external files: without <code>FORMAT.COM</code> in the image, that command does not exist.</li>
</ul>"""),
            ("Write protect error", """<p><b>Cause:</b> something prevents writes to the media - a physical switch on an SD card or adapter, a firmware lock on USB writes, or a Windows storage policy.</p>
<ul>
<li>Check the switch on the card or adapter.</li>
<li>Try another port and another card reader.</li>
<li>In Windows, check the storage policy for the device and any policy applied to removable media.</li>
</ul>"""),
            ("Detailed pages in Russian", """<p>The knowledge base has longer write-ups for four of these errors. They are in Russian:</p>
<ul>
<li><a href="/oshibka-non-system-disk.html">Non-System disk or disk error</a>;</li>
<li><a href="/oshibka-invalid-media.html">Invalid media type</a>;</li>
<li><a href="/oshibka-no-os.html">Missing operating system</a>;</li>
<li><a href="/oshibka-prevyshenie-4gb.html">Cannot exceed 4GB for FAT16</a>.</li>
</ul>
<p>If your message is not listed, start from <a href="/en/how-to-create-bootable-ms-dos-usb.html">the USB guide</a>, which covers the boot path end to end.</p>"""),
        ],
        "faq": [
            ("Is \"Non-System disk\" a sign of a dead stick?",
             "Not usually. The boot sector ran but the system files were missing. Read errors on several machines are a different problem."),
            ("Can I fix these errors from Windows?",
             "Most of them, yes: rewrite the stick. Partition-table repairs on a hard disk are better done from DOS after a backup."),
            ("Why does \"Bad command or file name\" appear for an existing command?",
             "Because it is on another drive or not in the path. Change to its directory, or add it to PATH in autoexec.bat."),
            ("Does the 4 GB message mean my stick is broken?",
             "No. It means the stick is larger than FAT16 allows. Use a smaller stick or a FAT16 first partition."),
        ],
        "howto": [
            ("Note the exact message", "Write down the wording and whether it appears before or after the DOS prompt."),
            ("Check the boot device", "Open the boot menu, confirm the stick is booted, and pick the entry without the UEFI prefix."),
            ("Rewrite the stick", "Recreate it as FAT16 with the system files included; most of these messages disappear here."),
            ("Test on a second machine", "If it fails identically, the stick or image is at fault; if it boots, the firmware settings are."),
        ],
    },

    # ------------------------------------------------------------------ 7
    {
        "slug": "hard-disk-diagnostics-from-dos",
        "cat": "Diagnostics",
        "h1": "Testing hard drives and memory from DOS",
        "title": "Hard drive and memory diagnostics from DOS | ms-dos.su",
        "desc": (
            "Testing hard drives and memory from DOS with MHDD, Victoria, Memtest86+ and "
            "SeaTools: SMART, surface scans, legacy IDE mode, and imaging before repair."
        ),
        "lead": (
            "DOS diagnostics talk to the hardware with no operating system in the way, which "
            "is exactly why they still find faults that Windows hides."
        ),
        "sections": [
            ("Why boot from DOS at all", """<p>DOS diagnostic tools reach the drive's SMART registers and issue raw read commands without a driver, a cache or a background service in between. That is why a drive that looks healthy in Windows can still fail an MHDD scan.</p>"""),
            ("Start with SMART", """<p>Before any surface scan, read the drive's own counters. The attributes worth watching:</p>
<ul>
<li><b>05 Reallocated sectors</b> - sectors the drive has retired. A growing count means the surface is going.</li>
<li><b>C5 Pending sectors</b> - sectors that could not be read and await a decision.</li>
<li><b>C6 Uncorrectable sectors</b> - reads that failed even after error correction.</li>
<li><b>C7 Interface CRC errors</b> - usually a cable or port problem, not the platters.</li>
</ul>
<p>A drive with reallocated sectors is not repaired by a scan. Copy the data first.</p>"""),
            ("Surface scans: MHDD and Victoria", """<p>MHDD boots from its own media and works with ATA and SATA drives when the controller is in legacy or IDE mode. It scans block by block and shows response times, so slow areas appear before they become errors. Its <b>ERASE</b> command overwrites sectors and destroys data; the same is true of write and remap in Victoria.</p>
<p>Victoria exists in DOS and Windows versions and combines SMART reading, a surface scan and simple repair actions. Treat every repair action as destructive: a remap writes to the drive, and a failing drive may not survive it.</p>"""),
            ("Memory: Memtest86+", """<p>Memory faults look like disk faults: corrupt files, random crashes, a DOS that will not load. Memtest86+ boots from USB or CD, writes patterns across RAM and compares what comes back. Run at least two full passes - one pass misses intermittent errors - and note the failing addresses.</p>
<ul>
<li>Test with XMP or EXPO disabled first; an unstable memory profile is a common cause.</li>
<li>If errors appear, test one module at a time to find the faulty stick.</li>
</ul>"""),
            ("SeaTools for Seagate drives", """<p>Seagate's SeaTools has a DOS version that runs the vendor's short and long tests. The long generic test reads the whole surface and is the one that matters for a warranty claim, so keep the result. For other brands use that vendor's own tool.</p>"""),
            ("When the tool cannot see the drive", """<p>Most DOS diagnostics expect the controller in IDE or legacy mode. With AHCI enabled the drive may be invisible to a tool that addresses legacy registers directly. The fix is in the firmware: set the SATA mode to IDE or Legacy, run the diagnostic, then put the setting back.</p>
<ul>
<li>Check the cable and try another port before blaming the tool.</li>
<li>NVMe drives are not supported by these utilities; they need a different toolset.</li>
<li>A drive the firmware does not detect will not be detected by DOS either; see <a href="/en/ms-dos-boot-errors-explained.html">boot errors</a>.</li>
</ul>"""),
            ("Image before you repair", """<p>Every repair action on a failing drive - remap, erase, low-level format - writes to the media. If the data matters, copy it to a different disk first and verify the copy; a dying drive may not survive a second attempt.</p>
<p>For MS-DOS media, <b>Create MBFU image from disk/floppy/USB</b> in MBFUTool captures the contents into a .mbfu container: a header, a zlib-compressed payload and a SHA-256 digest of the raw image. That gives you a verified copy to work from. It is not a forensic imager, and it is meant for DOS file systems.</p>"""),
            ("Order of work", """<ol>
<li>Read SMART and write the numbers down with the date.</li>
<li>Copy the data off, if the drive still reads.</li>
<li>Run a read-only surface scan and note the slow blocks and errors.</li>
<li>Decide: replace the drive, or repair it with the vendor's tool.</li>
<li>Test the memory separately before blaming the disk for corruption.</li>
</ol>"""),
        ],
        "faq": [
            ("Does MHDD work with NVMe drives?",
             "No. MHDD addresses ATA and SATA drives through legacy controller interfaces; NVMe needs a different tool."),
            ("How many Memtest86+ passes are enough?",
             "At least two full passes. One can miss errors that appear only when the modules warm up or when a pattern repeats."),
            ("Is a surface scan safe for the data?",
             "A read-only scan is. Erase, write and remap operations overwrite sectors, so copy the data first."),
            ("Will SeaTools work on another brand of drive?",
             "It may detect it, but the tests are written for Seagate drives. Use the drive maker's own tool elsewhere."),
        ],
        "howto": [
            ("Read the SMART data", "Note the reallocated, pending and CRC counters before running anything that writes to the drive."),
            ("Copy the data off", "If the drive still reads, copy the important files to another disk before any repair."),
            ("Scan the surface", "Boot MHDD or Victoria, run a read-only scan, look for slow blocks and errors."),
            ("Test the memory", "Run Memtest86+ for at least two full passes to rule out RAM."),
            ("Capture an image", "For DOS media, create a .mbfu image first so you can work from a verified copy."),
        ],
    },

    # ------------------------------------------------------------------ 8
    {
        "slug": "best-ms-dos-usb-tools",
        "cat": "Comparison",
        "h1": "Tools for writing MS-DOS images to USB: an honest comparison",
        "title": "Tools for writing MS-DOS images to USB | ms-dos.su",
        "desc": (
            "Rufus, WinSetupFromUSB, the HP format tool, Win32DiskImager and MBFUTool 2.0 "
            "compared by what they do with an MS-DOS image, and which to pick for which task."
        ),
        "lead": (
            "Most comparisons of USB writers compare marketing pages. Here is what each program "
            "does with an MS-DOS image, and where each one stops."
        ),
        "sections": [
            ("The job has two shapes", """<p>"Make a bootable DOS stick" covers two operations. Either you have an image - a byte-for-byte copy of a floppy or disk - and need it written to the device, or you have a folder of DOS files and need a boot sector and system files built around them. Some tools do the first, some the second; choosing the wrong family is why a tool seems not to work.</p>"""),
            ("Rufus", """<p>Rufus is free, open source and Windows-only. It is very good at what most people need: writing modern ISO images to USB, and creating a FreeDOS stick from the files it bundles. Its partition scheme options - MBR/BIOS versus GPT/UEFI - are the switch that decides whether a DOS stick can boot.</p>
<p>For MS-DOS, Rufus includes no Microsoft files. It writes an image you supply, or uses DOS files from a folder, but the MS-DOS part stays your responsibility - a licensing boundary, not a defect.</p>"""),
            ("WinSetupFromUSB", """<p>WinSetupFromUSB is built around installing Windows from USB, from the XP era to current releases, and handles the boot-menu work multi-source installers need. It is right when the job is a Windows installer, or a stick offering both Windows setup and a DOS entry. It is not an image writer for an arbitrary MS-DOS image.</p>"""),
            ("HP USB Disk Storage Format Tool", """<p>A small, old utility that formats a stick as FAT or FAT32 and can copy DOS system files from a folder to make it bootable. It works with files, not images: it cannot open an .img, .ima or .mbfu, and it does not check what it wrote. Its FAT32 option is useless for MS-DOS, but it still helps when you have DOS files and no imaging tool.</p>"""),
            ("dd and Win32DiskImager", """<p>These write an image byte for byte. <code>dd</code> on Linux, macOS or Windows through WSL is the classic form: <code>dd if=image.img of=/dev/sdX bs=4M status=progress</code>. Win32DiskImager is the Windows equivalent with a device picker.</p>
<p>Both are honest and dangerous for the same reason: point them at the wrong device and it is gone. Neither compares the device with the image as part of the write. Win32DiskImager reports that the write call returned, which is not verification; a read-back is a separate step.</p>"""),
            ("MBFUTool 2.0", """<p>MBFUTool is image-oriented and does exactly four things: <b>Write MS-DOS image to USB flash</b>, <b>Create MBFU image from disk/floppy/USB</b>, <b>Clone MS-DOS disk/floppy/USB to USB</b>, and <b>Edit MS-DOS image with DOS commands</b>. Editing runs in the bundled DOSBox 0.72 with a BEN menu.</p>
<p>Its .mbfu format is a container with a header, zlib compression and a SHA-256 digest of the raw image, and the program verifies that digest - the step the dd family leaves to you. It needs administrator rights, blocks writes to the system disk, and destroys the target stick's data. It ships no MS-DOS files: the image is yours, per the <a href="/en/ms-dos-license.html">licensing page</a>. Limits are FAT16: 4 GB maximum, 2 GB in practice, no image above 4 GB in DOSBox 0.72, Latin-only paths.</p>"""),
            ("Pick by task", """<ul>
<li><b>A FreeDOS stick in two minutes</b> - Rufus.</li>
<li><b>A Windows installer, or Windows plus a DOS entry</b> - WinSetupFromUSB.</li>
<li><b>A folder of DOS files and nothing else</b> - HP USB Disk Storage Format Tool.</li>
<li><b>An exact copy of an image, verified by hand</b> - dd or Win32DiskImager.</li>
<li><b>Your own MS-DOS image, written, verified, cloned and editable</b> - MBFUTool 2.0.</li>
</ul>
<p>Match the tool to what you are holding - an image or a folder of files - and to whether you need verification, cloning or editing afterwards. That decides whether the stick boots, which matters more than a feature list.</p>
<p>The MBFUTool trial runs 30 days with every feature, offline and without a key: <a href="https://ms-dos.su/#trial">trial details</a>.</p>"""),
        ],
        "faq": [
            ("Does Rufus include MS-DOS?",
             "No. It bundles FreeDOS, a different operating system. For MS-DOS you supply your own files or image."),
            ("Which of these tools verifies the write?",
             "MBFUTool verifies the SHA-256 digest stored in its .mbfu container. With dd or Win32DiskImager, verification is a manual read-back."),
            ("Can I use these tools on macOS or Linux?",
             "dd works everywhere. Rufus, WinSetupFromUSB, the HP tool, Win32DiskImager and MBFUTool are Windows programs."),
        ],
        "howto": [
            ("Decide what you have", "An image file and a folder of DOS files need different tools; note which one you have."),
            ("Check the target media", "The stick needs a FAT16 partition and an MBR partition table for a BIOS boot. Back it up first."),
            ("Write or create", "Write the image byte for byte, or create a boot sector and copy the system files."),
            ("Verify the result", "Compare the device with the image, or check the stored hash if the tool keeps one."),
            ("Test on real hardware", "A successful write is not a successful boot; try the stick on the target machine."),
        ],
    },
]