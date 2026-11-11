# Awesome Temporal & Dynamic Graph Learning

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated collection of papers, code, datasets, benchmarks, and libraries for **temporal and dynamic graph learning**. Topics include temporal graph neural networks, dynamic link prediction, text-attributed graphs, anomaly detection, and continual learning.

[Paper Explorer](https://luckygirl-xu.github.io/Awesome-DynamicGraphLearning/) · [Getting Started](#getting-started) · [Recent Papers](#recent-papers) · [Full Paper Lists](#full-paper-lists-by-topic) · [Datasets & Benchmarks](resources/datasets-and-benchmarks.md) · [Libraries](resources/libraries.md) · [Contributing](CONTRIBUTING.md)

## Getting Started

1. **Read a survey.** Start with [Representation Learning for Dynamic Graphs](https://arxiv.org/abs/1905.11485) or [Graph Neural Networks for Temporal Graphs](https://arxiv.org/abs/2302.01018).
2. **Explore implementations.** Start with [TCSD](https://github.com/LuckyGirl-XU/TCSD) (NeurIPS 2026), [TGAT](https://github.com/StatsDLMathsRecomSys/Inductive-representation-learning-on-temporal-graphs), [TGN](https://github.com/twitter-research/tgn), or [GraphMixer](https://github.com/CongWeilin/GraphMixer). [DyGLib](https://github.com/yule-BUAA/DyGLib) brings multiple temporal graph methods into one library.
3. **Choose a benchmark.** Explore [TGB](https://tgb.complexdatalab.com/) for temporal link and node prediction, [TGB-Seq](https://github.com/TGB-Seq/TGB-Seq) for sequential interaction dynamics, and [DTGB](https://github.com/zjs123/DTGB) for dynamic text-attributed graphs.

## Recent Papers

Representative papers across all seven topics, with separate tasks for continuous-time graphs. The selection uses 2026 papers, plus FastHeP (KDD 2025) for temporal hypergraphs. Browse the [full paper lists](#full-paper-lists-by-topic) for all years.

<!-- RECENT_PAPERS:START -->

| Paper | Venue | Topic / Task |
| --- | --- | --- |
| [TCSD: A New Perspective on Target-Conditioned Structural Dynamics for Link Prediction in Dynamic Graphs](https://openreview.net/forum?id=YfsyoH7YFs) · [Code](https://github.com/LuckyGirl-XU/TCSD) | NeurIPS 2026 | [CTDG · Link Prediction](papers/continuous-time.md#2026) |
| [Revisiting Node Affinity Prediction in Temporal Graphs](https://arxiv.org/pdf/2510.06940) | ICLR 2026 | [CTDG · Node Affinity](papers/continuous-time.md#2026) |
| [Hydra: Towards Transferable Multi-Task Learning on Temporal Graphs](https://openreview.net/forum?id=q45V4tagJs) | NeurIPS 2026 | [CTDG · Multi-task](papers/continuous-time.md#2026) |
| [Temporal Graph Thumbnail: Robust Representation Learning with Global Evolutionary Skeleton](https://proceedings.iclr.cc/paper_files/paper/2026/hash/df29d63af05cb91d705cf06ba5945b9d-Abstract-Conference.html) | ICLR 2026 | [DTDG · Representation Learning](papers/discrete-time.md#2026) |
| [Understanding Evolving Graph Structures for Large Discrete-Time Dynamic Graph Representation](https://www.vldb.org/pvldb/vol19/p862-xu.pdf) | VLDB 2026 | [DTDG · Evolving Structures](papers/discrete-time.md#2026) |
| [MoMent: Unlocking Multi-Modal Potentials for Dynamic Text-Attributed Graph Representation](https://arxiv.org/pdf/2502.19651) · [Code](https://github.com/LuckyGirl-XU/MoMent) | AAAI 2026 | [Text-attributed · Link Prediction](papers/text-attributed.md#2026) |
| [Mitigating Anomaly Hallucination: A Model-Agnostic Framework for Unsupervised Anomaly Detection on Dynamic Graphs](https://dl.acm.org/doi/10.1145/3770855.3817610) | KDD 2026 | [Anomaly Detection](papers/anomaly-detection.md#2026) |
| [FastHeP: Fast and Accurate Temporal Hypergraph Representation for Hyperedge Prediction](https://dl.acm.org/doi/10.1145/3690624.3709327) · [Code](https://github.com/LuckyGirl-XU/FastHeP) | KDD 2025 | [Hypergraph · Hyperedge Prediction](papers/temporal-hypergraphs.md#2025) |
| [Efficient Dynamic Algorithms for Graph Neural Networks with Non-Linearity](https://openreview.net/forum?id=DC1kP2puyf) | NeurIPS 2026 | [Streaming · Dynamic Updates](papers/streaming.md#2026) |
| [UFO: A Unified Flow-Oriented Framework for Robust Continual Graph Learning](https://openreview.net/forum?id=38kpqzHh0B) | NeurIPS 2026 | [Continual Learning](papers/continual-learning.md#2026) |

<!-- RECENT_PAPERS:END -->

<a id="Publications"></a>

<a id="research-topics"></a>

## Full Paper Lists by Topic

**Click a topic below to open its complete paper list**, including available surveys, benchmarks, and paper/code links organized by year. Use the [Paper Explorer](https://luckygirl-xu.github.io/Awesome-DynamicGraphLearning/) to filter across all topics.

### Graph Representations — Full Paper Lists

| Topic | Focus |
| --- | --- |
| <a id="continuous"></a>[Continuous-Time Dynamic Graphs — Full paper list](papers/continuous-time.md) | Timestamped interactions, event-based models, and temporal GNNs. |
| <a id="discrete"></a>[Discrete-Time Dynamic Graphs — Full paper list](papers/discrete-time.md) | Graph snapshots and evolving node representations. |
| <a id="DyTAGs"></a>[Dynamic Text-Attributed Graphs — Full paper list](papers/text-attributed.md) | Text, multimodal features, and language models on evolving graphs. |
| <a id="hyper"></a>[Temporal Hypergraphs — Full paper list](papers/temporal-hypergraphs.md) | Higher-order interactions and evolving hyperedges. |

### Tasks and Learning Settings — Full Paper Lists

| Topic | Focus |
| --- | --- |
| <a id="Anomaly"></a>[Anomaly Detection — Full paper list](papers/anomaly-detection.md) | Anomalous nodes, edges, and interaction patterns. |
| <a id="streaming"></a>[Streaming Graph Learning — Full paper list](papers/streaming.md) | Online updates and incremental graph computation. |
| <a id="continual"></a>[Continual Graph Learning — Full paper list](papers/continual-learning.md) | Evolving tasks, distribution shifts, and forgetting. |

Each collection includes available paper and code links, organized by year, with separate survey and benchmark sections where available. Papers may appear in more than one topic.

<a id="tools"></a>

## Resources

- [Datasets & Benchmarks](resources/datasets-and-benchmarks.md) — evaluation suites and dataset entry points.
- [Libraries & Implementations](resources/libraries.md) — temporal graph methods and supporting graph software.

## Contributing

Add a paper, suggest a resource, or report a broken link through a [pull request](https://github.com/LuckyGirl-XU/Awesome-DynamicGraphLearning/pulls) or [issue](https://github.com/LuckyGirl-XU/Awesome-DynamicGraphLearning/issues/new/choose). See the [contribution guidelines](CONTRIBUTING.md).

Maintained by [Yuanyuan Xu](https://luckygirl-xu.github.io/).
