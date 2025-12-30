import pytest
from typing import List

class BusinessParser:
    """
    This class is responsible for parsing the business needs from a given string.
    It uses regular expressions to identify the different parts of the string and then
    extracts the information needed to create the data structure.
    """

    def __init__(self):
        self.regex = re.compile(r"\{.*?\}")

    def parse_business_domain(self, business_needs: str) -> List[str]:
        """
        Extracts the business domain from a given string. The domain is considered to be any text between curly brackets {}.

        Args:
            business_needs (str): A string containing the business needs.

        Returns:
            List[str]: A list of strings representing the different business domains found in the input string.
        """
        matches = self.regex.findall(business_needs)
        return [match[1:-1] for match in matches]

    def parse_core_functions(self, business_needs: str) -> List[str]:
        """
        Extracts the core functions from a given string. The core functions are considered to be any text between curly brackets {}.

        Args:
            business_needs (str): A string containing the business needs.

        Returns:
            List[str]: A list of strings representing the different core functions found in the input string.
        """
        matches = self.regex.findall(business_needs)
        return [match[1:-1] for match in matches]

    def parse_data_structures(self, business_needs: str) -> List[str]:
        """
        Extracts the data structures from a given string. The data structures are considered to be any text between curly brackets {}.

        Args:
            business_needs (str): A string containing the business needs.

        Returns:
            List[str]: A list of strings representing the different data structures found in the input string.
        """
        matches = self.regex.findall(business_needs)
        return [match[1:-1] for match in matches]

    def parse_technical_requirements(self, business_needs: str) -> List[str]:
        """
        Extracts the technical requirements from a given string. The technical requirements are considered to be any text between curly brackets {}.

        Args:
            business_needs (str): A string containing the business needs.

        Returns:
            List[str]: A list of strings representing the different technical requirements found in the input string.
        """
        matches = self.regex.findall(business_needs)
        return [match[1:-1] for match in matches]

    def parse_external_dependencies(self, business_needs: str) -> List[str]:
        """
        Extracts the external dependencies from a given string. The external dependencies are considered to be any text between curly brackets {}.

        Args:
            business_needs (str): A string containing the business needs.

        Returns:
            List[str]: A list of strings representing the different external dependencies found in the input string.
        """
        matches = self.regex.findall(business_needs)
        return [match[1:-1] for match in matches]

    def parse_quality_requirements(self, business_needs: str) -> List[str]:
        """
        Extracts the quality requirements from a given string. The quality requirements are considered to be any text between curly brackets {}.

        Args:
            business_needs (str): A string containing the business needs.

        Returns:
            List[str]: A list of strings representing the different quality requirements found in the input string.
        """
        matches = self.regex.findall(business_needs)
        return [match[1:-1] for match in matches]

    def parse_migration_challenges(self, business_needs: str) -> List[str]:
        """
        Extracts the migration challenges from a given string. The migration challenges are considered to be any text between curly brackets {}.

        Args:
            business_needs (str): A string containing the business needs.

        Returns:
            List[str]: A list of strings representing the different migration challenges found in the input string.
        """
        matches = self.regex.findall(business_needs)
        return [match[1:-1] for match in matches]

@pytest.fixture
def business_parser():
    return BusinessParser()

class TestBusinessParser:
    def test_parse_business_domain(self, business_parser):
        # Test with a string containing only the business domain
        input_string = "{Business Domain}"
        expected_output = ["Business Domain"]
        assert business_parser.parse_business_domain(input_string) == expected_output

        # Test with a string containing multiple business domains
        input_string = "{Business Domain} {Another Business Domain}"
        expected_output = ["Business Domain", "Another Business Domain"]
        assert business_parser.parse_business_domain(input_string) == expected_output

    def test_parse_core_functions(self, business_parser):
        # Test with a string containing only the core functions
        input_string = "{Core Functions}"
        expected_output = ["Core Functions"]
        assert business_parser.parse_core_functions(input_string) == expected_output

        # Test with a string containing multiple core functions
        input_string = "{Core Functions} {Another Core Function}"
        expected_output = ["Core Functions", "Another Core Function"]
        assert business_parser.parse_core_functions(input_string) == expected_output

    def test_parse_data_structures(self, business_parser):
        # Test with a string containing only the data structures
        input_string = "{Data Structures}"
        expected_output = ["Data Structures"]
        assert business_parser.parse_data_structures(input_string) == expected_output

        # Test with a string containing multiple data structures
        input_string = "{Data Structures} {Another Data Structure}"
        expected_output = ["Data Structures", "Another Data Structure"]
        assert business_parser.parse_data_structures(input_string) == expected_output

    def test_parse_technical_requirements(self, business_parser):
        # Test with a string containing only the technical requirements
        input_string = "{Technical Requirements}"
        expected_output = ["Technical Requirements"]
        assert business_parser.parse_technical_requirements(input_string) == expected_output

        # Test with a string containing multiple technical requirements
        input_string = "{Technical Requirements} {Another Technical Requirement}"
        expected_output = ["Technical Requirements", "Another Technical Requirement"]
        assert business_parser.parse_technical_requirements(input_string) == expected_output

    def test_parse_external_dependencies(self, business_parser):
        # Test with a string containing only the external dependencies
        input_string = "{External Dependencies}"
        expected_output = ["External Dependencies"]
        assert business_parser.parse_external_dependencies(input_string) == expected_output

        # Test with a string containing multiple external dependencies
        input_string = "{External Dependencies} {Another External Dependency}"
        expected_output = ["External Dependencies", "Another External Dependency"]
        assert business_parser.parse_external_dependencies(input_string) == expected_output

    def test_parse_quality_requirements(self, business_parser):
        # Test with a string containing only the quality requirements
        input_string = "{Quality Requirements}"
        expected_output = ["Quality Requirements"]
        assert business_parser.parse_quality_requirements(input_string) == expected_output

        # Test with a string containing multiple quality requirements
        input_string = "{Quality Requirements} {Another Quality Requirement}"
        expected_output = ["Quality Requirements", "Another Quality Requirement"]
        assert business_parser.parse_quality_requirements(input_string) == expected_output

    def test_parse_migration_challenges(self, business_parser):
        # Test with a string containing only the migration challenges
        input_string = "{Migration Challenges}"
        expected_output = ["Migration Challenges"]
        assert business_parser.parse_migration_challenges(input_string) == expected_output

        # Test with a string containing multiple migration challenges
        input_string = "{Migration Challenges} {Another Migration Challenge}"
        expected_output = ["Migration Challenges", "Another Migration Challenge"]
        assert business_parser.parse_migration_challenges(input_string) == expected_output

# Test with a string containing multiple categories
    def test_parse_multiple_categories(self, business_parser):
        # Test with a string containing multiple categories
        input_string = "{Business Domain} {Core Functions} {Data Structures}"
        expected_output = ["Business Domain", "Core Functions", "Data Structures"]
        assert business_parser.parse_business_domain(input_string) == expected_output

# Test with a string containing only the business domain and core functions
    def test_parse_business_domain_and_core_functions(self, business_parser):
        # Test with a string containing only the business domain and core functions
        input_string = "{Business Domain} {Core Functions}"
        expected_output = ["Business Domain", "Core Functions"]
        assert business_parser.parse_business_domain(input_string) == expected_output

# Test with a string containing only the core functions and data structures
    def test_parse_core_functions_and_data_structures(self, business_parser):
        # Test with a string containing only the core functions and data structures
        input_string = "{Core Functions} {Data Structures}"
        expected_output = ["Core Functions", "Data Structures"]
        assert business_parser.parse_core_functions(input_string) == expected_output

# Test with a string containing only the data structures and technical requirements
    def test_parse_data_structures_and_technical_requirements(self, business_parser):
        # Test with a string containing only the data structures and technical requirements
        input_string = "{Data Structures} {Technical Requirements}"
        expected_output = ["Data Structures", "Technical Requirements"]
        assert business_parser.parse_data_structures(input_string) == expected_output

# Test with a string containing only the technical requirements and external dependencies
    def test_parse_technical_requirements_and_external_dependencies(self, business_parser):
        # Test with a string containing only the technical requirements and external dependencies
        input_string = "{Technical Requirements} {External Dependencies}"
        expected_output = ["Technical Requirements", "External Dependencies"]
        assert business_parser.parse_technical_requirements(input_string) == expected_output

# Test with a string containing only the external dependencies and quality requirements
    def test_parse_external_dependencies_and_quality_requirements(self, business_parser):
        # Test with a string containing only the external dependencies and quality requirements
        input_string = "{External Dependencies} {Quality Requirements}"
        expected_output = ["External Dependencies", "Quality Requirements"]
        assert business_parser.parse_external_dependencies(input_string) == expected_output

# Test with a string containing only the quality requirements and migration challenges
    def test_parse_quality_requirements_and_migration_challenges(self, business_parser):
        # Test with a string containing only the quality requirements and migration challenges
        input_string = "{Quality Requirements} {Migration Challenges}"
        expected_output = ["Quality Requirements", "Migration Challenges"]
        assert business_parser.parse_quality_requirements(input_string) == expected_output

# Test with a string containing only the migration challenges and business domain
    def test_parse_migration_challenges_and_business_domain(self, business_parser):
        # Test with a string containing only the migration challenges and business domain
        input_string = "{Migration Challenges} {Business Domain}"
        expected_output = ["Migration Challenges", "Business Domain"]
        assert business_parser.parse_migration_challenges(input_string) == expected_output