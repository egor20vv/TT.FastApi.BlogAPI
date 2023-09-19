from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv


user_route = InferringRouter(tags=['User'])


@cbv(router=user_route)
class UserAPI:
    
    @user_route.get('/user/me')
    async def get_about_me(credentianals):
        return {
            'name': 'USER NAME',
            'email': 'USER EMAIL'      
        }
    
    