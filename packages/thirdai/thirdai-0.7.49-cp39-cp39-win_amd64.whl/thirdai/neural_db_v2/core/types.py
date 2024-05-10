from dataclasses import dataclass
from typing import List, Optional, Union

import numpy as np
import pandas as pd
from pandera import typing as pt
from thirdai import data

# We typedef doc ID to anticipate switching over to string IDs
ChunkId = int

Score = float


@dataclass
class NewChunk:
    """A chunk that has not been assigned a unique ID."""

    # An optional identifier supplied by the user.
    custom_id: Union[str, int, None]

    # The text content of the chunk, e.g. a paragraph.
    text: str

    # Keywords / strong signals.
    keywords: str

    # Arbitrary metadata related to the chunk.
    metadata: dict

    # Parent document name
    document: str


@dataclass
class Chunk(NewChunk):
    """A chunk that has been assigned a unique ID."""

    # A unique identifier assigned by a chunk store.
    chunk_id: ChunkId


"""Design choices for batch objects:
- Column oriented so we can efficiently convert it to a ColumnMap
- Pandas series instead of Columns.
  - Series can contain dictionaries, which is useful for the metadata field. 
  - Many libraries natively accept Series or Numpy arrays, which
    Series can easily convert into, so this is useful for when we implement
    chunk stores or retrievers using external libraries.
  - Series are easy to work with in Python, preventing the need to write 
    more bindings and tools for Columns.
- Store individual columns as named fields instead of storing a dataframe to
  prevent errors from column name typos.
- __getitem__ method to access individual rows for convenience.
"""


@dataclass
class NewChunkBatch:
    custom_id: Union[pt.Series[str], pt.Series[int], None]
    text: pt.Series[str]
    keywords: pt.Series[str]
    metadata: Optional[pt.DataFrame]
    document: pt.Series[str]

    def __len__(self):
        return len(self.text)

    def __getitem__(self, i: int):
        return NewChunk(
            custom_id=self.custom_id[i],
            text=self.text[i],
            keywords=self.keywords[i],
            metadata=self.metadata[i],
            document=self.document[i],
        )

    def to_df(self):
        columns = {
            "text": self.text,
            "keywords": self.keywords,
            "document": self.document,
        }
        if self.custom_id is not None:
            columns["custom_id"] = self.custom_id
        else:
            columns["custom_id"] = pd.Series(np.full(len(self.text), None))

        return pd.DataFrame(columns)


@dataclass
class ChunkBatch:
    chunk_id: pt.Series[ChunkId]
    text: pt.Series[str]
    keywords: pt.Series[str]

    def __post_init__(self):
        self.chunk_id = self.chunk_id.reset_index(drop=True)
        self.text = self.text.reset_index(drop=True)
        self.keywords = self.keywords.reset_index(drop=True)

    def to_df(self):
        return pd.DataFrame(self.__dict__)


@dataclass
class CustomIdSupervisedSample:
    query: str
    custom_id: Union[List[str], List[int]]


@dataclass
class SupervisedSample:
    query: str
    chunk_id: List[ChunkId]


@dataclass
class CustomIdSupervisedBatch:
    query: pt.Series[str]
    custom_id: Union[pt.Series[List[str]], pt.Series[List[int]]]

    def __post_init__(self):
        self.query = self.query.reset_index(drop=True)
        self.custom_id = self.custom_id.reset_index(drop=True)

    def __getitem__(self, i: int):
        return CustomIdSupervisedSample(
            query=self.query[i],
            custom_id=self.custom_id[i],
        )

    def to_df(self):
        return pd.DataFrame(self.__dict__)


@dataclass
class SupervisedBatch:
    query: pt.Series[str]
    chunk_id: pt.Series[List[ChunkId]]

    def __post_init__(self):
        self.query = self.query.reset_index(drop=True)
        self.chunk_id = self.chunk_id.reset_index(drop=True)

    def __getitem__(self, i: int):
        return SupervisedSample(
            query=self.query[i],
            chunk_id=self.chunk_id[i],
        )

    def to_df(self):
        return pd.DataFrame(self.__dict__)
