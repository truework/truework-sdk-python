import json


class FixtureLoader:
    def load_fixture(self, relative_path):
        with open("tests/fixtures/{}".format(relative_path)) as f:
            return json.load(f)
