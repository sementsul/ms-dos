# -*- coding: utf-8 -*-
"""English SEO page data for ms-dos.su (batch 3)."""

ARTICLES = [
    {
        "slug": "secure-boot-asus-msi-steps",
        "cat": "BIOS",
        "h1": "Secure Boot and CSM on ASUS and MSI boards",
        "title": "Secure Boot and CSM on ASUS and MSI Boards | ms-dos.su",
        "desc": "Where Secure Boot and CSM sit on ASUS and MSI boards, what each switch does, why CSM can vanish in UEFI-only mode, and how to find a missing DOS USB stick.",
        "lead": "Two firmware switches decide whether a modern board will boot a DOS USB stick: Secure Boot and CSM. Their names and locations differ between ASUS and MSI, and on both brands the CSM entry can disappear once the board is set to a pure UEFI boot mode.",
        "sections": [
            (
                "ASUS: Advanced Mode and the Boot menu",
                "<p>On ASUS boards the relevant settings sit in Advanced Mode, which you reach by pressing <b>F7</b> in the initial setup screen. Open the <b>Boot</b> tab and look for <b>CSM</b>; in the same area, <b>Secure Boot</b> holds an <b>OS Type</b> option. Setting OS Type to <b>Other OS</b> relaxes the signature requirement, which is what a DOS-era loader needs. CSM must be enabled for a legacy boot sector to run at all. If the CSM item is missing, the board is in a UEFI-only state.</p>",
            ),
            (
                "MSI: Windows OS Configuration",
                "<p>On MSI boards the same pair lives under <b>Advanced</b> in the <b>Windows OS Configuration</b> submenu. Secure Boot is switched off there, and CSM is enabled in the same screen or in the boot-related submenu next to it. Some layouts place CSM on a separate <b>Boot</b> page. After changing either option, save and exit; the board re-enumerates boot devices on the next power-on.</p>",
            ),
            (
                "What each switch does",
                "<p><b>Secure Boot</b> is a firmware policy: the bootloader must carry a signature that the firmware trusts. A DOS boot sector has no such signature, so with Secure Boot on, the firmware refuses to hand control to it. <b>CSM</b> (Compatibility Support Module) is the opposite kind of switch: it keeps legacy interrupt and device services alive and lets the firmware read an MBR partition table and jump into a 512-byte boot sector. Enabling CSM does not disable Secure Boot, and disabling Secure Boot does not enable CSM. Treat them as two independent conditions that both have to be right.</p>",
            ),
            (
                "Why CSM can be hidden",
                "<p>Firmware hides the CSM entry when the boot mode is set to pure UEFI. On many boards this happens automatically once the boot list contains only UEFI entries, or after <b>Boot Mode</b> is changed to UEFI only. The way back is to switch the boot mode to CSM or legacy support first, then reopen setup: the CSM and legacy USB options reappear. On some models the CSM line only shows up after <b>Fast Boot</b> is disabled. Menu names vary by model and firmware build, so follow the tab names rather than an exact sequence.</p>",
            ),
            (
                "When the DOS stick is not in the boot menu",
                "<p>Check the stick before blaming the board. The image must have been written to the device, not copied as a file; the stick needs an MBR partition table with one active partition holding the DOS boot sector; FAT16 is the safe filesystem for DOS. Try a rear USB 2.0 port rather than a front-panel connector or a hub, enable <b>USB Legacy Support</b>, and re-plug the stick after enabling CSM. Use the one-time boot menu key at power-on to see whether the stick appears as a legacy device. If it appears only as a UEFI entry, the image is not a legacy one.</p>",
            ),
            (
                "A note on names",
                "<p>ASUS and MSI rename pages between generations, and the same option can move between Boot and Advanced. The descriptions above use the tab names that have stayed stable: Boot, CSM, Secure Boot, OS Type, Windows OS Configuration. Exact wording is not guaranteed, and no version number is implied.</p>",
            ),
        ],
        "faq": [
            (
                "Do I need to disable Secure Boot to boot DOS?",
                "Yes. A DOS boot sector is unsigned, so the firmware will not start it while Secure Boot is on. Disabling Secure Boot and enabling CSM together is the usual combination.",
            ),
            (
                "Why is there no CSM option on my board?",
                "The board is in UEFI-only boot mode. Switch the boot mode to CSM or legacy first, disable Fast Boot if the option stays hidden, then reopen setup.",
            ),
            (
                "Does the DOS stick show up as UEFI or legacy?",
                "A correctly written DOS image is a legacy MBR device. It should appear in the legacy or CSM list, not under UEFI. If it appears only as UEFI, rewrite the image.",
            ),
        ],
        "howto": [
            (
                "Enter firmware setup",
                "Restart and press the setup key at power-on (Del or F2 on most boards), then switch to Advanced Mode with F7 on ASUS.",
            ),
            (
                "Enable CSM",
                "On ASUS open Boot > CSM and enable it. On MSI open Advanced > Windows OS Configuration and enable CSM.",
            ),
            (
                "Relax or disable Secure Boot",
                "On ASUS set Secure Boot > OS Type to Other OS. On MSI set Secure Boot to disabled.",
            ),
            (
                "Select the stick",
                "Save and exit, re-plug the USB stick, open the one-time boot menu and choose the legacy entry for the stick.",
            ),
        ],
    },
    {
        "slug": "floppy-images-ima-vfd",
        "cat": "Guides",
        "h1": "Floppy images: .img, .ima and .vfd explained",
        "title": "Floppy Images: .img, .ima and .vfd Explained | ms-dos.su",
        "desc": "Raw floppy images explained: .img, .ima and .vfd, the standard geometries, why 1.44 MB is exactly 1,474,560 bytes, the 55 AA signature, and testing without a drive.",
        "lead": "A floppy image is a byte-for-byte copy of the sectors on a disk, with no container and no metadata. The extensions .img, .ima and .vfd all describe the same thing; the differences are historical and practical, not structural.",
        "sections": [
            (
                "One format, three names",
                "<p>A raw floppy image holds the disk's data area in logical order: sector 0 first, then the rest of track 0, then head 1 of track 0, and so on. Nothing inside the file records the geometry, so the file size is the only hint. <b>.img</b> is the generic name, <b>.ima</b> is used by some emulators and imaging tools for the same raw layout, and <b>.vfd</b> (virtual floppy disk) comes from VirtualBox and a few other virtualisers. All three open in the same tools.</p>",
            ),
            (
                "Standard geometries",
                "<p>Floppy formats are defined by cylinders, heads and sectors per track. The table lists the common PC geometries and the exact byte size each produces.</p><table><tr><td>Format</td><td>Cylinders</td><td>Heads</td><td>Sectors/track</td><td>Bytes</td></tr><tr><td>160K</td><td>40</td><td>1</td><td>8</td><td>163,840</td></tr><tr><td>360K</td><td>40</td><td>2</td><td>9</td><td>368,640</td></tr><tr><td>720K</td><td>80</td><td>2</td><td>9</td><td>737,280</td></tr><tr><td>1.2M</td><td>80</td><td>2</td><td>15</td><td>1,228,800</td></tr><tr><td>1.44M</td><td>80</td><td>2</td><td>18</td><td>1,474,560</td></tr><tr><td>2.88M</td><td>80</td><td>2</td><td>36</td><td>2,949,120</td></tr></table><p>The K and M labels are approximate: a 1.44 MB disk holds 1,474,560 bytes, not 1,440,000.</p>",
            ),
            (
                "Why 1.44 MB is exactly 1,474,560 bytes",
                "<p>Multiply the geometry: 80 cylinders × 2 heads × 18 sectors × 512 bytes = 1,474,560. Every factor is fixed by the standard, so the size is exact and every 1.44 MB image is that long. The same arithmetic gives 2,949,120 bytes for 2.88 MB, 1,228,800 for 1.2 MB, 737,280 for 720 KB and 368,640 for 360 KB. A file that is a few bytes off is either a different geometry or a damaged dump.</p>",
            ),
            (
                "The boot sector and the 0x55AA signature",
                "<p>Sector 0 is the boot sector. The last two bytes of the 512-byte sector are 0x55 followed by 0xAA; firmware checks them before jumping to the code at offset 0. DOS itself does not need the signature once the loader is running, but a board's CSM and most imaging tools do. A system image also carries the BIOS Parameter Block in the first bytes of the boot sector, describing the geometry and the FAT layout. Without the signature an image may still contain files but will not boot.</p>",
            ),
            (
                "Write protection and inspection",
                "<p>A real floppy has a physical write-protect tab; an image needs the equivalent at the filesystem level. Mark the file read-only when you keep a master copy, and write to USB or virtual media rather than editing the master. Images are made by reading the device sector by sector with a raw disk tool and inspected with a hex viewer: bytes 0–2 should be a jump instruction, 3–10 the OEM name, and 510–511 the signature. Comparing the file size with the table above is the fastest sanity check.</p>",
            ),
            (
                "What you can do without a physical drive",
                "<p>DOSBox 0.72 mounts a floppy image directly and boots it, so an image can be tested without hardware. VMware and VirtualBox attach .img and .vfd files as virtual floppy drives and boot from them; VirtualBox is where the .vfd name comes from. To put the same image on a real machine, MBFUTool 2.0 for Windows x64 writes an MS-DOS image to a USB stick, and one of its four operations turns a disk or floppy into a .mbfu image. Images above 4 GB cannot be mounted in DOSBox 0.72, which is irrelevant for floppies but matters for hard-disk images.</p>",
            ),
        ],
        "faq": [
            (
                "Are .img, .ima and .vfd the same format?",
                "Yes. All three are raw sector dumps with no header. Use the extension your emulator expects; the bytes do not change.",
            ),
            (
                "Why is my 1.44 MB image 1,474,560 bytes?",
                "That is the exact geometry product: 80 × 2 × 18 × 512. The label rounds the number.",
            ),
            (
                "Can I edit files inside an image without a floppy drive?",
                "Yes, with an emulator or an image editor. Keep an untouched master copy read-only and edit a working copy.",
            ),
        ],
        "howto": [
            (
                "Identify the geometry",
                "Read the file size and match it to the table; 1,474,560 bytes is a standard 1.44 MB disk.",
            ),
            (
                "Check the boot sector",
                "Open the first 512 bytes in a hex viewer and confirm the last two bytes are 55 AA.",
            ),
            (
                "Protect the master",
                "Set the file read-only and work on a copy; never edit the only known-good image.",
            ),
            (
                "Test before writing",
                "Boot the image in DOSBox 0.72 or attach it as a virtual floppy in VMware or VirtualBox.",
            ),
        ],
    },
    {
        "slug": "no-bootable-device-and-other-errors",
        "cat": "Guides",
        "h1": "“No bootable device”: fixing boot errors on modern PCs",
        "title": "“No Bootable Device”: Fixing Boot Errors on Modern PCs | ms-dos.su",
        "desc": "What “No bootable device”, “Non-System disk”, “Missing operating system” and “Invalid media type” mean, with a table for boot mode, CSM, active partition and USB.",
        "lead": "The five messages below all mean the same thing at heart: the firmware looked for something bootable and did not find it, or found it and rejected it. The wording tells you which stage failed.",
        "sections": [
            (
                "The messages, one by one",
                "<ul><li><b>No bootable device</b> — the firmware found no device with a valid boot record in the current boot mode.</li><li><b>Reboot and select proper boot device</b> — the same failure with a prompt; often boot order or the stick's mode.</li><li><b>Non-System disk or disk error</b> — a boot sector was found, but it is not a DOS system disk (no IO.SYS/MSDOS.SYS chain).</li><li><b>Missing operating system</b> — the boot sector ran but the partition it points to has no system files or the active flag is wrong.</li><li><b>Invalid media type</b> — the BPB or FAT type does not match what the loader expects; typical of a wrongly formatted or truncated image.</li></ul>",
            ),
            (
                "No bootable device, reboot and select proper boot device",
                "<p>These come from the firmware, before any DOS code runs. Either the boot mode does not match the image (UEFI firmware, legacy MBR image), or CSM is off, or the stick was not written as a bootable device. Check the one-time boot menu: a legacy image should appear as a legacy entry, not under UEFI. Try another port, preferably rear USB 2.0, and confirm the stick is not formatted as a UEFI-only device.</p>",
            ),
            (
                "Non-System disk and Missing operating system",
                "<p>These come from a loader that did run. The boot sector is present and the signature is valid, but the system files are missing, the partition is not marked active, or the BPB describes a different geometry than the image actually has. Rewrite the image with a tool that writes the whole device, not a file copy, and check that the partition carries the active flag.</p>",
            ),
            (
                "Invalid media type",
                "<p>The loader read the BPB and found a combination it cannot use: a FAT type that does not match the cluster count, a sector size other than 512, or a geometry field that contradicts the image size. This is common when a 1.44 MB image is written to a 2.88 MB geometry, or when an image was truncated during download. Compare the file size with the expected geometry first.</p>",
            ),
            (
                "Decision table",
                "<table><tr><td>Symptom</td><td>Likely cause</td><td>What to check</td></tr><tr><td>Firmware message, stick absent from the boot menu</td><td>Image not written as bootable, or wrong mode</td><td>Boot mode and CSM; one-time boot menu</td></tr><tr><td>Legacy image on a UEFI-only machine</td><td>CSM off or hidden</td><td>Enable CSM, disable Fast Boot</td></tr><tr><td>“Non-System disk”</td><td>Boot sector present, system files missing</td><td>Rewrite the image; check the active partition</td></tr><tr><td>“Missing operating system”</td><td>Active flag wrong or partition mismatch</td><td>Partition table and active flag</td></tr><tr><td>Works on one port, not another</td><td>USB controller or front-panel hub</td><td>Rear USB 2.0 port; USB legacy support</td></tr><tr><td>Secure Boot enabled</td><td>Unsigned loader refused</td><td>Disable Secure Boot or set OS Type to Other OS</td></tr></table>",
            ),
            (
                "Russian detail pages",
                "<p>Longer write-ups of individual messages are on the Russian pages: <a href='https://ms-dos.su/oshibka-non-system-disk.html'>Non-System disk</a>, <a href='https://ms-dos.su/oshibka-invalid-media.html'>Invalid media type</a>, <a href='https://ms-dos.su/oshibka-no-os.html'>No OS</a> and <a href='https://ms-dos.su/oshibka-prevyshenie-4gb.html'>the 4 GB limit</a>. They are in Russian; the table above covers the same checks in English.</p>",
            ),
        ],
        "faq": [
            (
                "Why does the stick boot on one PC and not another?",
                "Boot mode and CSM differ between machines. A legacy image needs CSM on and Secure Boot off; a UEFI-only machine will not list it.",
            ),
            (
                "I wrote the image but get Non-System disk. Is the image bad?",
                "Not necessarily. The boot sector was read, so the device is bootable; the system files or the active flag are the usual cause. Rewrite the whole device and check the partition.",
            ),
            (
                "Do the Russian pages cover the same errors?",
                "Yes, in more detail and in Russian. The messages and the checks are the same.",
            ),
        ],
        "howto": [
            (
                "Read the message",
                "Note whether it comes from the firmware (no device found) or from a loader (device found, files missing).",
            ),
            (
                "Match the boot mode",
                "Set the firmware to CSM or legacy for an MBR DOS image, and disable Secure Boot.",
            ),
            (
                "Check the device",
                "Confirm the image was written to the whole device, has an active partition and a 55 AA boot signature.",
            ),
            (
                "Try another port",
                "Move the stick to a rear USB 2.0 port, re-plug it, and use the one-time boot menu to pick the legacy entry.",
            ),
        ],
    },
]