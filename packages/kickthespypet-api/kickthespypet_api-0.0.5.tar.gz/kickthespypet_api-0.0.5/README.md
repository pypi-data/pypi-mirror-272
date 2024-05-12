# kickthespypet-api

A kickthespy.pet API wrapper for Python with fully documented and type-annotated. All API are made using [the javascript file from the website](https://kickthespy.pet/main.js)

## Installing

```shell
pip install git+https://github.com/timelessnesses/kickthespypet-api
# or
pip install kickthespypet-api
```

## Examples

```python
import kickthespypet_api

client = kickthespypet_api.KickTheSpyPetAPI()
client.get_bot_by_server_id(20).id
client.get_bot_by_server_invite("server invite here")
for bot in client.get_bot_user_ids_int():
    await (await bot_client.fetch_user(bot)).ban()\
client.close()

# or you can use `with`

with kickthespypet_api.KickTheSpyPetAPI() as client:
    # do stuff
# closed automatically once done

```  

Async:  

```python
import kickthespypet_api

client = kickthespypet_api.AsyncKickTheSpyPetAPI()
stuff = await client.get_bot_by_server_id(1000)
print(stuff)
await client.close()

# or you can use `async with`

async with kickthespypet_api.AsyncKickTheSpyPetAPI() as client:
    # do stuff
# closed automatically once done

```

`AsyncKickTheSpyPetAPI` is same API as `KickTheSpyPetAPI` but all of HTTP requests will be made with `aiohttp` instead of `requests` and they are asynchronous so you need to `await`.  
Reminder: if you don't use `(async) with`, you need to close the session by yourself.

## This is NOT fully documented and STABLE

Due to [kickthespy.pet](https://kickthespy.pet) doesn't have official documentation on their responses, I really can't document every values or states that [kickthespy.pet](https://kickthespy.pet) can send. Please open pull request for that if you know it's type and documentation. Check out at `kickthespypet_api/types.py` for list of `Unknown` types and unknown documentation of the value.
