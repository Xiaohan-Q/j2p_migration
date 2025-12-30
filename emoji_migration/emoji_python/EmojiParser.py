import re
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