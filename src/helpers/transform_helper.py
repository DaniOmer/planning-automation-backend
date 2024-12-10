from sqlalchemy.orm import class_mapper

class TransformHelper:
    @staticmethod
    def map_to_dict(obj):
        return {c.key: getattr(obj, c.key) for c in class_mapper(obj.__class__).columns}