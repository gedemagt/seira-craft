from seira_craft.default import DictCrafter

from seira_craft.seira import Seira

sequence = [
    dict(start=1, end=4, val=10),
    dict(start=4, end=5, val=11),
    dict(start=5, end=9, val=12),
]


crafter = DictCrafter(deep_copy=True)

crafter.check_for_overlaps(sequence)

sequence = Seira(crafter)
r = (
    sequence.insert(dict(start=0, end=1, val=9))
    .insert(dict(start=5, end=7, val=10))
    .repeat_all(3)
    .sequence()
)

r = crafter.insert(dict(start=1, end=27, val=1000), r)

for x in r:
    print(x)
