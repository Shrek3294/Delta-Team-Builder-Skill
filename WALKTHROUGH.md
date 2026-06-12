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

Pick whichever AI tool you already have, or jump straight to
[Codex](#option-a-codex-by-openai--recommended--free) if you have no preference —
it is free, made by the same team as ChatGPT, and has the simplest setup.

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

### Option A: Codex (by OpenAI) — Recommended — Free

Codex is made by **OpenAI, the same team behind ChatGPT**. It is completely free
and has a proper desktop app you can download like any normal program — including
from the **Microsoft Store** on Windows, which is the easiest way to get it.

**Download — pick whichever is easiest:**

- **Microsoft Store (Windows, easiest):** Open the Start menu, search
  **Microsoft Store**, then search for **OpenAI Codex** and click Install
- **Direct download:** https://github.com/openai/codex/releases — grab the
  latest `.exe` (Windows) or `.dmg` (Mac) installer

**Steps:**

1. Open the Codex desktop app after installing
2. Click **Open Folder** and select the project folder you downloaded in Step 1
3. The AI reads `CLAUDE.md` automatically when it opens the folder
4. Type your team order in the chat (see [What to Say to the AI](#step-3--what-to-say-to-the-ai) below)

It is free to use, no credit card required. You just need to sign in with a free
OpenAI account (the same one you use for ChatGPT if you have one).

**Tip for Codex:** Start your first message with:
`Read CLAUDE.md to understand the rules of this workspace, then build me a team.`

---

### Option B: Claude Code

Claude Code is made by Anthropic and is the tool this workspace was originally
designed for. It understands the `/build` command out of the box, which gives
you the most complete experience.

**Download:** https://claude.ai/code — desktop app for Windows and Mac.

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

### Option C: Cursor

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

### Option D: Qoder

Qoder is a standalone desktop app — you download and install it like any normal
program, no code editor required. It has a very generous free tier.

> **Heads up on the free tier:** Qoder's free plan runs on **Qwen** models.
> Qwen works fine for basic questions but is noticeably weaker than the AI in
> Codex, Claude Code, or Cursor when it comes to complex multi-file tasks like
> this one. You may get simpler teams or miss some Delta-specific nuances. If the
> results feel shallow, consider switching to one of the top options.

**Download:** Search for **Qoder** in your browser and download the desktop app
from their official site. Install it like any normal program.

**Steps:**

1. Open the Qoder desktop app
2. Look for an **Open Folder** or **Add Project** button and select the project
   folder you downloaded in Step 1
3. Open the chat panel
4. Type your team order (see [What to Say to the AI](#step-3--what-to-say-to-the-ai) below)

**Tip for Qoder:** Start your message with `Read CLAUDE.md first, then` to make
sure it loads the Delta rules before building.

---

### Option E: Antigravity (by Google)

Antigravity is Google's standalone AI coding app — download and install it like
any normal program. It also has a generous free tier.

> **Heads up on the free tier:** Same note as Qoder above — the free plan uses
> **Qwen** models, which are weaker than the paid AI in the other tools on this
> list. Great for trying things out, but for the most accurate Delta team builds
> you will get better results with Codex or Claude Code.

**Download:** Search for **Antigravity** in your browser and download the desktop
app from Google's official page. Install it like any normal program.

**Steps:**

1. Open the Antigravity desktop app
2. Click **Open Folder** or **Add Project** and select the project folder from
   Step 1
3. Open the chat panel
4. Type your team order (see [What to Say to the AI](#step-3--what-to-say-to-the-ai) below)

**Tip:** Start your message with: `Read CLAUDE.md for the rules of this workspace,
then build me a team.`

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
| Free, easiest setup, from the ChatGPT team | **Codex desktop app** (Option A) |
| The most complete `/build` experience | **Claude Code** (Option B) |
| To stay inside a code editor I already have | **Cursor** (Option C) |
| Free standalone app, okay for simple teams | **Qoder** or **Antigravity** (Options D/E — Qwen model, weaker) |
| To use it in a browser without installing anything | **claude.ai/code** (upload the key files) |

---

*Built by the creator of [Delta-Calc](https://modrinth.com/mod/delta-calc).*
