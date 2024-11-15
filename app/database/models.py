from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url= "sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key= True)
    tg_id = mapped_column(BigInteger)
'''
class Post(Base):
    # разобраться
    author: Mapped['User'] = relationship(back_populates='posts')
'''
class Preposition(Base):
    __tablename__ = "prepositions"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    part1: Mapped[str] = mapped_column(String(125))  
    prep: Mapped[int] = mapped_column(String(125))
    part2: Mapped[int] = mapped_column(String(125))
    description: Mapped[int] = mapped_column(String(125))

class Words(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key= True, autoincrement= True)
    word: Mapped[str] = mapped_column(String(125))  
    translation: Mapped[int] = mapped_column(String(125))
      

  

class Uncountable(Base):
    __tablename__ = "uncountable"
    

    id: Mapped[int] = mapped_column(primary_key= True)
    word: Mapped[str] = mapped_column(String(125))  
    translation: Mapped[int] = mapped_column(String(125)) 

class Uncountable2(Base):
    __tablename__ = "uncountable2"

    id: Mapped[int] = mapped_column(primary_key= True)
    word: Mapped[str] = mapped_column(String(125))  
    translation: Mapped[int] = mapped_column(String(125))       

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
