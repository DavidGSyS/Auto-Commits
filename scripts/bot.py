#!/usr/bin/env python3
"""GitHub Auto-Commits Bot

A professional-grade bot that generates realistic GitHub contribution patterns
by creating commits with varying frequencies and timestamps.

Usage:
    python scripts/bot.py                    # Generate commits for the last 365 days
    python scripts/bot.py --days 180         # Generate commits for the last 180 days
    python scripts/bot.py --dry-run          # Preview without committing
    python scripts/bot.py --max-commits 5    # Max 5 commits per day

Author: Auto-Commits Bot
License: MIT
"""

import os
import sys
import io
import json

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
import random
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config.json"
CONTRIBUTIONS_DIR = ROOT_DIR / "contributions"
CONTRIBUTIONS_FILE = CONTRIBUTIONS_DIR / "data.txt"
LOG_FILE = CONTRIBUTIONS_DIR / "bot.log"

# Realistic commit message templates
COMMIT_MESSAGES = [
    "refactor: improve code structure and readability",
    "feat: add new utility function",
    "fix: resolve edge case in data processing",
    "docs: update documentation",
    "chore: clean up unused imports",
    "style: format code according to standards",
    "perf: optimize algorithm performance",
    "test: add unit tests for core module",
    "build: update dependencies",
    "ci: improve pipeline configuration",
    "feat: implement new feature module",
    "fix: correct calculation logic",
    "refactor: extract reusable components",
    "docs: add inline code comments",
    "chore: update configuration files",
    "style: apply consistent formatting",
    "perf: reduce memory usage",
    "test: improve test coverage",
    "build: configure build optimization",
    "feat: enhance error handling",
]


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


def print_banner():
    """Display a professional ASCII banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║     🤖  AUTO-COMMITS BOT  v2.0                    ║
    ║     ─────────────────────────                      ║
    ║     GitHub Contribution Generator                  ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)


def log(message: str, level: str = "INFO"):
    """Log a message with timestamp and level."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    color_map = {
        "INFO": Colors.BLUE,
        "SUCCESS": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "STEP": Colors.CYAN,
    }
    color = color_map.get(level, Colors.RESET)
    
    icon_map = {
        "INFO": "ℹ️ ",
        "SUCCESS": "✅",
        "WARNING": "⚠️ ",
        "ERROR": "❌",
        "STEP": "▶️ ",
    }
    icon = icon_map.get(level, "  ")
    
    formatted = f"{Colors.DIM}[{timestamp}]{Colors.RESET} {color}{icon} {message}{Colors.RESET}"
    print(formatted)
    
    # Also write to log file
    try:
        CONTRIBUTIONS_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
    except Exception:
        pass


def load_config() -> dict:
    """Load configuration from config.json or return defaults."""
    defaults = {
        "max_commits_per_day": 10,
        "min_commits_per_day": 0,
        "days_back": 365,
        "branch": "main",
        "commit_hour_start": 9,
        "commit_hour_end": 23,
        "skip_weekends_probability": 0.3,
        "git_username": "Auto-Commits Bot",
        "git_email": "bot@autocommits.dev",
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            defaults.update(user_config)
            log("Configuration loaded from config.json", "INFO")
        except (json.JSONDecodeError, IOError) as e:
            log(f"Error loading config.json: {e}. Using defaults.", "WARNING")
    else:
        log("No config.json found. Using default configuration.", "INFO")
    
    return defaults


def run_git_command(command: str, check: bool = True) -> str:
    """Execute a git command and return stdout."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR),
        )
        if check and result.returncode != 0:
            log(f"Git command failed: {command}", "ERROR")
            log(f"stderr: {result.stderr.strip()}", "ERROR")
        return result.stdout.strip()
    except Exception as e:
        log(f"Exception running command: {e}", "ERROR")
        return ""


def setup_git(config: dict):
    """Configure git user identity."""
    log("Configuring git identity...", "STEP")
    run_git_command(f'git config user.name "{config["git_username"]}"')
    run_git_command(f'git config user.email "{config["git_email"]}"')
    log(f"Git user: {config['git_username']} <{config['git_email']}>", "INFO")


def make_commit(date: datetime, message: str, dry_run: bool = False):
    """Create a single commit with a specific date and message."""
    CONTRIBUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    if dry_run:
        log(f"[DRY RUN] Would commit: {date.strftime('%Y-%m-%d %H:%M')} → {message}", "INFO")
        return True
    
    # Append contribution entry
    with open(CONTRIBUTIONS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{date.isoformat()} | {message}\n")
    
    # Stage the file
    run_git_command(f"git add {CONTRIBUTIONS_FILE}")
    
    # Commit with the specific date
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Use environment variables for commit date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            cwd=str(ROOT_DIR),
            env=env,
        )
        return result.returncode == 0
    except Exception as e:
        log(f"Commit failed: {e}", "ERROR")
        return False


def generate_commits(
    days_back: int = 365,
    max_commits: int = 10,
    min_commits: int = 0,
    dry_run: bool = False,
    config: dict = None,
):
    """Generate realistic commit patterns over a date range."""
    if config is None:
        config = load_config()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
    hour_start = config.get("commit_hour_start", 9)
    hour_end = config.get("commit_hour_end", 23)
    skip_weekend_prob = config.get("skip_weekends_probability", 0.3)
    
    log(f"Date range: {start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')}", "INFO")
    log(f"Max commits/day: {max_commits} | Min commits/day: {min_commits}", "INFO")
    log(f"Active hours: {hour_start}:00 - {hour_end}:00", "INFO")
    
    if dry_run:
        log("🔍 DRY RUN MODE — No changes will be made", "WARNING")
    
    print()
    
    current_date = start_date
    total_commits = 0
    total_days = (end_date - start_date).days + 1
    days_with_commits = 0
    
    while current_date <= end_date:
        # Skip some weekends for realism
        is_weekend = current_date.weekday() >= 5
        if is_weekend and random.random() < skip_weekend_prob:
            current_date += timedelta(days=1)
            continue
        
        # Weighted random: more likely to have moderate commits
        weights = []
        for i in range(min_commits, max_commits + 1):
            if i == 0:
                weights.append(2)
            elif i <= 3:
                weights.append(5)
            elif i <= 6:
                weights.append(3)
            else:
                weights.append(1)
        
        num_commits = random.choices(
            range(min_commits, max_commits + 1), weights=weights, k=1
        )[0]
        
        if num_commits > 0:
            days_with_commits += 1
        
        for i in range(num_commits):
            hour = random.randint(hour_start, hour_end)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            commit_date = current_date.replace(
                hour=hour, minute=minute, second=second, microsecond=0
            )
            
            message = random.choice(COMMIT_MESSAGES)
            
            success = make_commit(commit_date, message, dry_run=dry_run)
            if success:
                total_commits += 1
        
        # Progress indicator
        progress = int(((current_date - start_date).days / total_days) * 100)
        bar_length = 30
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(
            f"\r  {Colors.CYAN}Progress: [{bar}] {progress}%{Colors.RESET}  "
            f"{Colors.DIM}({total_commits} commits){Colors.RESET}",
            end="",
            flush=True,
        )
        
        current_date += timedelta(days=1)
    
    print()  # New line after progress bar
    print()
    
    return total_commits, days_with_commits, total_days


def push_to_remote(branch: str = "main"):
    """Push commits to the remote repository."""
    log(f"Pushing to origin/{branch}...", "STEP")
    result = run_git_command(f"git push origin {branch}")
    if "error" in result.lower() or "fatal" in result.lower():
        log("Push failed. Make sure remote is configured.", "ERROR")
        return False
    log("Successfully pushed to remote!", "SUCCESS")
    return True


def print_summary(total_commits: int, days_with_commits: int, total_days: int):
    """Display a formatted summary of the bot run."""
    print(f"""
{Colors.GREEN}{Colors.BOLD}
    ┌─────────────────────────────────────────┐
    │           📊 RUN SUMMARY                │
    ├─────────────────────────────────────────┤
    │  Total commits:     {str(total_commits).rjust(8)}            │
    │  Days with commits: {str(days_with_commits).rjust(8)}            │
    │  Total days:        {str(total_days).rjust(8)}            │
    │  Avg commits/day:   {str(round(total_commits / max(total_days, 1), 1)).rjust(8)}            │
    └─────────────────────────────────────────┘
{Colors.RESET}""")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="🤖 Auto-Commits Bot — Generate realistic GitHub contributions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/bot.py                    Generate commits for the last 365 days
  python scripts/bot.py --days 180         Generate commits for the last 180 days
  python scripts/bot.py --dry-run          Preview mode (no actual commits)
  python scripts/bot.py --max-commits 5    Limit to 5 commits per day
        """,
    )
    parser.add_argument(
        "--days", type=int, default=None,
        help="Number of days back to generate commits (default: from config or 365)",
    )
    parser.add_argument(
        "--max-commits", type=int, default=None,
        help="Maximum commits per day (default: from config or 10)",
    )
    parser.add_argument(
        "--min-commits", type=int, default=None,
        help="Minimum commits per day (default: from config or 0)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview commits without actually creating them",
    )
    parser.add_argument(
        "--no-push", action="store_true",
        help="Generate commits but don't push to remote",
    )
    parser.add_argument(
        "--branch", type=str, default=None,
        help="Branch to push to (default: from config or 'main')",
    )
    return parser.parse_args()


def main():
    """Main entry point."""
    print_banner()
    
    args = parse_args()
    config = load_config()
    
    # CLI args override config
    days_back = args.days or config.get("days_back", 365)
    max_commits = args.max_commits if args.max_commits is not None else config.get("max_commits_per_day", 10)
    min_commits = args.min_commits if args.min_commits is not None else config.get("min_commits_per_day", 0)
    branch = args.branch or config.get("branch", "main")
    dry_run = args.dry_run
    
    # Setup
    if not dry_run:
        setup_git(config)
    
    # Generate
    log("Starting commit generation...", "STEP")
    total_commits, days_with_commits, total_days = generate_commits(
        days_back=days_back,
        max_commits=max_commits,
        min_commits=min_commits,
        dry_run=dry_run,
        config=config,
    )
    
    # Summary
    print_summary(total_commits, days_with_commits, total_days)
    
    # Push
    if not dry_run and not args.no_push and total_commits > 0:
        push_to_remote(branch)
    elif dry_run:
        log("Dry run complete. No commits were created.", "INFO")
    elif args.no_push:
        log("Commits generated locally. Use 'git push' to push manually.", "INFO")
    
    log("Bot finished. 🎉", "SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
