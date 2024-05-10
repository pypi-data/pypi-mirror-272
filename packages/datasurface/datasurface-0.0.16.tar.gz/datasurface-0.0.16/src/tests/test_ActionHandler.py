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

import os
import unittest

from datasurface.handler.action import RepositorywithCICD, GitHubCICD
from datasurface.md.Lint import ValidationTree


class Test_ActionHandlerForGitHub(unittest.TestCase):
    def test_ActionIterations(self):
        """This tries to start with a basic Ecosystem which defines 2 GZ and some resources. We then simulate a pull request to
        define the EU GZ and then the USA GZ. Finally we define the EU and USA teams and objects"""

        os.environ["GITHUB_TOKEN"] = "Fake Token"

        testSteps: list[list[str]] = [
            # Initial checkin of a eco.py
            ['src/tests/actionHandlerResources/step0', 'src/tests/actionHandlerResources/step1/base', 'main'],
            # Define EU GZ
            ['src/tests/actionHandlerResources/step1/base', 'src/tests/actionHandlerResources/step2/head_EU', 'EUmain'],
            # Define USA GZ
            ['src/tests/actionHandlerResources/step2/head_EU', 'src/tests/actionHandlerResources/step2/head_USA', 'USAmain'],
            # Define EU teams and objects
            ['src/tests/actionHandlerResources/step2/head_USA', 'src/tests/actionHandlerResources/step3', 'ParisMain'],
            # Define USA teams and objects
            ['src/tests/actionHandlerResources/step3', 'src/tests/actionHandlerResources/step4', 'NYMain']
        ]

        for step in testSteps:
            baseFolder: str = step[0]  # The main branch in to which we are trying to change
            headFolder: str = step[1]  # This branch contains the proposed new version of the model, it must be compatible with the main branch
            os.environ['HEAD_REPOSITORY'] = 'billynewport/test_step1'  # Repository is always the same, we just change branches

            print(f"Trying {baseFolder} -> {headFolder} with bad repo first")
            # first try a repository without permission to make change
            os.environ["HEAD_BRANCH"] = "BAD_BRANCH"
            cicd: RepositorywithCICD = GitHubCICD("GitHub")
            tree: ValidationTree = cicd.verifyPullRequest(baseFolder, headFolder)
            tree.printTree()
            self.assertTrue(tree.getErrors())  # Should have errors

            # Now switch to correct branch authorized to make change
            os.environ["HEAD_BRANCH"] = step[2]
            print(f"Trying {baseFolder} -> {headFolder} with good repo")
            tree: ValidationTree = cicd.verifyPullRequest(baseFolder, headFolder)
            if (tree.hasErrors()):
                tree.printTree()
                self.fail("Tree has errors")
