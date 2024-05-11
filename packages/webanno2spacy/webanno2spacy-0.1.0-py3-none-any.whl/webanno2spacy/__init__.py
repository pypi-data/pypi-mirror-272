"""
Schema of WebAnno TSV file:
    [ID] [START_CHAR-END_CHAR] [TEXT] [LABEL] [RELATION_TYPE] [RELATION_HEAD_ID]
    Contiguous spans have the same label.

    Example of WebAnno TSV file piece::

        #Text=«И все-таки я выжил, – подумал Калак, торопясь ... груди. – На этот раз ...».
        23-1	1541-1542	«	_	_	_
        23-2	1542-1543	И	replica[1]	speaks	23-10[0_1]
        23-3	1544-1552	все-таки	replica[1]	_	_
        23-4	1553-1554	я	replica[1]	_	_
        23-5	1555-1560	выжил	replica[1]	_	_
        23-6	1560-1561	,	_	_	_
        23-7	1561-1562	 	_	_	_
        23-8	1562-1563	–	_	_	_
        23-9	1564-1571	подумал	_	_	_
        ...
        23-22	1628-1629	.	_	_	_
        23-23	1629-1630	 	_	_	_
        23-24	1630-1631	–	_	_	_
        23-25	1632-1634	На	replica[2]	speaks	23-10[0_2]
        23-26	1635-1639	этот	replica[2]	_	_
        23-27	1640-1643	раз	replica[2]	_	_
        ...

See also:
    - WebAnno TSV 3.2 File format:
      https://webanno.github.io/webanno/releases/3.4.5/docs/user-guide.html#sect_webannotsv
    - spaCy custom relation extraction pipeline:
      https://www.youtube.com/watch?v=8HL-Ap5_Axo
"""

import csv
import logging
import re
from collections import defaultdict, Counter
from pathlib import Path
from typing import Iterator, Optional

import spacy
import typer
from spacy import Language
from spacy.tokens import Doc

logger = logging.getLogger(__name__)
app = typer.Typer()


@app.command()
def convert_file(
    spacy_model: str,
    input_text_file: Path,
    input_webanno_file: Path,
    *,
    output_file: Optional[Path] = None,
):
    nlp = spacy.load(spacy_model)

    # Read input text file to string:
    input_text_file = Path(input_text_file)
    text = input_text_file.read_text()

    # Read input WebAnno file as TSV:
    with open(input_webanno_file) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        doc = convert_rows(nlp, text, rd)

    # Write output file:
    if not output_file:
        output_file = input_webanno_file.with_suffix(".spacy")
    doc.to_disk(output_file)


LABEL_WITH_SUB_RE = re.compile(r"^(?P<label>[a-zA-Z0-9-_]+)\[(?P<sub>[a-zA-Z0-9-_]+)]$")
FREQUENCY_THRESHOLD_PERCENT = 0.02


def convert_rows(
    language: Language,
    text,
    rows: Iterator[list[str]],
) -> Doc:
    # e.g. { "replica": [..., (1632, 1634), ...], "actor": [...], ... }
    label_to_spans: dict[str, list[tuple[tuple[str, str] | None, int, int]]] = (
        defaultdict(list)
    )
    # e.g. { (1632, 1634): ("speaks", 1572, 1577), ... }
    span_to_dep: dict[tuple[int, int], list[tuple[str, int, int]]] = defaultdict(list)
    id_to_span: dict[str, tuple[int, int]] = {}
    lines_normalized: bool = False
    for row in rows:
        if not lines_normalized and len(row) == 1:
            line = row[0]
            if line.startswith("#Text=") and r"\r" in line:
                text = text.replace("\n", "\r\n")
                lines_normalized = True
            continue

        if len(row) < 6:
            continue
        token_id, span_str, _, label, dep_type, dep_head, *_ = row
        if label == "_":
            continue
        start, end = [int(x) for x in span_str.split("-")]
        id_to_span[token_id] = (start, end)
        if id_with_sub := LABEL_WITH_SUB_RE.match(dep_head):
            head = (str(dep_type), id_with_sub.group("label"))
        elif isinstance(dep_head, str) and dep_head != "_":
            head = (str(dep_type), dep_head)
        else:
            head = None
        if label_with_num := LABEL_WITH_SUB_RE.match(label):
            label = label_with_num.group("label")
            num = int(label_with_num.group("sub"))
            spans = label_to_spans[label]
            if len(spans) <= int(num - 1):
                spans.append((head, start, end))
            else:
                spans[num - 1] = (spans[num - 1][0] or head, spans[num - 1][1], end)
        else:
            label_to_spans[label].append((head, start, end))

    for label, spans in label_to_spans.items():
        for head, start, end in spans:
            if not head:
                continue
            dep_type, dep_head_id = head
            if dep_head_id not in id_to_span:
                continue
            head_start, head_end = id_to_span[dep_head_id]
            span_to_dep[(start, end)].append((dep_type, head_start, head_end))

    all_dep_labels = Counter(t[0] for sl in span_to_dep.values() for t in sl)
    # Log a warning when some label occurs rarer than X% of all labels:
    total_labels = sum(all_dep_labels.values())
    for label, count in all_dep_labels.items():
        if count / total_labels < FREQUENCY_THRESHOLD_PERCENT:
            logger.warning(
                f"{label=} has <{FREQUENCY_THRESHOLD_PERCENT * 100}% occurrences ({count})"
            )

    span_to_label: dict[tuple[int, int], str] = {}
    for label, spans in label_to_spans.items():
        for head, start, end in spans:
            span_to_label[(start, end)] = label
    del label_to_spans

    doc = language(text)
    doc.set_extension("rel", default=defaultdict(dict), force=True)

    # Fill spaCy Doc's "rel" extension property with dict:
    # { (0, 6): { "label1": 1.0, "label2": 0.0 },
    #   (6, 0): { "label1": 0.0, "label2": 0.0 }, ... }
    for span, span_label in span_to_label.items():
        # find the Span-object in Doc which correspond to our [span]-tuple:
        start, end = span
        doc_span = doc.char_span(start, end, label=span_label, alignment_mode="strict")
        if not doc_span:
            logger.warning(f"{span=} not found in Doc: [{text[start:end]}]")
            continue
        deps = span_to_dep[span]
        for actual_dep_label, head_start, head_end in deps:
            head_span = doc.char_span(head_start, head_end, alignment_mode="strict")
            if not head_span:
                logger.warning(
                    f"{head_span=} not found in Doc: [{text[head_start:head_end]}]"
                )
                continue
            # set the ground-truth rel in the Doc:
            rels = doc._.rel[(doc_span.start_char, head_start)]
            rels[actual_dep_label] = 1.0
            # fill other non-present rels with 0s, if any
            for dl in all_dep_labels:
                if dl not in rels:
                    rels[dl] = 0.0

    return doc


if __name__ == "__main__":
    typer.run(convert_file)
