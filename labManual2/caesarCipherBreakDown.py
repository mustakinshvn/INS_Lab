from typing import List, Dict
import sys
import string
from pathlib import Path

# A short ordered list of common words. More common words earlier for higher weight.
_COMMON_WORDS = [
    "the","be","to","of","and","a","in","that","have","i","it","for","not","on","with",
    "he","as","you","do","at","this","but","his","by","from","they","we","say","her","she",
    "or","an","will","my","one","all","would","there","their","what","so","up","out","if",
    "about","who","get","which","go","me","when","make","can","like","time","no","just",
    "him","know","take","people","into","year","your","good","some","could","them","see",
    "other","than","then","now","look","only","come","its","over","think","also","back",
    "after","use","two","how","our","work","first","well","way","even","new","want","because"
]

# Precompute weights: longer words and earlier (more common) words get higher weight.
_WORD_WEIGHTS: Dict[str, int] = {}
for idx, w in enumerate(_COMMON_WORDS):
    base = max(1, len(w))
    bonus = 3 if idx < 20 else 2 if idx < 50 else 1
    _WORD_WEIGHTS[w] = base * bonus

ALPHABET = string.ascii_lowercase
ALPHA_LEN = 26
_ALPHA_INDEX = {c: i for i, c in enumerate(ALPHABET)}


# Load sample ciphertext from nearby cipherText.txt if present.
_CIPHER_FILE = Path(__file__).parent / "cipherText.txt"
if _CIPHER_FILE.exists():
    try:
        SAMPLE_CIPHER = _CIPHER_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        SAMPLE_CIPHER = ""
else:
    SAMPLE_CIPHER = ""


def caesar_shift(s: str, shift: int) -> str:
    out = []
    for ch in s:
        if ch in _ALPHA_INDEX:
            i = _ALPHA_INDEX[ch]
            out.append(ALPHABET[(i - shift) % ALPHA_LEN])
        else:
            out.append(ch)
    return "".join(out)


def score_plaintext(plain: str, word_weights: Dict[str, int] = None) -> int:
    if word_weights is None:
        word_weights = _WORD_WEIGHTS
    score = 0
    # Count each word's non-overlapping occurrences (str.count) and add weight*count.
    # Longer words implicitly have larger weight.
    for w, wt in word_weights.items():
        if w in plain:
            cnt = plain.count(w)
            score += wt * cnt
    # tiny bonus for having many alphabetic characters (discourage weird outputs)
    score += sum(1 for ch in plain if ch.isalpha())
    return score


def break_caesar(cipher: str, top_n: int = 5) -> List[Dict]:
    """Try all shifts 1..25 and return top_n candidate decryptions sorted by score desc."""
    cipher = cipher.strip()
    # validate: expect lowercase letters only (user stated no spaces, lowercase)
    if not cipher:
        return []
    # allow only a-z; non-alpha left as-is but warn by score behavior
    candidates = []
    for shift in range(1, 26):
        plain = caesar_shift(cipher, shift)
        sc = score_plaintext(plain)
        candidates.append({"shift": shift, "plaintext": plain, "score": sc})
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:top_n]


def pretty_print_candidates(cands: List[Dict]):
    for c in cands:
        print(f"shift={c['shift']:2d}  score={c['score']:4d}  plaintext : {c['plaintext']}")


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        cipher_text = sys.argv[1].strip()
    elif SAMPLE_CIPHER:
        cipher_text = SAMPLE_CIPHER
        print(f"Using sample ciphertext from cipherText.txt: {cipher_text}")
    else:
        print("Error: cipherText.txt not found or empty. Provide ciphertext as argv or create cipherText.txt")
        sys.exit(2)
    if not cipher_text:
        print("Empty input.")
        sys.exit(1)
    results = break_caesar(cipher_text, top_n=10)
    pretty_print_candidates(results)