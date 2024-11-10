import logging
from typing import List

from fastapi import APIRouter
from sqlmodel import col, select

from apps.example.exceptions import PersonAlreadyExist, PersonNotFound
from apps.example.schemas import PersonIn, PersonOut
from extensions.fastapi.api import get, post
from extensions.fastapi.context import DependsOnContext
from models import Person

router = APIRouter(prefix='/v1/examples')
logger = logging.getLogger('example')


@get(router, '/', response_model=List[PersonOut])
async def list_person(context: DependsOnContext):
    people = await context.sa_session.scalars(
        select(Person).order_by(col(Person.created_at).desc())
    )
    return people.all()


@post(router, '/', response_model=PersonOut)
async def create_person(person_in: PersonIn, context: DependsOnContext):
    person = await context.sa_session.get(Person, person_in.first_name)
    if not person:
        person = Person(
            first_name=person_in.first_name, last_name=person_in.last_name
        )
        logger.info('Create new person: ' + str(person))
        context.sa_session.add(person)
        await context.sa_session.commit()
        return person
    else:
        raise PersonAlreadyExist


@get(router, '/{first_name}', response_model=PersonOut)
async def get_person(first_name: str, context: DependsOnContext):
    person = await context.sa_session.get(Person, first_name)
    if not person:
        raise PersonNotFound
    return person


@post(router, '/{first_name}/cache')
async def cache_person(first_name: str, context: DependsOnContext):
    person = await context.sa_session.get(Person, first_name)
    if not person:
        raise PersonNotFound

    person_out = PersonOut.parse_obj(person).json()
    logger.info('Cache person: ' + person_out)
    await context.redis.set(person.first_name, person_out)


@get(router, '/{first_name}/cache', response_model=PersonOut)
async def get_person_from_cache(first_name: str, context: DependsOnContext):
    person = await context.redis.get(first_name)
    if person:
        person = PersonOut.parse_raw(person)
        return person
    else:
        return None
