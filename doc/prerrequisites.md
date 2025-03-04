# How to Install Git

## Windows
1. Download the Git installer from the official website:
   - [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer and follow the setup instructions:
   - Choose the default editor for Git (e.g., Vim, Notepad++, or VS Code).
   - Select how Git should handle line endings (recommended: Checkout Windows-style, commit Unix-style).
   - Choose the default terminal emulator (recommended: Use MinTTY for better compatibility).
3. Complete the installation and open **Git Bash** or **Command Prompt** to verify:
   ```sh
   git --version
   ```

## macOS
1. Install Git via Homebrew (recommended):
   ```sh
   brew install git
   ```
2. Alternatively, install it from the official Git website:
   - [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
3. Verify the installation:
   ```sh
   git --version
   ```

## Linux (Debian/Ubuntu)
1. Update package lists:
   ```sh
   sudo apt update
   ```
2. Install Git:
   ```sh
   sudo apt install git -y
   ```
3. Verify the installation:
   ```sh
   git --version
   ```

## Linux (Fedora/RHEL)
1. Install Git using DNF:
   ```sh
   sudo dnf install git -y
   ```
2. Verify the installation:
   ```sh
   git --version
   ```

## Initial Git Configuration
After installation, set up your Git user information:
```sh
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```
To check your Git configuration:
```sh
git config --list
```

Now Git is ready to use!
