# Decision Log

## Purpose
Every project involves choices: which library to use, which approach to take,
how to split work. This document records those choices and the reasoning behind
them — so we (and evaluators) can see *how* we thought, not just *what* we built.

## How to fill this out
Add a new entry every time you make a non-trivial decision — especially if there
were multiple options on the table. Keep each entry short (a few lines is enough).

Use this format:

### [Short title of the decision]
- **Date:**
- **Situation:** what problem or question we were facing
- **Options considered:** the alternatives we looked at
- **Decision:** what we chose
- **Reasoning:** why we chose it

## Example

### Choice of vector database
- **Date:** 2026-03-10
- **Situation:** Needed to store and query dense embeddings for retrieval.
- **Options considered:** ChromaDB vs. FAISS
- **Decision:** ChromaDB
- **Reasoning:** Faster to set up given our timeline, built-in persistence,
  good enough performance for our dataset size. FAISS would have given more
  control but added setup overhead we didn't have time for.

## Notes
- It's fine to log decisions that turned out to be wrong later — just add a follow-up
  note explaining what changed and why. That's valuable too.
- Disagreements between teammates belong here: write the options each person
  proposed and how you settled on one (testing both, voting, deferring to whoever
  owns that part, etc.).
