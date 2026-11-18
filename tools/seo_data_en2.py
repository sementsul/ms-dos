# -*- coding: utf-8 -*-
"""English SEO page data for ms-dos.su (set 2)."""

ARTICLES = [
    {
        "slug": "ms-dos-command-reference",
        "cat": "Reference",
        "h1": "MS-DOS command reference: the commands you actually use",
        "title": "MS-DOS command reference: the commands you actually use | ms-dos.su",
        "desc": "A practical one-line reference for the MS-DOS commands people really use: DIR, COPY, XCOPY, FORMAT, FDISK, SYS, MEM and more, with the switches that matter.",
        "lead": "Most MS-DOS work is done with a dozen commands. This reference lists them one line at a time, with the switch that usually matters, plus warnings for the commands that destroy data.",
        "sections": [
            ("Files and directories", """<p>These commands list, navigate and manage directories. They are safe to try on any disk.</p>
<ul>
<li><b>DIR</b> — list a directory. <code>/P</code> pauses after each screen, <code>/W</code> gives the wide format, <code>/A</code> shows hidden and system files. See the <a href="https://ms-dos.su/komanda-dir.html">DIR command page</a>.</li>
<li><b>CD</b> — change directory. <code>CD \\</code> goes to the root, <code>CD ..</code> goes up one level.</li>
<li><b>MD</b> — make a directory. <b>RD</b> removes an empty one only.</li>
<li><b>PATH</b> — set the directories searched for programs, for example <code>PATH C:\\;C:\\DOS</code>.</li>
<li><b>SET</b> — show or set environment variables such as <code>COMSPEC</code> or <code>TEMP</code>.</li>
</ul>"""),
            ("Copying and renaming", """<p>COPY handles single files and simple concatenation. XCOPY handles directory trees, which is what you need when moving a whole folder structure between disks.</p>
<ul>
<li><b>COPY</b> — copy one file or several. Wildcards work: <code>COPY *.TXT A:</code>. Examples are on the <a href="https://ms-dos.su/komanda-copy.html">COPY command page</a>.</li>
<li><b>XCOPY</b> — copy directories. <code>/S</code> includes subdirectories, <code>/E</code> also copies empty ones.</li>
<li><b>REN</b> — rename a file in place. It cannot move a file to another directory.</li>
<li><b>ATTRIB</b> — show or change attributes. <code>+R</code> sets read-only, <code>-H</code> clears hidden.</li>
<li><b>TYPE</b> — print a text file to the screen, or <code>TYPE FILE.TXT | MORE</code> for long files.</li>
<li><b>EDIT</b> — the full-screen text editor that arrived with MS-DOS 5.00.</li>
</ul>"""),
            ("Deleting and recovering", """<p>Deletion in DOS is immediate. There is no recycle bin, so the only recovery route is UNDELETE, and only if the file has not been overwritten.</p>
<ul>
<li><b>DEL</b> — delete files. <code>/P</code> asks for confirmation before each file.</li>
<li><b>DELTREE</b> — delete a directory and everything inside it, without prompting.</li>
<li><b>UNDELETE</b> — try to restore deleted files. Stop writing to the disk first.</li>
</ul>"""),
            ("Disks, system files and diagnostics", """<p>The commands in this group change the disk itself. Read the warning below first.</p>
<p><b>Warning:</b> FORMAT, FDISK and DEL destroy data permanently. FORMAT erases the file system on the selected partition, FDISK can delete partitions and rewrite the partition table, and DEL removes files with no undo. Check the drive letter twice.</p>
<ul>
<li><b>FORMAT</b> — prepare a partition. <code>/S</code> also copies the system files, <code>/Q</code> does a quick format, <code>/U</code> forces an unconditional format.</li>
<li><b>FDISK</b> — create and delete partitions and set the active one.</li>
<li><b>SYS</b> — transfer the DOS system files to a disk so it becomes bootable.</li>
<li><b>CHKDSK</b> — check the disk and report lost clusters. <code>/F</code> fixes errors.</li>
<li><b>SCANDISK</b> — the later, more thorough checker introduced with MS-DOS 6.x.</li>
<li><b>MEM</b> — show conventional, upper and extended memory. <code>MEM /C</code> lists what is loaded where.</li>
<li><b>LABEL</b> — show or change the volume label.</li>
<li><b>SMARTDRV</b> — install a disk cache to speed up repeated reads.</li>
</ul>
<p>Command pages for the destructive tools: <a href="https://ms-dos.su/komanda-format.html">FORMAT</a>, <a href="https://ms-dos.su/komanda-fdisk.html">FDISK</a>, <a href="https://ms-dos.su/komanda-sys.html">SYS</a>.</p>"""),
            ("Switches worth remembering", """<p>Five switches cover most daily work. <code>/S</code> means include subdirectories for XCOPY and copy system files for FORMAT. <code>/P</code> means pause or prompt. <code>/W</code> means wide listing for DIR. <code>/A</code> means attributes for DIR and ATTRIB. <code>/Y</code> means answer yes to overwrite prompts. A stick made with MBFUTool 2.0 boots into a BEN menu for these tools, and writes to the system disk are blocked.</p>"""),
        ],
        "faq": [
            ("Do I need to memorise all of these?", "No. DIR, CD, COPY, DEL, MD and RD cover most work. The rest are needed when something breaks or when you prepare a disk."),
            ("Is DELTREE recoverable?", "Only with UNDELETE, and only if nothing has been written to the disk since."),
            ("Why does RD refuse to delete my directory?", "RD only removes empty directories. Delete the files inside first, or use DELTREE."),
        ],
        "howto": [
            ("Open a command prompt", "Boot MS-DOS, or start the DOS prompt from the BEN menu on an MBFUTool stick."),
            ("Identify the drive", "Run DIR on the letter you intend to use and confirm the files match the disk you mean."),
            ("Run the command", "Type the command with its switch, for example DIR /P or COPY *.TXT A:."),
            ("Verify the result", "List the directory again, or run CHKDSK on the disk, before you unplug anything."),
        ],
    },
    {
        "slug": "ms-dos-500-vs-622",
        "cat": "Comparison",
        "h1": "MS-DOS 5.00 vs 6.22: which one to put on a USB drive",
        "title": "MS-DOS 5.00 vs 6.22: which one to put on a USB drive | ms-dos.su",
        "desc": "MS-DOS 5.00 brought EDIT, QBASIC and HIMEM.SYS. MS-DOS 6.22 added SCANDISK, DEFRAG, MSAV and DriveSpace. Here is how to choose for real hardware.",
        "lead": "The choice between MS-DOS 5.00 and 6.22 is not about which is newer. It is about which machine the stick will boot and what size media it must handle. Both fit on a single floppy and both boot from a USB stick prepared with an image.",
        "sections": [
            ("What MS-DOS 5.00 brought", """<p>Version 5.00 was a large step. It introduced EDIT, a full-screen text editor that replaced the line editor EDLIN for everyday work, and QBASIC, a structured BASIC interpreter with a built-in editor. It added HIMEM.SYS as the standard way to manage extended memory, and it allowed DOS itself to load above 640 KB on 286 and later processors, freeing conventional memory.</p>
<p>It also added a shell and UNDELETE, and it made the memory story understandable: HIMEM.SYS loaded the XMS driver, and DOS could then be placed in the high memory area.</p>"""),
            ("What 6.x and 6.22 added", """<p>The 6.x line added the maintenance tools most people now associate with DOS. SCANDISK replaced CHKDSK as the thorough disk checker, DEFRAG defragmented disks, and MSAV provided antivirus scanning. Memory handling improved with MEMMAKER, which automated the CONFIG.SYS and AUTOEXEC.BAT tuning that used to be done by hand. DriveSpace replaced DoubleSpace, and 6.22 is the version that shipped with DriveSpace in place.</p>
<p>6.22 is also the last standalone release of MS-DOS, which is why it became the reference version for boot disks and DOS-based tools.</p>"""),
            ("The practical answer", """<p>For modern hardware and larger media, choose 6.22. It has the disk tools you need when a card or stick misbehaves, and its memory manager is easier to configure.</p>
<p>For a period-correct machine, choose 5.00. On a 286 or an early 386 with a small hard disk, 5.00 is lighter and matches the hardware. For very old machines, 3.3 remains the safe choice: it works on hardware that predates the 286 memory model and does not need HIMEM.SYS.</p>"""),
            ("Fitting a version onto a USB stick", """<p>An MS-DOS boot image is small, but the stick does not have to be. MBFUTool 2.0 writes an MS-DOS image to a USB stick, creates an .mbfu image from a disk, floppy or USB device, clones MS-DOS media to a stick, and lets you edit an image with DOS commands. It runs on Windows x64 and asks for administrator rights. Writes to the system disk are blocked and the target USB stick is erased, so move anything you want to keep first.</p>
<p>The file system is FAT16, up to 4 GB with about 2 GB practical. Images above 4 GB cannot be mounted in DOSBox 0.72, and paths must be latin-only. No MS-DOS files are shipped: you supply a lawful image; the licence notes are at <a href="https://ms-dos.su/en/ms-dos-license.html">ms-dos.su/en/ms-dos-license.html</a>. The trial runs 30 days with all features, offline and without a key; the full version is a one-time purchase on Boosty, one computer per licence.</p>"""),
            ("What not to expect", """<p>Neither version turns a modern PC into a retro machine. USB boot support depends on the BIOS, and some boards will not boot from a stick prepared this way. Test the boot first.</p>"""),
        ],
        "faq": [
            ("Can I run 6.22 on a 286?", "It will boot, but MEMMAKER and some tools expect a 386 or later. On a 286, 5.00 is the more comfortable fit."),
            ("Does 6.22 need more memory?", "The base system is comparable. The difference is the extra tools, which you do not have to load unless you run them."),
            ("Which version should a boot stick use?", "6.22 for maintenance work, because SCANDISK and DEFRAG are on the same disk. 5.00 if the stick is meant for a specific period machine."),
        ],
        "howto": [
            ("Check the target machine", "Note the processor class, the BIOS boot options and the size of the disk or card you need to work with."),
            ("Pick the version", "6.22 for modern hardware and larger media, 5.00 for a period 286 or 386, 3.3 for very old machines."),
            ("Prepare the image", "Create an .mbfu image and add or edit files with DOS commands inside it before writing anything to the stick."),
            ("Write and test", "Write the image to the USB stick, boot the target machine from it, and confirm the DOS prompt appears before using it on real data."),
        ],
    },
    {
        "slug": "himem-emm386-memory-management",
        "cat": "Guides",
        "h1": "HIMEM.SYS, EMM386 and the 640 KB problem",
        "title": "HIMEM.SYS, EMM386 and the 640 KB problem | ms-dos.su",
        "desc": "How conventional memory, UMB, XMS and EMS fit together in MS-DOS, with a sample CONFIG.SYS using HIMEM.SYS and EMM386, and when to leave EMM386 out.",
        "lead": "MS-DOS programs expect to run in the first 640 KB of memory. Every driver and resident program takes a slice of that space. HIMEM.SYS and EMM386 exist to move as much as possible out of it, and the four memory types are enough to fix most \"out of memory\" errors.",
        "sections": [
            ("The four memory areas", """<p><b>Conventional memory</b> is the first 640 KB. DOS itself, drivers and programs all compete for it. A program that refuses to start usually needs a larger free block there, not more total memory.</p>
<p><b>Upper memory</b> is the region between 640 KB and 1 MB. It is reserved for hardware, but unused parts can be remapped as UMBs, upper memory blocks, where drivers and resident programs can live.</p>
<p><b>Extended memory (XMS)</b> is everything above 1 MB. HIMEM.SYS manages it and provides the high memory area, the first 64 KB above 1 MB, where DOS can place part of itself.</p>
<p><b>Expanded memory (EMS)</b> is a bank-switched window, traditionally in upper memory, that lets programs address more than 640 KB in 16 KB pages. EMM386.EXE emulates EMS using extended memory.</p>"""),
            ("A sample CONFIG.SYS", """<p>The usual order matters: HIMEM.SYS first, then EMM386, then the devices you want to load high.</p>
<pre>DEVICE=C:\\DOS\\HIMEM.SYS
DEVICE=C:\\DOS\\EMM386.EXE NOEMS
DOS=HIGH,UMB
FILES=30
BUFFERS=20
DEVICEHIGH=C:\\DOS\\MOUSE.SYS</pre>
<p><code>DOS=HIGH,UMB</code> puts part of DOS above 1 MB and makes upper memory available. Replacing <code>NOEMS</code> with <code>RAM</code> enables both UMBs and an EMS page frame; use <code>NOEMS</code> when no program needs EMS, because the page frame costs 64 KB of upper memory.</p>"""),
            ("DEVICEHIGH and LH", """<p><code>DEVICEHIGH</code> in CONFIG.SYS and <code>LH</code> in AUTOEXEC.BAT both try to load a driver or program into a UMB instead of conventional memory. They only work if EMM386 is loaded and UMBs are enabled with <code>DOS=UMB</code>. If a driver fails to load high, DOS falls back to conventional memory, so the machine still boots.</p>
<p>MEMMAKER, available from MS-DOS 6.x, automates this tuning by trying combinations and rewriting the two files. On 5.00 the work is manual.</p>"""),
            ("When EMM386 helps and when it hurts", """<p>EMM386 is needed when a program requires EMS, which is common for older games and some CAD and spreadsheet software. It is also needed for <code>DEVICEHIGH</code> and <code>LH</code> to have anywhere to put things.</p>
<p>It gets in the way on a 286, where it cannot run, and on machines where nothing needs EMS and upper memory is already sufficient. If everything runs and MEM shows enough free conventional memory, EMM386 only costs a driver and boot time.</p>"""),
            ("Checking the result", """<p><code>MEM</code> prints a summary of conventional, upper, extended and expanded memory. <code>MEM /C</code> adds a list of loaded programs and drivers grouped by the region they occupy, which is the fastest way to see what is still in conventional memory. <code>MEM /F</code> shows free regions instead.</p>
<p>Read the largest free block, not the total. A program that needs 580 KB will not start if the total is 600 KB but fragmented into 400 KB and 200 KB pieces. Removing one resident program or moving it high often solves it.</p>"""),
            ("Memory and a bootable USB stick", """<p>A stick prepared with MBFUTool 2.0 boots into a BEN menu, and the DOS tools it launches run inside the same 640 KB. If a tool reports insufficient memory, the fix is in CONFIG.SYS on the image: move drivers high, drop anything unnecessary, and keep the image lean.</p>"""),
        ],
        "faq": [
            ("Do I need EMM386 if I have plenty of RAM?", "No. Without EMS-hungry software, NOEMS or no EMM386 at all gives you more upper memory for drivers."),
            ("Why does my program still say out of memory?", "It needs a large contiguous block in conventional memory. Check MEM /C and move residents high or remove them."),
            ("Can HIMEM.SYS run on a 286?", "Yes, and it is how DOS gets loaded above 640 KB there. EMM386 requires a 386 or later."),
        ],
        "howto": [
            ("Back up CONFIG.SYS", "Copy CONFIG.SYS and AUTOEXEC.BAT somewhere safe before you change the memory configuration."),
            ("Load HIMEM.SYS first", "Add DEVICE=C:\\DOS\\HIMEM.SYS as the first device line, then add DOS=HIGH,UMB."),
            ("Decide on EMS", "Use NOEMS unless a specific program needs expanded memory, in which case use RAM."),
            ("Move drivers high", "Change DEVICE= to DEVICEHIGH= and add LH in AUTOEXEC.BAT, then reboot and check MEM /C."),
        ],
    },
    {
        "slug": "dosbox-mount-and-imgmount",
        "cat": "Guides",
        "h1": "DOSBox mount and imgmount: folders, images and drives",
        "title": "DOSBox mount and imgmount: folders, images and drives | ms-dos.su",
        "desc": "How MOUNT exposes a folder as a DOS drive and IMGMOUNT attaches a floppy, hard disk or ISO image in DOSBox, with examples and the 4 GB limit.",
        "lead": "DOSBox gives you a Z: drive and nothing else. To reach real files you mount a folder as a drive or attach a disk image. The commands look similar and behave very differently, and mixing them up is the usual reason a program cannot find its files.",
        "sections": [
            ("MOUNT: a folder becomes a drive", """<p><code>MOUNT</code> maps a host directory to a drive letter inside DOSBox. Files are read and written directly on the host, so changes are visible immediately on both sides.</p>
<pre>MOUNT C C:\\DOSGAMES
C:</pre>
<p>The first path is the DOS drive letter, the second is the host folder. Once mounted, <code>C:</code> switches to it and normal DOS commands work. A folder mounted this way is not a disk image: there is no partition table, no boot sector and no fixed-size volume.</p>"""),
            ("IMGMOUNT: an image becomes a drive", """<p><code>IMGMOUNT</code> attaches a disk image file. DOSBox reads the image as if it were physical media, which is what you need for bootable disks and for software that reads raw sectors.</p>
<pre>IMGMOUNT A C:\\IMAGES\\BOOT.IMG -t floppy
IMGMOUNT C C:\\IMAGES\\DOS622.IMG -t hdd
IMGMOUNT D C:\\IMAGES\\CD.ISO -t iso</pre>
<p>The <code>-t</code> parameter states the media type: <code>floppy</code>, <code>hdd</code> or <code>iso</code>. Getting it wrong produces a drive that mounts but cannot be read, because the geometry or sector size does not match. A hard disk image carries a partition table, and an ISO is a CD file system.</p>"""),
            ("Why a mounted image is not a written USB stick", """<p>Mounting an image in DOSBox changes the image file on your host disk. It does not touch any USB stick. To put the image on real media it has to be written by a tool that writes raw sectors, which is a separate step with its own risks: the target is erased, and the result depends on the BIOS booting from it.</p>
<p>MBFUTool 2.0 performs that step on Windows x64: it writes an MS-DOS image to a USB stick, creates an .mbfu image from a disk, floppy or USB device, clones MS-DOS media to a stick, and edits an image with DOS commands. It requires administrator rights, blocks writes to the system disk, and uses FAT16 up to 4 GB with about 2 GB practical. Paths must be latin-only. No MS-DOS files are shipped; you supply a lawful image, as described at <a href="https://ms-dos.su/en/ms-dos-license.html">ms-dos.su/en/ms-dos-license.html</a>.</p>"""),
            ("The [autoexec] section", """<p>Commands typed at the DOSBox prompt disappear when you exit. Put them in the <code>[autoexec]</code> section of <code>dosbox.conf</code> and they run at every start.</p>
<pre>[autoexec]
MOUNT C C:\\DOSGAMES
C:
SET PATH=C:\\;C:\\DOS</pre>
<p>Keep the section short and put the mount first, because later commands depend on the drive existing. A wrong path fails silently at startup, so test the MOUNT line by hand once.</p>"""),
            ("The 4 GB limit", """<p>DOSBox 0.72 cannot mount images larger than 4 GB. A larger image can be written to a stick by a Windows tool, but it cannot be attached in DOSBox 0.72 for testing or editing. Keep images at or below 4 GB, staying near 2 GB, which is a FAT16 size DOS handles comfortably. The MBFUTool trial runs 30 days with all features, offline and without a key; the full version is a one-time purchase on Boosty, one computer per licence.</p>"""),
        ],
        "faq": [
            ("Can I write to a mounted folder?", "Yes. MOUNT gives direct access to the host folder, so files created in DOSBox appear there immediately."),
            ("Why does my image mount but show no files?", "The -t type is probably wrong, or the image is not a DOS file system. Check whether it is floppy, hdd or iso."),
            ("Does IMGMOUNT write to my USB stick?", "No. It only reads and writes the image file on the host. Writing to a stick is a separate operation."),
        ],
        "howto": [
            ("Create a folder for your DOS files", "Make a directory on the host, for example C:\\DOSGAMES, and put the program files inside it."),
            ("Mount it", "Type MOUNT C C:\\DOSGAMES at the DOSBox prompt, then C: to switch to the new drive."),
            ("Or attach an image", "Use IMGMOUNT with the correct -t type for a floppy, hard disk or ISO image."),
            ("Make it permanent", "Add the same commands to the [autoexec] section of dosbox.conf so they run at every start."),
        ],
    },
]