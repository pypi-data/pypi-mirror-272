# nnfasta

Neural Net efficient fasta Dataset for Training.

Should be memory efficient across process boundaries.
So useful as input to torch/tensorflow dataloaders etc.

Presents a list of fasta files as a simple `abc.Sequence`
so you can inquire about `len(dataset)` and retrieve
`Record`s with `dataset[i]`

## Install

Install:

```bash
pip install nnfasta
```

**There are no dependencies.**, you just need a modern (>= 3.9) python.

## Usage

```python
from nnfasta import nnfastas

dataset = nnfastas(['athaliana.fasta','triticum.fasta','zmays.fasta'])

# display the number of sequences
print(len(dataset))

# get a particular record
rec = dataset[20]
print('sequence', rec.id, rec.description, rec.seq)
```

**Warning**: No checks are made for the existence of
the fasta files. Also files of zero length will be rejected
by `mmap`.

A `Record` mimics biopython's `Record` and is simply:

```python
@dataclass
class Record:
    id: str
    """Sequence ID"""
    description: str
    """Line prefixed by '>'"""
    seq: str
    """Sequence stripped of whitespace and uppercased"""

    @property
    def name(self) -> str:
        return self.id
```

## Arguments

You can give `nnfastas` either a filename, a `Path`, the actual
bytes in the file or an open file pointer (opened with `mode="rb"`)
*OR* a list of these things.

## Test and Train Split best practice

Use `LazyFasta`

```python
from nnfasta import nnfastas, LazyFasta
from sklearn.model_selection import train_test_split

dataset = nnfastas(['athaliana.fasta','triticum.fasta','zmays.fasta'])
train_idx, test_idx = train_test_split(range(len(dataset)),test_size=.1,shuffle=True)

# these are still Sequence[Record] objects.

train_data = LazyFasta(datset, train_idx)
test_data = LazyFasta(datset, test_idx)

# *OR* ... this is basically the same
import torch
train_data, test_data = torch.utils.data.random_split(dataset, [.9, .1])

```

Enjoy peps!
