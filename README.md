# Siera Craft

**Siera Craft** is a Python package designed for managing and manipulating sequences with items that span intervals.

## Features

- Handle sequences of items that span specific intervals.
- Detect and manage overlaps within sequences.
- Flexibly insert and manipulate sequence items.
- Default and customizable handlers (`Crafters`) for different sequence types.

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
from seira_craft.siera import Siera
from seira_craft.default import DefaultCrafter

# Initialize a DefaultCrafter
crafter = DefaultCrafter()

# Sample sequence of items (modify as per your data structure)
sequence = [...]

# Initialize Siera with the crafter and sequence
s = Siera(crafter, sequence=sequence)

# Manipulate sequence using Siera methods
...
```

For detailed documentation and advanced usage, please refer to the respective module documentation.

## Contribute

Contributions are welcome! Feel free to open issues for feature requests, bug reports, or submit pull requests.

## License

MIT License. See [LICENSE](LICENSE) for more details.
