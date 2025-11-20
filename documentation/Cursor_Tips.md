# Technical Realization in Cursor

---

## Why This Matters
In Cursor, understanding the difference between Assistant and Agent modes — and how they share context — is essential to applying the workflow effectively.  
💬 and ⚙️ each have their own conversation memory, but **the only persistent shared context is the codebase and pinned files**.

---

## Ask vs. Do in Cursor

| 💬 **Assistant (Ask panel)** | ⚙️ **Agent (Do / inline edit)** |
|------------------------------|--------------------------------|
| Pre-prompted for discussion, planning, explanations | Pre-prompted for direct code editing |
| Keeps chat history | No ongoing “chat” history — fresh each run |
| Uses pinned files + project state for context | Uses pinned files + project state for context |

**Key points:**
- No need to say “be an assistant” or “be an agent” — Cursor already knows the mode.  
- 💬 and ⚙️ do **not** share conversation memory — **the only persistent shared context is the codebase and pinned files**.  
- Switching back to 💬 restores full discussion history for that Assistant 
    - Not 100% sure if this is true for the Agent.
- Ask panel can also write (e.g. in the requirements file) when explicitly asked.

---

## Reload Warning

- Reloading Cursor **clears conversation history** for both 💬 and ⚙️.
- **Pinned files remain** — they are your persistent memory.
- To keep important discussion context:


---

## Where to Host the Context

**Inside coding environment**  
- Version-controlled & persistent  
- Both 💬 and ⚙️ see the same files  
- Example: `style_guide.md`, coding rules, API contracts  
- Requires discipline to keep clean

**Outside coding environment**  
- Freedom to explore ideas  
- Example: brainstorming new features with ChatGPT  
- Must copy/paste into code environment

**Hybrid (recommended)**  
- Scope outside → move cleaned `requirements.md` inside & pin it  
- Example: external scoping → clean requirements → pinned file in project  
- Keeps creative chaos separate, but ensures agent sees final scope

---

## Pinned Context Strategy

Example file structure:

project root folder:  
requirements.md       → pinned, defines scope  
style_guide.md        → pinned, ensures naming/style  
basic_rules.md        → pinned, lists unchangeable files & workflow rules  
static/index.html     → never edited unless explicit  
src/                  → editable code

**basic_rules.md** example:
# Basic Project Rules
- Maintain a single static HTML in /static/index.html. Never create additional HTML files.
- Do not change files in /static unless explicitly told.
- Follow formatting from style_guide.md for all code.
- Implement features according to requirements.md only.

**Tip:** Keep all rounds as sections inside `requirements.md` so only one file needs to be pinned.

