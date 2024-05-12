

![image](images/logo.png)

Qflow is a Python library tailored for asynchronous orchestration of machine learning pipelines. It allows users to define their pipelines declaratively, with the flexibility for processing at each stage to run either remotely or locally. The library supports a wide range of operations, which can be customized with user-defined Python functions.

## Instalation

<details open>
<summary>Install</summary>

clone repo and install [requirements.txt](https://github.com/dotmoovs/quokka/requirements.txt) in a
[**Python>=3.7.0**](https://www.python.org/) environment.

```bash
pip install -r requirements.txt
```

</details>

<details open>
<summary>Example</summary>

Simple wordcount example with no remote stages. We can define a qflow pipeline as follows:



```python
from qflow import (
    QWorkflow,
    QFileSource,
    QFlatMap,
    QNativeMap,
    QAggregate
)
from qflow.functools import fst, snd, head


class WordCount(QWorkflow):

    def forward(self, input_text):
        
        results = (
            QFileSource(input_text) 
            | QFlatMap(
                lambda line: line.split()
                ) 
            | QNativeMap(
                lambda word: (word, 1)
                ) 
            | QAggregate(
                key_factory = fst
                )
            | QNativeMap(
                lambda words: ( fst(head(words)), sum(map(snd, words)) )
                )
        )

        return results
```

To use this pipeline we can run it as follows:

```python
# create the processing pipeline.
workflow = WordCount()

# run the pipeline with the file "input.txt" as input.
results = workflow("input.txt")

print(results)


```

</details>