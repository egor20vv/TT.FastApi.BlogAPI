from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from neo4j import AsyncTransaction

from ..._db_init import get_transaction
from ...utils import compile_cyphir_list_formatter

from ...entity._post_entity import PostEntity
from ...entity._user_entity import UserEntity

async def create_post(by: str, data: PostEntity) -> PostEntity:
    body_format = compile_cyphir_list_formatter(center=':', right='${}', around=('{', '}'))
    return_format = compile_cyphir_list_formatter(center='as', left='ps.{}', right='{}')
    dumped_data = data.model_dump()
    # dumped_data.update(id=uuid4())
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx 
        result = await tx.run(f"""
            match (p:{UserEntity.__name__}) where p.username = $username
            merge (p)-[c:CREATED]->(ps:{PostEntity.__name__} {body_format(dumped_data)})
            on create set c.at = $at, c.id = $post_id
            return {return_format(dumped_data)}
            """,
            dumped_data, username=by, at=datetime.utcnow(), post_id=str(uuid4())
        )
        single = await result.single()
        summary = await result.consume()
        if not summary.counters.contains_updates:
            raise ValueError(f'User "{by}" not found')
        return PostEntity.model_validate(single)


async def get_user_posts_by_date_ordered(
    by: str, 
    skip: int = 0,
    limit: int | None = None,
    desc: bool = False
) -> List[Tuple[datetime, PostEntity]]:
    queried_order_dict = {
        False: 'order by at',
        True: 'order by at desc'
    }
    query_order = queried_order_dict[desc]
    position = f'skip {skip} ' + (f'limit {limit}' if limit else '')
    
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match (p:{UserEntity.__name__})-[c:CREATED]->(ps:{PostEntity.__name__})
            where p.username = $username 
            return c.at as at, ps
            {query_order}
            {position}
            """,
            username=by
        )
        return [(d['at'].to_native(), PostEntity.model_validate(d['ps'])) for d in await result.data()]
        
async def get_user_posts_by_rate_ordered(
    by: str,
    skip: int = 0,
    limit: int | None = None,
    desc: bool = False
) -> List[Tuple[int, PostEntity]]:
    queried_order_dict = {
        True: 'order by c desc',
        False: 'order by c'
    }
    query_order = queried_order_dict[desc]
    position = f'skip {skip} ' + (f'limit {limit}' if limit else '')
    
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match (p:{UserEntity.__name__})-[:CREATED]->(ps:{PostEntity.__name__})
            optional match (p)<-[l:LIKED]-(:{UserEntity.__name__})
            where p.username = $username 
            return count(l) as c, ps
            {query_order}
            {position}
            """,
            username=by
        )
        return [(d['c'], PostEntity.model_validate(d['ps'])) for d in await result.data()]
