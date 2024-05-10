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

from datasurface.md import Team, GovernanceZoneDeclaration, GovernanceZone, InfrastructureVendor, InfrastructureLocation, TeamDeclaration
from datasurface.md import Ecosystem
from datasurface.platforms.aws.AmazonAWS import AmazonAWSDataPlatform
from datasurface.platforms.azure.Azure import AzureDataplatform, AzureKeyVaultCredential
from datasurface.md.Documentation import PlainTextDocumentation
from datasurface.md.GitOps import GitHubRepository
from datasurface.md.Governance import CloudVendor, DataPlatformCICDExecutor, DefaultDataPlatform, InfraStructureLocationPolicy
from datasurface.md.Lint import ValidationTree
from tests.nwdb.nwdb import defineTables as defineNWTeamTables
from tests.nwdb.nwdb import defineWorkspaces as defineNWTeamWorkspaces


def createEcosystem() -> Ecosystem:
    ecosys: Ecosystem = Ecosystem(
        "Test",
        GitHubRepository("billynewport/repo", "ECOmain"),

        # Data Platforms
        DefaultDataPlatform(
            AzureDataplatform(
                "Azure Platform",
                PlainTextDocumentation("Test"),
                DataPlatformCICDExecutor(GitHubRepository("owner/repo", "branch")),
                AzureKeyVaultCredential("vault", "maincred"))),
        AmazonAWSDataPlatform("AWS Platform", PlainTextDocumentation("Test"), DataPlatformCICDExecutor(GitHubRepository("owner/repo", "branch"))),

        # GovernanceZones
        GovernanceZoneDeclaration("USA", GitHubRepository("billynewport/repo", "USAmain")),
        GovernanceZoneDeclaration("EU", GitHubRepository("billynewport/repo", "EUmain")),
        GovernanceZoneDeclaration("UK", GitHubRepository("billynewport/repo", "UKmain")),

        # Infra Vendors and locations
        InfrastructureVendor(
            "AWS",
            CloudVendor.AWS,
            PlainTextDocumentation("Amazon AWS"),
            InfrastructureLocation(
                "USA",
                InfrastructureLocation("us-east-1"),  # Virginia
                InfrastructureLocation("us-west-1")),
            InfrastructureLocation(
                "UK",
                InfrastructureLocation("eu-west-1"),  # Ireland
                InfrastructureLocation("eu-west-2")),  # London
            InfrastructureLocation(
                "EU",
                InfrastructureLocation("eu-central-1"),  # Frankfurt
                InfrastructureLocation("eu-west-3"))),
        InfrastructureVendor(
            "MyCorp",
            PlainTextDocumentation("Private USA company data centers"),
            InfrastructureLocation(
                "USA",
                InfrastructureLocation("NJ_1"),
                InfrastructureLocation("NY_1")),
            InfrastructureLocation(
                "UK",
                InfrastructureLocation("London"),
                InfrastructureLocation("Cambridge"))),
        InfrastructureVendor(
            "Azure",
            CloudVendor.AZURE,
            PlainTextDocumentation("Microsoft Azure"),
            InfrastructureLocation(
                "USA",
                InfrastructureLocation("Central US"),  # Iowa
                InfrastructureLocation("East US"),  # Virginia
                InfrastructureLocation("East US 2"),  # Virginia
                InfrastructureLocation("East US 3"),  # Georgia
                InfrastructureLocation("North Central US"),  # Illinois
                InfrastructureLocation("South Central US"),  # Texas
                InfrastructureLocation("West Central US"),  # Wyoming
                InfrastructureLocation("West US"),  # California
                InfrastructureLocation("West US 2"),  # Washington
                InfrastructureLocation("West US 3"))  # Arizona
            )
        )

    gzUSA: GovernanceZone = ecosys.getZoneOrThrow("USA")

    gzUSA.add(
            TeamDeclaration("FrontOffice", GitHubRepository("billynewport/repo", "FOmain")),
            TeamDeclaration("MiddleOffice", GitHubRepository("billynewport/repo", "MOmain")),
            TeamDeclaration("NorthWindTeam", GitHubRepository("billynewport/repo", "NWmain")),
            TeamDeclaration("BackOffice", GitHubRepository("billynewport/repo", "BOmain")),
            InfraStructureLocationPolicy("Azure USA Only", PlainTextDocumentation("Test"), ecosys.getAllChildLocations("Azure", ["USA"]), None)
        )

    gzEU: GovernanceZone = ecosys.getZoneOrThrow("EU")
    gzEU.add(
            TeamDeclaration("FrontOffice", GitHubRepository("billynewport/repo", "FOmain")),
            TeamDeclaration("MiddleOffice", GitHubRepository("billynewport/repo", "MOmain")),
            TeamDeclaration("BackOffice", GitHubRepository("billynewport/repo", "BOmain"))
            )

    gzUK: GovernanceZone = ecosys.getZoneOrThrow("UK")
    gzUK.add(
        TeamDeclaration("FrontOffice", GitHubRepository("billynewport/repo", "FOmain")),
        TeamDeclaration("MiddleOffice", GitHubRepository("billynewport/repo", "MOmain")),
        TeamDeclaration("BackOffice", GitHubRepository("billynewport/repo", "BOmain"))
    )

    # Fill out the NorthWindTeam managed by the USA governance zone
    nw_team: Team = ecosys.getTeamOrThrow("USA", "NorthWindTeam")
    defineNWTeamTables(ecosys, gzUSA, nw_team)
    defineNWTeamWorkspaces(ecosys, nw_team, ecosys.getLocationOrThrow("Azure", ["USA", "Central US"]))

    tree: ValidationTree = ecosys.lintAndHydrateCaches()
    if (tree.hasErrors()):
        tree.printTree()
        raise Exception("Ecosystem validation failed")
    return ecosys


def test_Validate():
    ecosys: Ecosystem = createEcosystem()
    vTree: ValidationTree = ecosys.lintAndHydrateCaches()
    if (vTree.getErrors()):
        print(vTree)
        raise Exception("Ecosystem validation failed")
    else:
        print("Ecosystem validated OK")


if __name__ == "__main__":
    test_Validate()
