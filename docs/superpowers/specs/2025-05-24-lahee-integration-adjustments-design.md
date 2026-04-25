# Design: LAHEE Integration Adjustments

## 1. Server Lifecycle: First-Launch Initialization
- **Requirement:** The LAHEE server must only be initialized the **first time** EmulationStation is launched during a console session.
- **Persistence:** Once started, the server should remain active throughout the session (even when ES restarts after a game) until the hardware is shut down or rebooted.
- **Rationale:** Prevents multiple server instances and ensures a stable connection for RetroArch and other clients throughout the session.

## 2. Centralized Data Storage (`RetroAchievements` Folder)
- **Location:** At the root of the partition used for games. ES will determine this path dynamically by referencing its own configured ROM directory (e.g., `EASYROMS/RetroAchievements/` or equivalent).
- **Internal Organization:**
    - **Console Subfolders:** Data is organized by console (e.g., `nes/`, `snes/`, `gbc/`).
    - **File Naming Convention:** Descriptive filenames for achievement data: `<GameID>-<Game Name>.set.json` (e.g., `1446-Super Mario Bros.set.json`).
- **Contents:**
    - **Console Folders:** Scraped achievement data (`.set.json`) and badge icons.
    - **Root Level:** Player profile data and avatars.
- **Rationale:** Facilitates user backups, manual management, and access for external scraping scripts.

## 3. Game Media: Icon Scraping
- **Convention:** Game icons (box art/icons for the ES menu) are treated as standard ES media types, following the same logic as marquees or screenshots.
- **Storage:** Saved to the system's local `images` folder (e.g., `nes/images/`).
- **Metadata:** Recorded in the `<icon>` tag within the `gamelist.xml` for the respective system.
- **Rationale:** Maintains consistency with existing ES media management workflows.
