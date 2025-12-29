---
name: git-pushing
description: Stage, commit, and push git changes with conventional commit messages. Use when user wants to commit and push changes, mentions pushing to remote, or asks to save and push their work. Also activates when user says "push changes", "commit and push", "push this", "push to github", or similar git workflow requests.
---

# Git Push Workflow

Stage all changes, create a conventional commit, and push to the remote branch.

## When to Use

Automatically activate when the user:
- Explicitly asks to push changes ("push this", "commit and push")
- Mentions saving work to remote ("save to github", "push to remote")
- Completes a feature and wants to share it
- Says phrases like "let's push this up" or "commit these changes"

## Workflow

**ALWAYS use the script** - do NOT use manual git commands:

```bash
bash .claude/skills/git-pushing/scripts/smart_commit.sh
```

With custom message:
```bash
bash .claude/skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
```

Script handles: staging, conventional commit message, Claude footer, push with -u flag.

## Authentication Setup

**Recommended: Use HTTPS with Personal Access Token**

The script automatically checks for SSH URL rewrites and uses HTTPS for authentication:

1. Remote URLs should use HTTPS format: `https://github.com/username/repo.git`
2. Git will prompt for credentials or use stored credentials
3. If you have a global SSH rewrite (`url.git@github.com:.insteadOf`), the script will warn you

**To configure HTTPS authentication:**
```bash
# Set remote to HTTPS
git remote set-url origin https://github.com/username/repo.git

# Store credentials (optional)
git config --global credential.helper store
```

## Security Checks

**Automatic security scanning** runs before every push to detect:

- ❌ Internal hourly rates (e.g., `$200-$250/hr`)
- ❌ Client names in code examples
- ❌ Client-specific file paths (e.g., `User-Files/work-tracking/client-name/`)
- ❌ Company branding in generic examples
- ❌ Forbidden document types (.docx proposals, contracts, etc.)

**Configure patterns:** Edit `.claude/skills/git-pushing/scripts/security_patterns.conf`

**Bypass security check** (NOT recommended):
```bash
SKIP_SECURITY_CHECK=1 bash .claude/skills/git-pushing/scripts/smart_commit.sh
```

## Edge Cases Handled

- **No commits yet**: Script handles repos with no HEAD gracefully
- **SSH rewrites**: Detects and warns about global SSH URL rewrites
- **New branches**: Automatically uses `-u` flag for first push
- **No changes**: Exits gracefully if nothing to commit
- **Sensitive data**: Blocks push if sensitive patterns detected
