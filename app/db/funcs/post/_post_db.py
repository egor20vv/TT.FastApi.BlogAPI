from datetime import datetime
from typing import List, Literal, Tuple
from uuid import uuid4
from neo4j import AsyncTransaction

from ..._db_init import get_transaction
from ...utils import compile_cyphir_list_formatter

from ...entity._post_entity import PostEntity
from ...entity._user_entity import UserEntity


async def create_post(by: str, data: PostEntity) -> Tuple [str, PostEntity]:
    body_format = compile_cyphir_list_formatter(center=':', right='${}', around=('{', '}'))
    # return_format = compile_cyphir_list_formatter(center='as', left='ps.{}', right='{}')
    dumped_entity_data = data.model_dump()
    # dumped_entity_data.update(at=datetime.utcnow(), id=str(uuid4()))
    dumped_relateion_data = {'at': datetime.utcnow(), 'id': str(uuid4())}
    # dumped_full_data = {**dumped_entity_data, **dumped_relateion_data}
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx 
        result = await tx.run(f"""
            match (p:{UserEntity.__name__}) where p.username = $username
            create (p)-[c:CREATED {body_format(dumped_relateion_data)}]->(ps:{PostEntity.__name__} {body_format(dumped_entity_data)})
            return c.id as post_id, ps
            """,
            **dumped_entity_data, **dumped_relateion_data, username=by
        )
        single = await result.single()
        summary = await result.consume()
        if not summary.counters.contains_updates:
            raise ValueError('No actions occured')
        return single['post_id'], PostEntity.model_validate(single['ps'])

async def get_user_posts_by_date_ordered(
    by: str, 
    skip: int = 0,
    limit: int | None = None,
    desc: bool = False
) -> List[Tuple[datetime, str, str, PostEntity]]:
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
            return c.at as at, c.id as post_id, p.username as creator, ps
            {query_order}
            {position}
            """,
            username=by
        )
        return [(d['at'].to_native(), d['post_id'], d['creator'], PostEntity.model_validate(d['ps'])) 
                for d in await result.data()]
        
async def get_user_posts_by_rate_ordered(
    by: str,
    skip: int = 0,
    limit: int | None = None,
    desc: bool = False
) -> List[Tuple[int, str, str, PostEntity]]:
    queried_order_dict = {
        True: 'order by cl desc',
        False: 'order by cl'
    }
    query_order = queried_order_dict[desc]
    position = f'skip {skip} ' + (f'limit {limit}' if limit else '')
    
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match (p:{UserEntity.__name__})-[c:CREATED]->(ps:{PostEntity.__name__})
            optional match (p)<-[l:LIKED]-(:{UserEntity.__name__})
            where p.username = $username 
            return count(l) as cl, c.id as post_id, p.username as creator, ps
            {query_order}
            {position}
            """,
            username=by
        )
        return [(d['c'], d['post_id'], d['creator'], PostEntity.model_validate(d['ps'])) 
                for d in await result.data()]

async def get_followed_posts_by_date_ordered(
    by: str, 
    skip: int = 0, 
    limit: int | None = None, 
    desc: bool = False
) -> Tuple[datetime, str, str, PostEntity]:
    queried_order_dict = {
        True: 'order by at desc',
        False: 'order by at'
    }
    query_order = queried_order_dict[desc]
    position = f'skip {skip} ' + (f'limit {limit}' if limit else '')
    
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match (by:{UserEntity.__name__})-[:SUBBED]->(to:{UserEntity.__name__})-[c:CREATED]->(ps:{PostEntity.__name__})
            where by.username = $username 
            return c.at as at, c.id as post_id, to.username as creator, ps
            {query_order}
            {position}
            """,
            username=by
        )
        # data = await result   
        return [(d['at'], d['post_id'], d['creator'], PostEntity.model_validate(d['ps'])) 
                for d in await result.data()]
    
async def like_post(by: str, post_id: str, state: Literal['like', 'unlike']):
    case_state = {
        'like': 'merge (u)-[l:LIKED]->(ps)',
        'unlike': 'match (u)-[l:LIKED]->(ps) delete l'
    }
    queried_state = case_state[state]
    
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match (u:{UserEntity.__name__}) where u.username=$username
            match ()-[c:CREATED]->(ps:{PostEntity.__name__}) where c.id=$post_id
            {queried_state}
            """,
            username=by, post_id=post_id
        )
        
        consume = await result.consume()
        if not consume.counters.contains_updates:
            raise ValueError('No changes')
        
async def get_post_likers(post_id: str) -> List[UserEntity]:
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match ()-[c:CREATED]->(ps:{PostEntity.__name__})<-[:LIKED]-(u:{UserEntity.__name__})
            where c.id=$post_id
            return u
            """,
            post_id=post_id
        )
        data = await result.data()
        if data == []:
            raise ValueError('Found nothing')
        return [UserEntity.model_validate(u['u']) for u in data] 
    
async def get_post_comments(post_id: str, 
                            skip: int = 0, limit: int | None = None,
                            ) -> list[dict]:
    position = f'skip {skip} ' + (f'limit {limit}' if limit else '')
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match ()-[cr:CREATED]->(ps:{PostEntity.__name__})<-[ct:COMMENT]-(c:Comment)<-[:COMMENTED]-(u:{UserEntity.__name__})
            optional match (ls:{UserEntity.__name__})-[liked:LIKED]->(c)
            where cr.id=$post_id
            return ct.id as id, ct.at as at, u.username as who, cr.id as post_id, c.message as message, count(ls) as likes
            order by at desc
            {position}
            """,
            post_id=post_id
        )
        data = await result.data()
        if data == []:
            raise ValueError('No comments')
        
        return [{'id': c['id'], 
                'publicated': c['at'].to_native(), 
                'by': c['who'], 
                'post': c['post_id'], 
                'message': c['message'], 
                'likes': c['likes']}
                for c in data]
    
async def create_comment(user_id: str, post_id: str, message: str) -> Tuple[str, datetime, str, str, str, int]:
    body_format = compile_cyphir_list_formatter(center=':', right='${}', around=('{', '}'))
    dumped_comment = {'message': message}
    dumped_comment_relation = {'id': str(uuid4()), 'at': datetime.utcnow()}
    async with get_transaction() as tx:
        tx: AsyncTransaction = tx
        result = await tx.run(
            f"""
            match (u:{UserEntity.__name__}) where u.username=$username
            match ()-[cr:CREATED]->(ps:{PostEntity.__name__}) where cr.id=$post_id
            create (u)-[:COMMENTED]->(c:Comment {body_format(dumped_comment)})-[:COMMENT {body_format(dumped_comment_relation)}]->(ps)
            """,
            **dumped_comment, **dumped_comment_relation, username=user_id, post_id=post_id
        )
        consume = await result.consume()
        if not consume.counters.contains_updates:
            raise ValueError('No changes')
        return {
            'id': dumped_comment_relation['id'], 
            'publicated': dumped_comment_relation['at'], 
            'by': user_id, 
            'post': post_id, 
            'message': message, 
            'likes': 0}
        