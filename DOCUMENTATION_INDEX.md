# Documentation Index

Complete guide to all documentation files for Marketo API import process.

## 📚 Documentation Files Overview

### Core Script Documentation

#### **[IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md)** ⭐ START HERE
- **Purpose:** Complete reference for `import_leads.py`
- **Audience:** Anyone using the import script
- **Contents:**
  - Function descriptions (all 6 functions)
  - Configuration requirements
  - Usage examples
  - Error handling guide
  - Troubleshooting
  - Performance tips
  - Security considerations
- **Length:** ~800 lines
- **Best for:** Understanding how the script works

#### **[MODULE_REFERENCE.md](MODULE_REFERENCE.md)** ⭐ FOR DEVELOPERS
- **Purpose:** Technical reference for module dependencies
- **Audience:** Developers, Python programmers
- **Contents:**
  - Module structure diagram
  - Dependency graph
  - config.py variables
  - TokenManager class reference
  - Import resolution
  - Data flow diagrams
  - Call stack during execution
- **Length:** ~600 lines
- **Best for:** Understanding code architecture

---

### Token Management Documentation

#### **[TOKEN_MANAGEMENT.md](TOKEN_MANAGEMENT.md)**
- **Purpose:** Token lifecycle and management implementation
- **Audience:** Users wanting to understand token mechanics
- **Contents:**
  - Token generation process
  - Expiration tracking
  - Proactive validation
  - Auto-refresh mechanism
  - Long-running operation support
  - Token lifespan (1 hour)
- **Length:** ~400 lines
- **Best for:** Understanding how tokens work

#### **[TOKEN_TESTING_SUMMARY.md](TOKEN_TESTING_SUMMARY.md)**
- **Purpose:** Guide to token testing scripts
- **Audience:** Users testing token validity
- **Contents:**
  - When to use which test script
  - Test output interpretation
  - Common scenarios
  - Token status indicators
- **Length:** ~300 lines
- **Best for:** Running token tests

#### **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**
- **Purpose:** One-page token management summary
- **Audience:** Quick lookup reference
- **Contents:**
  - Key features overview
  - Common scenarios
  - Feature comparison table
  - Links to detailed docs
- **Length:** ~200 lines
- **Best for:** Quick reminders

---

### Testing Documentation

#### **[TEST_TOKEN_GUIDE.md](TEST_TOKEN_GUIDE.md)**
- **Purpose:** Comprehensive token testing guide
- **Audience:** Users who need to verify tokens
- **Contents:**
  - How to check token validity
  - Detailed troubleshooting
  - Expected outputs
  - Token information reference
  - Monitoring tokens during import
- **Length:** ~400 lines
- **Best for:** Troubleshooting token issues

#### **[COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)**
- **Purpose:** Exact commands and their outputs
- **Audience:** Users who prefer command examples
- **Contents:**
  - Command syntax
  - Example outputs
  - Decision trees
  - Status code interpretation
- **Length:** ~300 lines
- **Best for:** Copy-paste commands and expected results

---

### Quick Start Guides

#### **[README.md](README.md)**
- **Purpose:** Main overview and quick start
- **Audience:** First-time users
- **Contents:**
  - 3-step quick start
  - File structure
  - Feature overview
  - Common tasks table
- **Length:** ~200 lines
- **Best for:** Getting started quickly

#### **[QUICK_START.md](QUICK_START.md)** (if created)
- One-minute setup guide
- Minimal prerequisites
- Basic workflow

---

## 📖 How to Use This Documentation

### Scenario 1: "I just want to run the import"

1. Read: [README.md](README.md) - 5 min
2. Verify token: `python3 verify_token.py` - 1 min
3. Run import: `python3 import_leads.py` - variable
4. Done! ✓

---

### Scenario 2: "I want to understand how it works"

1. Read: [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - 30 min
2. Read: [MODULE_REFERENCE.md](MODULE_REFERENCE.md) - 20 min
3. Skim: [TOKEN_MANAGEMENT.md](TOKEN_MANAGEMENT.md) - 10 min
4. Now you understand the architecture ✓

---

### Scenario 3: "My token isn't working"

1. Run: `python3 verify_token.py` - 1 min
2. Read: [TEST_TOKEN_GUIDE.md](TEST_TOKEN_GUIDE.md) troubleshooting - 10 min
3. Apply solution from troubleshooting guide
4. Test again: `python3 verify_token.py` ✓

---

### Scenario 4: "I need to know a specific command"

1. Search: [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) - 2 min
2. Copy command and run
3. Compare output to expected output ✓

---

### Scenario 5: "The import failed, I need to debug"

1. Check error in console output
2. Search in: [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) Troubleshooting section
3. Apply fix
4. Rerun import ✓

---

## 🎯 Documentation by Topic

### Authentication & Tokens

| Question | Document | Section |
|----------|----------|---------|
| How do tokens work? | TOKEN_MANAGEMENT.md | Token Lifecycle |
| How do I test my token? | TEST_TOKEN_GUIDE.md | How Each Script Works |
| What's error 601? | IMPORT_LEADS_DOCUMENTATION.md | Troubleshooting |
| When do tokens refresh? | TOKEN_MANAGEMENT.md | Auto-Refresh Mechanism |
| How long do tokens last? | TOKEN_TESTING_SUMMARY.md | Token Information |

### Running the Import

| Question | Document | Section |
|----------|----------|---------|
| How do I run the import? | README.md | Usage |
| What's the exact command? | COMMAND_REFERENCE.md | Quick Test |
| What will it output? | IMPORT_LEADS_DOCUMENTATION.md | Expected Output |
| How does it work? | IMPORT_LEADS_DOCUMENTATION.md | Workflow |
| What if it fails? | IMPORT_LEADS_DOCUMENTATION.md | Error Handling |

### Configuration

| Question | Document | Section |
|----------|----------|---------|
| What's in config.py? | MODULE_REFERENCE.md | config.py Module |
| How do I set credentials? | IMPORT_LEADS_DOCUMENTATION.md | Configuration |
| What should CSV look like? | IMPORT_LEADS_DOCUMENTATION.md | CSV File Requirements |
| Where do I find the URLs? | MODULE_REFERENCE.md | MARKETO_BASE_URL |

### Code Understanding

| Question | Document | Section |
|----------|----------|---------|
| What modules are imported? | MODULE_REFERENCE.md | Imports in import_leads.py |
| What does TokenManager do? | MODULE_REFERENCE.md | TokenManager Class |
| What functions exist? | IMPORT_LEADS_DOCUMENTATION.md | Functions |
| How do modules interact? | MODULE_REFERENCE.md | Dependency Graph |
| What's the call stack? | MODULE_REFERENCE.md | Execution Flow |

### Troubleshooting

| Issue | Document | Section |
|-------|----------|---------|
| Token invalid | IMPORT_LEADS_DOCUMENTATION.md | Issue: Access token invalid |
| CSV not found | IMPORT_LEADS_DOCUMENTATION.md | Issue: CSV file does not exist |
| CSV too large | IMPORT_LEADS_DOCUMENTATION.md | Issue: CSV file is too large |
| Connection refused | IMPORT_LEADS_DOCUMENTATION.md | Issue: Connection refused |
| Missing columns | IMPORT_LEADS_DOCUMENTATION.md | Issue: CSV missing columns |
| Test failures | TEST_TOKEN_GUIDE.md | Troubleshooting |

---

## 📋 Documentation Checklist

### Before Running Import

- [ ] Read: [README.md](README.md)
- [ ] Check: `python3 verify_token.py`
- [ ] Verify: config.py has correct settings
- [ ] Validate: CSV file exists and has correct columns

### When Troubleshooting

- [ ] Check: Error message in console
- [ ] Search: [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md)
- [ ] Read: Relevant troubleshooting section
- [ ] Apply: Suggested solution
- [ ] Test: `python3 verify_token.py`

### When Learning Architecture

- [ ] Read: [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md)
- [ ] Read: [MODULE_REFERENCE.md](MODULE_REFERENCE.md)
- [ ] Read: [TOKEN_MANAGEMENT.md](TOKEN_MANAGEMENT.md)
- [ ] Review: Code comments in `.py` files

---

## 🔍 Search Guide

### By Keyword

**"token"**
- [TOKEN_MANAGEMENT.md](TOKEN_MANAGEMENT.md)
- [TEST_TOKEN_GUIDE.md](TEST_TOKEN_GUIDE.md)
- [MODULE_REFERENCE.md](MODULE_REFERENCE.md)

**"error 601"**
- [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - Marketo Error Codes

**"401"**
- [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - HTTP Status Codes

**"CSV"**
- [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - CSV Validation & Configuration

**"permission"**
- [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - LaunchPoint permissions

**"timeout"**
- [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - Troubleshooting section

**"polling"**
- [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - get_import_status function

---

## 📚 Reading Order

### For First-Time Users

1. **[README.md](README.md)** (5 min)
   - Get overview and quick start

2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** (5 min)
   - Understand key features

3. **[COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)** (10 min)
   - See actual commands and outputs

4. **Run:** `python3 import_leads.py`
   - Execute the import

---

### For Developers

1. **[MODULE_REFERENCE.md](MODULE_REFERENCE.md)** (20 min)
   - Understand module structure

2. **[IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md)** (30 min)
   - Detailed function reference

3. **[TOKEN_MANAGEMENT.md](TOKEN_MANAGEMENT.md)** (15 min)
   - Token implementation details

4. **Review code** (30 min)
   - Read `import_leads.py`, `token_manager.py`, `config.py`

---

### For Troubleshooting

1. **Check error message** (1 min)
   - Note the specific error

2. **Search documentation** (2 min)
   - Use Ctrl+F to find error message

3. **Read solution** (5 min)
   - Follow recommended fix

4. **Test solution** (2 min)
   - Run verify/import script again

5. **Success!** ✓

---

## 📞 Quick Help

### "How do I...?"

**...run the import?**
→ [README.md](README.md) - Usage section

**...test my token?**
→ [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) - Run This First

**...fix error 601?**
→ [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - Troubleshooting

**...understand the code?**
→ [MODULE_REFERENCE.md](MODULE_REFERENCE.md) - Module Structure

**...see an example?**
→ [IMPORT_LEADS_DOCUMENTATION.md](IMPORT_LEADS_DOCUMENTATION.md) - Examples section

**...know what command to run?**
→ [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) - Summary Table

---

## 🎓 Learning Path

### Beginner Path (30 min)
```
README.md → QUICK_REFERENCE.md → COMMAND_REFERENCE.md → Run import!
```

### Intermediate Path (1 hour)
```
README.md → IMPORT_LEADS_DOCUMENTATION.md → TEST_TOKEN_GUIDE.md → Run import!
```

### Advanced Path (2 hours)
```
MODULE_REFERENCE.md → IMPORT_LEADS_DOCUMENTATION.md → 
TOKEN_MANAGEMENT.md → Review code → Run import!
```

### Troubleshooting Path (15 min)
```
Error message → Search docs → Troubleshooting section → Apply fix → Test
```

---

## 📄 File List

| File | Size | Type | Purpose |
|------|------|------|---------|
| README.md | 4 KB | Quick Start | Main overview |
| IMPORT_LEADS_DOCUMENTATION.md | 25 KB | Reference | Complete script docs |
| MODULE_REFERENCE.md | 20 KB | Reference | Module architecture |
| TOKEN_MANAGEMENT.md | 15 KB | Technical | Token lifecycle |
| TOKEN_TESTING_SUMMARY.md | 10 KB | Guide | Testing overview |
| TEST_TOKEN_GUIDE.md | 18 KB | Guide | Detailed testing |
| QUICK_REFERENCE.md | 8 KB | Quick | One-pager |
| COMMAND_REFERENCE.md | 12 KB | Reference | Commands & outputs |
| DOCUMENTATION_INDEX.md | 6 KB | Navigation | This file |

**Total:** ~118 KB of documentation

---

## 🎯 Documentation Goals

✅ **Comprehensive** - Covers all aspects  
✅ **Accessible** - Easy to navigate  
✅ **Practical** - Full of examples  
✅ **Detailed** - Deep dives available  
✅ **Cross-referenced** - Easy navigation  

---

## 💡 Pro Tips

1. **Use Ctrl+F** - Search documentation quickly
2. **Bookmark sections** - Save troubleshooting pages
3. **Print command reference** - Keep by your desk
4. **Share test guide** - With team members
5. **Keep README open** - During first run

---

## 🚀 Next Steps

1. **Read:** Start with [README.md](README.md)
2. **Test:** Run `python3 verify_token.py`
3. **Run:** Execute `python3 import_leads.py`
4. **Success!** ✓

Happy importing! 🎉
