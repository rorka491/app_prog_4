from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider
from src.di.client import ClientProvider
from src.di.repository import RepositoryProvider
from src.di.service import ServiceProvider
from src.di.sqlalchemy import SQLAlchemyProvider


container = make_async_container(
    SQLAlchemyProvider(),
    ClientProvider(),
    ServiceProvider(),
    RepositoryProvider(),
    FastapiProvider(),
)


