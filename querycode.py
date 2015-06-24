# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement
import pprint 
def get_or_create_two(session, model, defaults=None, **kwargs):
    try:
        query = session.query(model).filter_by(**kwargs)
 
        instance = query.first()
 
        if instance:
            return instance, False
        else:
            session.begin(nested=True)
            try:
                params = dict((k, v) for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement))
                params.update(defaults)
                instance = model(**params)
 
                session.add(instance)
                session.commit()
 
                return instance, True
            except IntegrityError as e:
                session.rollback()
                instance = query.one()
 
                return instance, False
    except Exception as e:
        raise e


##replaces
## db.session.query(Race.ID).filter_by(RaceDate = racedate_, RaceCourseCode= racecoursecode_, RaceNumber= racenumber_).first().ID
def get_id(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance.ID
    else:
        return None

def get_or_create(session, model, **kwargs):
	instance = session.query(model).filter_by(**kwargs).first()
	if instance:
		return instance
	else:
		try:
			instance = model(**kwargs)
			session.add(instance)
			session.commit()
		except IntegrityError as e:
			session.rollback()
	return instance

