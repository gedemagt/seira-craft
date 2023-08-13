# Siera Craft

**Siera Craft** is a Python package to help craft and manipulate sequences.

## Installation

### Using pip

```bash
pip install siera-craft
```

### Using poetry

```bash
poetry add siera-craft
```

## Usage

### Basic Example

```python
from datetime import datetime

from seira_craft.default import DefaultCrafter
from seira_craft.seira import Sequence
from dataclasses import dataclass


@dataclass
class Segment:
    start: datetime
    end: datetime
    val: str

    def copy(self):
        return Segment(self.start, self.end, self.val)


crafter = DefaultCrafter[Segment]()
seq = Sequence[Segment](crafter)

seq.insert(Segment(
    start=datetime(2023, 1, 1, 1), 
    end=datetime(2023, 1, 1, 2),
    val="First Interval"
))

seq.insert(Segment(
    start=datetime(2023, 1, 1, 1, 30), 
    end=datetime(2023, 1, 1, 2, 30),
    val="Second Interval"
))

print(seq.sequence())
```

## License

MIT License. See [LICENSE](LICENSE) for more details.
