from typing import List
from neo4j import AsyncTransaction

from .._db_init import get_transaction
from ..entity import UserEntity
from ..utils import compile_cyphir_list_formatter


async def create_user(user_entity: UserEntity) -> str:
    merge_body_format = compile_cyphir_list_formatter(':', right='${}', around=('{', '}'))
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        user_entity_dump = user_entity.model_dump()
        result = await tx.run(
            f"""merge (p:{UserEntity.__name__} """
            f"""{merge_body_format(user_entity_dump)}) """ 
            f"""return p.username as username""",
            user_entity_dump
        )
        single_result = await result.single()
        return single_result['username']


async def get_user(username: str) -> UserEntity:
    return_format = compile_cyphir_list_formatter('as', 'p.{}', '{}')
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""match (p:{UserEntity.__name__}) """
            f"""where p.username = $username """
            f"""return {return_format(UserEntity.model_fields)}""",
            username=username
        )
        user_result = dict(await result.single())
        return UserEntity.model_validate(user_result)

async def update_user(username: str, update: dict) -> List[UserEntity]:
    set_format = compile_cyphir_list_formatter('=', 'p.{}', '${}')
    return_format = compile_cyphir_list_formatter('as', 'p.{}', '{}')
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""match (p:{UserEntity.__name__}) """
            f"""where p.username = $username """
            f"""set {set_format(update)} """
            f"""return {return_format(UserEntity.model_fields)}""",
            update, username=username
        )
        return [UserEntity.model_validate(e) for e in await result.data()] 

async def delete_user(username: str) -> None:
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        await tx.run(
            f"""match (p:{UserEntity.__name__}) """
            f"""where p.username = $username """
            f"""delete p """,
            username=username
        )
        