from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy import distinct, func

from db.base_class import Base
from db.session import DB

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.DB = DB

    def get(self, model_id: Any) -> Optional[ModelType]:
        with self.DB() as db:
            return db.query(self.model).filter(self.model.id == model_id).first()

    def get_multi(self, offset: int = 0, limit: int = 100) -> List[ModelType]:
        with self.DB() as db:
            return db.query(self.model).offset(offset).limit(limit).all()

    def get_many(self, query_data):
        query = self.query_time_range(query_data)
        total = query.with_entities(func.count(self.model.id)).scalar()
        data = query.offset(query_data['offset']).limit(query_data['limit']).all()
        return {'rows': data, 'total': total}

    def get_one_by_field(self, field_name, field_value, order_desc=True):
        with self.DB() as db:
            if order_desc:
                return db.query(self.model).filter(getattr(self.model, field_name) == field_value).order_by(
                    self.model.id.desc()).first()
            else:
                return db.query(self.model).filter(getattr(self.model, field_name) == field_value).first()

    def create(self, obj_in: dict) -> ModelType:
        with self.DB() as db:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            # self.DB.refresh()
            return db_obj

    # optimization: "self.DB.execute(self.model.__table__.insert(), obj_in)"
    def create_many(self, obj_in):
        with self.DB() as db:
            objs = [self.model(**_) for _ in obj_in]
            db.bulk_save_objects(objs)
            db.commit()
            # self.DB.refresh()
            return objs

    # def create_or_update_many(self, obj_in):
    #     with self.DB() as db:
    #         db.begin_nested()
    #         objs = [self.model(**_) for _ in obj_in]
    #         # session = Session()
    #         # for obj in data_list:
    #         #     session.merge(MyModel(**obj))
    #         # session.commit()
    #         # db.bulk_update_mappings(self.model, obj_in,
    #         #                         where=self.model.device_serial_no.in_(d['device_serial_no'] for d in obj_in))
    #         for obj_data in obj_in:
    #             db.merge(self.model(**obj_data))
    #         db.commit()
    #         # self.DB.refresh()
    #         return objs

    def update(
            self,
            db_obj: ModelType,
            obj_in: dict
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = dict(obj_in)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        with self.DB() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

    def update_by_field(self, field_name: str, field_value: str, update_data: dict):
        with self.DB() as db:
            db.query(self.model).filter(getattr(self.model, field_name) == field_value).update(update_data)
            db.commit()
            # db.refresh()

    def remove(self, obj: ModelType):
        with self.DB() as db:
            db.delete(obj)
            db.commit()
            return obj

    def remove_by_id(self, obj_id: int):
        with self.DB() as db:
            obj = db.query(self.model).get(obj_id)
            db.delete(obj)
            db.commit()
            return obj

    def get_field_values(self, field: str):
        with self.DB() as db:
            field_values = db.query(distinct(getattr(self.model, field))).all()
            return [_[0] for _ in field_values if _[0]]

    def query_time_range(self, query_data, query=None, order_desc=False):
        with self.DB() as db:
            if not query:
                query = db.query(self.model)
            if query_data.get('start_time'):
                query = query.filter(self.model.created_at >= query_data.get('start_time'))
            if query_data.get('end_time'):
                query = query.filter(self.model.created_at <= query_data.get('end_time'))
            if order_desc:
                query = query.order_by(self.model.id.desc())
            return query
