# Repository Security Configuration

**Last Updated:** 2025-12-29
**Repository:** https://github.com/mbcoalson/skills
**Purpose:** Document security measures protecting sensitive company and client data

---

## Security Overview

This repository uses a **multi-layer defense-in-depth** approach to prevent sensitive data from being accidentally committed to the public GitHub repository.

### What We Protect Against

- ❌ Internal hourly rates (e.g., `$200-$250/hr`)
- ❌ Client names in code examples (Schomp, Real Atlas, SECC, etc.)
- ❌ Client-specific file paths (`User-Files/work-tracking/client-name/`)
- ❌ Company branding in generic examples ("Iconergy")
- ❌ Forbidden document types (`.docx` proposals, contracts, `.msi` installers)
- ❌ Environment files (`.env`, `.env.*`)
- ❌ Credential files (`credentials.json`)

---

## Security Layers

### Layer 1: Local Security Check (PRIMARY PROTECTION)

**Location:** `.claude/skills/git-pushing/scripts/security_check.sh`

**Trigger:** Runs automatically before every commit when using:
```bash
bash .claude/skills/git-pushing/scripts/smart_commit.sh
```

**What It Does:**
- Scans all staged files for sensitive patterns
- Blocks commit if sensitive data detected
- Fast (<1 second), runs locally
- Configurable via `.claude/skills/git-pushing/scripts/security_patterns.conf`

**Patterns Checked:**
```bash
# Hourly rates
\$[0-9]{2,3}[\-][0-9]{2,3}/hr

# Client names
"Schomp", "Real Atlas", "SECC"

# Client-specific paths
/secc-fort-collins/
/real-atlas/
/schomp/
User-Files/Opportunities/[A-Z]

# Forbidden files
work-documentation/references/*.docx
proposals/*.docx
contracts/*.docx
**/*.msi
```

**Bypass (Emergency Only):**
```bash
SKIP_SECURITY_CHECK=1 bash .claude/skills/git-pushing/scripts/smart_commit.sh
```

⚠️ **Warning:** Bypassing this check is your ONLY local protection. Use with extreme caution.

---

### Layer 2: GitHub Branch Rulesets

**Status:** ✅ ACTIVE
**Location:** Repository Settings → Rules → Rulesets
**Ruleset Name:** `Main Branch Protection + Sensitive Files`

**Target:** `main` branch (default branch)

**Enabled Rules:**

✅ **Restrict deletions**
- Prevents accidental deletion of `main` branch
- Only users with bypass permission can delete

✅ **Block force pushes**
- Prevents `git push --force`
- Protects commit history from being rewritten
- Prevents accidentally overwriting commits

✅ **Require a pull request before merging**
- Enforces PR workflow (even for solo developer)
- Required approvals: 0 (can self-approve)
- Creates review checkpoint before merging to `main`

**NOT Available (GitHub Free Tier Limitation):**

❌ **Restrict file paths**
- This feature is not available in the current GitHub plan
- Would have blocked specific file patterns server-side
- See "Future Enhancements" for alternatives

---

### Layer 3: .gitignore (FUTURE)

**Status:** ⚠️ NOT YET IMPLEMENTED

**Recommended Additions:**
```gitignore
# Sensitive files that should NEVER be committed
**/.env
**/.env.*
**/credentials.json
*.msi
*.exe

# Client-specific directories
User-Files/work-tracking/secc-fort-collins/
User-Files/work-tracking/real-atlas/
User-Files/work-tracking/schomp/
User-Files/Opportunities/*/

# Sensitive documents
**/work-documentation/references/*.docx
**/proposals/*.docx
**/contracts/*.docx
```

**To Implement:**
1. Add patterns to `.gitignore`
2. Commit and push
3. Test by trying to stage a sensitive file

---

### Layer 4: GitHub Actions (FUTURE)

**Status:** ⚠️ NOT YET IMPLEMENTED

**Purpose:** Server-side validation after push

**Proposed Workflow:** `.github/workflows/security-check.yml`

```yaml
name: Security Check
on: [push, pull_request]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Check for sensitive files
        run: |
          # Block .env files
          if git ls-files | grep -E '\\.env$'; then
            echo "❌ .env files detected"
            exit 1
          fi

          # Block client folders
          if git ls-files | grep -E 'User-Files/work-tracking/.+/'; then
            echo "❌ Client-specific folders detected"
            exit 1
          fi

          # Block credentials
          if git ls-files | grep -E 'credentials\\.json$'; then
            echo "❌ Credentials file detected"
            exit 1
          fi

          echo "✅ No sensitive files detected"
```

**Benefits:**
- Runs on every push automatically
- Blocks merges if sensitive files detected
- Works even if local check is bypassed
- Free for public repositories

---

## Testing Security Protections

### Test 1: Local Security Check

**Test blocking sensitive file:**
```bash
# Create a test .env file
echo "SECRET_KEY=test123" > .env

# Try to commit (should be blocked)
bash .claude/skills/git-pushing/scripts/smart_commit.sh

# Expected: Security check fails, commit blocked

# Clean up
rm .env
```

**Test blocking client name:**
```bash
# Create file with client name
echo "Project for Schomp Nissan" > test-client.md

# Try to commit (should be blocked)
bash .claude/skills/git-pushing/scripts/smart_commit.sh

# Expected: Security check fails, commit blocked

# Clean up
rm test-client.md
```

### Test 2: GitHub Branch Protection

**Test force push prevention:**
```bash
# Try to force push (should be blocked by GitHub)
git push --force origin main

# Expected: GitHub rejects with ruleset violation
```

**Test direct push:**
```bash
# Direct push should succeed (0 required approvals)
echo "# Test" >> test.md
git add test.md
git commit -m "test: direct push"
git push origin main

# Expected: Push succeeds (allowed by current config)
```

---

## Security Incident Response

### If Sensitive Data Was Pushed

**Immediate Actions:**

1. **DO NOT** try to delete the commit (it's still in history)
2. **Contact GitHub** to purge sensitive data:
   - Go to repository Settings
   - Contact Support
   - Request sensitive data removal
3. **Remove sensitive data** from working copy
4. **Commit sanitized version**
5. **Update security patterns** to prevent recurrence

**Post-Incident:**

1. Review what bypassed the security check
2. Update `security_patterns.conf` with new patterns
3. Add to `.gitignore` if applicable
4. Document in this file

---

## Configuration Files

### security_patterns.conf

**Location:** `.claude/skills/git-pushing/scripts/security_patterns.conf`

**Current Patterns:**

```bash
# Client-specific file paths
CLIENT_PATH_PATTERNS=(
    "/secc-fort-collins/"
    "/real-atlas/"
    "/schomp/"
    "User-Files/Opportunities/[A-Z]"
)

# Client names to check for
CLIENT_NAMES=(
    "Schomp"
    "Real Atlas"
    "SECC"
)

# Company branding patterns
COMPANY_BRANDING_PATTERNS=(
    "Mid-tier \\(Iconergy\\)"
    "Value Proposition for Iconergy"
    "Iconergy pricing"
)

# Forbidden file patterns
FORBIDDEN_FILE_PATTERNS=(
    "work-documentation/references/.*\\.docx$"
    "work-documentation/references/.*TASK.*ORDER.*\\.docx$"
    "work-documentation/references/.*proposal.*\\.docx$"
)
```

**To Add New Pattern:**

1. Edit `.claude/skills/git-pushing/scripts/security_patterns.conf`
2. Add pattern to appropriate array
3. Test with a dummy file
4. Commit the updated config

---

## Current Security Posture

### ✅ What IS Protected

| Protection | Layer | Status |
|------------|-------|--------|
| Hourly rates | Local check | ✅ Active |
| Client names | Local check | ✅ Active |
| Client paths | Local check | ✅ Active |
| Company branding | Local check | ✅ Active |
| Forbidden docs | Local check | ✅ Active |
| Force pushes | GitHub ruleset | ✅ Active |
| Branch deletion | GitHub ruleset | ✅ Active |

### ⚠️ What Is NOT Protected

| Gap | Impact | Mitigation |
|-----|--------|------------|
| File path restrictions not available in GitHub | Can't block files server-side | Use local check religiously |
| No GitHub Actions scanning | Bypass of local check not caught | Add GitHub Actions workflow |
| No .gitignore for sensitive files | Files can be staged accidentally | Add comprehensive .gitignore |
| Security check can be bypassed | SKIP_SECURITY_CHECK=1 disables all local protection | Use with extreme caution |

### 🎯 Recommended Improvements

**Priority 1 (Do Now):**
- [ ] Add comprehensive `.gitignore` patterns
- [ ] Test security check with various scenarios
- [ ] Document any new client names or paths as they arise

**Priority 2 (Next Week):**
- [ ] Implement GitHub Actions security workflow
- [ ] Create pre-commit git hook (prevents bypassing smart_commit.sh)

**Priority 3 (Future):**
- [ ] Upgrade to GitHub Enterprise for file path restrictions
- [ ] Set up automated security audits (weekly scan of all files)

---

## Maintenance Schedule

**Weekly:**
- Review recent commits for any false positives/negatives
- Update `security_patterns.conf` with new client names

**Monthly:**
- Test all security layers
- Review and update this documentation
- Check for GitHub feature updates

**Quarterly:**
- Full security audit of repository
- Review all committed files for sensitive data
- Evaluate need for additional protections

---

## Contact & Support

**Questions about security setup:**
- Review `.claude/skills/git-pushing/SKILL.md`
- Review `.claude/skills/git-pushing/scripts/README.md`

**Report security incidents:**
- Document in this file under "Security Incident Response"
- Update patterns immediately
- Consider GitHub support if data was pushed

---

## Change Log

### 2025-12-29
- ✅ Created initial security documentation
- ✅ Implemented local security check (Layer 1)
- ✅ Configured GitHub branch rulesets (Layer 2)
- ⚠️ Identified that file path restrictions not available in GitHub plan
- 📝 Documented current security posture and gaps
- 📝 Defined future enhancement roadmap

### Future Changes
- Document updates to `security_patterns.conf`
- Track implementation of additional security layers
- Record any security incidents and resolutions

---

**Built with [Claude Code](https://claude.com/claude-code)**
