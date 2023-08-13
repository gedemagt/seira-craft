from seira_craft.default import DictCrafter


def test_dict_crafter_overrides():

    crafter = DictCrafter()

    instance = dict(
        start=1,
        end=3,
        val=10
    )

    assert crafter.get_start(instance) == 1
    assert crafter.get_end(instance) == 3

    expected = dict(
        start=6,
        end=7,
        val=12
    )

    assert crafter.copy(instance, 6, 7, val=12) == expected


def test_dict_crafter_insert():

    crafter = DictCrafter()

    sequence = [
        dict(
            start=1,
            end=3,
            val=5,
            change_me="T"
        ),
        dict(
            start=3,
            end=6,
            val=10,
            change_me="T"
        ),
        dict(
            start=6,
            end=10,
            val=15,
            change_me="T"
        )
    ]

    instance = dict(
        start=2,
        end=5,
        val=7,
        change_me="F"
    )

    new_sequence = crafter.insert(instance, sequence, change_me="F")

    assert new_sequence == [
        dict(
            start=1,
            end=2,
            val=5,
            change_me="F"
        ),
        dict(
            start=2,
            end=5,
            val=7,
            change_me="F"
        ),
        dict(
            start=5,
            end=6,
            val=10,
            change_me="F"
        ),
        dict(
            start=6,
            end=10,
            val=15,
            change_me="T"
        )
    ]


def test_dict_crafter_insert_group_by():

    crafter = DictCrafter()

    sequence = [
        dict(
            start=1,
            end=3,
            val=5,
            group=1
        ),
        dict(
            start=3,
            end=6,
            val=5,
            group=1
        ),
        dict(
            start=1,
            end=3,
            val=10,
            group=2
        ),
        dict(
            start=3,
            end=6,
            val=15,
            group=2
        )
    ]

    instance = dict(
        start=2,
        end=5,
        val=7,
        group=2
    )

    new_sequence = crafter.insert(instance, sequence, group_by=lambda x: x["group"])

    assert new_sequence == list(sorted([
        dict(
            start=1,
            end=3,
            val=5,
            group=1
        ),
        dict(
            start=3,
            end=6,
            val=5,
            group=1
        ),
        dict(
            start=1,
            end=2,
            val=10,
            group=2
        ),
        dict(
            start=2,
            end=5,
            val=7,
            group=2
        ),
        dict(
            start=5,
            end=6,
            val=15,
            group=2
        )
    ], key=lambda x: x["start"]))


def test_dict_crafter_translate():

    crafter = DictCrafter()

    instance = dict(
        start=6,
        end=10,
        val=15,
        change_me="T"
    )

    new_instance = crafter.translate(instance, 7)
    assert new_instance == dict(
        start=6 + 7, end=10 + 7, val=15, change_me="T"
    )


def test_dict_crafter_copy():

    crafter = DictCrafter()

    instance = dict(
        start=6,
        end=10,
        val=15,
        change_me="T"
    )

    new_instance = crafter.copy(instance, 7, 11, change_me="F")
    assert new_instance == dict(
        start=7, end=11, val=15, change_me="F"
    )


def test_dict_crafter_overlaps():

    crafter = DictCrafter()

    assert not crafter.overlaps(
        dict(start=1, end=3),
        dict(start=3, end=6)
    )

    assert crafter.overlaps(
        dict(start=1, end=4),
        dict(start=3, end=6)
    )

    assert crafter.overlaps(
        dict(start=4, end=5),
        dict(start=3, end=6)
    )

    assert crafter.overlaps(
        dict(start=3, end=6),
        dict(start=4, end=5)
    )

    assert crafter.overlaps(
        dict(start=3, end=6),
        dict(start=1, end=4)
    )


def test_crafter_repeat():

    crafter = DictCrafter()

    sequence = [
        dict(start=1, end=10),
        dict(start=12, end=30)
    ]

    new_sequence = crafter.repeat(sequence, 2)
    assert new_sequence == [
        dict(start=1, end=10),
        dict(start=12, end=30),
        dict(start=30, end=48),
        dict(start=48, end=66),
    ]


def test_crafter_repeat_all():

    crafter = DictCrafter()

    sequence = [
        dict(start=1, end=10),
        dict(start=12, end=30)
    ]

    new_sequence = crafter.repeat_all(sequence, 2)
    assert new_sequence == [
        dict(start=1, end=10),
        dict(start=12, end=30),

        dict(start=1 + 29, end=10 + 29),
        dict(start=12 + 29, end=30 + 29),

        dict(start=1 + 29*2, end=10 + 29*2),
        dict(start=12 + 29*2, end=30 + 29*2),
    ]