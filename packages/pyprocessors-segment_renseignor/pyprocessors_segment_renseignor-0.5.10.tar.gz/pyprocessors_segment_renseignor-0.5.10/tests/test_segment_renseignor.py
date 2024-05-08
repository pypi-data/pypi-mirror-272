import json
from pathlib import Path

from pymultirole_plugins.v1.schema import Document, DocumentList

from pyprocessors_segment_renseignor.segment_renseignor import (
    SegmentRenseignorProcessor,
    SegmentRenseignorParameters,
)


def test_model():
    model = SegmentRenseignorProcessor.get_model()
    model_class = model.construct().__class__
    assert model_class == SegmentRenseignorParameters


def test_segment_renseignor():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/renseignor-document-test.json")
    with source.open("r") as fin:
        jdoc = json.load(fin)
        original_doc = Document(**jdoc)
    processor = SegmentRenseignorProcessor()
    parameters = SegmentRenseignorParameters()

    docs = processor.process([original_doc], parameters)
    assert len(docs) == 28
    result = Path(testdir, "data/renseignor-document-segmented.json")
    dl = DocumentList(__root__=docs)
    with result.open("w") as fout:
        print(dl.json(exclude_none=True, exclude_unset=True, indent=2), file=fout)
