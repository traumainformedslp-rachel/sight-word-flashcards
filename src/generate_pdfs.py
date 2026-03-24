#!/usr/bin/env python3
"""
Generate printable sight word flashcard PDFs.

Two decks:
  1. Frequency Bands — color-coded by word rank (Tier 1–4)
  2. Montessori Grammar — color-coded by part of speech

Requires: pip install reportlab

Usage: python generate_pdfs.py
Output: pdf/sight-words-frequency-bands.pdf, pdf/sight-words-montessori.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
import math
import os

W, H = letter

# ============================================================
# DATA
# ============================================================

WORDS = [
    "the","and","a","to","I","you","in","of","it","he","is","was","for","on","that",
    "with","but","his","all","they","my","so","be","she","up","at","are","one","said",
    "what","this","when","we","me","have","as","do","like","out","can","her","not",
    "then","your","no","there","day","just","it's","see","little","time","from","had",
    "now","will","I'm","go","were","too","them","him","some","big","get","if","good",
    "don't","down","by","how","know","an","oh","more","their","could","about","back",
    "who","or","make","into","look","very","would","right","here","love","way","night",
    "did","new","come","our","two","want","made","over","around"
]

SENTENCES = {
    "the":"Pass me the book.","and":"You and I can go.","a":"I saw a bird.",
    "to":"We need to leave.","I":"I will be there.","you":"Can you help?",
    "in":"She is in the room.","of":"A cup of water.","it":"Give it to me.",
    "he":"He ran fast.","is":"The sky is blue.","was":"She was happy.",
    "for":"This is for you.","on":"The cat is on the bed.","that":"Look at that!",
    "with":"Come with me.","but":"Small but strong.","his":"That is his coat.",
    "all":"We ate all of it.","they":"They went home.","my":"This is my turn.",
    "so":"I was so tired.","be":"Just be yourself.","she":"She left early.",
    "up":"Stand up now.","at":"Meet me at noon.","are":"You are kind.",
    "one":"Pick one color.","said":"He said hello.","what":"What happened?",
    "this":"Read this page.","when":"Call me when ready.","we":"We did it together.",
    "me":"Tell me more.","have":"I have time.","as":"Fast as lightning.",
    "do":"What do you think?","like":"I like this song.","out":"Go out and play.",
    "can":"You can do it.","her":"Give her the note.","not":"I am not sure.",
    "then":"Eat first, then go.","your":"Bring your bag.","no":"There is no rush.",
    "there":"Look over there.","day":"What a great day.","just":"Just keep going.",
    "it's":"It's almost done.","see":"I can see it now.","little":"A little more time.",
    "time":"It takes time.","from":"A note from home.","had":"She had a plan.",
    "now":"Start now.","will":"I will try again.","I'm":"I'm on my way.",
    "go":"Let's go outside.","were":"They were ready.","too":"Me too!",
    "them":"Help them out.","him":"Ask him first.","some":"Have some water.",
    "big":"That's a big step.","get":"Go get your coat.","if":"Tell me if you can.",
    "good":"Good job today.","don't":"I don't mind.","down":"Sit down here.",
    "by":"Stand by the door.","how":"How does this work?","know":"I know the answer.",
    "an":"Grab an apple.","oh":"Oh, I see now!","more":"Tell me more.",
    "their":"That's their choice.","could":"You could try.","about":"Think about it.",
    "back":"I'll be right back.","who":"Who said that?","or":"Now or later?",
    "make":"Let's make a plan.","into":"Walk into the room.","look":"Look at this!",
    "very":"That's very cool.","would":"I would like that.","right":"You're right.",
    "here":"Come over here.","love":"I love this place.","way":"Find a better way.",
    "night":"Good night.","did":"You did great.","new":"Try something new.",
    "come":"Come with us.","our":"This is our spot.","two":"Pick two options.",
    "want":"What do you want?","made":"She made it work.","over":"Start over fresh.",
    "around":"Look around you.",
}

WORD_POS = {
    "the":"article","and":"conjunction","a":"article","to":"preposition",
    "I":"pronoun","you":"pronoun","in":"preposition","of":"preposition",
    "it":"pronoun","he":"pronoun","is":"verb","was":"verb",
    "for":"preposition","on":"preposition","that":"pronoun",
    "with":"preposition","but":"conjunction","his":"pronoun",
    "all":"adjective","they":"pronoun","my":"pronoun","so":"adverb",
    "be":"verb","she":"pronoun","up":"adverb","at":"preposition",
    "are":"verb","one":"adjective","said":"verb","what":"pronoun",
    "this":"pronoun","when":"adverb","we":"pronoun","me":"pronoun",
    "have":"verb","as":"conjunction","do":"verb","like":"verb",
    "out":"adverb","can":"verb","her":"pronoun","not":"adverb",
    "then":"adverb","your":"pronoun","no":"adverb","there":"adverb",
    "day":"noun","just":"adverb","it's":"pronoun","see":"verb",
    "little":"adjective","time":"noun","from":"preposition","had":"verb",
    "now":"adverb","will":"verb","I'm":"pronoun","go":"verb",
    "were":"verb","too":"adverb","them":"pronoun","him":"pronoun",
    "some":"adjective","big":"adjective","get":"verb","if":"conjunction",
    "good":"adjective","don't":"verb","down":"adverb","by":"preposition",
    "how":"adverb","know":"verb","an":"article","oh":"interjection",
    "more":"adjective","their":"pronoun","could":"verb","about":"preposition",
    "back":"adverb","who":"pronoun","or":"conjunction","make":"verb",
    "into":"preposition","look":"verb","very":"adverb","would":"verb",
    "right":"adjective","here":"adverb","love":"verb","way":"noun",
    "night":"noun","did":"verb","new":"adjective","come":"verb",
    "our":"pronoun","two":"adjective","want":"verb","made":"verb",
    "over":"preposition","around":"preposition",
}

# ============================================================
# PALETTES
# ============================================================

BAND_PALETTES = {
    1: {"bg":"#0B1D26","accent":"#56CFE1","text":"#E8F4F8","label":"TIER 1  ·  MOST FREQUENT","band_name":"1 – 25"},
    2: {"bg":"#1A1408","accent":"#F4B942","text":"#FAF0D7","label":"TIER 2  ·  HIGH FREQUENCY","band_name":"26 – 50"},
    3: {"bg":"#1F0F14","accent":"#E8637A","text":"#F8E4E8","label":"TIER 3  ·  GROWING","band_name":"51 – 75"},
    4: {"bg":"#0B1A12","accent":"#6BCB77","text":"#E2F5E8","label":"TIER 4  ·  ADVANCING","band_name":"76 – 100"},
}

MONTESSORI_PALETTES = {
    "verb":        {"bg":"#1A0A0A","accent":"#E63946","text":"#F8E0E0","label":"VERB","symbol":"●"},
    "noun":        {"bg":"#111111","accent":"#C8C8C8","text":"#EAEAEA","label":"NOUN","symbol":"▲"},
    "adjective":   {"bg":"#0A0E1A","accent":"#3A6EDB","text":"#D8E4F8","label":"ADJECTIVE","symbol":"▲"},
    "article":     {"bg":"#0C1520","accent":"#7EB8E0","text":"#DCF0FF","label":"ARTICLE","symbol":"△"},
    "pronoun":     {"bg":"#140A1A","accent":"#9B59B6","text":"#EAD8F4","label":"PRONOUN","symbol":"▲"},
    "preposition": {"bg":"#081A10","accent":"#27AE60","text":"#D0F0DE","label":"PREPOSITION","symbol":"☽"},
    "conjunction": {"bg":"#1A0F10","accent":"#E8A0B0","text":"#F8E8EC","label":"CONJUNCTION","symbol":"▬"},
    "adverb":      {"bg":"#1A1208","accent":"#E89B2D","text":"#F8ECD8","label":"ADVERB","symbol":"●"},
    "interjection":{"bg":"#1A1608","accent":"#F1C40F","text":"#FFF8DC","label":"INTERJECTION","symbol":"!"},
}

# ============================================================
# LAYOUT
# ============================================================

COLS = 2
ROWS = 3
CARDS_PER_PAGE = COLS * ROWS
MARGIN = 0.45 * inch
GUTTER = 0.2 * inch
CARD_W = (W - 2 * MARGIN - (COLS - 1) * GUTTER) / COLS
CARD_H = (H - 2 * MARGIN - (ROWS - 1) * GUTTER) / ROWS
CARD_R = 14


def draw_rounded_rect(c, x, y, w, h, r, fill_color):
    c.setFillColor(fill_color)
    c.setStrokeColor(fill_color)
    c.setLineWidth(0)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)


def get_card_pos(idx):
    col = idx % COLS
    row = idx // COLS
    x = MARGIN + col * (CARD_W + GUTTER)
    y = H - MARGIN - (row + 1) * CARD_H - row * GUTTER
    return x, y


def get_back_card_pos(idx):
    col = idx % COLS
    row = idx // COLS
    mirrored_col = (COLS - 1) - col
    x = MARGIN + mirrored_col * (CARD_W + GUTTER)
    y = H - MARGIN - (row + 1) * CARD_H - row * GUTTER
    return x, y


def get_band(num):
    if num <= 25: return 1
    if num <= 50: return 2
    if num <= 75: return 3
    return 4


def draw_page_bg(c):
    c.setFillColor(HexColor("#0a0a0a"))
    c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_front(c, x, y, word, num, pal, top_right_label):
    bg = HexColor(pal["bg"])
    accent = HexColor(pal["accent"])
    text_col = HexColor(pal["text"])

    draw_rounded_rect(c, x, y, CARD_W, CARD_H, CARD_R, bg)

    c.setFillColor(accent)
    c.roundRect(x + 24, y + CARD_H - 14, CARD_W - 48, 2.5, 1, fill=1, stroke=0)

    c.setFillColor(accent)
    c.setFont("Courier-Bold", 9)
    c.drawString(x + 22, y + CARD_H - 30, f"#{str(num).zfill(3)}")

    c.saveState()
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFillAlpha(0.3)
    c.setFont("Courier", 7)
    c.drawRightString(x + CARD_W - 22, y + CARD_H - 30, top_right_label)
    c.restoreState()

    font_size = 56 if len(word) <= 3 else 48 if len(word) <= 5 else 38 if len(word) <= 7 else 32
    c.setFillColor(text_col)
    c.setFont("Helvetica-Bold", font_size)
    tw = c.stringWidth(word, "Helvetica-Bold", font_size)
    c.drawString(x + (CARD_W - tw) / 2, y + CARD_H / 2 - font_size / 3 + 2, word)

    c.saveState()
    c.setFillColor(accent)
    c.setFillAlpha(0.25)
    c.setFont("Courier", 6)
    c.drawCentredString(x + CARD_W / 2, y + 16, pal.get("label", "SIGHT WORD FLASHCARD"))
    c.restoreState()


def draw_back(c, x, y, word, num, pal, sentence):
    bg = HexColor(pal["bg"])
    accent = HexColor(pal["accent"])
    text_col = HexColor(pal["text"])

    draw_rounded_rect(c, x, y, CARD_W, CARD_H, CARD_R, bg)

    c.setFillColor(accent)
    c.roundRect(x + 24, y + CARD_H - 14, CARD_W - 48, 2.5, 1, fill=1, stroke=0)

    c.saveState()
    c.setFillColor(text_col)
    c.setFillAlpha(0.5)
    c.setFont("Helvetica", 15)
    tw = c.stringWidth(word, "Helvetica", 15)
    c.drawString(x + (CARD_W - tw) / 2, y + CARD_H - 46, word)
    c.restoreState()

    c.setFillColor(accent)
    max_w = CARD_W - 50

    if c.stringWidth(sentence, "Helvetica", 17) <= max_w:
        c.setFont("Helvetica", 17)
        sw = c.stringWidth(sentence, "Helvetica", 17)
        c.drawString(x + (CARD_W - sw) / 2, y + CARD_H / 2 - 12, sentence)
    else:
        c.setFont("Helvetica", 14)
        words_list = sentence.split()
        lines, current = [], ""
        for w in words_list:
            test = current + " " + w if current else w
            if c.stringWidth(test, "Helvetica", 14) <= max_w:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        total_h = len(lines) * 22
        start_y = y + CARD_H / 2 + total_h / 2 - 18
        for i, line in enumerate(lines):
            lw = c.stringWidth(line, "Helvetica", 14)
            c.drawString(x + (CARD_W - lw) / 2, start_y - i * 22, line)

    c.saveState()
    c.setFillColor(accent)
    c.setFillAlpha(0.2)
    c.setFont("Courier", 6.5)
    c.drawCentredString(x + CARD_W / 2, y + 16, f"#{str(num).zfill(3)}  ·  USE IN A SENTENCE")
    c.restoreState()


# ============================================================
# FREQUENCY BAND DECK
# ============================================================

def build_frequency_deck(output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle("Sight Word Flashcards — Frequency Bands")
    c.setAuthor("RTN Communication & Literacy")

    total_pages = math.ceil(len(WORDS) / CARDS_PER_PAGE)

    # Cover
    draw_page_bg(c)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W/2, H - 120, "Sight Word Flashcards")
    c.saveState()
    c.setFillColor(HexColor("#ffffff")); c.setFillAlpha(0.4)
    c.setFont("Courier", 10)
    c.drawCentredString(W/2, H - 148, "THE FIRST 100 CHILDREN'S PICTURE BOOK SIGHT WORDS")
    c.restoreState()
    c.saveState()
    c.setFillColor(HexColor("#ffffff")); c.setFillAlpha(0.25)
    c.setFont("Courier", 8)
    c.drawCentredString(W/2, H - 170, "(Green et al., 2024)  ·  From Making Words Stick (Ness & Miles, 2025)")
    c.restoreState()

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W/2, H - 260, "Color Key")
    swatch_w, swatch_h = 340, 56
    key_start_y = H - 330
    for band_num in [1, 2, 3, 4]:
        pal = BAND_PALETTES[band_num]
        sy = key_start_y - (band_num - 1) * (swatch_h + 14)
        sx = (W - swatch_w) / 2
        draw_rounded_rect(c, sx, sy, swatch_w, swatch_h, 10, HexColor(pal["bg"]))
        c.setFillColor(HexColor(pal["accent"]))
        c.roundRect(sx + 16, sy + swatch_h - 8, swatch_w - 32, 2, 1, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(sx + 20, sy + 18, pal["band_name"])
        c.setFillColor(HexColor(pal["text"]))
        c.setFont("Courier", 8)
        c.drawRightString(sx + swatch_w - 20, sy + 20, pal["label"])

    c.saveState()
    c.setFillColor(HexColor("#ffffff")); c.setFillAlpha(0.15)
    c.setFont("Courier", 7)
    c.drawCentredString(W/2, 24, "RTN COMMUNICATION & LITERACY")
    c.restoreState()
    c.showPage()

    # Cards
    for page_idx in range(total_pages):
        start = page_idx * CARDS_PER_PAGE
        end = min(start + CARDS_PER_PAGE, len(WORDS))
        page_words = WORDS[start:end]

        draw_page_bg(c)
        c.setFillColor(HexColor("#333333")); c.setFont("Courier", 6)
        c.drawCentredString(W/2, 10, f"SIGHT WORDS  ·  FRONT  ·  PAGE {page_idx+1}/{total_pages}  ·  PRINT DOUBLE-SIDED, FLIP ON SHORT EDGE")
        for i, word in enumerate(page_words):
            num = start + i + 1
            pal = BAND_PALETTES[get_band(num)]
            x, y = get_card_pos(i)
            draw_front(c, x, y, word, num, pal, pal["band_name"])
        c.showPage()

        draw_page_bg(c)
        c.setFillColor(HexColor("#333333")); c.setFont("Courier", 6)
        c.drawCentredString(W/2, 10, f"SIGHT WORDS  ·  BACK  ·  PAGE {page_idx+1}/{total_pages}")
        for i, word in enumerate(page_words):
            num = start + i + 1
            pal = BAND_PALETTES[get_band(num)]
            x, y = get_back_card_pos(i)
            draw_back(c, x, y, word, num, pal, SENTENCES[word])
        c.showPage()

    c.save()
    print(f"  ✓ {output_path}")


# ============================================================
# MONTESSORI GRAMMAR DECK
# ============================================================

def build_montessori_deck(output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle("Sight Word Flashcards — Montessori Grammar")
    c.setAuthor("RTN Communication & Literacy")

    total_pages = math.ceil(len(WORDS) / CARDS_PER_PAGE)

    # Cover
    draw_page_bg(c)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(W/2, H - 100, "Sight Word Flashcards")
    c.saveState()
    c.setFillColor(HexColor("#ffffff")); c.setFillAlpha(0.4)
    c.setFont("Courier", 10)
    c.drawCentredString(W/2, H - 128, "MONTESSORI GRAMMAR COLOR CODING")
    c.restoreState()
    c.saveState()
    c.setFillColor(HexColor("#ffffff")); c.setFillAlpha(0.25)
    c.setFont("Courier", 8)
    c.drawCentredString(W/2, H - 150, "(Green et al., 2024)  ·  From Making Words Stick (Ness & Miles, 2025)")
    c.restoreState()

    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(W/2, H - 210, "Montessori Grammar Color Key")

    legend_order = [
        ("verb", "Action words", "is, was, said, have, go..."),
        ("pronoun", "Stand-in words", "I, you, he, she, they..."),
        ("adverb", "Modifiers (how/when/where)", "so, up, not, now, very..."),
        ("preposition", "Position & relation words", "to, in, of, for, on..."),
        ("adjective", "Describing words", "all, little, big, good, new..."),
        ("conjunction", "Connecting words", "and, but, as, if, or"),
        ("article", "Noun introducers", "the, a, an"),
        ("noun", "Person/place/thing words", "day, time, way, night"),
        ("interjection", "Exclamation words", "oh"),
    ]
    swatch_w, swatch_h = 420, 44
    key_start_y = H - 250
    for i, (pos, desc, examples) in enumerate(legend_order):
        pal = MONTESSORI_PALETTES[pos]
        sy = key_start_y - i * (swatch_h + 8)
        sx = (W - swatch_w) / 2
        draw_rounded_rect(c, sx, sy, swatch_w, swatch_h, 8, HexColor(pal["bg"]))
        c.setFillColor(HexColor(pal["accent"]))
        c.roundRect(sx + 12, sy + swatch_h - 6, swatch_w - 24, 2, 1, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(sx + 16, sy + 16, f"{pal['symbol']}  {pal['label']}")
        c.setFillColor(HexColor(pal["text"] if "text" in pal else "#cccccc"))
        c.setFont("Helvetica", 8)
        c.drawString(sx + 16, sy + 4, desc)
        c.saveState()
        c.setFillColor(HexColor(pal["text"] if "text" in pal else "#cccccc")); c.setFillAlpha(0.45)
        c.setFont("Courier", 7)
        c.drawRightString(sx + swatch_w - 16, sy + 16, examples)
        c.restoreState()

    c.saveState()
    c.setFillColor(HexColor("#ffffff")); c.setFillAlpha(0.15)
    c.setFont("Courier", 7)
    c.drawCentredString(W/2, 24, "RTN COMMUNICATION & LITERACY")
    c.restoreState()
    c.showPage()

    # Cards
    for page_idx in range(total_pages):
        start = page_idx * CARDS_PER_PAGE
        end = min(start + CARDS_PER_PAGE, len(WORDS))
        page_words = WORDS[start:end]

        draw_page_bg(c)
        c.setFillColor(HexColor("#333333")); c.setFont("Courier", 6)
        c.drawCentredString(W/2, 10, f"MONTESSORI GRAMMAR  ·  FRONT  ·  PAGE {page_idx+1}/{total_pages}  ·  PRINT DOUBLE-SIDED, FLIP ON SHORT EDGE")
        for i, word in enumerate(page_words):
            num = start + i + 1
            pos = WORD_POS[word]
            pal = MONTESSORI_PALETTES[pos]
            x, y = get_card_pos(i)
            # For Montessori, top-right shows POS symbol + label
            c.saveState()
            draw_front(c, x, y, word, num, pal, f"{pal['symbol']} {pal['label']}")
            c.restoreState()
        c.showPage()

        draw_page_bg(c)
        c.setFillColor(HexColor("#333333")); c.setFont("Courier", 6)
        c.drawCentredString(W/2, 10, f"MONTESSORI GRAMMAR  ·  BACK  ·  PAGE {page_idx+1}/{total_pages}")
        for i, word in enumerate(page_words):
            num = start + i + 1
            pos = WORD_POS[word]
            pal = MONTESSORI_PALETTES[pos]
            x, y = get_back_card_pos(i)
            draw_back(c, x, y, word, num, pal, SENTENCES[word])
        c.showPage()

    c.save()
    print(f"  ✓ {output_path}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pdf")
    os.makedirs(out_dir, exist_ok=True)

    print("Generating sight word flashcard PDFs...\n")
    build_frequency_deck(os.path.join(out_dir, "sight-words-frequency-bands.pdf"))
    build_montessori_deck(os.path.join(out_dir, "sight-words-montessori.pdf"))
    print("\nDone!")
