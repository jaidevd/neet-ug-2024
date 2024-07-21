# coding: utf-8
import fitz
import pandas as pd
import re
from tqdm import tqdm
import glob
import os.path as op


FILES = glob.glob('pdfs/*.pdf')
pattern = re.compile(r'^\s+(?P<srl>\d+)\s+(?P<marks>-?\d+)\s+$')
address_pat = re.compile(
        r'Page No\.\s+\d+\n(.*?)\n(?:NEET \(UG\) 2024)?', re.DOTALL)


def extract_address(text):
    match = address_pat.search(text)
    if match:
        return match.group(1).strip()
    return None


scores = []
addresses = []
for file in tqdm(FILES):
    with fitz.open(file) as doc:
        center_scores = []
        address = None
        centre = int(op.splitext(op.basename(file))[0])
        for page in doc:
            for i, b in enumerate(page.get_text_blocks()):
                s = b[-3]
                if i == 0:
                    address = extract_address(s)
                    if address is None:
                        from ipdb import set_trace
                        set_trace()
                        raise ValueError('Bad address')
                    addresses.append({'centre': centre, 'address': address})
                else:
                    match = re.match(pattern, s)
                    if match:
                        rec = {'centre': centre}
                        rec.update(match.groupdict())
                        center_scores.append(rec)
        scores.extend(center_scores)

df = pd.DataFrame.from_records(scores)
assert df['centre'].nunique() == 4750
for center, xdf in df.groupby('centre'):
    assert len(xdf) == xdf['srl'].nunique()

df.to_csv("data3.csv", index=False)
pd.DataFrame.from_records(addresses).drop_duplicates().to_csv(
    'addresses.tsv', index=False, sep='\t')

with pd.ExcelWriter('neet-2024-scores.xlsx') as writer:
    df.iloc[:1_000_000].to_excel(writer, sheet_name='Scores-1', index=False)
    df.iloc[1_000_000:2_000_000].to_excel(writer, sheet_name='Scores-2', index=False)
    df.iloc[2_000_000:].to_excel(writer, sheet_name='Scores-3', index=False)
    pd.DataFrame(addresses).drop_duplicates().to_excel(writer, sheet_name='Centres', index=False)
