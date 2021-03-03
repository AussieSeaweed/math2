from unittest import main

from auxiliary import ExtendedTestCase

from math2.econ import EffectiveInterest, Project, Relationship, combinations, relationship


class InstrumentTestCase(ExtendedTestCase):
    def test_relationships(self) -> None:
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 1000000), Relationship.INDEPENDENT)
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 7000), Relationship.MUTUALLY_EXCLUSIVE)
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 10000), Relationship.RELATED)

    def test_combinations(self) -> None:
        self.assertLen(tuple(combinations([5000, 7000, 6000, 3000], 10000)), 8)

    def test_projects(self) -> None:
        self.assertAlmostEqual(Project(-20000, 4000 - 1000, 4000, 10).present_worth(EffectiveInterest(0.05)),
                               9680.783294664216)
        self.assertAlmostEqual(Project(-20000, 4000 - 1000, 4000, 10).annual_worth(EffectiveInterest(0.05)),
                               727.9268005526942)


if __name__ == '__main__':
    main()
