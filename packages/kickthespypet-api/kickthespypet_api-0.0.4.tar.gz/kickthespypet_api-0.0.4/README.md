# kickthespypet-api

A kickthespy.pet API wrapper for Python with fully documented and type-annotated. All API are made using [the javascript file from the website](https://kickthespy.pet/main.js)

## Installing

```shell
pip install git+https://github.com/timelessnesses/kickthespypet-api
# or
pip install kickthespypet-api
```
You also need `discord` version of your choice (not installed automatically)

## Examples

```python
import kickthespypet_api

client = kickthespypet_api.KickTheSpyPetAPI()
client.get_bot_by_server_id(20).id
client.get_bot_by_server_invite("server invite here")
for bot in client.get_bot_user_ids_int():
    await (await bot_client.fetch_user(bot)).ban()
```

`AsyncKickTheSpyPetAPI` is same API as `KickTheSpyPetAPI` but all of HTTP requests will be made with `aiohttp` instead of `requests` and they are asynchronous so you need to `await`

## This is NOT stable

This module is not YET been confirmed to work in every situation and some requests might fails. Please open an issue for that.
