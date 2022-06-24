from core.configs import settings
from core.database import engine

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


async def create_tables() -> None:
    print('Creating tables on database')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('Tables created successfully.')


if __name__ == '__main__':
    import asyncio

    asyncio.get_event_loop().run_until_complete(create_tables())
