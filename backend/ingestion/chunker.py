# page-wise chunking; preserves page/span metadata

from typing import List, Dict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import json
# from pathlib import Path


def _load_page_index(page_index_path: str) -> Dict: 
    with open(page_index_path, 'r', encoding='utf-8') as f:
        return json.load(f) # loads the word map
    #Parses JSON into a Python dictionary and returns it. The dictionary contains page text and word metadata.


def make_page_chunks(manifest: Dict, *, chunk_size: int = 1000, chunk_overlap: int = 120) -> List[Document]:
    """Create chunks per page, preserving span offsets and page metadata."""
    pi = _load_page_index(manifest["page_index_path"])
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    documents: List[Document] = []

    for page_str, payload in pi.items():
        page_no = int(page_str)
        text = payload.get("text", "")
        if not text:
            continue
        chunks = splitter.split_text(text)
        # Recompute spans within page text
        cursor = 0
        for ch in chunks:
            # Find the chunk in page text from current cursor to handle duplicates
            rel = text.find(ch, cursor)
            if rel < 0:
                rel = text.find(ch)  # fallback
                # If not found after cursor, try searching the entire page.
            if rel < 0:
                rel = 0
                # Absolute fallback — avoid crashing.
            start = rel
            end = rel + len(ch)
            cursor = end
            metadata = {
                "doc_id": manifest["doc_id"],
                "source_path": manifest["source_path"],
                "name": manifest["name"],
                "page": page_no,
                "span_start": start,
                "span_end": end,
            }
            documents.append(Document(page_content=ch, metadata=metadata))

    return documents
