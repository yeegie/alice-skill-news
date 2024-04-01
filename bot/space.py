from services import SessionService
import asyncio
from datetime import datetime, timedelta
from json import dumps

from datetime import date, datetime

def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code
    Example:
        date = json.dumps(date_raw, default=json_serial)
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

async def main():
    date = (datetime.now() + timedelta(minutes=3)).isoformat() + 'Z'
    print(f'{date=}')

    await SessionService.create(
        user_id=423420323,
        secret="пизда хуй",
    )

if __name__ == '__main__':
    asyncio.run(main())
