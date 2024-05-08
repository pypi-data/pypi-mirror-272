# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""

# bring classes directly into package namespace, to save some typing
from .similarity import SimilarityABC
from .bert_similarity import BertSimilarity
from .bert_similarity import BertSimilarity as Similarity

from .fast_bert_similarity import AnnoySimilarity, HnswlibSimilarity
from .literal_similarity import (
    SimHashSimilarity,
    TfidfSimilarity,
    BM25Similarity,
    WordEmbeddingSimilarity,
    CilinSimilarity,
    HownetSimilarity,
    SameCharsSimilarity,
    SequenceMatcherSimilarity,
)
from .ensemble_similarity import EnsembleSimilarity

from .utils.util import cos_sim, dot_score, pairwise_dot_score, pairwise_cos_sim, normalize_embeddings, \
    semantic_search, paraphrase_mining_embeddings, community_detection