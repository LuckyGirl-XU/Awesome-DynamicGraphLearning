# Datasets & Benchmarks

[Home](../README.md) · [Research Topics](../README.md#research-topics) · [Libraries](libraries.md)

Benchmark entry points for temporal graph learning, dynamic text-attributed graphs, and anomaly detection.

| Benchmark | Scope | Resources |
| --- | --- | --- |
| **TGB — Temporal Graph Benchmark** | Dynamic link and node property prediction; temporal knowledge graphs and heterogeneous graphs. | [Website & leaderboards](https://tgb.complexdatalab.com/) · [Code](https://github.com/shenyangHuang/TGB) · [Paper](https://proceedings.neurips.cc/paper_files/paper/2023/file/066b98e63313162f6562b35962671288-Paper-Datasets_and_Benchmarks.pdf) |
| **TGB-Seq** | Temporal graph evaluation with complex sequential interaction dynamics. | [Paper](https://arxiv.org/abs/2502.02975) · [Code & datasets](https://github.com/TGB-Seq/TGB-Seq) |
| **DTGB** | Dynamic text-attributed graphs. | [Paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/a65d054a407f94c34ecfb598fb540a0d-Paper-Datasets_and_Benchmarks_Track.pdf) · [Code & datasets](https://github.com/zjs123/DTGB) |
| **BAG** | Anomaly detection on dynamic graphs. | [Paper](https://ojs.aaai.org/index.php/AAAI/article/view/38510) · [Code & datasets](https://github.com/frhuaaa/BAG) |

## Evaluation Checklist

- Use the benchmark's chronological split and preprocessing instructions.
- Match the task, prediction horizon, negative sampling, and evaluation metric when comparing methods.
- Report dataset versions, feature sources, random seeds, and whether evaluation is transductive or inductive.

## More Benchmark Papers

- [Continuous-time dynamic graphs](../papers/continuous-time.md#benchmarks)
- [Dynamic text-attributed graphs](../papers/text-attributed.md#benchmarks)
- [Anomaly detection](../papers/anomaly-detection.md#benchmarks)
- [Continual graph learning](../papers/continual-learning.md#benchmarks)
