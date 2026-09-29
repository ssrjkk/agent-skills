#!/usr/bin/env bash
set -euo pipefail

# Claude Skills Library — Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/ssrjkk/agent-skills/main/install.sh | bash

REPO="ssrjkk/agent-skills"
BRANCH="main"
INSTALL_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"

echo " Installing Claude Skills Library..."
echo " Target: $INSTALL_DIR"

# Check for git
if ! command -v git &>/dev/null; then
    echo " git is required. Install it first: https://git-scm.com/downloads"
    exit 1
fi

# Check for Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "  Python 3.9+ recommended for SDK tools"
    echo "   Install: https://python.org/downloads/"
fi

# Clone or update
if [ -d "$INSTALL_DIR/.git" ]; then
    echo " Updating existing installation..."
    cd "$INSTALL_DIR"
    git pull origin "$BRANCH"
else
    echo " Cloning repository..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone --depth 1 --branch "$BRANCH" "https://github.com/$REPO.git" "$INSTALL_DIR"
fi

# Install Python SDK
if command -v pip3 &>/dev/null; then
    echo " Installing Python SDK..."
    pip3 install "$INSTALL_DIR" 2>/dev/null || true
elif command -v pip &>/dev/null; then
    echo " Installing Python SDK..."
    pip install "$INSTALL_DIR" 2>/dev/null || true
fi

echo ""
echo " Claude Skills Library installed!"
echo ""
echo " Stats:"
if command -v claude-skills &>/dev/null; then
    claude-skills stats
elif [ -f "$INSTALL_DIR/scripts/list-skills.py" ]; then
    cd "$INSTALL_DIR" && python scripts/list-skills.py
fi
echo ""
echo " Usage:"
echo "   cd $INSTALL_DIR"
echo "   make validate    # Validate all skills"
echo "   make quality     # Quality analysis"
echo "   make stats       # Show statistics"
echo ""
echo " Add skills to your Claude Code workflow:"
echo '   export CLAUDE_SKILLS_DIR="$HOME/.claude/skills"'
