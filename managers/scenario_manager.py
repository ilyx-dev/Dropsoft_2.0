from utils.helpers import read_json_file


class ScenarioManager:
    def __init__(self, scenario_path: str):
        self._scenarios = read_json_file(scenario_path)

    def get_scenario(self, scenario_name: str) -> dict:
        matched_scenarios = [s for s in self._scenarios if s['name'] == scenario_name]

        if len(matched_scenarios) == 0:
            raise ValueError(f"Scenario '{scenario_name}' not found.")
        elif len(matched_scenarios) > 1:
            raise ValueError(f"Multiple scenarios found with the name '{scenario_name}'.")

        return matched_scenarios[0]