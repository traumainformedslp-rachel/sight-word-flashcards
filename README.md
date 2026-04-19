# Sight Word Flashcards

Interactive and printable flashcards for **the first 100 children's picture book sight words** (Green et al., 2024), from *Making Words Stick* (Ness & Miles, 2025).

Designed for **older students** learning to read — clean, modern, dark-themed UI that doesn't feel juvenile.

## 🎯 Live App

Open `index.html` in any browser. No build step, no dependencies, no install.

**[→ Try it on GitHub Pages](https://traumainformedslp-rachel.github.io/sight-word-flashcards/)**

## Features

- **Montessori grammar color coding** — each word is colored by part of speech (verb = red, pronoun = purple, preposition = green, etc.)
- **Filter by grammar category** — drill just verbs, just pronouns, etc.
- **Flip cards** — front shows the word, back shows a grammar label + example sentence
- **Sort as you go** — mark words "Got It" or "Still Learning"; unlearned words auto-loop for review
- **Start Over** — traffic-light reset button clears progress and reshuffles mid-session
- **Track progress** — export a dated JSON report of known/learning words (great for classroom data)
- **Print free flashcards** — one-click print-friendly sheet (6 cards per page with example sentences) — no PDF needed
- **Keyboard shortcuts** — Space to flip, arrow keys to sort (K/S also work)
- **Collapsible color key** for reference
- **Light / Dark theme** toggle
- **Mobile-responsive** — works on phones and tablets
- **Zero dependencies** — single HTML file, runs offline

## Printable PDFs

Two print-ready PDF decks are included in `pdf/`:

| File | Color System | What It Encodes |
|------|-------------|-----------------|
| `sight-words-frequency-bands.pdf` | Teal → Amber → Rose → Green | How common the word is (Tier 1–4) |
| `sight-words-montessori.pdf` | 9 Montessori grammar colors | Part of speech (verb, pronoun, etc.) |

Both include:
- Cover page with color key and printing instructions
- 6 cards per sheet (2×3 grid), 17 sheets
- Double-sided: fronts = word, backs = example sentence (mirrored for alignment)
- Print on cardstock, flip on short edge

### Montessori Grammar Colors

| Color | Part of Speech | Symbol | Examples |
|-------|---------------|--------|----------|
| 🔴 Red | Verb | ● | is, was, said, have, go |
| 🟣 Purple | Pronoun | ▲ | I, you, he, she, they |
| 🟠 Orange | Adverb | ● | so, up, not, now, very |
| 🟢 Green | Preposition | ☽ | to, in, of, for, on |
| 🔵 Blue | Adjective | ▲ | all, little, big, good |
| 🩷 Pink | Conjunction | ▬ | and, but, as, if, or |
| 🩵 Light Blue | Article | △ | the, a, an |
| ⚪ Gray | Noun | ▲ | day, time, way, night |
| 🟡 Gold | Interjection | ! | oh |

## Regenerating PDFs

The Python script that generates both PDFs is included:

```bash
pip install reportlab
python src/generate_pdfs.py
```

Output goes to `pdf/`.

## Word List Source

The first 100 CPB (Children's Picture Book) sight words from:

> Green, K. et al. (2024). As cited in *Making Words Stick* © 2025 by Molly Ness and Katharine Pace Miles. Published by Scholastic Inc.

## License

MIT — free to use, modify, and share. Word list and Montessori color system are referenced for educational purposes.

---

Built by [RTN Communication & Literacy](https://rachelslp.org)
