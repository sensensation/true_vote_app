# @pytest.fixture(scope="session")
# async def container(db_settings: DatabaseSettings) -> AsyncIterator[Container]:
#     async with lifespan(app):
#         app.state.container.db.override(providers.Singleton(AlchemyDatabase, settings=db_settings))
#         app.state.container.wire(packages=[events.tasks, cli])
#         yield app.state.container
