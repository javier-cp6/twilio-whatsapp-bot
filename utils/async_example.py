import asyncio

text_start = "start"

async def say_after(text):
  await asyncio.sleep(5)
  print(text, "from function")
  return text

async def main(q):
  print(text_start)
  text = await say_after(q)
  await say_after(q + " again")
  print(text)

# coroutines
async def main_new(q):
  print(text_start)
  task1 = asyncio.create_task(say_after(q))
  task2 = asyncio.create_task(say_after(q + " again"))

  text = await task1
  await task2
  print(text)

asyncio.run(main_new("hello"))