# Getting Started

Welcome to the **Shell-style SVG Profile Generator** – a Python tool that creates beautiful, terminal-style SVG profiles for your GitHub README, automatically updated with your latest stats and information.

## Overview

This tool generates a customizable SVG image that displays your developer profile in a terminal/ricing aesthetic. The image includes:

- **System Info**: OS, uptime (calculated from birthday), current job position, and company
- **Development**: Programming languages, used tools, and IDE preferences
- **GitHub Stats**: Repositories, commits, stars, and followers (auto-updated!)
- **Contact**: Email, website, LinkedIn, and work contact

The SVG is designed to be embedded in your GitHub profile README and can be automatically updated via GitHub Actions to keep your stats current.

## Quick Start

### 1. Clone the Repository

The idea is that you can simply fork this repository and rename it to your Github's username to start customizing it.

```bash
git clone https://github.com/ItsShunya/ItsShunya.git <your_username>
cd <your_username>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your Profile

Create your configuration file in `config/YourUsername.yaml`:

```yaml
User:
  Username: "YourGitHubUsername"
  Name: "FirstName"
  Surname: "LastName"
  Birthday: "YYYY-MM-DD"  # Used to calculate uptime
  Operative_System: "Your OS"  # e.g., "NixOS", "Arch Linux", "macOS"
  Position: "Your Job Title"
  Company: "Your Company"
  IDE: "Your Editor"  # e.g., "VSCode", "Neovim", "IntelliJ"

Languages:
  Programming:
    - "C"
    - "Python"
    - "JavaScript"
    # Add your languages here
  Other:
    - "Bash"
    - "SQL"
    # Scripts, query languages, etc.
  Real:
    - "English"
    - "Spanish"
    # Human languages you speak

Activities:
  Software:
    - "Embedded"
    - "Web Development"
    - "ML/AI"
    # Your software development areas
  Hardware:
    - "Embedded"
    - "RTOS"
    - "PCB"
    # Hardware skills (if applicable)
  Other:
    - "Swimming"
    - "Photography"
    # Hobbies and interests

Contact:
  Personal_Mail: "your.email@example.com"
  Web: "https://yourwebsite.com"
  Work_Mail: "work@company.com"
  Linkedin: "https://linkedin.com/in/yourprofile"
```

### 4. Set Up GitHub Token (local development)

Create a `.env` file in the root directory with the following format:

```bash
ACCESS_TOKEN=<github_access_token>
USER_NAME=<github_username>
OUTPUT_PATH=./output
```

The Github access token is used to fetch your personal stats (commits, repo, stars, etc) from the Github's GraphQL API.

**To create a GitHub token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `read:user`, `public_repo`
4. Copy the token to your `.env` file

### 5. Generate Your Profile

```bash
python src/main.py
```

Your SVG will be generated at `output/profile.svg`!

## Customization

### Themes

The tool comes with several built-in color themes:

- **Tokyo Night** 
- **Dracula**
- **Nord**
- **Gruvbox Dark**
- **Monokai**
- **Catppuccin Mocha** (default)

To change the theme, modify the theme selection in your config or the `SvgGenerator` initialization.

### ASCII Banner

You can customize the ASCII art banner displayed in your profile:

1. Edit `ascii/banner.py` to add your own banner
2. Or choose from existing banners by changing `DEFAULT_BANNER`

### Layout

Modify `main.py` to:
- Reorder sections
- Add/remove information fields
- Adjust spacing and positioning
- Add custom elements

## Automatic Updates (GitHub Actions)

To keep your GitHub stats fresh, set up automatic updates:

### 1. Create GitHub Action Workflow

Create `.github/workflows/update-profile.yml`:

```yaml
name: Update profile

on:
  push:
    branches:
      - main
  schedule:
    - cron: "0 4 * * *"

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Get Python
        uses: actions/setup-python@v5

      - name: Configure pip cache
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/cache/requirements.txt') }}
          restore-keys: ${{ runner.os }}-pip-

      - name: Install dependencies
        run: python -m pip install -r cache/requirements.txt
        
      - name: Update README file
        env:
          ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}
          USER_NAME: ${{ secrets.USER_NAME }}
        run: python src/main.py

      - name: Commit
        run: |-
          git add .
          git diff
          git config --global user.email "github-actions-bot@<your-username>.github.io"
          git config --global user.name "<your-username>/GitHub-Actions-Bot"
          git commit -m "Updated PROFILE" -a || echo "No changes to commit"
          git push

```

### 2. Add Repository Secrets

Go to your repository Settings → Secrets and variables → Actions, and add:

- `ACCESS_TOKEN`: Your GitHub personal access token
- `USER_NAME`: Your GitHub username

### 3. Embed in Your Profile README

Add this to your GitHub profile README.md:

```markdown
![Profile](https://raw.githubusercontent.com/yourusername/riced-shell-profile/main/output/profile.svg)
```

Or as a link:

```markdown
[![Profile](https://raw.githubusercontent.com/yourusername/riced-shell-profile/main/output/profile.svg)](https://github.com/yourusername)
```

## Project Structure

```
.
├── config/              # YAML configuration files
│   └── YourUsername.yaml
├── ascii/               # ASCII art and logos
│   ├── banner.py
│   └── logos.py
├── svg/                 # SVG generation logic
│   └── svg_generator.py
├── graphql/             # GitHub API queries
│   └── github.py
├── utils/               # Utility functions
│   ├── format.py
│   ├── time.py
│   └── timer.py
├── themes/              # Color schemes
│   └── themes.py
├── output/              # Generated SVG files
│   └── profile.svg
├── main.py              # Main entry point
└── requirements.txt     # Python dependencies
```

## Configuration Fields Explained

| Field | Description | Example |
|-------|-------------|---------|
| `Username` | Your GitHub username (used for API queries) | `"ItsShunya"` |
| `Name` | Your first name | `"Victor"` |
| `Surname` | Your last name | `"Luque"` |
| `Birthday` | Date of birth (calculates "uptime") | `"1998-05-26"` |
| `Operative_System` | Your primary OS | `"NixOS"` |
| `Position` | Your job title/role | `"Embedded Software Engineer"` |
| `Company` | Where you work | `"INBRAIN Neuroelectronics"` |
| `IDE` | Your preferred code editor | `"VSCode"` |
| `Languages.Programming` | Programming languages you use | `["C", "Python"]` |
| `Languages.Other` | Scripts, markup, query languages | `["Bash", "SQL"]` |
| `Languages.Real` | Human languages you speak | `["English", "Spanish"]` |
| `Activities.Software` | Software development areas | `["Embedded", "ML/AI"]` |
| `Activities.Hardware` | Hardware skills | `["PCB", "RTOS"]` |
| `Activities.Other` | Hobbies and interests | `["Swimming"]` |
| `Contact.*` | Your contact information | Various URLs/emails |

## GitHub Stats

The tool automatically fetches and displays:

- **Total Repositories**: Public repos you own
- **Contributed Repos**: Repos where you're a collaborator
- **Total Commits**: Commits in the last 7 days
- **Total Stars**: Stars across all your repos
- **Followers**: Your GitHub follower count

These stats are fetched via GitHub's GraphQL API and update automatically when you regenerate the SVG.

## Troubleshooting

### GitHub API Rate Limits

If you hit rate limits:
- Ensure your `GITHUB_TOKEN` is set correctly
- Authenticated requests have higher limits (5,000/hour vs 60/hour)

### SVG Not Updating

- Check GitHub Actions logs for errors
- Verify repository secrets are set correctly
- Ensure the workflow has write permissions

### Missing Dependencies

```bash
pip install --upgrade -r requirements.txt
```