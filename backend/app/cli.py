import asyncclick as click
import asyncio
import random

from backend.database import connect_database
from schemas.dto.user import UserCreateDto
from services.user import UserService

from faker import Faker
from faker.providers import internet


@click.group()
def cli():
    pass


@click.command()
@click.option('--count', type=int, default=1, help='Generate n fake users')
@click.option('--locale', type=str, default='ru_RU', help='locale format -- en_EN')
async def create_fake_user(count: int, locale: str) -> None:
    '''Generate fake user'''
    await connect_database()
    faker = Faker(locale=locale)
    faker.add_provider(internet)

    for i in range(count):
        user = UserCreateDto(
            user_id=random.randint(100000000, 999999999),
            email=faker.email(),
            full_name=faker.user_name(),
            username=f'@{faker.user_name()}',
        )
        await UserService.create(user)
        click.echo(f'[{i+1}] {user}')


if __name__ == '__main__':
    asyncio.run(create_fake_user())
