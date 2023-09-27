import asyncio
import aiohttp
import re
import requests
from datetime import datetime
from more_itertools import chunked
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from db import PG_DSN, Characters, Base

CHUCK_SIZE = 10

id_count = requests.get('https://swapi.dev/api/people/').json()['count']


engine = create_async_engine(PG_DSN)


async def get_people(session, people_id):
    result = await session.get(f'https://swapi.dev/api/people/{people_id}')
    return await result.json()


async def main():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()
        async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with aiohttp.ClientSession() as web_session:
            for chunk_id in chunked(range(1, id_count+ 1), CHUCK_SIZE):
                coros = [get_people(web_session, i) for i in chunk_id]
                result = await asyncio.gather(*coros)

                # --- запись данных в БД ---
                people_list = []
                for item in result:
                    people_list.append(Characters(
                            id=int(re.search('\d+', item.get('url', '0')).group(0)),
                            birth_year=item.get('birth_year'),
                            eye_color=item.get('eye_color'),
                            films=','.join(item.get('films', [])),
                            gender=item.get('gender'),
                            hair_color=item.get('hair_color'),
                            height=item.get('height'),
                            homeworld=item.get('homeworld'),
                            mass=item.get('mass'),
                            name=item.get('name'),
                            skin_color=item.get('skin_color'),
                            species=','.join(item.get('species', [])),
                            starships=','.join(item.get('starships', [])),
                            vehicles=','.join(item.get('vehicles', []))
                        ))

                async with async_session_maker() as orm_session:
                    orm_session.add_all(people_list)
                    await orm_session.commit()
                    
if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    end = datetime.now()
    print(end - start)