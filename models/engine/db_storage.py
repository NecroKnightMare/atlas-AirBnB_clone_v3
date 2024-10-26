#!/usr/bin/python3
"""
this module handles the mysql database storage backend of
our web service
"""


import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def valid_models():
    from models.user import User
    from models.state import State
    from models.city import City
    from models.place import Place
    from models.amenity import Amenity
    from models.review import Review
    return {
            'User': User,
            'State': State,
            'City': City,
            'Place': Place,
            'Amenity': Amenity,
            'Review': Review
            }

def metadata_create_all(engine):
    '''
    all classes that inherit from Base must be
    imported before calling create_all()
    '''
    from models.base_model import Base
    from models.user import User
    from models.state import State
    from models.city import City
    from models.place import Place
    from models.amenity import Amenity
    from models.review import Review
    Base.metadata.create_all(engine)

class DBStorage:
    # __objects = {}
    __engine = None
    __session = None
    __session_generator = None
    __db_url = None

    def __init__(self):
        env = os.environ.get('HBNB_ENV')
        env_user = os.environ.get('HBNB_MYSOL_USER', 'hbnb_dev')
        env_user_pwd = os.environ.get('HBNB_MYSOL_PWD', 'hbnb_dev_pwd')
        env_host = os.environ.get('HBNB_MYSOL_HOST', 'localhost')
        env_db = os.environ.get('HBNB_MYSOL_DB', 'hbnb_dev_db')

        self.__db_url = "mysql+mysqldb://{}:{}@{}/{}".format(
                env_user, env_user_pwd, env_host, env_db)

        self.__engine = create_engine(self.__db_url, pool_pre_ping=True)
        metadata_create_all(self.__engine)
        self.__session_generator = sessionmaker(
                self.__engine, expire_on_commit=False)
        self.__session_generator = scoped_session(self.__session_generator)
        if env == "test":
            metadata.drop_all(self.__engine)
        self.__session = self.__session_generator()

    def all(self, search_class=None):

        """
        returns a dictionary of objects based on the class given
        """
        # call self.save() first?
        results = {}
        if search_class == None:
            for table in valid_models().values:
                query = self.__session.query(table)
                query = self.construct_dict(query)
                results.update(query)
            return results
        else:
            query = self.__session.query(search_class)
            return construct_dict(query)

    def new(self, obj):
        """
        adds a new object to the dictionary object with
        the key string <class>.<id>
        """
        # this might just be enough, since obj would
        # presumably already be mapped to the database table
        self.__session.add(obj)

    def save(self):
        """
        save all changes onto to the database
        """
        self.__session.commit()

    def reload(self):
        """
        expire session and reload a new one
        """
        try:
            self.__session.close()
        except InvalidRequestError:
            pass
        # create all tables in the database (sqlalchemy)
        # use Session.refresh() ?
        metadata_create_all(self.__engine)
        self.__session = self.__session_generator()

    def delete(self, obj=None):
        """
        remove the given object from __objects if it exist within
        if nothing is given do nothing
        """
        if obj == None:
            return
        else:
            ObjClass = type(obj)
            (self
             .__session
             .query(ObjClass)
             .filter(ObjClass.id == obj.id)
             .delete(synchronize_session=False))

    def construct_key(self, obj):
        """
        helper method to construct key for object dictionary
        """
        return type(obj).__name__ + "." + obj.id

    def construct_dict(self, query_records):
        dictionary = {}
        for entry in query_records:
            key = construct_key(entry)
            dictionary.update({key: entry})
        return dictionary
