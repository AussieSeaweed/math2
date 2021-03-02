from unittest import main

from auxiliary.tests import ExtendedTestCase

from math2.economics import Project, Relationship, combinations, pa, relationship


class InterestTestCase(ExtendedTestCase):
    def test_relationships(self):
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 1000000), Relationship.INDEPENDENT)
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 7000), Relationship.MUTUALLY_EXCLUSIVE)
        self.assertEqual(relationship([5000, 7000, 6000, 3000], 10000), Relationship.RELATED_BUT_NOT_MUTUALLY_EXCLUSIVE)

    def test_combinations(self):
        self.assertEqual(len(tuple(combinations([5000, 7000, 6000, 3000], 10000))), 8)

    def test_projects(self):
        self.assertAlmostEqual(Project(20000, 4000, 4000, 1000, 10).present_worth(0.05), 9680.783294664216)
        self.assertAlmostEqual(Project(20000, 4000, 4000, 1000, 10).annual_worth(0.05), 727.9268005526942)
        # self.assertAlmostEqual(Project(20000, 4000, 4000, 1000, 10).annual_worth(0.05) * pa(0.05, 10),
        #                        Project(20000, 4000, 4000, 1000, 10).present_worth(0.05))


if __name__ == '__main__':
    main()
