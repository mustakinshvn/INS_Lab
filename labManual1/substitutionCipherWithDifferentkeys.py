import re
import random
import math
from collections import Counter

# substitutionCipherWithDifferentkeys_frequency_only.py
# GitHub Copilot
# Solver using only letter frequency distribution (no other heuristics).


CIPHER_1 = """af p xpkcaqvnpk pfg, af ipqe qpri, gauuikifc tpw, ceiri udvk tiki afgarxifrphni cd eao-
-wvmd popkwn, hiqpvri du ear jvaql vfgikrcpfgafm du cei xkafqaxnir du xrwqedearcdkw pfg
du ear aopmafpcasi xkdhafmr afcd fit pkipr. ac tpr qdoudkcafm cd lfdt cepc au pfwceafm
epxxifig cd ringdf eaorinu hiudki cei opceiopcaqr du cei uaing qdvng hi qdoxnicinw tdklig dvc-
-pfg edt rndtnw ac xkdqiigig, pfg edt odvfcpafdvr cei dhrcpqnir--ceiki tdvng pc niprc kiopaf dfi
mddg oafg cepc tdvng qdfcafvi cei kiripkqe"""

CIPHER_2 = """aceah toz puvg vcdl omj puvg yudqecov, omj loj auum klu thmjuv hs klu zlcvu shv
zcbkg guovz, upuv zcmdu lcz vuwovroaeu jczoyyuovomdu omj qmubyudkuj vukqvm. klu
vcdluz lu loj avhqnlk aodr svhw lcz kvopuez loj mht audhwu o ehdoe eunumj, omj ck toz
yhyqeoveg auecupuj, tlokupuv klu hej sher wcnlk zog, klok klu lcee ok aon umj toz sqee hs
kqmmuez zkqssuj tckl kvuozqvu. omj cs klok toz mhk umhqnl shv sowu, kluvu toz oezh lcz
yvhehmnuj pcnhqv kh wovpue ok. kcwu thvu hm, aqk ck zuuwuj kh lopu eckkeu ussudk hm
wv. aonncmz. ok mcmukg lu toz wqdl klu zowu oz ok scskg. ok mcmukg-mcmu klug aunom kh
doee lcw tuee-yvuzuvpuj; aqk qmdlomnuj thqej lopu auum muovuv klu wovr. kluvu tuvu zhwu
klok zlhhr klucv luojz omj klhqnlk klcz toz khh wqdl hs o nhhj klcmn; ck zuuwuj qmsocv klok"""

ENGLISH_FREQ_ORDER = "etaoinshrdlcumwfgypbvkjxqz"
LETTERS = "abcdefghijklmnopqrstuvwxyz"

split_re = re.compile(r"[^a-zA-Z]+")

def letter_frequency_order(text):
    cnt = Counter(c.lower() for c in text if c.isalpha())
    order = [pair[0] for pair in cnt.most_common()]
    return order, cnt

def build_mapping_by_frequency(cipher_text):
    order, cnt = letter_frequency_order(cipher_text)
    mapping = {}
    # Map most frequent cipher letters to most frequent English letters
    for i, c in enumerate(order):
        if i < len(ENGLISH_FREQ_ORDER):
            mapping[c] = ENGLISH_FREQ_ORDER[i]
    # Fill remaining cipher letters with remaining plain letters in alphabetical order
    remaining_plain = [ch for ch in LETTERS if ch not in mapping.values()]
    for ch in LETTERS:
        if ch not in mapping:
            mapping[ch] = remaining_plain.pop(0)
    return mapping

def decode_with_map(text, mapping):
    out = []
    for ch in text:
        lower = ch.lower()
        if lower.isalpha():
            decoded = mapping.get(lower, '?')
            out.append(decoded.upper() if ch.isupper() else decoded)
        else:
            out.append(ch)
    return "".join(out)

def solve_cipher_frequency_only(cipher_text, name="Cipher"):
    print("====", name, "====")
    mapping = build_mapping_by_frequency(cipher_text)
    decoded = decode_with_map(cipher_text, mapping)
    print("\nDecoded (frequency mapping only):\n")
    print(decoded[:2000])
    print("\nMapping (cipher -> plain):")
    for c in LETTERS:
        print(f"{c} -> {mapping[c]}", end=", ")
    print("\n")
    return decoded

def main():
    dec1 = solve_cipher_frequency_only(CIPHER_1, "Cipher-1")
    print("\n\n")
    dec2 = solve_cipher_frequency_only(CIPHER_2, "Cipher-2")

if __name__ == "__main__":
    main()
