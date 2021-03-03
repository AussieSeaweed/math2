# from unittest import main
#
# from math2.econ import Project, Relationship, combinations, relationship
# from math2.utils import ExtendedTestCase
#
#
# class InstrumentTestCase(ExtendedTestCase):
#     def test_relationships(self) -> None:
#         self.assertEqual(relationship([5000, 7000, 6000, 3000], 1000000), Relationship.INDEPENDENT)
#         self.assertEqual(relationship([5000, 7000, 6000, 3000], 7000), Relationship.MUTUALLY_EXCLUSIVE)
#         self.assertEqual(relationship([5000, 7000, 6000, 3000], 10000), Relationship.RELATED_BUT_NOT_MUTUALLY_EXCLUSIVE)
#
#     def test_combinations(self) -> None:
#         self.assertEqual(len(tuple(combinations([5000, 7000, 6000, 3000], 10000))), 8)
#
#     def test_projects(self) -> None:
#         self.assertAlmostEqual(Project(20000, 4000, 4000, 1000, 10).present_worth(0.05), 9680.783294664216)
#         self.assertAlmostEqual(Project(20000, 4000, 4000, 1000, 10).annual_worth(0.05), 727.9268005526942)
#
#
# if __name__ == '__main__':
#     main()
