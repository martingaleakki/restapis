from flask import jsonify
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def getAllPuppies():
    puppies = session.query(Puppy).all()
    return jsonify(Puppies=[i.serialize for i in puppies])

def makeANewPuppy(name,description):
  puppy = Puppy(name = name, description = description)
  session.add(puppy)
  session.commit()
  return jsonify(Puppy=puppy.serialize)

def getPuppy(id):
	return "Getting Puppy with id %s" % id

def updatePuppy(id):
  return "Updating a Puppy with id %s" % id

def deletePuppy(id):
  return "Removing Puppy with id %s" % id



class Puppy(Base):
    __tablename__ = 'puppy'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
       		'id': self.id,
           'name': self.name,
           'description' : self.description
       }