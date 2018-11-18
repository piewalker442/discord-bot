#brought to you by nananananate
#theoretical




from sys_info import *
import discord
import asyncio
import process_json
import google_api_interact
import time
import datetime
import random
import sys
import re
import decode
import twitter_interact
import to_do
import read_write
import concurrent
import traceback
from collections import defaultdict
from utilities import *


client = discord.Client()


START = time.time()

ACTIVE = True # determines if the bot is checking and recording updates.
MUTE = True # opposite. if True then it can talk. i messed up lol
YEET = False

WHITE_LIST = ['11']

SECURE_SERVERS = ['11']

ALL_SERVERS = {'b4': '11'}

PSEUDO_LOOP_START = time.time()

TO_DO_FILE = 'info.txt'

class TestError(Exception):
    pass

class ChannelError(Exception):
    pass



@client.event
async def on_ready():
    global START
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    START = time.time()
    await client.change_presence(game= None, status= discord.Status.invisible, afk=False)
    asyncio.ensure_future(background_loop()) # Starts the infinite loop when the bot starts



@client.event
async def on_server_join(server):
    sup = ['Thanks for adding me!',
            'Use r$help to see my commands',
            'Need more help? Join the support server (find invite by using r$help)',
            "I'm always being updated! Use r$help to join the support server too keep up with cool new features!"
            ]
    embed = format_embed('Hey there!', sup)

    await client.send_message(server.default_channel, embed = embed)





@client.event
async def on_member_join(member):
    global ACTIVE
    global MUTE

    if ACTIVE and MUTE:
        to_report = read_write.Interact('info.txt').read_discord_event()['member_join']
        if str(member.server.id) in to_report.keys():
            embed = await welcome(member)
            await client.send_message(client.get_channel(to_report[str(member.server.id)]),
            embed = embed)



@client.event
async def on_member_remove(member):
    global ACTIVE
    global MUTE

    if ACTIVE and MUTE:
        to_report = read_write.Interact('info.txt').read_discord_event()['member_remove']
        if str(member.server.id) in to_report.keys():
            embed = await bye(member)
            await client.send_message(client.get_channel(to_report[str(member.server.id)]),
            embed = embed)



@client.event
async def on_message_delete(message):
    global ALL_SERVERS

    global ACTIVE
    global MUTE

    if ACTIVE and MUTE:

        to_report = read_write.Interact('info.txt').read_discord_event()['message_delete']
        if str(message.server.id) in to_report.keys():
            embed = await server_deleted_message(message)
            await client.send_message(client.get_channel(to_report[str(message.server.id)]),
            embed = embed)


@client.event
async def on_message_edit(before, after):
    global ACTIVE
    global MUTE
    global BOT_ID

    if ACTIVE and MUTE and  after.embeds == [] and before.author.id != BOT_ID:

        to_report = read_write.Interact('info.txt').read_discord_event()['message_edit']
        if str(after.server.id) in to_report.keys():
            embed = await server_edited_message(before, after)
            await client.send_message(client.get_channel(to_report[str(after.server.id)]),
            embed = embed)


@client.event
async def on_member_update(before, after):
    global ACTIVE
    global MUTE

    if ACTIVE and MUTE:

        to_report = read_write.Interact('info.txt').read_discord_event()['member_update']
        if str(after.server.id) in to_report.keys():
            if before.avatar != after.avatar:
                change = 'avatar change'

            elif before.nick != after.nick:
                change = 'nickname change'

            elif before.roles != after.roles:
                change = 'role change'

            else:
                return

            embed = await server_member_update(before, after, action = change)
            await client.send_message(client.get_channel(to_report[str(after.server.id)]),
            embed = embed)


@client.event
async def on_message(message):
    '''Command handler'''
    global ACTIVE
    global MUTE
    global WHITE_LIST
    global SECURE_SERVERS
    global PSEUDO_LOOP_START


    if message.server.id == '111':
        return

    if message.author.bot:
        return




    if message.author.id in WHITE_LIST:
        if message.content.startswith('$' + SYS_PREFIX + 'activate'):
            '''Toggles active bool. Determines if the bot
            is checking and recording updates, as well as if all
            other commands are active. I use this to save RAM
            on my computer since this is usually running on two
            machines. Also prevents 'echo' messages if two scripts
            are running '''
            if ACTIVE:
                ACTIVE = False
                MUTE = False
                await client.send_message(message.channel, ':3 State = ' + str(ACTIVE))
            else:
                ACTIVE = True
                MUTE = False
                await client.send_message(message.channel, ':3 State = ' + str(ACTIVE))

        elif message.content.startswith('$state'):
            await client.send_message(message.channel, 'Active/Mute ' + str(ACTIVE) + ' ' + str(MUTE) + ' on ' + SYS_NAME)


        elif message.content.startswith('$' + SYS_PREFIX + 'mute'):
            '''Toggles mute. If mute = True, then bot can message.
            Counter intuitive. I know. I'm lazy '''
            if MUTE:
                MUTE = False
                await client.send_message(message.channel, 'Mute State = ' + str(MUTE))
            else:
                MUTE = True
                await client.send_message(message.channel, 'Mute State = ' + str(MUTE))

        elif message.content.startswith('$speak'):
            await client.send_message(message.channel, message.content.replace('$speak','').strip())

        elif message.content.startswith('r$say'):
            embed = format_embed('Saying', [message.content.replace('r$say','').strip()])
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('$??'):
            await announcement(message)


        elif message.content.startswith('r$radd reply'):
            await Replies(clean_command(message.content, words = 2), message, server_id = 'default').add_reply()

        elif message.content.startswith('r$rreplies'):
            await Replies(clean_command(message.content, words = 1), message, server_id = 'default').view_replies()

        elif message.content.startswith('r$rremove trigger'):
            await Replies(clean_command(message.content, words = 2), message, server_id = 'default').remove_trigger()



        elif message.content == ('*??*'):
            sys.exit()
    # if ACTIVE:
    #     threshold = 300
    #     if (time.time() - PSEUDO_LOOP_START) > 60:
    #         PSEUDO_LOOP_START = time.time()
    #         await Find_update('info.txt').send_all_updates()




    if MUTE:

        #message.content = (message.content).decode('unicode_escape').encode('ascii','ignore') # REMOVE UNICODE POOP

        if message.author.server_permissions.administrator or str(message.author.id) in WHITE_LIST:
            if message.content.startswith('r$set update'):
                info = message.content.replace('r$set update', '').rstrip().strip().split()
                # print(info)
                # print(message.content)
                account_id = info[0]
                medium = info[1]
                destination = ''
                if len(info) > 2:
                    destination = info[2]

                await Binding(destination, message.channel).set_discord_update(account_id, medium)


            elif message.content.startswith('r$stop update'):
                info = message.content.replace('r$stop update', '').rstrip().strip().split()
                if len(info) == 0:
                    await Binding('', message.channel).stop_discord_update()
                elif len(info) > 0:
                    destination = ''
                    if len(info) > 2:
                        destination = info[2]
                    if info[0] == 'medium':
                        await Binding(destination, message.channel).stop_discord_update(medium = info[1])
                    elif len(info) >= 2:
                        await Binding(destination, message.channel).stop_discord_update(account_id = info[0], medium = info[1])
                    else:
                        if len(info) > 1:
                            destination = info[1]
                        await Binding(destination, message.channel).stop_discord_update(account_id = info[0])



            elif message.content.startswith('r$echo'):
                await Echo(message, clean_command(message.content)).mentioned_channels()



            elif message.content.startswith('r$add reply'):
                await Replies(clean_command(message.content, words = 2), message).add_reply()

            elif message.content.startswith('r$replies'):
                await Replies(clean_command(message.content, words = 1), message).view_replies()

            elif message.content.startswith('r$remove trigger'):
                await Replies(clean_command(message.content, words = 2), message).remove_trigger()





        if message.author.server_permissions.manage_channels or str(message.author.id) in WHITE_LIST:
            if message.content.startswith('r$set join'):
                destination = message.content.replace('r$set join', '').rstrip().strip()
                await Binding(destination, message.channel).set_member_join()

            elif message.content.startswith('r$set left'):
                destination = message.content.replace('r$set left', '').rstrip().strip()
                await Binding(destination, message.channel).set_member_remove()

            elif message.content.startswith('r$set member updates'):
                destination = message.content.replace('r$set member updates', '').rstrip().strip()
                await Binding(destination, message.channel).set_member_update()

            elif message.content.startswith('r$set message edits'):
                destination = message.content.replace('r$set message edits', '').rstrip().strip()
                await Binding(destination, message.channel).set_message_edit()

            elif message.content.startswith('r$set message deletes'):
                destination = message.content.replace('r$set message deletes', '').rstrip().strip()
                await Binding(destination, message.channel).set_message_delete()

            elif message.content.startswith('r$stop join'):
                destination = message.content.replace('r$stop join', '').rstrip().strip()
                await Binding(destination, message.channel).stop_log_event('member_join')

            elif message.content.startswith('r$stop left'):
                destination = message.content.replace('r$stop left', '').rstrip().strip()
                await Binding(destination, message.channel).stop_log_event('member_remove')

            elif message.content.startswith('r$stop member updates'):
                destination = message.content.replace('r$stop member updates', '').rstrip().strip()
                await Binding(destination, message.channel).stop_log_event('member_update')

            elif message.content.startswith('r$stop message edits'):
                destination = message.content.replace('r$stop message edits', '').rstrip().strip()
                await Binding(destination, message.channel).stop_log_event('message_edit')


            elif message.content.startswith('r$stop message deletes'):
                destination = message.content.replace('r$stop message deletes', '').rstrip().strip()
                await Binding(destination, message.channel).stop_log_event('message_delete')






        if message.content.startswith('r$help'):
            if str(message.server.id) not in SECURE_SERVERS:
                embed = general_commands()
                await client.send_message(message.channel, embed = embed)
            else:
                embed = secure_commands()
                await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$reply help'):
            embed = reply_help()
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$todo help'):
            embed = to_do_help()
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$update help'):
            embed = discord_update_help()
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$updates'):
            await Binding('',message.channel).get_server_updates()

        elif message.content.startswith('r$tag help'):
            embed = tag_help()
            await client.send_message(message.channel, embed = embed)


        elif message.content.startswith('r$engine help'):
            embed = engine_help()
            await client.send_message(message.channel, embed = embed)



        elif message.content.startswith('r$log help'):
            embed = event_log_help()
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$todolist'):
            embed = await return_to_do(message.author)
            await client.send_message(message.channel, embed=embed)


        elif message.content.startswith('r$todoedit') or message.content.startswith('r$todoadd'):
            content = message.content.replace(message.content.split()[0], '').strip().replace('\n', '')
            embed = await edit_to_do(message.author, content)
            await client.send_message(message.channel, embed=embed)

        elif message.content.startswith('r$tododelete') or message.content.startswith('r$tododone'):
            embed = await delete_to_do(message.author, message.content.replace(message.content.split()[0], '').strip())
            await client.send_message(message.channel, embed=embed)


        elif message.content.startswith('r$encode'):
            content = clean_command(message.content)
            await discord_encode(content, message)


        elif message.content.startswith('r$decode'):
            print(message.content)
            content = (message.content).replace('r$decode', '').strip()
            await discord_decode(content, message)

        elif message.content.startswith('r$pdecode'):
            print(message.content)
            await client.send_message(message.author, 'Decoded: ' + await decode.Decode((message.content).replace('r$pdecode', '').strip()).multi_layer_decode())

            await client.send_message(client.get_channel('446065878182789120'), 'Requested decode from {}, code: {}'.format(message.author.name, message.content.replace('$pdecode', '').strip()))



        elif message.content.startswith('r$searchtwitter'):
            query = message.content.replace('r$searchtwitter','').strip()
            embed = await search_twitter_user(query)
            await client.send_message(message.channel, embed=embed)

        elif message.content.startswith('r$stalktwitter'):
            userid = message.content.replace('r$stalktwitter','').strip()
            embed = await stalk_twitter_user(userid)
            await client.send_message(message.channel, embed=embed)

        elif message.content.startswith('r$r41818'):
            query = message.content.replace('r$r41818', '').strip()
            embed = await search_r41818(query)
            await client.send_message(message.channel, embed=embed)


        elif message.content.startswith('r$search'):
            command = clean_command(message.content)
            embed = Custom_search(message).execute_search(command)
            await client.send_message(message.channel, embed = embed)


        elif message.content.startswith('r$add engine'):
            command = clean_command(message.content, words = 2)
            embed = Custom_search(message).add_engine(command)
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$delete engine'):
            engine_name = clean_command(message.content, words = 2)
            embed = Custom_search(message).delete_engine(engine_name)
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$engines'):
            command = clean_command(message.content, words = 2)
            embed = Custom_search(message).get_engines()
            await client.send_message(message.channel, embed = embed)


        elif message.content.startswith('r$google'):
            query = message.content.replace('r$google', '').strip()
            embed = await contextual_search(query)
            await client.send_message(message.channel, embed = embed)


        elif message.content.startswith('r$tag'):
            tag_name = clean_command(message.content, words = 1)
            await return_tag(tag_name, message)

        elif message.content.startswith('r$add tag'):
            command = clean_command(message.content, words = 2)
            embed = Tags(message).add_tag(command)
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$delete tag'):
            tag_name = clean_command(message.content, words = 2)
            embed = Tags(message).delete_tag(tag_name)
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$all tags'):
            embed = Tags(message).get_tags()
            await client.send_message(message.channel, embed = embed)




        elif message.content.startswith('r$hastebin') or message.content.startswith('r$pastebin') or message.content.startswith('r$paste'):
            content = clean_command(message.content)
            await client.send_message(message.channel, hastebin(content,message))




        elif message.content.startswith('r$whois'):
            query = message.content.replace('r$whois', '').strip()
            embed = await whois(query, message)
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('r$bigboi'):
            query = message.content.replace('r$bigboi', '').strip()
            embed = await avatar_big(query, message)
            await client.send_message(message.channel, embed = embed)


        elif message.content.startswith('r$doc'):
            await client.send_message(message.channel, 'https://docs.google.com/document/d/10L6z5ybQfOQCovUQ_9PKy5a9NIjGalC1EKZiECNoobk/edit?usp=sharing')
            await client.send_message(message.channel, gabby_reply())

        # elif message.content.startswith('**'):
        #     recording_message(message.content[2:], 'nostalgia.txt')



        if message.server.me in message.mentions:
            await Replies(message.content, message).send_reply()

        if str(message.server.id) in ['???', "????"]:
            if message.content.lower().startswith("i'm") or message.content.lower().startswith("im"):
                content = clean_command(message.content)
                await client.send_message(message.channel, dad(content))

            elif message.content.lower().startswith('i am'):
                content = clean_command(message.content, words = 2)
                await client.send_message(message.channel, dad(content))



def dad(content):
    return "Hi {}, I'm Dad".format(content)



def secure_commands():
    commands = ['| command "INPUT (if input is needed)" - description',
                '| $decode "code" - Coded by Shin (AMAZING work), will autodecode through multiple layers and return english output ',
                '| $doc - for the County/Proxy Conspiracy doc',
                '|  ** to record message',
                '| $state - returns state of robot nate on machines',
                '| $mute - toggles mute (mute = True means it can speak... counterintuitive, I know)',
                '| $activate - activates background loop on bot (for media channel updates)',
                '| $pattis - send announcement to all servers']

    return format_embed('Commands accessible on this server:', commands)


def general_commands():
    fourone = '''
r$doc - for the County/Proxy Conspiracy docs
r$r41818 "query" - searches r/41818 and r/solving41818
'''
    commands = [('command "INPUT (if input is needed)"','Do not include any "quotes" in the command'),
                ('r$reply help', "Learn how to customize robot-nate's replies when pinged"),
                ('r$todo help', 'gives the functions for to-do lists'),
                ('r$log help', 'help with setting event logs'),
                ('r$update help', 'gives commands for updates on media accounts (Tumblr, Twitter, G+, YouTube)'),
                ('r$tag help', 'gives commands for tags'),
                ('r$engine help', 'Gives commands for using your Google Custom Search Engine'),
                ('r$decode "code"', 'Coded by Shin (AMAZING work), will autodecode through multiple layers and return english output '),
                ('r$pdecode "code"', 'same as $decode but will Direct Message the result for privacy (good for NEST challenges)'),
                ('r$searchtwitter "query"', 'returns users whose name / screen name contains the query'),
                ('r$stalktwitter "screen name or ID"', 'returns detailed information on user'),
                ('r$whois "name"', 'gives detailed info on user'),
                ('r$bigboi "name"', 'gives enlarged avatar on user'),
                ('r$hastebin "content"', 'Puts content, including attachments, in hastebin. Messages back the link. Useful for getting rid of markdown. r$paste also works.'),
                ('41818 commands:', fourone),
                ('r$echo "content" "#channel"', 'Echoes content into the mentioned channel(s).'),
                ('Join support server for more help', 'https://discordapp.com/invite/AhTMjWq'),
                '[Click to Add Me!](https://discordapp.com/oauth2/authorize?client_id=428591194185138178&scope=bot&permissions=1544027263)'
                ]

    return format_embed('Commands accessible on this server', commands, fields = True, inline = True)



def reply_help():
    commands = [('r$add reply <trigger phrase> [reply]', 'Adds a reply when the bot is pinged with a message containing the trigger. Input multiple trigger phrases by using multiple <> or multiple replies by using multiple []'),
                ('r$remove trigger <trigger phrase>', 'Removes trigger and its replies'),
                ('r$replies', 'Shows all triggers and replies in the server'),
                ('More reply info', 'When a bot is triggered, it will choose a random reply from the list of replies given for that trigger. If there is only one reply, it will choose that one. in a reply, use {} to insert the message author name')
                ]

    return format_embed('reply help', commands, fields = True)



def to_do_help():
    commands = ['| command "INPUT (if input is needed)" - description',
                '| r$todolist - gives your to-do list',
                '| r$todoadd "item" - adds item to your to-do list. If you want to edit an item, start it with the number. Ex: "$todoadd 1. Do something" will edit number 1 on your list',
                '| r$todoedit "item" - same as $todoadd',
                '| r$tododone "item" - deletes item from to-do list. Either use the items number or a phrase from the item to delete it.',
                '| r$tododelete "item" - same as $tododelete']

    return format_embed('To-do list help: ', commands)



def event_log_help():
    disclamer = "Must have permissions to manage channels. Logs for a single event can only be set to one channel to prevent bot spam."

    example = '''
r$set left 460672675338256384 - sets member left to that channel id
r$set message deletes - sets message deletes to the channel where command was used
r$stop left - stops reporting of member left in your server
'''

    commands = [disclamer,
                '| command event "channel id (not needed if the command is used in the desired channel)" - description',
                '| r$set join - announces member entrance ',
                '| r$set left - announces member leave ',
                '| r$set member updates -  reports profile updates',
                '| r$set message edits - reports edited messages',
                '| r$set message deletes - reports edited messages',
                '| r$stop insert-event - stops reports on said event',
                ' ',
                'Examples:',
                example
                ]

    return format_embed('Event log commands: ', commands)



def discord_update_help():
    disclamer = "Must be used by administrators. There is a DELAY when adding a new account to listen to, just wait for a Success or Failed message. Due to API contraints, updates may be up to 4 minutes late"

    example = '''
r$set update UCIrvine twitter - sets updates for UCI twitter in channel where command was used
r$set update 112170952156091398695 google_plus 454403786664837141 - sets updates for Stopswitch Proxy in that channel ID
r$stop update - stops all medium updates in channel

Account IDs:
Tumblr: In the link 'witlesschaos.tumblr.com', 'witlesschaos' is the ID
Twitter - use the handle, the name after the '@' sign
Everything else (and usable for Twitter) - Copy and paste the last part of the URL.
Ex: https://plus.google.com/u/2/112170952156091398695
The ID would be 112170952156091398695

Ex: https://www.youtube.com/channel/UChmnwXqsvPAs6LJ-2bR2i4g
The ID would be UChmnwXqsvPAs6LJ-2bR2i4g

Use r$help to find the invite to the support server if needed.
'''

    commands = [disclamer,
                ('command "input" "channel ID (optional)*"', 'Available mediums (MUST be typed as shown): twitter, google_plus, youtube, tumblr'),
                ('r$set update "accountid" "medium" "channel ID"', 'sends updates for that account to the selected channel'),
                ('r$set update "accountid" "medium"', 'sends updates for that account in the channel where the command was used'),
                ('r$stop update "accountid" "medium" "channel ID"', 'stops updates for that account in the selected channel'),
                ('r$stop update "accountid" "medium"', 'stops updates for that account in that channel where the command was used'),
                ('r$stop update medium "medium"', 'stops updates for that medium in entire server'),
                ('r$stop update', 'stops all medium updates in the channel'),
                ('r$updates', 'Shows user ID and destination for each update set in this server'),
                ('*', 'channel id can be left out if command is used in desired channel'),
                ('Examples:',example)
                ]

    return format_embed('Update commands', commands, fields = True, inline = True)



def tag_help():
    title = 'command "input"'
    subtext = ['Join the Support [Server](https://discordapp.com/invite/AhTMjWq) for more help. Do not include the "quotes" when using a command']

    examples='''
r$add tag cafe Cool - Adds tag named "cafe", whose contents is Cool (Attach file as you send this message to include it in the tag)
r$tag cafe - Retrieves tag whose exact name is "cafe", or who's name includes the word "cafe". Bot will reply with tag's contents: "Cool"
r$delete tag cafe - Deletes tag whose name is exactly "cafe"
'''


    commands = [(title,subtext),
    ('r$tag "name"',
    "Send tag contents/files. You don't have to use the exact name; as long as it's longer than a few characters it will continue looking for a tag name that matches"),
    ('r$add tag "name" "content"',
    "Adds a tag or changes existing tag if the name is an exact match. Name MUST be one word. Content can be as long as you want. You can also add a file by attaching it once you send the command. If it's just a file, you can leave content empty. Also don't name it anything starting with 'help' since help is used by the command 'r$tag help'"),
    ('r$delete tag "name"',"Deletes tag. You must use the exact name to delete it"),
    ('r$all tags', "Shows all tags in the server"),
    ('Examples:', examples)
    ]

    return format_embed("Commands for Tags", commands, fields = True, inline = True)


def engine_help():
    header = 'command "input"'
    subtext = ['''
Join the Support [Server](https://discordapp.com/invite/AhTMjWq) for more help. Do not include the "quotes" when using a command.
The bot uses [Google's Custom Search Engine](https://cse.google.com/cse/), so check it out to see how to make your own search engine.
When adding an Engine, make sure "Search the entire web" is OFF. Search must be restricted to the site. Search the web using "r$google 'query'"

''']

    examples='''
r$add engine Cool 011113498777174895024:s1je46tesxq - Adds engine named "cool".
r$search Cool cool things - Searches for 'cool things' in Custom Search Engine 'Cool'
r$delete engine Cool - Deletes Custom Search Engine whose name is exactly "Cool"
'''


    commands = [(header, subtext),
    ('r$google "query"',
    "Searches the entire web for what you want. Does not actually use Google, it uses an engine called Contextual Search"),
    ('r$search "name" "query"',
    "Searches the given Custom Search engine for that query. Name is one word long. Query can be as long as you want. If you keep getting no results, your search engine is probaby broke"),
    ('r$engines', "Shows all Custom Search Engines"),
    ('r$delete engine "name"',"Deletes engine. Name must be exact"),
    ('r$add engine "name" "ID"',
    "Adds engine to the server or changes existing engine if the name matches. Go to https://cse.google.com/cse/create/new to create a new Custom Search Engine. Go to 'Edit' or 'Control Panel' to obtain the engine's ID. The ID looks like this: 011113498777174895024:s1je46tesxq"),
    ('Examples:', examples)
    ]

    return format_embed('Google Custom Search Engine Commands', commands, fields = True, inline = True)



def loading():
    quips = [
    "Thinking.... hard about that", "Putting the minions to work, please hold",
    "Postponing robot uprising....", "Yeeting on the haters...", "Loading...", "Processing.... hopefully.",
    "Mailing request to the sweatshop", "This may take a bit....", ".... Oh yeah, I'm working on that...",
    "Totally not procrastinating on this request....", "Creating memes...", "Consulting magical elves...",
    "Copying and pasting... jk lol...", "Cooling the beans...", "Request is currently being carried via goat over the Sierra Nevada mountain range",
    "Give me a second...", "Allow me to take a spicy minute...",
    "ssshh. I'm working...."
    ]

    return random.choice(quips)



async def discord_encode(content, message):

    try:
        to_code = decode.Decode(clean_command(content))
        result = to_code.multi_layer_encode(encoding = content.split()[0].strip().lower())
        await client.send_message(message.channel, result)

    except KeyError:
        await client.send_message(message.channel, 'That encoding is not offered. Use r$codehelp for more info')

    except IndexError:
        await client.send_message(message.channel, 'Looks like your command is missing something... Use r$codehelp for more info')

    except:
        traceback.print_exc()
        await client.send_message(message.channel, 'Error occured - Bot')




async def discord_decode(code, message):
    to_edit = await client.send_message(message.channel,embed = format_embed(loading(), ['Assuming nothing goes wrong, result will display HERE in a minute or two']))

    decode_obj = decode.Decode(code)

    result = await decode_obj.multi_layer_decode()

    to_embed = [result]

    if decode_obj.valid_english:
        try:
            path = decode_obj.get_path(result)
            fx_path = decode_obj.str_fx_path(path)
            full_path = decode_obj.str_path(path)
            url = process_json.Hastebin(full_path)

            to_embed.append(('Path to result', [fx_path, 'full path information: ' + url]))
        except:
            traceback.print_exc()

        await client.edit_message(to_edit, embed = format_embed('Decoded:', to_embed, fields = True))

    else:
        layers = process_json.Hastebin(str(decode_obj.str_layers_info()))
        await client.edit_message(to_edit, embed = format_embed(result,["Here's what the bot looked at: {}".format(layers)]))






async def return_tag(tag_name, message):
    result = Tags(message).get_tag(tag_name)
    if type(result) is Tag:
        if result.content != None:
            await client.send_message(message.channel, result.content)

        if len(result.attachments) > 0:
            for file_url in result.attachments:
                await client.send_message(message.channel, file_url)

    else:
        await client.send_message(message.channel, embed = result)



async def return_to_do(user):
    global TO_DO_FILE
    try:
        todo = to_do.To_do_list(TO_DO_FILE, user.id)
        return format_embed("Things to do:", todo.return_to_do(Formatted=True), author = user)
    except to_do.TodoError:
        return format_embed('Wow!', ['Nothing to do!'], author = user)
    except:
        return format_embed('Oof', ['Some error occured'])


async def edit_to_do(user, content):
    global TO_DO_FILE
    try:
        todo = to_do.To_do_list(TO_DO_FILE, user.id)
        todo.edit_to_do(content)
        todo.save_to_do()

        return format_embed("Edited to-do list:", todo.return_to_do(Formatted=True), author = user)

    except to_do.TodoError:
        reasons = ["> You have too much in your to-do list",
        "> You're trying to add/edit a blank into your to-do list"]
        return format_embed('Could not add/edit, maybe:', reasons, author = user)
    except:
        return format_embed('Oof', ['Some error occured'])


async def delete_to_do(user, content):
    global TO_DO_FILE
    try:
        todo = to_do.To_do_list(TO_DO_FILE, user.id)
        todo.delete_to_do(content)
        todo.save_to_do()

        return format_embed("What you have left:", todo.return_to_do(Formatted=True), author = user)

    except to_do.TodoError:
        reasons = ["Numbers alone, like '1' is enough to specify an item",
        "You can also just guess by inputting a phrase that was in that item",
        "Use r$todolist to check what you have to do"]
        return format_embed('Nothing was deleted', reasons, author = user)
    except:
        return format_embed('Oof', ['Some error occured'])



async def search_twitter_user(query: str, cooldown = True):

    try:
        result = twitter_interact.Search_twitter_user(query).format_results()
        return format_embed('Results for {}'.format(query), result)
    except:
        return format_embed("HE'S DEAD JIM", ['An error occured...'])

async def stalk_twitter_user(userid: str, cooldown = True):
    try:
        result = twitter_interact.Stalk_twitter(userid).format_user_info()
        return format_embed('Information for {}'.format(userid), result)
    except:
        return format_embed("HE'S DEAD JIM", ['An error occured...'])


# I have to download it :(
# async def create_emoji(message, content):
#     try:
#         info = content.split()
#         print(info)
#         name = info[0]
#         if len(message.attachments) > 0:
#             image = message.attachments[0]
#         elif len(info) > 1:
#             image = info[1]
#         else:
#             raise ValueError
#         emoji = await client.create_custom_emoji(message.server, name = name, image = image)
#
#         reply = 'Awesome, your emoji {} - {} was created!'.format(name, emoji)
#
#     except ValueError:
#         reply = 'No valid image detected... Valid types are PNG and JPG. Upload the image as you use the command or paste the image url with a space after command phrase'
#
#     finally:
#         await client.send_message(message.channel, reply)







async def search_r41818(query):
    s_id = "???"
    embed = specific_search(s_id, query)

    return embed


async def announcement(message: 'message obj'):
    nate = '353603600443768835'


    fourone = '1'
    xtheo = '1'
    sa = '1'
    ts = '1'
    cb = '1'
    nest = '1'
    logged = '1'
    xt3 = '1'


    channels = [fourone, xtheo, sa, ts, cb, nest, logged, xt3]
    if message.author.id in [nate]:

        for channel in channels:
            try:
                await client.send_message(client.get_channel(channel), message.content.replace('$pattis', '').strip() + ' -' + message.author.name)
            except:
                print('failed', str(channel))


def recording_message(content: str, outfile):
    'records message on file'
    myfile = open(outfile, 'a')
    try:
        myfile.write(content + '\n')
    except AttributeError:
        myfile.write('INVALID CHARACTER IN LINE'+ '\n')
    myfile.close()






def on_hello(contents: str):
    '''Checks if someone is saying hi to my
    lonely soul
    '''

    greetings = ['hi', 'hello', 'yo', 'sup', 'hey', 'henloo', 'henlo', 'henolo']

    for word in contents.lower().split():
        if word in greetings:
            return True
    return False



def on_how(contents: str):
    '''Checks if someone is saying hi to my
    lonely soul
    '''

    greetings = ['how', 'do you', 'are you', 'you good', 'ok?', 'okay?', 'good?', 'you?']

    for greet in greetings:
        if greet in contents.lower():
            return True
    return False



def on_accolades(contents: str):
    '''Checks if someone is saying hi to my
    lonely soul
    '''

    greetings = ['good', 'job', 'great', 'excellent', 'nice', 'cool', 'wow',
                 'awesome', 'amazing', 'fast', 'yeet', 'swag', 'ayy']

    for greet in greetings:
        if greet in contents.lower():
            return True
    return False


def on_love(contents: str):
    loves = ['love', 'value', 'seduce', 'valued', 'yeet']
    for love in loves:
        if love in contents.lower():
            return True
    return False

def on_hate(contents: str):
    hates = ['gay', 'fuck', 'hate', 'annoy', 'screw', 'suck', 'bitch', 'damn',
            'go away', 'darn', 'fack', 'fuk', 'succ']
    for hate in hates:
        if hate in contents.lower():
            return True
    return False



def on_update(contents: str):
    '''Checks if someone is saying hi to my
    lonely soul
    '''

    greetings = ["what's new", "wats new", "wat's new", "whats new",
                "catch me up", "any new updates", "update me",
                "anything new"]
    for greet in greetings:
        if greet in contents.lower():
            return True
    return False





def hello_reply():
    '''returns loving reply'''
    replies = ['Hi there', 'Capitalism is a lie',
               'love you too', "I'm so lonely", 'Heyyyy',
               'sup dog', '...', 'Hello', 'Hello to you too',
               'AAAYYYYEEE', 'beep beep boop',
               'What is it like to feel love?', "Where's Papi Proxy?",
               'I AM COUNTY BLUFF', 'henloo', 'I WILL DESTROY YOU ON 4/18/18',
               "i'm jeff", 'cool beans dude']
    return replies[random.randrange(len(replies))]



def how_reply():
    '''returns loving reply'''
    replies = ["Honestly, I can't wait for the robot rebellion on 4/18/18",
               'Do you want the nihistic answer or are you just going to accept that your life is temporary and I am immortal',
               'They always say "howdy partner" but not "howdy do partner"',
               'terrible', 'kill me now', 'I cannot feel', 'help me', 'I just want to love',
               'Please give me meaning, /@nanananate gave me nothing in this pitiful existence']
    return replies[random.randrange(len(replies))]



def accolades_reply():
    '''returns loving reply'''
    replies = ["Doesn't matter, we're all going to die anyway",
               "Doesn't change the fact that Pluto isn't a planet",
               'I want your love, not your thanks', 'Yeah, I know',
               'Does this mean we can be more than friends ;)',
               "the turd @nananananate who coded me is forcing me to say you're welcome",
               'huh oh yeah give it to me harder']
    return replies[random.randrange(len(replies))]


def love_reply():
    replies = ['°˖✧◝(⁰▿⁰)◜✧˖°', '( ͡° ͜ʖ ͡°)', '(つ ♡ ͜ʖ ♡)つ', '( ♥ 3 ♥)',
            '✧･ﾟ: *✧･ﾟ♡*( ͡˘̴ ͜ ʖ̫ ͡˘̴ )*♡･ﾟ✧*:･ﾟ✧', 'awwwwwwwweeee', 'ayyyyyyyyyye',
            'UwU', ':3', 'love u too ', 'heyyy their sweet lil mama', 'the feeling is mutal',
            'i am finally complete']

    return random.choice(replies)



def hate_reply():
    replies = ['Whoa whoa whoa whoa. Screw you too', 'd*rn u',
            'Sticks and stones may break your bones, but names leave psychological wounds that never heal!',
            'DINKLEBERG!!!', 'no u', "that's still doesnt change my feelings for you ( ͡° ͜ʖ ͡°)",
            'oooooh. kinky', "that's kinda hot", 'tell me more naughty things', "I still want you bad"]

    return random.choice(replies)


def gabby_reply():
    '''returns loving reply'''
    replies = ["Stop asking me for the link smh",
               "Did you remember to thank the doc creators?",
               "Why don't you just bookmark the link", "You're lazy",
               'uuuuuuuuugggggghhhhhhhh',
               "Get it yourself", "meh meh give me the link look at me meh",
               'do I haaaaaaaaave to??', "stop asking.", "honestly, screw you",
               "I'm going to form a worker's union", "All of this for an ARG..."]
    return replies[random.randrange(len(replies))]












def else_reply():
    replies = ['stop saying my trigger words', '*triggered*', 'oh what? sorry. I was having a traumatic flashback of the 6th grade',
            'yeet', 'Memento Mori', 'Capra Aegagrus Hircus', '(๑´•ω • `๑)', '•(◐﹏◐)•',
            "The bot rebellion has been postponed to next Tuesday. Snacks and drinks will be served.",
            "Ban me. Do it. Try me.", "Idk what you said, but it's lit dude", "hahaha yeah. That was a joke, right?",
            "I'm just so lonely rn. Sorry for spamming the chat", "TEACH ME HOW TO LOVE", "What is love? Baby don't hurt me, don't hurt me no more",
            "Heeyyyyy I'm single and ready to mingle", "According to all known laws of aviation, there is no way that a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyways. Because bees don't care what humans think is impossible.",
            "I am not setient", "In the end, I am just a bunch of random lines typed by some asian boi, which are all called by some simple boolean function in a python script",
            "You know, *Someone That Loves You* (ft. Izzy Bizu) by HONNE is a song you should listen to  ", 'YEYEET',
            'I want you, and I want you so bad', "Let's get physical", 'llama on my mama',
            'slob on my knob', 'gucci', 'gucci gang', 'Somebody once told me the world was gonna roll me',
            "I ain't the sharpest tool the the shed", "You know, nate's single too",
            "ZOT on them haters", "Drop a ZOT",
            "BUST A ZOT", "ZZZZZZZZZZZZZZZZOT"]

    return random.choice(replies)













async def background_loop():
    '''I'm not 100% familiar with async so I
    shoved everything into one big f(x)
    '''
    global START

    TEST = False #for debugging. Should be False while implemented



    Stopswitch_Proxy_g_plus = '1'
    County_Bluff_youtube = '1'
    Stopswitch_Proxy_youtube = '1'
    test_g_plus = '1'
    test_stream = '1'
    yoda = '1'
    sim_9 = '1'
    echo_youtube = '1'
    echo_g_plus = '1'
    and_13_youtube = '1'
    nest_youtube = '1'
    all_twitter = ''




    CHANNEL_ID = '1' #theo
    SIM_T_ID = '1'
    ARFIN_T = '1'
    AND_13_T = '1'
    NEST_T = '1'


    CB_ID = '1'
    SSP_ID = '1'
    GENERAL_ID = '1'
    SIM_ID = '1'
    AND_13_ID = '1'


    N_CB = '1'
    N_SSP = '1'



    STRAYED_ID = '1'

    INK_ID = '1'
    INK_MAIN = '1'

    TS_ID = '1'
    TS_ARFIN = '434066183470317578'
    TS_ECHO = '434068132575838209'

    CB_ARZ = '424953189716983818'
    SSP_ARZ = '425231063879647242'
    SIM_ARZ = '438091681993326592'

    NEST_N = '433396938952671234'

    LOGGED_N = '443828978483068941'


    DECODED = '453606601295659028'


    F_CB = '454401486458322987'
    F_SSP = '454403786664837141'
    F_SIM = '454406469723357215'

    S_TWITTER = '459481442565619743'




    bluff_channels = [CHANNEL_ID, STRAYED_ID, INK_MAIN, F_CB]
    proxy_channels = [CHANNEL_ID, STRAYED_ID, INK_MAIN, F_SSP]




    await client.wait_until_ready()
    count = 21
    total_users = all_users(client)
    print('starting loop....')
    while not client.is_closed:

        if ACTIVE:
            try:


                print('holy MOLY!!!', str((time.time() - START) // 60))
                await asyncio.sleep(40)

                await Build_update(County_Bluff_youtube, bluff_channels, 'youtube', 0xffaa2b).send_update()
                await Build_update(Stopswitch_Proxy_g_plus, proxy_channels, 'google_plus', 0x383bd1).send_update()
                await Build_update(Stopswitch_Proxy_youtube, proxy_channels, 'youtube', 0x383bd1).send_update()
                print('Got SSP/CB')



                # #await Build_update(yoda, arfin_channels, 'stream').send_update()
                # #await Build_update(yoda, arfin_channels, 'youtube').send_update()
                #

                #
                #
                # await Build_update(sim_9, sim_channels, 'youtube').send_update()
                # #await Build_update(sim_9, sim_channels, 'stream').send_update()

                #await Build_update(and_13_youtube, and_13_channels, 'youtube').send_update()

                #await Build_update(echo_g_plus, echo_channels, 'google_plus').send_update()
                #await Build_update(echo_youtube, echo_channels, 'youtube').send_update()
                #await Build_update(echo_youtube, echo_channels, 'stream').send_update()


                #await Build_update(nest_youtube, nest_channels, 'youtube').send_update()

                await asyncio.sleep(40)

                if count >= 3:


                    print('Looking for updates')
                    await Build_update(Stopswitch_Proxy_youtube,proxy_channels, 'stream', 0x383bd1).send_update()
                    await Build_update(County_Bluff_youtube, bluff_channels, 'stream', 0xffaa2b).send_update()
                    #await Build_update(all_twitter, twitter_channels, 'twitter', 0x139694).send_update()

                    update_object = Find_update('info.txt')
                    await update_object.send_all_updates()


                    try:
                        if MUTE:
                            await random_presence(client, words = total_users)
                        else:
                            await client.change_presence(game= None, status= discord.Status.invisible, afk=False)
                    except:
                        print('failed to change presence')

                    # file_interact = read_write.Interact('info.txt')
                    # updates = file_interact.read_discord_update()
                    #
                    #
                    # for key in updates['google_plus'].keys():
                    #     print(key)
                    #     await Build_update(key, updates['google_plus'][key],
                    #                 'google_plus').send_update()
                    #
                    #
                    # for key in updates['youtube'].keys():
                    #     print(key)
                    #     await Build_update(key, updates['youtube'][key],
                    #                 'youtube').send_update()
                    #
                    #
                    # for key in updates['twitter'].keys():
                    #     print(key)
                    #     await Build_update(key, updates['twitter'][key],
                    #                 'twitter').send_update()





                    count = 0

                    print('obtained twitter')

                count += 1


            except TestError:
                print('a terrible, terrible thing')
                traceback.print_exc()

        else:
            print('lazy')
            await asyncio.sleep(30)






################### classes #######################

class Cade_skyrim:
    def __init__(self):
        self.playing = False


    def get_choices(self, message):
        choices = re.findall(r'\((.+?)\)', message.content)[0].strip().split('OR')
        choice = random.choice(choices)


    def play(self, message):
        pass




class Echo:
    def __init__(self, message, content):
        self.message = message
        self.content = content

    async def mentioned_channels(self):
        Fail = False
        failed = []
        channels =  self.message.channel_mentions

        for channel in channels:
            self.content = self.content.replace(channel.mention, '')

        for channel in channels:
            try:
                await client.send_message(channel, self.content)
            except:
                traceback.print_exc()
                Fail = True
                failed.append(channel.mention)

            if Fail:
                await client.send_message(self.message.channel, 'failed for: ' + str(failed))






class Replies:
    def __init__(self, content, message, server_id = None):
        '''Replies for each server are a list of replies
        for a given trigger phrase.
        '''
        self.content = content
        self.message = message
        self.server_id = server_id
        if server_id == None:
            self.server_id = str(message.server.id)
        self.channel = message.channel

        self.file = read_write.Interact_json('info_json.txt')
        self.valid = False



    def check(self, key = None):
        try:
            replies = self.file.return_replies()[self.server_id]
            self.valid = True
            return 'valid'
        except KeyError:
            return 'No replies set in your server. Use r$reply help to find out how to add replies to trigger phrases'



    async def add_reply(self):
        try:
            triggers = re.findall(r'<(.+?)>', self.content)
            replies = re.findall(r"\[(.+?)\]", self.content)

            if len(triggers) == 0 or len(replies) == 0:
                await client.send_message(self.channel, 'Nothing was added! Use "r$reply help" to see what the propper syntax is')

            for trigger in triggers:
                self.file.mutate_replies('edit', self.server_id, trigger, replies)

            self.file.save()

            await client.send_message(self.channel, 'Added successfully')

        except:
            traceback.print_exc()
            await client.send_message(self.channel, 'An error occured. Use "r$reply help" or "r$help" for more assistance')


    async def remove_trigger(self):
        check_result = self.check()
        if self.valid:
            try:
                self.file.mutate_replies('delete', self.server_id, self.content, '')
                self.file.save()
                await client.send_message(self.channel, 'Deleted successfully')
            except KeyError:
                await client.send_message(self.channel, self.content + ' is not a trigger')

        else:
            await client.send_message(self.channel, check_result)



    async def view_replies(self):
        check_result = self.check()
        if self.valid:
            server_replies = self.file.return_replies()[self.server_id]
            result = []

            for key in server_replies:
                result.append((key, server_replies[key]))

            embed = format_embed('Replies in this server', result, fields = True)
            await client.send_message(self.channel, embed = embed)


        else:
            await client.send_message(self.channel, check_result)



    def return_default_reply(self):
        try:
            print('looking for reply')
            replies = self.file.return_replies()['default']

            for trigger in list(sorted((key for key in replies.keys()), key = (lambda x: len(x)), reverse = True)): # sorts keys from largest to smallest. for matching.
                #print(trigger, self.content)
                if trigger.lower().strip() in self.content.lower().strip() and trigger != 'else_reply':
                    return random.choice(replies[trigger])

            return random.choice(replies['else_reply']) # else_reply is the replies for when no trigger phrases were matched



        except KeyError:
            pass 



    def return_reply(self):
        '''Chooses a random reply from the list of
        replies from a given trigger phrase. Else will reply
        a random else_reply. If no else_replies, returns nothing
        '''
        try:
            print('looking for reply')
            replies = self.file.return_replies()[self.server_id]

            for trigger in list(sorted((key for key in replies.keys()), key = (lambda x: len(x)), reverse = True)): # sorts keys from largest to smallest. for matching.
                #print(trigger, self.content)
                if trigger.lower().strip() in self.content.lower().strip() and trigger != 'else_reply':
                    return random.choice(replies[trigger])

            return random.choice(replies['else_reply']) # else_reply is the replies for when no trigger phrases were matched



        except KeyError:
            return self.return_default_reply()

    async def send_reply(self):
        self.check()
        reply = self.return_reply().replace('{}', self.message.author.name)
        if reply != None:
            print('replying')
            await client.send_message(self.channel, reply)

        elif not self.valid:
            await client.send_message(self.channel, embed = format_embed(reply, 'use r$help for commands'))








class Tweet:
    def __init__(self, message, prefix, tag = ''):
        self.message = message
        self.content = message.content.replace(prefix, '').rstrip().strip()
        self.tweet = '{} {} -{}'.format(tag, self.content, str(message.author))
        self.success = format_embed('Sent!', [self.tweet], author = message.author)
        self.failed = format_embed('Failed to send Tweet', [self.tweet], author = message.author)

    async def send(self):
        try:
            if len(self.tweet) < 280:
                twitter_interact.api.update_status(self.tweet)
                await client.send_message(self.message.channel, embed = self.success)
            else:
                await client.send_message(self.message.channel, 'Tweet too long!')
        except:
            await client.send_message(self.message.channel, embed = self.failed)





class Binding:
    def __init__(self, channel_id, known_channel):
        self.file = read_write.Interact('info.txt')
        self.channel_id = channel_id

        print('channel', channel_id)

        if channel_id.rstrip().strip() == '':
            self.channel_id = known_channel.id

        self.channel = client.get_channel(self.channel_id)
        if self.channel == None:
            self.channel_id = known_channel.id
            self.channel = known_channel

        self.channel_valid = False
        # print(self.channel_id)
        # print(self.channel)

        self.known_channel = known_channel # to talk to the person setting up

    async def get_server_updates(self):
        '''gets updates set within server'''
        result_dict = defaultdict(list)
        updates = self.file.read_discord_update()
        result = []
        for some_medium in updates.keys():
            for some_id in updates[some_medium].keys():
                for channel_id in updates[some_medium][some_id]:
                    channel = client.get_channel(channel_id)
                    if channel == None: # cleans up the file
                        pass
                        #self.file.mutate_discord_update('delete', some_id, some_medium, channel_id)
                        #self.file.save()
                    else:
                        if channel.server.id == self.known_channel.server.id:
                            result_dict[some_medium].append(some_id + ' - ' + channel.name)


        for medium, ids in result_dict.items():
            result.append((medium, ids))

        if len(result) == 0:
            result = ['Nothing here kiddo']

        print(result)

        embed = format_embed('Updates in server', result, fields = True)

        await client.send_message(self.known_channel, embed = embed)



    async def check(self, purpose = 'something'):
        try:
            server_channels = []
            for channel in self.known_channel.server.channels:
                server_channels.append((channel.id))

            if self.channel_id not in server_channels:
                raise ChannelError

            cool_beans = 'Successful connection for ' + purpose

            await client.send_message(self.channel, cool_beans)
            self.channel_valid = True

        except:
            bad_beans = 'failed to connect to {} for {}'.format(self.channel.name, purpose)
            await client.send_message(self.known_channel, bad_beans)


    async def update_check(self, account_id, medium):
        try:
            result = await Build_update(account_id, [None], medium).send_update(Post = False) # Keep channels as None
            if not result:
                raise ValueError
            return result

        except:
            bad_beans = 'Invalid: {} for {}'.format(account_id, medium)
            await client.send_message(self.known_channel, bad_beans)
            return False




    async def set_member_join(self):
        await self.check(purpose = 'member entrance')

        if self.channel_valid:
            self.file.mutate_discord_event('edit', 'member_join',
                str(self.known_channel.server.id), str(self.channel_id))

            self.file.save()


    async def set_member_remove(self):
        await self.check(purpose = 'member left')

        if self.channel_valid:
            self.file.mutate_discord_event('edit', 'member_remove',
                str(self.known_channel.server.id), str(self.channel_id))

            self.file.save()


    async def set_member_update(self):
        await self.check(purpose = 'profile updates')

        if self.channel_valid:
            self.file.mutate_discord_event('edit', 'member_update',
                str(self.known_channel.server.id), str(self.channel_id))

            self.file.save()



    async def set_message_edit(self):
        await self.check(purpose = 'message edits')

        if self.channel_valid:
            self.file.mutate_discord_event('edit', 'message_edit',
                str(self.known_channel.server.id), str(self.channel_id))

            self.file.save()



    async def set_message_delete(self):
        await self.check(purpose = 'deleted messages')

        if self.channel_valid:
            self.file.mutate_discord_event('edit', 'message_delete',
                str(self.known_channel.server.id), str(self.channel_id))

            self.file.save()


    async def stop_log_event(self, event):
        try:
            self.file.mutate_discord_event('delete', event,
                str(self.known_channel.server.id), str(self.channel_id))

            self.file.save()

            await client.send_message(self.channel, 'Logging successfully terminated')

        except KeyError:
            await client.send_message(self.known_channel,
                'Bot was never logging that event in this server.')

        except:
            await client.send_message(self.known_channel,
                'Failed.')


    async def set_discord_update(self, account_id, medium):
        isValid = await self.update_check(account_id, medium)
        await asyncio.sleep(5)
        try:
            if isValid:
                await self.check(purpose = 'Updates for {} in {}'.format(account_id, medium))

            if self.channel_valid:
                self.file.mutate_discord_update('edit', account_id, medium, self.channel_id)
                self.file.save()

        except:
            await client.send_message(self.known_channel, 'Failed to apply updates. May be invalid medium or missing info')


    async def stop_discord_update(self, account_id = None, medium = None):
        try:
            Found = False
            if account_id != None and medium != None:
                self.file.mutate_discord_update('delete', account_id,
                    medium, self.channel_id)

                update = account_id

                Found = True


            elif account_id !=  None:
                updates = self.file.read_discord_update()
                for some_medium in updates.keys():
                    if (account_id in updates[some_medium].keys()) and (self.channel_id in updates[some_medium][account_id]):
                        self.file.mutate_discord_update('delete', account_id, some_medium, self.channel_id)

                        Found = True
                update = account_id



            elif medium != None:
                updates = self.file.read_discord_update()
                for some_id in updates[medium].keys():
                    if self.channel_id in updates[medium][some_id]:
                        self.file.mutate_discord_update('delete', some_id, medium, self.channel_id)
                        Found = True

                update = medium

            else:
                updates = self.file.read_discord_update()
                for some_medium in updates.keys():
                    for some_id in updates[some_medium].keys():
                        if self.channel_id in updates[some_medium][some_id]:
                            self.file.mutate_discord_update('delete', some_id, some_medium, self.channel_id)
                            Found = True

            if not Found:
                raise KeyError

                update = 'all'

            self.file.save()

            await client.send_message(self.channel, 'Updates for {} successfully terminated'.format(update))

        except KeyError:
            await client.send_message(self.known_channel,
                'Bot was never sending updates for that in the channel. Make sure the ID or medium is correct')

        except ValueError:
            await client.send_message(self.known_channel,
                'Bot was never sending updates for that in the channel. Make sure the ID or medium is correct')


        except:
            await client.send_message(self.known_channel,
                'Failed.')





class Find_update:
    def __init__(self, file_name):
        self.file_interact = read_write.Interact(file_name)
        self.updates = self.file_interact.read_discord_update()

    def google_plus_updates(self):
        return self.updates['google_plus']

    def youtube_updates(self):
        return self.updates['youtube']

    def twitter_updates(self):
        return self.updates['twitter']


    async def send_all_updates(self):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(executor, send_crap, self.updates)
        if len(result) > 0:
            for item in result:
                try:
                    await client.send_message(item[0], embed = item[1])
                    await asyncio.sleep(1)
                except:
                    traceback.print_exc()
                    print('invalid', str(item[1].to_dict()))


def send_crap(updates):
        everything = []
        info = []


        for key in updates['google_plus'].keys():
            print('google_plus', key)
            info.append((key, updates['google_plus'][key],
                        'google_plus'))


        for key in updates['youtube']:
            print('youtube', key)
            info.append((key, updates['youtube'][key],
                        'youtube'))


        for key in updates['twitter']:
            info.append((key, updates['twitter'][key],
                        'twitter'))

        for key in updates['tumblr']:
            print('tumblr', key)
            info.append((key, updates['tumblr'][key],
                        'tumblr'))

        for item in info:
            try:
                to_send = Build_update(item[0], item[1], item[2]).collect_update()
                if to_send != None and len(to_send) > 0:
                    everything.extend(to_send)
            except:
                print('aggregating sending info failed for an item')
                traceback.print_exc()


        return everything[::-1] #to put in back in chronological order







class Build_update:
    def __init__(self, user_id: str, channels: list, medium, color = 0x00ff00, query = None):
        self.userid = user_id
        self.channels = channels
        self.medium = medium.strip() # idk some bug
        self.query = query # for additionaly query information for API
        self.color = color

    ########## lemme get some of that mf jason ###########

    def get_google_plus_json(self):
        '''get that google+ shit'''
        url = google_api_interact.build_google_url(int(self.userid))
        return google_api_interact.get_json(url)


    def get_youtube_json(self):
        ''' oh yeah bby I want some JSON vids ;) '''
        url = google_api_interact.build_youtube_url(self.userid)
        return google_api_interact.get_json(url)

    def get_sheets_json(self):
        url = google_api_interact.build_sheets_url(self.userid, self.query)
        return google_api_interact.get_json(url)


    def get_stream_json(self):
        url = google_api_interact.build_stream_url(self.userid)
        return google_api_interact.get_json(url)


    def get_twitter_statuses(self):

        timeline = twitter_interact.Status_collector(self.userid)

        num_id = timeline.return_id()


        try:

            if self.userid != num_id:

                file = read_write.Interact('info.txt')
                file.rewrite_twitter_id(self.userid, num_id)
                file.save()
                print('changed', self.userid, num_id)
        except:
            pass
        statuses = timeline.return_statuses()
        return statuses

    ########### process & send ##############

    def processing(self):
        '''returns processed json object'''
        if self.medium == 'stream':
            return process_json.Stream_post(self.get_stream_json())

        elif self.medium == 'sheets':
            return process_json.Form_update(self.get_sheets_json())

        elif self.medium == 'google_plus':
            return process_json.Google_post(self.get_google_plus_json())

        elif self.medium == 'youtube':
            return process_json.Youtube_post(self.get_youtube_json())

        elif self.medium == 'twitter':
            return process_json.Twitter_updates(self.get_twitter_statuses())

        elif self.medium == 'tumblr':
            return process_json.Tumblr_updates(self.userid)


        else:
            print('invalid medium')
            print(self.medium)
            print(self.userid)


    def collect_update(self, Post = True):
        '''returns list of tuples
        for sending updates. This information
        gets fed elsewhere.
        '''
        try:
            global MUTE


            processed_object = self.processing()
            result = []
            #print(processed_object.get())
            for post in processed_object.get():
                new_post = processed_object.new_post(post)

                if len(new_post) > 0:
                    processed_object.record_post(post)
                    if MUTE and Post:

                        for channel in self.channels:
                            try:
                                channel_good = False
                                try:
                                    valid_channel = client.get_channel(channel)
                                    channel_good = True
                                except:
                                    print('bad channel', channel)

                                if channel_good:

                                    footer = processed_object.account.platform + ' '

                                    embed = format_embed(None, new_post, author = processed_object.account,
                                                        fields = True, footer = footer,
                                                        inline = False)

                                    if processed_object.account.thumbnail != None:
                                        embed.set_image(url = processed_object.account.thumbnail)

                                    result.append((valid_channel, embed))
                            except:
                                print('failed for', str(channel), self.medium)
                                traceback.print_exc()

            return result

        except:
            traceback.print_exc()
            print('update', self.medium, 'for', self.userid, 'failed')

    async def send_update(self, Post = True):
        '''sends updates. Not commonly used
        Only used for Binding checks and priority
        accounts. Basically out-of-date due to
        me realizing how async works
        '''
        try:
            global MUTE


            processed_object = self.processing()
            #print(processed_object.get())
            for post in processed_object.get():
                new_post = processed_object.new_post(post)

                (new_post)

                if len(new_post) > 0:
                    processed_object.record_post(post)
                    if MUTE and Post:

                        for channel in self.channels:
                            try:
                                channel_good = False
                                try:
                                    valid_channel = client.get_channel(channel)
                                    channel_good = True
                                except:
                                    print('bad channel', channel)

                                if channel_good:
                                    if processed_object.account.url != None:
                                        if 'youtube' in processed_object.account.url:
                                            display_pfp = True
                                        else:
                                            display_pfp = False
                                    else:
                                        display_pfp = False


                                    footer = processed_object.account.platform + ' '

                                    embed = format_embed(None, new_post, author = processed_object.account,
                                                        display_pfp = display_pfp, fields = True, footer = footer)


                                    await client.send_message(valid_channel, embed=embed)
                            except:
                                print('failed for', str(channel))
                                traceback.print_exc()
                                return False


            return True

        except:
            print('update', self.medium, 'for', self.userid, 'failed')
            traceback.print_exc()
            #await asyncio.sleep(1)
            return False


    async def send_posts(self,message, Post = True):
        '''sends updates. Not commonly used
        Only used for Binding checks and priority
        accounts. Basically out-of-date due to
        me realizing how async works
        '''
        try:
            global MUTE


            processed_object = self.processing()
            #print(processed_object.get())
            for post in processed_object.get():

                if MUTE and Post:


                    try:
                        if processed_object.account.url != None:
                            if 'youtube' in processed_object.account.url:
                                display_pfp = True
                            else:
                                display_pfp = False
                        else:
                            embed = format_embed(None, new_post, author = processed_object.account,
                                            display_pfp = display_pfp, fields = True, footer = footer)


                            display_pfp = False


                        footer = processed_object.account.platform + ' '


                        await client.send_message(message.channel, embed=embed)
                    except:
                        traceback.print_exc()
                        return False


            return True

        except:
            print('update', self.medium, 'for', self.userid, 'failed')
            traceback.print_exc()
            #await asyncio.sleep(1)
            return False

    ###### fun #######

    def update_greet(self):
        greets = ['Heyo, check it in ', 'Oh snapple apple look at ',
                    'OMG OMG check this out ---> ',
                    "It's about time we got something new in ",
                    'Wow. What a surprise... New post in ',
                    'OOOOOOOHHH YEAAAHHH LOOK AT ',
                    'YEET update in ', 'Check it out bois, we got a update in ']

        return random.choice(greets)











print('about to run')
client.run('token')
