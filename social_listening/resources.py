from dagster import ConfigurableResource


class Keyword(ConfigurableResource):
    value: str

    def get_value(self) -> str:
        return self.value
