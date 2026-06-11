# How to Use This Team Builder — No Coding Experience Needed

This workspace lets an AI assistant build you a competitive Cobblemon Delta team.
You give it your required mons and budget, it reads through all the meta data and
outputs a full team with a detailed battle guide.

**You do not need to know how to code.** You just need to download the files,
open them in one of the supported AI tools, and ask for a team.

---

## What You Need (the short version)

1. The project files on your computer (covered in the next section)
2. One AI tool from the list below — most are free to start

Pick whichever AI tool you already have, or jump straight to the
[Claude Code](#option-a-claude-code-recommended) section if you have no preference.

---

## Step 1 — Download the Project Files

### Option A: Download as a ZIP (no coding required)

1. Go to the GitHub page for this project
2. Click the green **Code** button near the top right
3. Click **Download ZIP**
4. Once it downloads, right-click the ZIP file and choose **Extract All** (Windows)
   or double-click it (Mac)
5. Remember where you extracted it — you will point your AI tool at this folder

### Option B: Use Git (if you already have it)

Open a terminal (search "cmd" on Windows, "Terminal" on Mac), paste this, and press Enter:

```
git clone https://github.com/Shrek3294/cobblemon-delta-team-builder.git
```

Then run:

```
cd cobblemon-delta-team-builder
git lfs pull
```

The `git lfs pull` step downloads the large learnset file. If you skip it the
AI still works — it just will not be able to look up full learnsets on its own.

---

## Step 2 — Pick Your AI Tool

All of these tools work the same basic way: you open the project folder inside
them, and the AI automatically reads the instructions in `CLAUDE.md` so it knows
all the Delta-specific rules. Then you just chat with it.

---

### Option A: Claude Code (Recommended)

Claude Code is made by Anthropic and is the tool this workspace was designed for.
It understands the `/build` command out of the box.

**Download:** https://claude.ai/code — there is a desktop app for Windows and Mac.

**Steps:**

1. Open the Claude Code desktop app
2. Click **Open Folder** (or press `Ctrl+K` then type "open folder")
3. Navigate to the folder you extracted/cloned in Step 1 and select it
4. Wait a moment — Claude will read `CLAUDE.md` automatically
5. Type your order in the chat (see [What to Say to the AI](#step-3--what-to-say-to-the-ai) below)

**The `/build` command:**

If you want the full experience, type `/build` in the chat. Claude will walk you
through a short intake (required mons, playstyle, budget) and then generate a
complete team plus a battle guide document.

---

### Option B: Cursor

Cursor is a code editor with a powerful built-in AI chat. It looks like VS Code
if you have used that before.

**Download:** https://www.cursor.com — free to start.

**Steps:**

1. Open Cursor
2. Go to **File → Open Folder**
3. Select the project folder you downloaded
4. Open the AI chat panel — press `Ctrl+L` (Windows/Linux) or `Cmd+L` (Mac)
5. Make sure **"Include project files"** or **"Codebase"** context is turned on
   (there is usually a toggle or a `@codebase` option in the chat input)
6. Type your team order (see [What to Say to the AI](#step-3--what-to-say-to-the-ai) below)

**Tip for Cursor:** Start your message with `Read CLAUDE.md first, then` — this
makes sure the AI loads the instructions before it starts building.

---

### Option C: Codex (by OpenAI)

OpenAI's Codex is a terminal-based AI agent similar to Claude Code.

**Download:** https://github.com/openai/codex — requires Node.js. If you do not
have Node.js installed, download it first from https://nodejs.org (click the LTS
version).

**Steps:**

1. Open a terminal (search "cmd" on Windows, "Terminal" on Mac)
2. Install Codex by typing this and pressing Enter:
   ```
   npm install -g @openai/codex
   ```
3. Navigate into the project folder:
   ```
   cd path\to\cobblemon-delta-team-builder
   ```
   (Replace `path\to\` with wherever you extracted the files — for example
   `cd C:\Users\YourName\Downloads\cobblemon-delta-team-builder`)
4. Start Codex:
   ```
   codex
   ```
5. Codex will read the folder automatically. Type your team order in the prompt.

**Tip for Codex:** At the start of your first message, say:
`Read CLAUDE.md to understand the rules of this workspace, then build me a team.`

---

### Option D: Qodo (also known as Qoder)

Qodo is an AI coding assistant that works as an extension inside VS Code.

**Steps:**

1. Install VS Code if you do not have it: https://code.visualstudio.com
2. Open VS Code, go to the **Extensions** panel (the four-squares icon on the left
   sidebar, or press `Ctrl+Shift+X`)
3. Search for **Qodo** and click Install
4. Go to **File → Open Folder** and select the project folder you downloaded
5. Open the Qodo chat panel from the left sidebar
6. In the chat, type your team order (see below)

**Tip for Qodo:** Type `@workspace` at the start of your message so Qodo
searches the whole project before answering.

---

### Option E: Gemini Code Assist / Antigravity (by Google)

Google's AI coding tools (including Antigravity) work as extensions inside
VS Code or through a web interface.

**Steps for VS Code extension:**

1. Install VS Code if you do not have it: https://code.visualstudio.com
2. Open the Extensions panel (`Ctrl+Shift+X`) and search for
   **Gemini Code Assist** or **Antigravity** and click Install
3. Sign in with your Google account when prompted
4. Go to **File → Open Folder** and select the project folder
5. Open the AI chat panel and type your order

**Steps for web interface:**

1. Go to the tool's web interface and start a new chat
2. Look for an **Upload files** or **Attach folder** option
3. Upload the `CLAUDE.md`, `notes/` folder, and `data/team-builder.json` — these
   three together give the AI everything it needs to build a team
4. Type your order

**Tip:** Start your message with: `Read the attached CLAUDE.md for the rules of
this workspace. Then build me a team.`

---

## Step 3 — What to Say to the AI

Once your AI tool has the project open, just describe what you want. Here are
some example messages you can copy and paste:

### Basic team (no specific requirements)

```
I want a team for Cobblemon Delta ranked. My budget is flexible. I like balanced
teams that can handle both offense and defense. Build me the best team you can.
```

### Team around a specific mon

```
I want to build a team around Tinkaton-Gamma. I like balance playstyle.
My budget is around 500k per mon. Build me a full team.
```

### Hyper offense

```
Build me a hyper offense team. I have Draculedge and Sevygarde available.
No budget limit. I want to climb fast.
```

### If you want the full battle guide document

```
/build
```

This starts the guided intake. Claude will ask you a few questions and then
produce a complete Word document (.docx) with team identity, sets, leads,
win conditions, matchup guide, and everything else.

---

## Step 4 — Getting Your Team Out

The AI will produce a **Pokepaste** (the team in copy-paste format for the game)
and optionally a **battle guide document**.

### Pokepaste

The Pokepaste block looks like this and can be copied directly into the game:

```
Tinkaton-Gamma @ Heavy-Duty Boots
Ability: Parasol Prayer
Timid Nature
EVs: 252 HP / 4 Def / 252 SpD
- Updraft
- Moonblast
- Defog
- Moonlight
```

Copy the whole block and paste it into the Cobblemon Delta team importer.

### Battle guide document

If you ran `/build` (Claude Code) or asked for a full guide, the AI will save a
`.docx` file into the `teams/` folder inside the project. Open it with Microsoft
Word, Google Docs, or LibreOffice.

---

## Frequently Asked Questions

**Do I need to install Python?**

Only if you want to run the damage calculator yourself (`tools/calc.py`). For
just getting a team built, no Python is needed — the AI does everything in chat.

**The AI says it cannot read some files — what do I do?**

Make sure you opened the whole project folder, not just one file. In any of the
tools above, use **File → Open Folder** and select the top-level
`cobblemon-delta-team-builder` folder.

**The learnsets file is missing or the AI cannot find moves — what happened?**

The learnsets file is large (43 MB) and stored separately via Git LFS. Run
`git lfs pull` in a terminal inside the project folder to download it. If you
downloaded the ZIP instead of using git, the file may be a text stub — in that
case use the git clone method from Step 1 Option B.

**Can I use this on my phone?**

Claude Code has a web version at https://claude.ai/code that works in a browser.
Upload the `CLAUDE.md` and the key notes files, then chat with it — you will not
get the full `/build` experience but you can get a solid team.

**Something looks wrong in the team the AI built — what do I do?**

The AI cross-checks every move against the legality data before finishing. If
something slips through, just tell it: `Check that every move on [mon name] is
legal in Cobblemon Delta ranked.` It will recheck and fix it.

**I want to run this for my own clients — can I fork it?**

Yes. Fork the GitHub repo, update `notes/player_notes.md` with your own
pricing/credentials, and point the AI at your fork. Everything is MIT-style
open for personal use.

---

## Quick Reference — Which Tool Should I Use?

| I want... | Use |
|---|---|
| The easiest setup possible | **Claude Code desktop app** |
| To stay inside a code editor I already have | **Cursor** or **VS Code + Qodo/Gemini** |
| A terminal-based agent like Claude Code but from OpenAI | **Codex** |
| To use it in a browser without installing anything | **claude.ai/code** (upload the key files) |

---

*Built by the creator of [Delta-Calc](https://modrinth.com/mod/delta-calc).*
