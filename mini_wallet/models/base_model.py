"""
This file contains commons models
"""
from datetime import datetime
import uuid

import flask_sqlalchemy as fsa
import sqlalchemy as sa
from mini_wallet import db
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime


class utcnow(expression.FunctionElement):
    type = DateTime()


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class BaseModel(db.Model):
    """
    This class is the abstract model that inherited from other model
    """

    __abstract__ = True
   
    id = sa.Column(sa.String(36), primary_key=True, default=str(uuid.uuid4()))
    created_at = sa.Column(
        sa.DateTime(),
        default=datetime.utcnow,
        server_default=utcnow(),
        nullable=False,
    )
    updated_at = sa.Column(
        sa.DateTime(),
        default=datetime.utcnow,
        onupdate=utcnow(),
        nullable=False,
        server_default=utcnow(),
        server_onupdate=utcnow(),
    )
    is_deleted = sa.Column(sa.Boolean(), default=False, server_default="false")
    deleted_at = sa.Column(sa.DateTime(), default=None)

    def save(self) -> "BaseModel":
        """
        This method used to add new record to table or update existing record

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()       
            raise

    def add_flush(self) -> "BaseModel":
        """
        This method similar with save, but use flush method of sqlalchemy instead of
        commit

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()      
            raise

    def delete(self) -> "BaseModel":
        """
        This method used to mark the record to deleted

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            self.is_deleted = True
            self.deleted_at = datetime.utcnow()

            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()     
            raise

    def delete_flush(self) -> "BaseModel":
        """
        This method similar with delete, but use flush method of sqlalchemy instead of
        commit

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            self.is_deleted = True
            self.deleted_at = datetime.utcnow()

            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()
            
            raise

    def bulk_delete(self, objects) -> "BaseModel":
        """
        This method used to mark the record to deleted

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            for data in objects:
                data.is_deleted = True
                data.deleted_at = datetime.utcnow()

                db.session.add(data)

            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            
            raise

    @classmethod
    def base_query(cls) -> fsa.BaseQuery:
        """
        This method used to get base query that remove soft deleted file

        Returns:
            fsa.BaseQuery -- [Base query object]
        """
        return cls.query.filter_by(is_deleted=False)

    def hard_delete(self) -> "BaseModel":
        """This method is used to hard delete a record from database
        Warning: The deleted row will gone forever
        """
        try:
            db.session.delete(self)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            
            raise

    def hard_delete_flush(self) -> "BaseModel":
        """This method is used to hard delete a record from database without session commit
        Warning: The deleted row will gone forever
        """
        try:
            db.session.delete(self)
            db.session.flush()

        except Exception as e:
            db.session.rollback()
            
            raise

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception:
            db.session.rollback()
            raise

    def bulk_save(self, objects) -> "BaseModel":
        """
        This method used to save bulk object

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.bulk_save_objects(objects)
            db.session.commit()
            return objects

        except Exception as e:
            db.session.rollback()
            
            raise

    def bulk_update(self, objects) -> "BaseModel":
        """
        This method used to update bulk object

        Returns:
            [BaseModel] -- [The model object]
        """
        try:
            db.session.bulk_update_mappings(self, objects)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            
            raise
