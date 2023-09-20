import asyncio
from datetime import datetime
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncTransaction
from neo4j.exceptions import Neo4jError
from pydantic import BaseModel
from contextlib import asynccontextmanager
from pydantic import field_validator
from neo4j.time import DateTime
    

class DbInitData(BaseModel):
    uri: str
    dbname: str
    username: str
    password: str


_driver: AsyncDriver = None
_dbname: str = None


def init_db(data: DbInitData):
    global _driver, _dbname
    _driver = AsyncGraphDatabase.driver(
        uri=data.uri, auth=(data.username, data.password)
    )
    _dbname = data.dbname


@asynccontextmanager
async def get_transaction() -> AsyncTransaction:
    global _driver, _dbname
    if not _driver:
        raise Exception('driver is not initialized')
    async with _driver.session(database=_dbname) as session:
        tx = await session.begin_transaction()
        try:
            yield tx
            await tx.commit()
        except Neo4jError as e:
            raise e
        finally:
            await tx.close()




# class UserEntity(BaseModel):
#     # guid: uuid4 # primary
#     username: str # unique index
#     email: str # unique index
#     password_hash: str
    
#     fullname: str | None = None
#     born: datetime | None = None
#     photo: str | None = None

#     @field_validator('born', mode='before')
#     def parse_born(dt: DateTime | datetime | None):
#         if not dt:
#             return None
#         if isinstance(dt, datetime):
#             return dt
#         else:
#             return dt.to_native()

# async def main(uri, name, pass_, dbname):
#     init_db(DbInitData(uri=uri, dbname=dbname, username=name, password=pass_))
#     async with get_transaction() as tx:
#         username = await create_user(UserEntity(
#             password_hash='aaa',
#             username='egorvvv',
#             fullname='Egor Vvor',
#             email='email@email.com',
#             born=datetime.utcnow(),
#         ))
#         username = await create_user(UserEntity(
#             password_hash='aaa',
#             username='egorvvv',
#             fullname='Egor Vvor',
#             email='email@email.com',
#             born=datetime.utcnow(),
#         ))
#         username = await create_user(UserEntity(
#             password_hash='aaa',
#             username='egorvvv',
#             fullname='Egor Vvor',
#             email='email@email.com',
#             born=datetime.utcnow(),
#         ))
#         # await update_user('egorvvv', {'email': 'egor32vv@gmail.com', 'born': datetime.utcnow()})
#         # user_entity = await get_user(username)
#         await delete_user('egorvvv')
#         # deleted_user_entity = await get_user('egorvvv')
#         # print(deleted_user_entity)
    
#     # async with next(get_transaction()) as tx:
   

# if __name__ == '__main__':
#     asyncio.run(main('neo4j://109.237.147.212:7687', 'neo4j', '1234qwer', 'neo4j'))
