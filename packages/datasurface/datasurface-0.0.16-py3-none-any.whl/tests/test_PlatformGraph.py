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
from datasurface.md.Governance import DataPlatform, DataTransformerNode, Ecosystem, EcosystemPipelineGraph, \
    ExportNode, IngestionNode, PipelineNode, PlatformPipelineGraph, TriggerNode

from tests.nwdb.eco import createEcosystem


class Test_PlatformGraphs(unittest.TestCase):

    def test_PipelineGraph(self):
        eco: Ecosystem = createEcosystem()

        azurePlatform: DataPlatform = eco.getDataPlatformOrThrow("Azure Platform")
        self.assertEqual(eco.getDefaultDataPlatform(), azurePlatform)

        graph: EcosystemPipelineGraph = EcosystemPipelineGraph(eco)

        self.assertIsNotNone(graph.roots.get(azurePlatform))

        pi: PlatformPipelineGraph = graph.roots[azurePlatform]
        self.assertEqual(len(pi.workspaces), 3)

        self.assertEqual(len(pi.dataContainerExports), 1)

        # Left hand side of pipeline graph should just be ingestions
        ingestionRoots: set[PipelineNode] = pi.getLeftSideOfGraph()
        for ir in ingestionRoots:
            self.assertTrue(str(ir).startswith("Ingest"))

        # Right hand side of pipeline graph should be exports to assets
        rightHandLeafs: set[PipelineNode] = pi.getRightSideOfGraph()
        for rh in rightHandLeafs:
            self.assertTrue(str(rh).startswith("Export"))

        # Check every ingest is followed by an export
        self.assertTrue(pi.checkNextStepsForStepType(IngestionNode, ExportNode))
        # Check exports are only followed by a trigger
        self.assertTrue(pi.checkNextStepsForStepType(ExportNode, TriggerNode))
        # Check triggers are only followed by a datatransformer
        self.assertTrue(pi.checkNextStepsForStepType(TriggerNode, DataTransformerNode))
        # Check DataTransformers are followed by ingestion
        self.assertTrue(pi.checkNextStepsForStepType(DataTransformerNode, IngestionNode))

        graphStr: str = pi.graphToText()

        print(graphStr)
