# benchmark.py

from evaluation.evaluate import evaluate

modes = [
    "zero_shot",
    "few_shot",
    "cot",
    "react"
]

for mode in modes:
    print(f"\nRunning {mode}...")
    evaluate(mode=mode, sample_size=50)