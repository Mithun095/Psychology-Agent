# Contributing to Cycology Agent

Thank you for wanting to contribute to Cycology Agent! 💚

This document outlines our git workflow and contribution guidelines to ensure smooth collaboration.

---

## 📋 Team Structure

| Member | Role | Branch | Directory |
|--------|------|--------|-----------|
| **Myth** | Lead / AI | `main`, `feature/core-agent` | `agent/`, `shared/` |
| **Thushara** | Frontend | `feature/frontend` | `frontend/` |
| **Vignesh** | Backend | `feature/backend` | `backend/` |

---

## ⚠️ Golden Rules

> **CRITICAL**: Follow these rules to avoid merge conflicts!

1. **NEVER work directly on `main`** - Always use your feature branch
2. **ONLY edit files in your assigned directory** - Never touch other directories
3. **Pull from main before starting work** - Always sync before coding
4. **Commit frequently with clear messages** - Small commits are easier to review

---

## 🔄 Git Workflow

### Initial Setup (Do Once)

```bash
# Clone the repository
git clone https://github.com/your-org/cycology-agent.git
cd cycology-agent

# Create your feature branch
# For Thushara:
git checkout -b feature/frontend

# For Vignesh:
git checkout -b feature/backend

# Push branch to remote
git push -u origin your-branch-name
```

### Daily Workflow

```bash
# 1. Start of day - sync with main
git checkout main
git pull origin main
git checkout your-branch
git merge main

# 2. Make your changes in YOUR directory only

# 3. Stage and commit
git add .
git commit -m "feat: description of what you did"

# 4. Push to your branch
git push origin your-branch
```

### Commit Message Format

Use this format: `type: description`

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding tests |

**Examples:**
```
feat: add chat input component
fix: resolve socket connection error
docs: update API documentation
```

---

## 📤 Creating a Pull Request

1. Push all your changes to your branch
2. Go to GitHub repository
3. Click "New Pull Request"
4. Select your branch → main
5. Add description of changes
6. Request review from **Myth**
7. Wait for approval before merging

---

## 🚫 What NOT to Do

- ❌ Don't edit files in other team members' directories
- ❌ Don't push directly to main
- ❌ Don't merge without PR approval from Myth
- ❌ Don't rebase if you've already pushed (use merge instead)
- ❌ Don't leave uncommitted changes when switching branches

---

## 🆘 If You Have Merge Conflicts

```bash
# Pull latest main
git checkout main
git pull origin main

# Go to your branch and merge
git checkout your-branch
git merge main

# If conflicts appear, open conflicted files
# Look for <<<<<<< and >>>>>>> markers
# Fix the conflicts manually
# Then:
git add .
git commit -m "fix: resolve merge conflicts"
git push origin your-branch
```

---

## 📁 Directory Boundaries

```
✅ Thushara can ONLY edit:
   frontend/

✅ Vignesh can ONLY edit:
   backend/

✅ Myth manages:
   agent/
   shared/
   docs/
   Root files (README, CONTRIBUTING, etc.)
```

---

## 🤖 Using Antigravity

Each team member has a workflow file with a ready-to-use prompt:

- **Thushara**: `.agent/workflows/thushara-frontend.md`
- **Vignesh**: `.agent/workflows/vignesh-backend.md`

Open your workflow file and copy the prompt into Antigravity to get started!

---

## 💬 Communication

- Use GitHub Issues for bugs and feature requests
- Tag team members in PRs for reviews
- Ask Myth for any architectural decisions

---

**Happy Coding! 💚**
