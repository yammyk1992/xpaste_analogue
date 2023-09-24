# from app_text import app
# from starlette.requests import Request
# from starlette.responses import Response
#
# from database import async_session_maker
#
#
# @app.middleware('http')
# async def get_session(request: Request, call_next):
#     response = Response("Internal server Error", status_code=500)
#     try:
#         request.state.db = async_session_maker()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response

