from paralympics.models import Event, Region
from paralympics import db, ma


class RegionSchema(ma.SQLAlchemySchema):
    """Marshmallow schema defining the attributes for creating a new region."""

    class Meta:
        model = Region
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    NOC = ma.auto_field()
    region = ma.auto_field()
    notes = ma.auto_field()


class EventSchema(ma.SQLAlchemyAutoSchema):
    """Marshmallow schema for the attributes of an event class. Inherits all
     the attributes from the Event class."""

    class Meta:
        model = Event
        include_fk = True
        load_instance = True
        sqla_session = db.session
        include_relationships = True
