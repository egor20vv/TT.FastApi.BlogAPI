from neo4j import AsyncGraphDatabase
from utils import singleton





@singleton
class DbNeo4j:
    
    def __init__(self, uri: str, user: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
    
    async def get_session(self):
        async with self.driver.session() as session:
            yield session
    
    
async def test_function():
    session = await DbNeo4j.get_session()        
    await session.run('')
    
if __name__ == '__main__':
    DbNeo4j('neo4j+s://localhost:7687', 'neo4f', '1234qwer')
    db = DbNeo4j()
    