from pathlib import Path
import json, re

text_path = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-48ab8abb9a.md")
text = text_path.read_text(encoding="utf-8")

# Strip to body after title
marker = "*** START OF THE PROJECT GUTENBERG EBOOK THE UNITED STATES CONSTITUTION ***"
idx = text.find(marker)
text_clean = text[idx + len(marker):].strip()
footer = "*** END OF THE PROJECT GUTENBERG EBOOK THE UNITED STATES CONSTITUTION ***"
fidx = text_clean.find(footer)
if fidx != -1:
    text_clean = text_clean[:fidx].strip()

lines = text_clean.splitlines()
cut = 0
for i, l in enumerate(lines):
    if l.startswith("THE CONSTITUTION OF THE UNITED STATES OF AMERICA, 1787"):
        cut = i
        break
constitution_body = "\n".join(lines[cut:])

anchors = {
    "legislative_art1s1": "All legislative Powers herein granted shall be vested in a Congress of the United States, which shall consist of a Senate and House of Representatives.",
    "commerce_art1s8": "To regulate Commerce with foreign Nations, and among the several States, and with the Indian Tribes.",
    "tax_art1s8": "To lay and collect Taxes, Duties, Imposts and Excises, to pay the Debts and provide for the common Defence and general Welfare of the United States; but all Duties, Imposts and Excises shall be uniform throughout the United States;",
    "coin_art1s8": "To coin Money, regulate the Value thereof, and of foreign Coin, and fix the Standard of Weights and Measures;",
    "tender_art1s10": "No State shall enter into any Treaty, Alliance, or Confederation; grant Letters of Marque and Reprisal; coin Money; emit Bills of Credit; make any Thing but gold and silver Coin a Tender in Payment of Debts; pass any Bill of Attainder, ex post facto Law, or Law impairing the Obligation of Contracts, or grant any Title of Nobility.",
    "militia_art1s8_call": "To provide for calling forth the Militia to execute the Laws of the Union, suppress Insurrections and repel Invasions;",
    "militia_art1s8_organize": "To provide for organizing, arming, and disciplining, the Militia, and for governing such Part of them as may be employed in the Service of the United States, reserving to the States respectively, the Appointment of the Officers, and the Authority of training the militia according to the discipline prescribed by Congress;",
    "treason_art3s3": "Treason against the United States, shall consist only in levying War against them, or in adhering to their Enemies, giving them Aid and Comfort. No Person shall be convicted of Treason unless on the Testimony of two Witnesses to the same overt Act, or on Confession in open Court.",
    "habeas_art1s9": "The Privilege of the Writ of Habeas Corpus shall not be suspended, unless when in Cases of Rebellion or Invasion the public Safety may require it.",
    "attainder_art1s9": "No Bill of Attainder or ex post facto Law shall be passed.",
    "attainder_art1s10": "No State shall enter into any Treaty, Alliance, or Confederation; grant Letters of Marque and Reprisal; coin Money; emit Bills of Credit; make any Thing but gold and silver Coin a Tender in Payment of Debts; pass any Bill of Attainder, ex post facto Law, or Law impairing the Obligation of Contracts, or grant any Title of Nobility.",
    "expostfacto_art1s9": "No Bill of Attainder or ex post facto Law shall be passed.",
    "expostfacto_art1s10": "No State shall enter into any Treaty, Alliance, or Confederation; grant Letters of Marque and Reprisal; coin Money; emit Bills of Credit; make any Thing but gold and silver Coin a Tender in Payment of Debts; pass any Bill of Attainder, ex post facto Law, or Law impairing the Obligation of Contracts, or grant any Title of Nobility.",
    "contract_art1s10": "No State shall enter into any Treaty, Alliance, or Confederation; grant Letters of Marque and Reprisal; coin Money; emit Bills of Credit; make any Thing but gold and silver Coin a Tender in Payment of Debts; pass any Bill of Attainder, ex post facto Law, or Law impairing the Obligation of Contracts, or grant any Title of Nobility.",
    "money_art1s8": "To coin Money, regulate the Value thereof, and of foreign Coin, and fix the Standard of Weights and Measures;",
    "money_art1s10": "coin Money; emit Bills of Credit; make any Thing but gold and silver Coin a Tender in Payment of Debts; pass any Bill of Attainder, ex post facto Law, or Law impairing the Obligation of Contracts, or grant any Title of Nobility.",
    "writ_art1s9": "The Privilege of the Writ of Habeas Corpus shall not be suspended, unless when in Cases of Rebellion or Invasion the public Safety may require it.",
    "emolument_art1s6": "No Senator or Representative shall, during the Time for which he was elected, be appointed to any civil Office under the authority of the United States, which shall have been created, or the Emoluments whereof shall have been increased during such time; and no Person holding any Office under the United States, shall be a Member of either House during his Continuance in Office.",
    "emolument_art2s1": "The President shall, at stated Times, receive for his Services, a Compensation, which shall neither be encreased nor diminished during the Period for which he shall have been elected, and he shall not receive within that Period any other Emolument from the United States, or any of them."
}

anchor_offsets = {}
for k, v in anchors.items():
    idx = constitution_body.find(v)
    if idx == -1:
        vv = " ".join(v.split())
        idx = constitution_body.find(vv)
        v = vv
    if idx == -1:
        raise SystemExit(f"anchor not found: {k}")
    anchor_offsets[k] = idx

term_needles = {
    "legislative": [("legislative_art1s1","All legislative Powers")],
    "commerce": [("commerce_art1s8","regulate Commerce with foreign Nations, and among the several States, and with the Indian Tribes.")],
    "tax": [
        ("tax_art1s8","To lay and collect Taxes, Duties, Imposts and Excises, to pay the Debts"),
        ("tax_art1s8","all Duties, Imposts and Excises shall be uniform throughout the United States"),
    ],
    "coin": [
        ("coin_art1s8","To coin Money, regulate the Value thereof, and of foreign Coin,"),
    ],
    "tender": [("tender_art1s10","make any Thing but gold and silver Coin a Tender in Payment of Debts")],
    "militia": [
        ("militia_art1s8_call","To provide for calling forth the Militia to execute the Laws of the Union,"),
        ("militia_art1s8_organize","To provide for organizing, arming, and disciplining, the Militia"),
        ("militia_art1s8_organize","training the militia according to the discipline prescribed by Congress"),
    ],
    "treason": [("treason_art3s3","Treason against the United States")],
    "habeas corpus": [("habeas_art1s9","The Privilege of the Writ of Habeas Corpus shall not be suspended, unless when in Cases of Rebellion or Invasion the public Safety may require it.")],
    "attainder": [
        ("attainder_art1s9","No Bill of Attainder or ex post facto Law shall be passed."),
        ("attainder_art1s10","Bill of Attainder"),
    ],
    "ex post facto": [
        ("expostfacto_art1s9","ex post facto Law shall be passed."),
        ("expostfacto_art1s10","ex post facto Law"),
    ],
    "contract": [("contract_art1s10","Law impairing the Obligation of Contracts")],
    "money": [
        ("money_art1s8","To coin Money, regulate the Value thereof"),
    ],
    "writ": [("writ_art1s9","The Privilege of the Writ of Habeas Corpus shall not be suspended, unless when in Cases of Rebellion or Invasion the public Safety may require it.")],
    "emolument": [
        ("emolument_art1s6","Emoluments whereof shall have been increased"),
        ("emolument_art2s1","any other Emolument from the United States"),
    ]
}

rows = []
for term, occs in term_needles.items():
    for anchor_key, needle in occs:
        anchor_start = anchor_offsets[anchor_key]
        local = constitution_body[anchor_start: anchor_start + len(anchors[anchor_key])]
        start2 = local.find(needle)
        if start2 == -1:
            start2 = local.find(" ".join(needle.split()))
            needle = " ".join(needle.split())
        if start2 == -1:
            raise SystemExit(f"needle fail {term} {anchor_key}: {needle!r}")
        rows.append((term, anchor_key, needle, anchor_start + start2, anchor_start + start2 + len(needle)))

# Build unique rows and print
out = {}
for term, anchor_key, needle, start, end in rows:
    out.setdefault(term, []).append({"anchor": anchor_key, "needle": needle, "start": start, "end": end})

print(json.dumps({
    "body_len": len(constitution_body),
    "rows": out
}, indent=2))
