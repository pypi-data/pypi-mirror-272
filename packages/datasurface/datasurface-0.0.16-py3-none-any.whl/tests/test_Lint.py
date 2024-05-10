"""
Copyright (C) 2024 William Newport

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import unittest
from datasurface.md.GitOps import GitHubRepository

from datasurface.md.Lint import ProblemSeverity, ValidationProblem, ValidationTree


class TestLint(unittest.TestCase):
    def test_RepositoryLint(self):
        r: GitHubRepository = GitHubRepository("billynewport/repo", "FOmain")
        tree: ValidationTree = ValidationTree(r)
        r.lint(tree)
        self.assertFalse(tree.hasErrors())

        r: GitHubRepository = GitHubRepository("billynewport/repo", "FOmain")
        tree: ValidationTree = ValidationTree(r)
        r.lint(tree)
        self.assertFalse(tree.hasErrors())

        # If tree has any problems marked as ERROR then hasErrors return true
        tree = ValidationTree("")
        tree.addProblem("This is a problem")
        self.assertTrue(tree.hasErrors())
        self.assertFalse(tree.hasWarnings())
        tree.printTree()
        self.assertEqual(tree.numErrors, 1)
        self.assertEqual(tree.numWarnings, 0)

        tree = ValidationTree("")
        tree.addProblem("This is a problem", sev=ProblemSeverity.WARNING)
        self.assertFalse(tree.hasErrors())
        self.assertTrue(tree.hasWarnings())
        tree.printTree()
        self.assertEqual(tree.numErrors, 0)
        self.assertEqual(tree.numWarnings, 1)

        # Tree with a non error has issues, tree with an error has errors also
        tree.addProblem("This is a problem", sev=ProblemSeverity.INFO)
        self.assertFalse(tree.hasErrors())
        self.assertTrue(tree.hasWarnings())
        tree.addProblem("This is a problem", sev=ProblemSeverity.ERROR)
        self.assertTrue(tree.hasErrors())

    def test_ValidationProblem(self):
        v: ValidationProblem = ValidationProblem("This is a problem", ProblemSeverity.ERROR)
        self.assertEqual(str(v), "ERROR:This is a problem")

        v = ValidationProblem("This is a problem", ProblemSeverity.WARNING)
        self.assertEqual(str(v), "WARNING:This is a problem")

    def test_printEmptyTree(self):
        tree = ValidationTree("")

        self.assertFalse(tree.hasErrors())
        self.assertFalse(tree.hasWarnings())
