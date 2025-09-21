import hikari as hi
import openai

bot = hi.GatewayBot(token="", intents=hi.Intents.ALL_UNPRIVILEGED | hi.Intents.MESSAGE_CONTENT)
oai_token = ''

openai.api_key = oai_token

allowed_channels = [1082382912286101605, 416822240030490644]

def generate_response(prompt):
    completion = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    answer = completion.choices[0].text
    return answer

@bot.listen(hi.GuildMessageCreateEvent)
async def chat(event):
    if event.is_bot or event.channel_id not in allowed_channels:
        return
    await event.message.respond(generate_response(event.content), reply=True)

bot.run() 