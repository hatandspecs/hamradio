---
layout: default
title: WSJT-X on Fedora Linux for the Yaesu FTX-1
category: article
date: 2026-04-26
---

This guide details the steps required to configure a stable WSJT-X environment on Fedora Linux for use with the Yaesu FTX-1. The process focuses on three specific technical areas: time synchronization, hardware access, and audio stream persistence.

### Technical Requirements for WSJT-X on Fedora Linux

#### 1. Time Synchronization
Digital modes like FT8 require the system clock to be synchronized within approximately 500 milliseconds of UTC. Fedora uses `chrony` as the default Network Time Protocol (NTP) client. The configuration process involves enabling the `chronyd` service and forcing an immediate synchronization (stepping the clock) to ensure the offset is minimized before the software begins decoding.



#### 2. Hardware Access and Service Conflicts
Standard Linux distributions often run a service called `brltty` to support Braille displays. This service frequently misidentifies USB-to-serial converters (such as those used for CAT control in Yaesu radios) and prevents other applications from accessing the serial port. The setup process involves masking this service. Additionally, the user account must be added to the `dialout` and `audio` groups to permit direct access to the radio's serial interface and sound card.

#### 3. Audio Stream Persistence
Fedora’s modern audio stack, PipeWire, typically suspends audio nodes when they are idle to conserve power. This can cause a delay in the transition from receive to transmit, which may clip the start of a transmission. To prevent this, a custom WirePlumber rule is created to disable the "suspend-on-idle" feature for ALSA nodes.

#### 4. Package Management and Version Control
To ensure stability, the process involves removing any pre-release or experimental builds of WSJT-X. The standard General Availability (GA) version is installed alongside the latest `hamlib` libraries. Once installed, the WSJT-X package is locked using the `dnf versionlock` plugin to prevent the system from automatically updating to a potentially unstable future release.



---

### Implementation Script

The following script automates the installation and configuration described above.

```bash
#!/bin/bash
set -e

# --- CONFIGURATION ---
# Target the stable General Availability (GA) version
STABLE_WSJTX="wsjtx"
echo "--- WSJT-X STABLE CONFIGURATOR for KD3CCO ---"

# 1. HARDWARE & SPACE DETECTION
echo "Step 1: Analyzing system..."
CPU_CORES=$(nproc)
echo "Detected: ${CPU_CORES} CPU Cores. Ready for decoding."

# 2. THE TOTAL RESET
echo "Step 2: Removing experimental/pre-release versions..."
# Unlocking first ensures we can actually remove it
sudo dnf versionlock delete wsjtx 2>/dev/null || true
sudo dnf remove -y wsjtx hamlib hamlib-utils hamlib-devel 2>/dev/null || true
sudo dnf clean all

# 3. INSTALL STABLE VERSION
echo "Step 3: Installing Stable WSJT-X and core Hamlib..."
# Removed hamlib-utils as it is now integrated into hamlib
sudo dnf install -y wsjtx hamlib chrony pavucontrol 'dnf-command(versionlock)'

# 4. ENSURE LATEST RIG DEFINITIONS
echo "Step 4: Ensuring Hamlib is up to date..."
# This ensures you have the latest Yaesu FTX-1 definitions
sudo dnf upgrade -y hamlib

# 5. VERSION LOCK
# This prevents dnf update from accidentally pulling in a future beta/RC version
echo "Step 5: Locking WSJT-X to the current stable release..."
sudo dnf versionlock add wsjtx

# 6. PERMISSIONS & RIG CONTROL FIX
echo "Step 6: Configuring USB/Serial and masking conflicts..."
# dialout for CAT control; audio for PipeWire/Alsa access
sudo usermod -a -G dialout,audio $USER
# Disable brltty (common conflict with USB-to-Serial adapters)
sudo systemctl mask brltty || true

# 7. TIME SYNC (The 'FT8 Heartbeat')
echo "Step 7: Calibrating sub-second time accuracy via Chronyd..."
sudo systemctl enable --now chronyd
sudo chronyc -a makestep

# 8. AUDIO ENGINE OPTIMIZATION (PipeWire Fix)
# This prevents your rig's audio from 'sleeping' during RX/TX gaps
echo "Step 8: Applying PipeWire idle-suspend fix..."
mkdir -p ~/.config/wireplumber/wireplumber.conf.d
cat <<EOF > ~/.config/wireplumber/wireplumber.conf.d/50-no-suspend.conf
monitor.alsa.rules = [
  {
    matches = [ { node.name = "~alsa_input.*" }, { node.name = "~alsa_output.*" } ],
    actions = { update-props = { session.suspend-on-idle = false } }
  }
]
EOF

# 9. OS GUI INTEGRATION
echo "Step 9: Finalizing menu shortcuts..."
mkdir -p ~/.local/share/applications
if [ -f /usr/share/applications/wsjtx.desktop ]; then
    cp /usr/share/applications/wsjtx.desktop ~/.local/share/applications/
fi

echo "-------------------------------------------------------"
echo "STABLE INSTALL COMPLETE: KD3CCO STATION READY"
echo "Current Hamlib Version: $(rigctl --version | head -n 1)"
echo "-------------------------------------------------------"
echo "1. REBOOT/LOGOUT: Required for USB 'dialout' permissions."
echo "2. VERIFY SYNC: Run 'chronyc tracking' to ensure < 100ms offset."
echo "-------------------------------------------------------"

read -p "Launch WSJT-X and Volume Control now? (y/n) " choice
if [[ "$choice" =~ ^[Yy]$ ]]; then
    wsjtx &
    pavucontrol &
fi
```

---

### Instructions for Execution

1.  **Create the script file:**
    Use a text editor to create a new file named `configure_wsjtx.sh`.
2.  **Make the script executable:**
    Before the script can be run, it needs the correct permissions. Run the following command in your terminal:
    `chmod +x configure_wsjtx.sh`
3.  **Run the script:**
    Execute the script with the following command:
    `./configure_wsjtx.sh`
4.  **Finalize Permissions:**
    Once the script completes, you must **log out and log back in** to your Fedora session. This ensures that the new group permissions for `dialout` and `audio` are applied to your user account.


# WSJT-X Radio Settings for the Yaseu FTX-1

Radio Settings that worked for my FTX-1:

| Parameter | Setting |
| :--- | :--- |
| **Rig** | Yaesu FT-991 |
| **Serial Port** | /dev/ttyUSB0 |
| **Baud Rate** | 38400 |
| **Data Bits** | Eight |
| **Stop Bits** | Two |
| **Handshake** | None |
| **Force Control Lines** | no selections |
| **PTT Method** | CAT |
| **Port** | /dev/ttyACM0 |
| **Transmit Audio Source** | Front/Mic |
| **Mode** | Data |
| **Split Operation** | Fake it |


# Testing my WSJT-X Configuration using WSPR mode
Please see the following article:
[How to use WSPR with WSJT-X](../using_wspr_wsjtx/)