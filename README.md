# Awesome Temporal & Dynamic Graph Learning

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated collection of papers, code, datasets, benchmarks, and libraries for **temporal and dynamic graph learning**. Topics include temporal graph neural networks, dynamic link prediction, text-attributed graphs, anomaly detection, and continual learning.

[Getting Started](#getting-started) · [Recent Papers](#recent-papers) · [Research Topics](#research-topics) · [Datasets & Benchmarks](resources/datasets-and-benchmarks.md) · [Libraries](resources/libraries.md) · [Contributing](CONTRIBUTING.md)

## Getting Started

1. **Read a survey.** Start with [Representation Learning for Dynamic Graphs](https://arxiv.org/abs/1905.11485) or [Graph Neural Networks for Temporal Graphs](https://arxiv.org/abs/2302.01018).
2. **Explore implementations.** Start with [TGAT](https://github.com/StatsDLMathsRecomSys/Inductive-representation-learning-on-temporal-graphs), [TGN](https://github.com/twitter-research/tgn), or [GraphMixer](https://github.com/CongWeilin/GraphMixer). [DyGLib](https://github.com/yule-BUAA/DyGLib) brings multiple temporal graph methods into one library.
3. **Choose a benchmark.** Explore [TGB](https://tgb.complexdatalab.com/) for temporal link and node prediction, [TGB-Seq](https://github.com/TGB-Seq/TGB-Seq) for sequential interaction dynamics, and [DTGB](https://github.com/zjs123/DTGB) for dynamic text-attributed graphs.

## Recent Papers

Selected 2026 papers. Browse the [topic collections](#research-topics) for the complete list.

| Paper | Venue | Topic |
| --- | --- | --- |
| [Revisiting Node Affinity Prediction in Temporal Graphs](https://arxiv.org/abs/2510.06940) | ICLR 2026 | [Continuous-time](papers/continuous-time.md#2026) |
| [Temporal Graph Thumbnail: Robust Representation Learning with Global Evolutionary Skeleton](https://iclr.cc/virtual/2026/poster/10008743) | ICLR 2026 | [Discrete-time](papers/discrete-time.md#2026) |
| [Unlocking Multi-Modal Potentials for Dynamic Text-Attributed Graph Representation](https://arxiv.org/abs/2502.19651) | AAAI 2026 | [Text-attributed](papers/text-attributed.md#2026) |
| [BAG: Benchmarking Anomaly Detection on Dynamic Graphs](https://ojs.aaai.org/index.php/AAAI/article/view/38510) | AAAI 2026 | [Anomaly detection](papers/anomaly-detection.md#benchmarks) |
| [Hermes: A Multi-Scale Spatial-Temporal Hypergraph Network for Stock Time Series Forecasting](https://openreview.net/forum?id=nMUDgtUWOF) | NeurIPS 2026 | [Hypergraphs](papers/temporal-hypergraphs.md#2026) |
| [UFO: A Unified Flow-Oriented Framework for Robust Continual Graph Learning](https://openreview.net/forum?id=38kpqzHh0B) | NeurIPS 2026 | [Continual learning](papers/continual-learning.md#2026) |

<a id="Publications"></a>

## Research Topics

### Graph Representations

| Topic | Focus |
| --- | --- |
| <a id="continuous"></a>[Continuous-Time Dynamic Graphs](papers/continuous-time.md) | Timestamped interactions, event-based models, and temporal GNNs. |
| <a id="discrete"></a>[Discrete-Time Dynamic Graphs](papers/discrete-time.md) | Graph snapshots and evolving node representations. |
| <a id="DyTAGs"></a>[Dynamic Text-Attributed Graphs](papers/text-attributed.md) | Text, multimodal features, and language models on evolving graphs. |
| <a id="hyper"></a>[Temporal Hypergraphs](papers/temporal-hypergraphs.md) | Higher-order interactions and evolving hyperedges. |

### Tasks and Learning Settings

| Topic | Focus |
| --- | --- |
| <a id="Anomaly"></a>[Anomaly Detection](papers/anomaly-detection.md) | Anomalous nodes, edges, and interaction patterns. |
| <a id="streaming"></a>[Streaming Graph Learning](papers/streaming.md) | Online updates and incremental graph computation. |
| <a id="continual"></a>[Continual Graph Learning](papers/continual-learning.md) | Evolving tasks, distribution shifts, and forgetting. |

Each collection includes available paper and code links, organized by year, with separate survey and benchmark sections where available. Papers may appear in more than one topic.

<a id="tools"></a>

## Resources

- [Datasets & Benchmarks](resources/datasets-and-benchmarks.md) — evaluation suites and dataset entry points.
- [Libraries & Implementations](resources/libraries.md) — temporal graph methods and supporting graph software.

## Contributing

Add a paper, suggest a resource, or report a broken link through a [pull request](https://github.com/LuckyGirl-XU/Awesome-DynamicGraphLearning/pulls) or [issue](https://github.com/LuckyGirl-XU/Awesome-DynamicGraphLearning/issues/new/choose). See the [contribution guidelines](CONTRIBUTING.md).
