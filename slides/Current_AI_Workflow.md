# Agent-Based Coding Workflow
**Work in progress**
---

## Motivation

Over the past **month** I’ve experimented with coding agents:
- Created small projects 
  - most were **demonstrations for statistical concepts** from scratch.
- Applied this workflow to create **JavaScript demos**
  - Aven though I basically don’t know JavaScript 😄.  
  - I can read it thanks to R, Python, and Java experience — but I can’t “speak”.
- **Disclaimer:** This is a document in progress — a reflection on my current working style, not a final “best way.”

---

## Introduction – Why This Matters

Without a clear split between **discussion** and **execution**, coding projects risk:
- Mixing unfinished ideas into code too early → inconsistent edits.
- Slower progress from constant back-and-forth changes.

⚠️ **Beware of lost context!**  
  Happens if you split roles without persistent context (use pinned files).

---

## Roles at a Glance

| 💬 **Assistant** | ⚙️ **Agent** |
|------------------|-------------|
| Broad discussion & brainstorming | Executes code changes |
| Clarifies goals & scope | Works from fixed requirements |
| Produces requirements doc | Edits/refactors codebase |

---

## Two Modes of Interaction

1. **Assistant → Agent**  
   - Start with 💬 Assistant to explore and scope.  
   - Create a clean requirements file.  
   - Hand over to ⚙️ Agent for implementation.

2. **Direct to Agent**  
   - Go straight to ⚙️ Agent when requirements are already clear.  
   - Best for quick, small, well-defined changes.

---

## Step 0 – Don’t Skip This

**Subject Scoping**  
- Define problem & goal  
- Decide features & constraints  
- Identify required inputs  
- Note edge cases

💡 **Note:** This step is done with an **assistant** (often external, e.g., ChatGPT), kept *outside* the project to freely explore ideas before defining the first `requirements.md`.

---

## Step 0 – Round 0 Prompt (External Assistant)

Talk to ChatGPT about the project and then: 
```
> I want to define the initial scope for a coding project. Please ask me clarifying questions until we have a clear:  
> - Problem statement  
> - Goals and success criteria  
> - Feature list  
> - Constraints and assumptions  
> - Required inputs and outputs  
> - Edge cases and possible pitfalls  
> Once you have enough information, summarize the requirements in a concise, well-structured Markdown document.  
> Don’t start coding — just focus on getting the requirements complete and unambiguous.
```

After this, create or paste the result into `requirements.md` in Cursor, pin it.

---
## Step 1 – Send to Agent ⚙️

- Provide only relevant code files + requirements  
- Keep discussion out of prompt  
- Let ⚙️ Agent edit per requirements

---

## Step 2 – Review & Iterate 💬->⚙️...

- Test changes in your dev environment  
- Note issues or missing features  
- Add a new “Round” section in the requirements file via the 💬 Assistant.
  - I did extra files but I it's better to add sections to the existing file to keep the context.
- Use ChatGPT or 'cursor ask' for minor fixes and clarifications.

💡 **Note:** If only small changes are needed, you may skip the assistant and talk **directly to the agent** for quick fixes.

---

## Step 3 – Polishing

- Improve UI, names, style, docs  
- Avoid new features here — stay on scope  
- Can involve **multiple agents** ⚙️,⚙️,⚙️
  - e.g., one for refactoring, one for docs.  
- For very minor edits (e.g., changing a title), I sometimes code directly myself.

---

## Choosing the Right Mode

💬 **Assistant → Agent**  
Use when:
- Requirements are unclear
- You need brainstorming & scope alignment

⚙️ **Direct to Agent**  
Use when:
- Requirements are already written
- Task is small, quick, well-defined

---

## General Tips

### Reuse Past Work
- Reference similar projects for consistency  

# Example

## Linear Regression Demo
After the second epoch:
![Linear Regression Demo](../lr/screenshot_after_round_2.png)

## The Requirement (in Round 3)

Nearly all requirements are met, but there are still some issues to address.

1. The network is still noy working properly (see the screenshot, and hand drawn sketch how it should look like.
2. Remove Reset slider button (not needed).
3. Add a button on the left side to create new data points.

<img src="../lr/sketch_round3.jpeg" alt="Linear Regression Demo" width="300"/>

<small>Actually I did not use the assistant but wrote it directly to the requirements file.</small>



# Technical Realization in Cursor

---

## Ask vs. Do in Cursor

| 💬 **Assistant (Ask panel)** | ⚙️ **Agent (Do / inline edit)** |
|------------------------------|--------------------------------|
| Pre-prompted for discussion, planning, explanations | Pre-prompted for direct code editing |
| Keeps chat history | No ongoing “chat” history — fresh each run |
| Uses pinned files + project state for context | Uses pinned files + project state for context |

**Key points:**
- **No need to say “be an assistant” or “be an agent”** — Cursor already knows the mode.  
- 💬 and ⚙️ **don’t share conversation memory** — they connect via pinned files and the current codebase.  
- Switching back to 💬 restores full discussion history.

---

## Where to Host the Context

**Inside coding environment**  
- Version-controlled & persistent  
- Both 💬 and ⚙️ see the same files  
- Requires discipline to keep clean

**Outside coding environment**  
- Freedom to explore ideas  
- Must copy/paste into code environment

**Hybrid (recommended)**  
- Scope outside → move cleaned `requirements.md` inside & pin it  
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

---

## Multiple Assistants & Agents

- **Assistants**: Multiple chat threads in Ask panel — each with its own conversation history, all seeing pinned/project files.
- **Agents**: Each inline edit or “edit in chat” run is a new agent instance — also sees pinned/project files.
- **Pinned files** = the bridge between all assistants and agents.

---

![Diagram: Multiple assistants and agents linked via pinned files](diagram-placeholder)

---

## Reload Warning

- Reloading Cursor **clears conversation history** for both 💬 and ⚙️.
- **Pinned files remain** — they are your persistent memory.
- To keep important discussion context:
  - Write it into pinned files, or  
  - Save notes externally.

---

## Reflection – Two Ends of the Spectrum

**Planning-heavy work** → *Best for Assistant → Agent*  
- *Example: Academic writing*  
  - Needs a frozen structure before drafting.  
  - Ensures consistent tone, formatting, and flow.

**Exploration-heavy work** → *Best for direct Agent use*  
- *Example: Investigative data analysis*  
  - Plan evolves continuously through interactive plotting and testing.  
  - Requirements emerge dynamically.

**Middle ground:**  
- Explore first (Agent-only) → then switch to planning (Assistant → Agent) for final structured output.

---

## Closing Reflection

Right now, I am in the **Assistant phase** of my own workflow — discussing and refining ideas with a conversational partner.  
Later, the assistant (💬) will hand over to the agent (⚙️) — in this case, ChatGPT itself — to apply these agreed changes to the slides.  
This mirrors exactly how I envision the workflow being used in practice.

---

## Summary

- **Scope first, code second**  
- 💬 for thinking, ⚙️ for doing  
- Keep context persistent with pinned files  
- Use `basic_rules.md` to lock down project invariants