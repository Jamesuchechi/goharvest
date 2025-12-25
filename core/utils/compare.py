from typing import Dict


def compare_results(result1, result2) -> Dict:
    return {
        'result_1': str(result1.id),
        'result_2': str(result2.id),
        'summary': {},
        'diff': '',
    }
