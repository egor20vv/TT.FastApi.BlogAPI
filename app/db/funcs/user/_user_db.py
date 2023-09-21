from typing import List
from neo4j import AsyncTransaction

from ..._db_init import get_transaction
from ...entity import UserEntity
from ...utils import compile_cyphir_list_formatter


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


async def get_user_by_username(username: str) -> UserEntity | None:
    return_format = compile_cyphir_list_formatter('as', 'p.{}', '{}')
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""match (p:{UserEntity.__name__}) """
            f"""where p.username = $username """
            f"""return {return_format(UserEntity.model_fields)}""",
            username=username
        )
        single = await result.single()
        if not single:
            return None
        else:
            user_result = dict(single)
            return UserEntity.model_validate(user_result)

async def get_user_by_email(email: str) -> UserEntity:
    return_format = compile_cyphir_list_formatter('as', 'p.{}', '{}')
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""match (p:{UserEntity.__name__}) """
            f"""where p.email = $email """
            f"""return {return_format(UserEntity.model_fields)} """,
            email=email
        )
        user_result = dict(await result.single())
        return UserEntity.model_validate(user_result)
    
async def is_user(*, username: str | None = None, email: str | None = None) -> bool:
    if username is None and email is None:
        raise ValueError('username and email can not be null both')
    
    condition = ''
    query_args = {}
    if username:
        condition += 'p.username = $username'
        query_args['username'] = username
    if email:
        if username:
            condition += ' or '
        condition += 'p.email = $email'
        query_args['email'] = email
        
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""match (p:{UserEntity.__name__}) """
            f"""where {condition} """
            f"""return count(p) as c""",
            query_args
        )
        user_result = await result.single()
        return user_result['c'] != 0


async def update_user(username: str, update: dict) -> UserEntity:
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
        single = await result.single()
        if not single:
            raise ValueError(f'username ({username}) is not found', username)
        return UserEntity.model_validate(single)

async def delete_user(username: str) -> None:
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        await tx.run(
            f"""match (p:{UserEntity.__name__}) """
            f"""where p.username = $username """
            f"""delete p """,
            username=username
        )
        