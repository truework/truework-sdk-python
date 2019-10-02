from attr import attrs, attrib


@attrs(frozen=True)
class Earnings(object):
    year = attrib()
    base = attrib()
    overtime = attrib()
    commission = attrib()
    bonus = attrib()
    total = attrib()

    @staticmethod
    def convert_to_truework_object(json_object):
        return Earnings(
            year=json_object.get("year"),
            base=json_object.get("base"),
            overtime=json_object.get("overtime"),
            commission=json_object.get("commission"),
            bonus=json_object.get("bonus"),
            total=json_object.get("total"),
        )
