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

## Weak Signal Propagation Reporter (WSPR)

The Weak Signal Propagation Reporter, or **WSPR** (pronounced "whisper"), is a digital protocol designed for probing radio propagation paths using very low-power transmissions. Unlike other digital modes intended for two-way communication, WSPR is primarily a beaconing system.

### Purpose and Interest
Operators use WSPR to assess the performance of their station and to monitor real-time ionospheric conditions. Because the protocol utilizes a highly narrow bandwidth (approximately 6 Hz) and advanced forward error correction, it can be decoded even when the signal is significantly below the noise floor—often at Signal-to-Noise Ratios (SNR) as low as -28 dB.

This mode is of particular interest to amateur radio operators for several reasons:
* **Antenna Evaluation:** By transmitting at a fixed low power (typically 200mW to 5W) and checking global reception reports, an operator can determine the efficiency and radiation pattern of a new antenna design.
* **Propagation Mapping:** It provides a data-driven look at which bands are "open" to specific geographic regions without requiring a human operator on the other end to acknowledge a call.
* **Scientific Contribution:** The data generated by WSPR "spots" is often used by researchers to study the behavior of the ionosphere and the impact of solar activity on radio waves.

### History of WSPR
WSPR was released in 2008 by Dr. Joe Taylor, K1JT, a Nobel Prize-winning astrophysicist. It was developed to apply sophisticated digital signal processing techniques to the problem of weak-signal VHF/UHF and HF propagation. It has since become a standard tool in the amateur radio community, with thousands of automated stations providing a continuous stream of propagation data to global databases.

For further technical details, see the [WSPR Wikipedia page](https://en.wikipedia.org/wiki/WSPR_(amateur_radio_software)).

---

### WSJT-X Configuration for WSPR

These notes outline the standard configuration and calibration process for WSPR operations using WSJT-X.

#### 1. Input Level Calibration (Receive)
The green vertical bar in the lower-left corner monitors audio input.
* **Target Range:** Aim for 30 to 50 dB.
* **Red Zone:** If the meter shows red, reduce input gain immediately to prevent distortion.
* **Adjustment:** Use your operating system's sound mixer or the interface device properties.

#### 2. Power Settings (Metadata)
The Power (dBm) field in the Settings menu (General tab) is for database reporting, not hardware control.
* **10 Watts:** Set to 40 dBm.
* **5 Watts:** Set to 37 dBm.
* **Important:** Ensure this value is updated if you change your radio's physical transmit power.

#### 3. Transmit Audio Calibration (Output)
Use the 'Tune' function to calibrate the vertical Pwr slider (lower right) to achieve your target RF output power without overdriving the radio.
1. **Prepare:** Set your radio to the desired RF output power (e.g., 10W).
2. **Tune:** Click the 'Tune' button in WSJT-X to emit a continuous carrier.
3. **Adjust:** Move the Pwr slider until your radio's power meter reads the target output.
4. **Monitor ALC:** Verify the radio's ALC meter. If the ALC is high or pegged, reduce the Pwr slider and increase the radio's own gain control to compensate until power is steady with minimal ALC.
5. **Finish:** Click 'Tune' again to stop.

#### 4. Band Hopping
Band hopping allows automated monitoring across multiple bands.
* **Setup:** Navigate to Settings > Band Hopping (or the Band Hopping tab).
* **Configuration:** Select the desired bands.
* **Activation:** Check the 'Band Hop' box in the main window.
* **Mechanism:** The software will cycle through selected bands during the 2-minute transmit/receive intervals.



---

## Results

Initial testing confirms that the WSJT-X configuration is fully operational on the Fedora workstation. The system utilizes a single USB-C connection to the Yaesu FTX-1, which handles three primary functions:
1.  **CAT Control:** The software successfully manages the VFO (Frequency), mode switching, and PTT (Push-to-Talk) via the virtual serial port.
2.  **Audio Input (RX):** Audio from the radio is routed to the computer for decoding.
3.  **Audio Output (TX):** Modulated digital tones are sent from the computer to the radio for transmission.

### Audio Gain Staging
Achieving a clean signal required careful "gain staging" across several software and hardware layers. In digital modes, overdriving the audio results in "splatter" or harmonics that interfere with other operators. The following settings were adjusted to achieve the correct ALSA levels:
* **WSJT-X "PWR" Slider:** This acts as the primary fine-tuning control for the audio output level sent to the radio.
* **OS Volume Mixer:** Both the input (Capture) and output (Playback) levels in Fedora’s volume control must be set to a point where the signal is strong but not clipping.
* **Radio Menu Settings:** The "USB Gain" setting on the Yaesu FTX-1 was adjusted to calibrate the incoming audio from the computer.

To contribute to the global propagation map, the **"Upload Spots"** option must be enabled in the WSJT-X settings. This sends decodes to the [WSPRnet](https://www.wsprnet.org) database.

### Station Documentation
The following screenshot illustrates WSJT-X running in WSPR mode, successfully decoding multiple stations across the passband.

<img src="{{ '/assets/images/wspr-wsjtx-2026-04-26 16-51.png' | relative_url }}" alt="WSJT-X Running WSPR" width="600">

By utilizing [WSPR Rocks](https://wspr.rocks), it is possible to generate a graphical representation of station performance. Filtering by "TX Call" using callsign **KD3CCO** displays a map of every station that successfully decoded my beacon. This provides an objective measure of my transmitter's reach and current propagation. Conversely, filtering by "RX Call" displays the locations of the beacons my station was able to hear and decode.

The map below shows the TX spot reports for the initial test session.

<img src="{{ '/assets/images/wsprrocks_20260426-172319.png' | relative_url }}" alt="WSPR Rocks TX Map" width="600">