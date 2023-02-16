# pseudoPy

This repository contains the files and instructions for replicating the experiments described in [[1]](#1).

The software requirements can be installed with 
    
    pip install -r requirements.txt

The file [`parse_json.py`](./parse_json.py) simply preprocesses the [CodeSearchNet](https://github.com/microsoft/CodeXGLUE/tree/main/Code-Text/code-to-text) dataset by fetching all the Python files and the corresponding target summaries, and saves them in two files (`[train|test|valid]_py_fun` and `[train|test|valid]_py_en`), in which the summary in the i-th row in the summary file is referred to the function at the i-th row in teh code file.

The file [`pseudonl.py`](./pseudonl.py) processes the files produced by [`parse_json.py`](./parse_json.py) and translates all the contained Python functions in pseudoPy.

The file [`scores.py`](./scores.py) is used to preprocess the summary files and compute the BLEU and USE+cos scores.
To properly run it, it is required to clone a repository [[2]](#2): 

    git clone https://github.com/similarityMetrics/similarityMetrics.git

# References

<a id="1">[1]</a> C. Ferretti and M. Saletta. "*Naturalness in Source Code Summarization. How Significant is it?*". Submitted to 31st International Conference on Program Comprehension (ICPC). 2023.

<a id="2">[2]</a>S. Haque et al. "*Semantic similarity metrics for evaluating source code summarization*". In: Proceedings of the 30th IEEE/ACM International Conference on Program Comprehension (ICPC). ACM, 2022, pp. 36–47.

# Citation

If you find this repository useful for your work, please include the following citation:

```
@inproceedings{preudoPy,
  author    = {Claudio Ferretti and Martina Saletta},
  title     = {Naturalness in Source Code Summarization. How Significant is it?},
  booktitle = {31st International Conference on Program Comprehension (ICPC) [submitted]},
  pages     = {},
  publisher = {{IEEE}},
  year      = {2022},
}
```
