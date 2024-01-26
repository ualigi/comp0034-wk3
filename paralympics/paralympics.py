from flask import current_app as app
from flask import Flask
from paralympics.schemas import RegionSchema, EventSchema
from paralympics import db
from paralympics.models import Region, Event
from flask import make_response


@app.route('/')
def hello():
    return f"Hello!"


# Flask-Marshmallow Schemas
regions_schema = RegionSchema(many=True)
region_schema = RegionSchema()
events_schema = EventSchema(many=True)
event_schema = EventSchema()


@app.get("/regions")
def get_regions():
    """Returns a list of NOC region codes and their details in JSON."""
    # Select all the regions using Flask-SQLAlchemy
    all_regions = db.session.execute(db.select(Region)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = regions_schema.dump(all_regions)
    # Return the data
    return result


@app.get("/events")
def get_events():
    """Returns a list of events and their details in JSON."""
    # Select all events using Flask-SQLAlchemy
    all_events = db.session.execute(db.select(Event)).scalars()
    # Get the data using Marshmallow schema (returns JSON)
    result = events_schema.dump(all_events)
    # Return the data
    return result


@app.get("/events/<event_id>")
def get_event(event_id):
    """ Returns the event with the given id JSON.

    :param event_id: The id of the event to return
    :param type event_id: int
    :returns: JSON
    """
    event = db.session.execute(
        db.select(Event).filter_by(id=event_id)
        ).scalar_one_or_none()
    return event_schema.dump(event)


@app.get("/regions/<NOC>")
def get_region(NOC):
    """ Returns the event with the given NOC JSON.

    :param NOC: The NOC of the region to return
    :param type event_id: str
    :returns: JSON
    """
    region = db.session.execute(
        db.select(Region).filter_by(NOC=NOC)
        ).scalar_one()
    return region_schema.dump(region)

@app.post("/events")
def add_events():
    from Flask import request
    """ Adds a new event.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
    event_schema.load()

    :returns: JSON"""
    ev_json = request.get_json()
    event = event_schema.load(ev_json)
    db.session.add(event)
    db.session.commit()
    return {"message": f"Event added with id= {event.id}"}


@app.post('/regions')
def add_regions():
    from Flask import request
    """ Adds a new region.

    Gets the JSON data from the request body and uses this to deserialise JSON to an object using Marshmallow
    event_schema.load()

    :returns: JSON"""
    reg_json = request.get_json()
    region = region_schema.load(reg_json)
    db.session.add(region)
    db.session.commit()
    return {"message": f"Region added with NOC= {region.NOC}"}


@app.delete('/events/<int:event_id>')
def delete_event(event_id):
    """ Deletes an event.

    Gets the event from the database and deletes it.

    :returns: JSON"""
    event = db.session.execute(
        db.select(Event).filter_by(event_id=event_id)
    ).scalar_one_or_none()
    db.session.delete(event)
    db.session.commit()
    return {"message": f"Event deleted with id= {event_id}"}


@app.delete("/regions/<NOC>")
def delete_region(NOC):
    """Deletes a region.

    Gets the region from the database and deletes it.

    :returnsl JSON"""
    region = db.session.execute(
        db.select(Region).filter_by(NOC=NOC)
    ).scalar_one()
    db.session.delete(region)
    db.session.commit()
    return {"message": f"Region deleted with NOC= {NOC}"}


@app.patch("/events/<event_id>")
def event_update(event_id):
    from Flask import request
    """Updates changed fields for the event.

    """
    # Find the event in the database
    existing_event = db.session.execute(
        db.select(Event).filter_by(event_id=event_id)
    ).scalar_one_or_none()
    # Get the updated details from the json sent in the HTTP patch request
    event_json = request.get_json()
    # Use Marshmallow to update the existing records with the changes from the json
    event_updated = event_schema.load(event_json, instance=existing_event, partial=True)
    # Commit the changes to the database
    db.session.add(event_updated)
    db.session.commit()
    # Return json showing the updated record
    updated_event = db.session.execute(
        db.select(Event).filter_by(event_id=event_id)
    ).scalar_one_or_none()
    result = event_schema.jsonify(updated_event)
    response = make_response(result, 200)
    response.headers["Content-Type"] = "application/json"
    return response