#brought to you by nananananate
#theoretical
from utilities import *



from sys_info import *
import discord
import asyncio
import process_json
#import google_api_interact  <---- not needed
import time
import datetime
import random
import sys
import decode
from collections import defaultdict

client = discord.Client()


START = time.time()

ACTIVE = False # determines if the bot is checking and recording updates.
MUTE = False # opposite. if True then it can talk. i messed up lol
YEET = False
WATCH = False
AUTO_KICK = False

#### keeps track of particularly unsavory actions ####
BAD_MOJO = 0
BAD_MOJO_START = time.time()
BAD_MOJOS = dict()
USER_MOJOS = defaultdict(int)

BOT_ID = '428591194185138178'
SERVER_SPAM_COUNT = defaultdict(int)
USER_SPAM_COUNT = defaultdict(int)
START_TIME = time.time()
WHITE_LIST = ['353603600443768835', '428591194185138178', '305903987570376705', '259927585922744321', '151989901171097601']


BLACK_LIST = ['402323397855412225', '443879063879417856', '443879337255763968',
            '396204113630855179', '443893245064511498', '397877485368246283',
            '151815836590538752']
SUSPICIOUS = ['171004992436699136', '426189666237284355', '194923718689030144', '426111803903180801', '444722133114028042']

IGNORE_CHANNELS = []

#madmac = 171004992436699136

#qalil / coordsix, maybe black tulip 397877485368246283

#396204113630855179 gandhi - banned
# ufo / black tulip(not?) 151815836590538752
#426189666237284355 county bluff

#194923718689030144 cicada - snerx
#426111803903180801 other cicada
# 444722133114028042 turd


DESTINATIONS = {'test': '459160915317620736', 'secure': '459160915317620736',
                'secure alert': '459766162520145938', 'dump': '459160588400984084',
                'nest': '442038925176078346', 'spam': '459160625537613826',
                'joined': '459160501843394561', 'message-deleted': '460672772012769290',
                'message-edits': '460672675338256384', 'profile-edits': '460672559667740672'}

CREATOR = '<@353603600443768835>'

test_alerts = {'test': '445875218695716865', 'secure alert': '459766162520145938',
        'backup comms': '446023203375022081'}

ALERTS = {'test': '445875218695716865', 'secure alert': '459766162520145938', 'b4': '454393077256421387'}

#431655161119768578




class TestError(Exception):
    pass


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(client.email)
    print('------')
    #await client.change_presence(game= None, status= discord.Status.invisible, afk=False)
    #await test_edit_message()




@client.event
async def on_server_join(server):
    embed = Stalk_server(str(server.id)).stalking()

    await client.send_message(client.get_channel('494222198480044043'), embed = embed)



@client.event
async def on_member_join(member):
    global AUTO_KICK
    global DESTINATIONS
    global ACTIVE


    if ACTIVE and member.server.id in WATCH_THESE_SERVERS.values():
        destination = DESTINATIONS['secure']

        joined = DESTINATIONS['joined']


        embed = await join_left(member, 'joined')
        await client.send_message(client.get_channel(joined), embed = embed)


        if AUTO_KICK:
            try:
                await client.kick(member)
                await client.send_message(client.get_channel(destination), auto_kick_report(member, 'successful'))
            except TestError:
                await client.send_message(client.get_channel(destination), auto_kick_report(member))



@client.event
async def on_member_remove(member):
    global DESTINATIONS
    global ACTIVE
    joined = DESTINATIONS['joined']

    if ACTIVE and str(member.server.id) in WATCH_THESE_SERVERS.values():
        embed = await join_left(member, 'left')
        await client.send_message(client.get_channel(joined), embed = embed)






@client.event
async def on_message_delete(message):
    global ACTIVE
    global DESTINATIONS

    if ACTIVE and str(message.server.id) in WATCH_THESE_SERVERS.values():
        try:
            embed = await report_message(message, state = 'deleted')

            await client.send_message(client.get_channel(DESTINATIONS['message-deleted']), embed = embed)
        except TestError:
            print('failed to report message delete')



@client.event
async def on_message_edit(before, after):
    global ACTIVE
    global DESTINATIONS
    global BOT_ID

    if ACTIVE and after.embeds == [] and before.author.id != BOT_ID and before.server.id in WATCH_THESE_SERVERS.values():
        try:

            embed = await report_message(before, state = 'before')
            await client.send_message(client.get_channel(DESTINATIONS['message-edits']), embed = embed)

            embed_2 = await report_message(after, state = 'after')
            await client.send_message(client.get_channel(DESTINATIONS['message-edits']), embed = embed_2)

        except TestError:
            print('failed to report message edit')



@client.event
async def on_member_update(before, after):
    global ACTIVE
    global DESTINATIONS
    global WATCH_THESE_SERVERS

    if ACTIVE and before.server.id in WATCH_THESE_SERVERS.values():

        if before.avatar != after.avatar:
            change = 'avatar change'
            await member_edit(before, after, DESTINATIONS['profile-edits'], action = change)


        elif before.nick != after.nick:
            change = 'nickname change'
            await member_edit(before, after, DESTINATIONS['profile-edits'], action = change)

        elif before.roles != after.roles:
            change = 'role change'
            await member_edit(before, after, DESTINATIONS['profile-edits'], action = change)



@client.event
async def on_message(message):
    '''Command handler'''
    global WHITE_LIST
    global BLACK_LIST
    global WATCH
    global SUSPICIOUS
    global ACTIVE
    global IGNORE_CHANNELS


    #await client.kick(client.get_server('425771582879957013').get_member('402323397855412225'))

    # print((await client.get_user_info('402323397855412225')).name)   <---- MAGIC!

    #await client.kick(client.get_server('425771582879957013').get_member('443879063879417856'))


    #await client.kick(client.get_server('425771582879957013').get_member('443879337255763968'))
    if message.channel.id in IGNORE_CHANNELS:
        return

    if message.server.id == '454572095049826318':
        return

    if message.server.id == '458158588888743938' or message.author.id in WHITE_LIST:


        if message.content.startswith('$' + SYS_PREFIX + 'sactivate'):
            '''Toggles active bool. Determines if the bot
            is checking and recording updates, as well as if all
            other commands are active. I use this to save RAM
            on my computer since this is usually running on two
            machines. Also prevents 'echo' messages if two scripts
            are running '''
            if ACTIVE:
                ACTIVE = False
                await client.send_message(message.channel, 'Security State = ' + str(ACTIVE))
            else:
                ACTIVE = True
                await client.send_message(message.channel, 'Security State = ' + str(ACTIVE))

        elif message.content.startswith('$sstate'):
            await client.send_message(message.channel, 'Security Active = ' + str(ACTIVE) + ' on ' + SYS_NAME)




    if ACTIVE:

        if message.server.id in WATCH_THESE_SERVERS.values():
            current = Watching(message)

            if WATCH:
                await current.send_watch()

            await current.spam_counter()

            try:
                await log_message_image(message)
            except TestError:
                print('failed to log image in ' + str(message.id))



        if message.content.startswith('$stalkname'):
            user_id = message.content.replace('$stalkname', '').strip()
            embed = await Stalking(user_id).embed_matched_names()
            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('$serving'):
            await client.send_message(message.channel, 'serving ' + serving() + ' users')

        elif message.content.startswith('$getchannels'):
            id = message.content.split()[1]
            server_channels(id)

        elif message.content.startswith('$stalkinvite'):
            invite_id = message.content.replace('$stalkinvite', '').strip()
            embed = await invite_info(invite_id)

            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('$invites'):
            server_id = message.content.replace('$invites', '').strip()
            embed = await server_invites(server_id)

            await client.send_message(message.channel, embed = embed)

        elif message.content.startswith('$delinvite'):
            invite_id = message.content.replace('$delinvite', '').strip()
            try:
                await delete_invte(invite_id)
                await client.send_message(message.channel, 'invite deleted')
            except:
                await client.send_message(message.channel, 'failed to delete invite')


        elif message.content.startswith('$estimateprune'):
            days = message.content.replace('$estimateprune', '').strip()
            embed = await estimate_prune(message.server, int(days))
            await client.send_message(message.channel, embed = embed)

        # elif message.content.startswith('$ping'):
        #     time = ping_time(message)
        #     await client.send_message(message.channel, 'yeet time: ' + time)




        if message.server.id == '458158588888743938' or message.author.id in WHITE_LIST:
            if message.content.startswith('$stalkid'):
                user_id = message.content.replace('$stalkid', '').strip()
                embed = await Stalking(user_id).embed_user_info()
                await client.send_message(message.channel, embed = embed)

            elif message.content.startswith('$stalkserver'):
                server_id = message.content.replace('$stalkserver','').strip()
                embed = Stalk_server(server_id).stalking()
                await client.send_message(message.channel, embed=embed)

            elif message.content.startswith('$servers'):
                await client.send_message(message.channel, all_servers())

            elif message.content.startswith('$securehelp'):
                embed = super_secure_commands()
                await client.send_message(message.channel, embed = embed)

            elif message.content.startswith('$start_help'):
                embed = startup_help()
                await client.send_message(message.channel, embed = embed)


            elif message.content.startswith('$stalk_help'):
                embed = stalk_help()
                await client.send_message(message.channel, embed = embed)


            elif message.content.startswith('$cleanhouse'):
                await clean_house(BLACK_LIST)

            elif message.content.startswith('$hackban'):
                users = message.content.replace('$hackban', '').strip().split()
                await clean_house(users)

            elif message.content.startswith('$serverban'):
                info = message.content.replace('$serverban', '').strip().split()
                await server_ban(info[0],info[1])

            elif message.content.startswith('$getmessages'):
                serverid = message.content.replace('$getmessages', '').strip()
                print('we in here')
                await get_messages(serverid)


            elif message.content.startswith('$dumpmessages'):
                info = message.content.replace('$dumpmessages', '').strip().split()
                channelid = info[0]
                dumpid = info[1]
                print('we in here')

                to_dump = Dumping(channelid, dumpid)

                await to_dump.dump_messages()

            elif message.content.startswith('$backingup'):
                info = message.content.replace('$backingup', '').strip().split()
                origin_server= info[0]
                target_server = info[1]


                backup = Backup(origin_server, target_server)

                await backup.backing_up()



            elif message.content == '_TISUELA_':
                sys.exit()


            elif message.content.startswith('$defcon'):
                command_breakdown = message.content[1:].split()
                raidmode = Raidmode(server = command_breakdown[1], defcon = command_breakdown[0])
                await raidmode.defcons()


            elif message.content == '$watch':
                '''Toggles active bool. Determines if the bot
                is checking and recording updates, as well as if all
                other commands are active. I use this to save RAM
                on my computer since this is usually running on two
                machines. Also prevents 'echo' messages if two scripts
                are running '''
                if ACTIVE:
                    WATCH = False
                    await client.send_message(message.channel, ':3 State = ' + str(WATCH))
                else:
                    WATCH = True
                    await client.send_message(message.channel, ':3 State = ' + str(WATCH))


            elif message.content.startswith('$blacklist'):
                embed = await userlist_info(BLACK_LIST)
                await client.send_message(message.channel, embed = embed)

            elif message.content.startswith('$suspicious'):
                embed = await userlist_info(SUSPICIOUS)
                await client.send_message(message.channel, embed = embed)



            elif message.content.startswith('$estimate_all_prune'):
                days = message.content.replace('$estimate_all_prune', '').strip()
                embed = await estimate_all_prune(int(days))
                await client.send_message(message.channel, embed = embed)

            elif message.content == '$batman':
                await client.change_presence(game= None, status= discord.Status.invisible, afk=False)

            elif message.content == '$obnoxious':
                await client.change_presence(game= discord.Game(name = 'death is inevitable'))












######### functons ############


def super_secure_commands():
    commands = ['| $command "INPUT (if input is needed)" - description',
                '| $start_help - shows commands for startup/shutdown of the bot',
                '| $stalk_help - returns commands for gathering user information',
                '| $servers - gives list of servers accessible by robot-nate',
                '| $cleanhouse - EMERGENCY ONLY, or else consult @nananananate, will ban users on blacklist',
                '| $watch - toggles if robot-nate is monitoring servers, default is False',
                '| $blacklist - gives users in blacklist',
                '| $estimateprune "number" - estimates number of pruned members given days',
                '| $suspicious - gives list of suspicious users',
                '| $batman - bot will appear offline',
                '| $obnoxious - bot will appear online w/ game playing status',
                '| $helpdefcon - Information on the defcon functions and commands',
                '| $hackban "ID number" - EMERGENCY ONLY, or else consult @nananananate. bans user across all servers bot has access to. Seperate multiple IDs with a space to ban more users',
                '| $serving - gives amount of users being served',
                '| $backingup "origin server id" "backup server id" – backs up entire server automatically, with channels. Takes several hours to complete',
                '| $getmessages "target server id" – Like the backingup command, except it all gets printed out together on the console, with channels as dividers',
                '| $dumpmessages "origin channel id" "target channel id" Duplicates an entire channel into another designated channel',
                '| $invites "server id" - returns all invites for that server',
                '| $delinvite "invite id" - deletes invite. duh.',
                '| $stalkinvite "invite id" - returns detailed information of that invite']

    return format_embed('Commands accessible on this server:', commands)



def startup_help():
    words = '''
If something goes wrong and the bot needs to be shut down or started back up, here's how to do itself.
| $activate - toggles the active state of the "public" script, which is everything having to do with updates and decoding.
| $mute - toggles mute state of the public script (described above). TRUE means that it CAN speak. Counterintuitive, I know.
The bot DEFAULTS to FALSE meaning that upon using $activate, the bot will NOT send any messages.
| $sactivate - toggles the active state of the security script, which is everything having to do with logging, stalking, and raid-related functions.
There is no mute command for this

The reason why I include $mute for the main script is because, sometimes, the bot needs time to update itself. Having it default to false allows the bot
to write old updates it was offline for into its logs, thus preventing spam. Now that the bot is online most of the time, it's usually safe to use $mute
immediately after $activate.

These commands are mostly used when the bot crashes. Thus, the script MUST be running in order for these commands to be used.
If no reply is sent upon using these commands, the script is not running. Depending on what machine it's running on, the time
for the script to be put back up may vary
'''
    return format_embed('Startup help', [words])


def stalk_help():
    words = '''
So here's how I normally do it:
First I search for the username, this command returns all users who's username contains that string; like nana would return nananananate.
| $stalkname 'query' - returns usernames and IDs

I copy the ID into this command:
| $stalkid 'ID' - returns user information, even if it is not in a known server.

Also here's the stuff for twitter:
| $searchtwitter - query - returns users whose name / screen name contains the query
| $stalktwitter - screen name or ID - returns detailed information on user
'''
    return format_embed('Startup help', [words])




def defcon_help():
    commands = ['There are three levels I have implemented for defcon. When this is not in use, the default is no Defcon at all.',
                'Defcon 3 is the least critical level. It will mute the bot and place it offline.',
                'Defcon 2 indicates that there may be a raid soon. In addition to Defcon 3, it will also deactivate the background loops and unnecessary commands to prevent anyone from Spamming the bot',
                'Defon 1 indicates that a raid is in progress. In addition to Defcon 3 and 2, it will also run hackbans on all blacklisted users and activate the kick-on-arrival function. Adminsitration on all servers will be notified. All important information will be dumped here.']
    return format_embed('Defcon information', commands)



def all_servers():
    'Messages all servers bot has access to'
    servers = '\n'.join('{} | {}'.format(server.name, server.id) for server in client.servers)
    return process_json.Hastebin(str(servers))

def server_channels(id: str):
    'Prints all channels bot can see to the console'
    server = client.get_server(id)

    for channel in server.channels:
        print(channel.name)




def auto_kick_report(member, state = 'unsuccessful'):
    '''To help keep track of who gets
    auto kicked. This will help get these ppl back in'''
    return 'Autokicked on join {} in server {}: {} | {}'.format(state, member.server.name, member.name, member.id)



async def join_left(member, action):
    'Builds embed for join/left users'
    title = '{} {}'.format(action, member.server.name)
    embed = await Stalking(str(member.id)).embed_user_info(title = title)
    return embed



async def member_edit(member_before, member_after, destination, action = 'Profile edit'):
    '''SENDS out message edit report (DOES NOT ONLY BUILD EMBED, ALSO SENDS.)'''
    title = '{} detected in {}; Before:'.format(action, member_before.server.name)
    embed = await Stalking(str(member_before.id), useroverride = member_before, serveroverride = [member_before.server]).embed_user_info(title = title)

    await client.send_message(client.get_channel(destination), embed = embed)

    title_2 = '{} detected in {}; After:'.format(action, member_after.server.name)
    embed_2 = await Stalking(str(member_after.id), useroverride = member_after, serveroverride = [member_after.server]).embed_user_info(title = title_2)

    await client.send_message(client.get_channel(destination), embed = embed_2)



async def userlist_info(users: list):
    '''Gives list of usernames and IDs'''
    blacked = []
    for userid in users:
        user = await client.get_user_info(userid)

        blacked.append('name: {} | id: {}'.format(user.name, str(user.id)))

    return format_embed('Users', blacked)



async def clean_house(users: 'list of IDs', announce = True):
    '''Bans all users in blacklist in all servers'''
    global DESTINATIONS
    for user in users:
        for server in client.servers:
            try:
                if str(server.id) != '424918128850370560':  #41818
                    user_obj = await client.get_user_info('353603600443768835')
                    #await client.ban(server.get_member(user))
                    await client.http.ban(user_obj, server.id, 0)
                    # await client.http.unban(user, server.id, 0)
                    print('ban success for', user_obj.name, 'on', server.name)
                    if announce:
                        await client.send_message(client.get_channel(DESTINATIONS['spam']), 'ban success for ' + user_obj.name + ' on ' + server.name)
            except:
                print('ban failed for', user_obj.name, 'on', server.name)
                if announce:
                    await client.send_message(client.get_channel(DESTINATIONS['spam']), 'ban failed for ' + user_obj.name + ' on ' + server.name)



async def server_ban(server_id, user_id):


        server = client.get_server(server_id)
        the_bot = server.get_member(client.user.id)
        print('Can Ban', the_bot.server_permissions.ban_members)
        #user = client.get_user_info(user_id)
        user = discord.Object(user_id)
        user.server = server
        await client.ban(user)
        print('ban success', str(user.name), server.name)








async def get_messages(serverid: str):
    print('getting logs')
    server = client.get_server(serverid)
    for channel in server.channels:
        print('-----------------', channel.name, '-----------------')
        print(channel.id)
        try:
            async for message in client.logs_from(channel, limit=500):
                info = Watching(message)
                info.print_message()
        except:
            print('insufficient perms')

        print('\n\n')


async def estimate_prune(server, days: int):
    result = []
    failed = []

    try:
        amount = await client.estimate_pruned_members(server = server, days = days)
        result.append('server: {} | estimate pruned: {}'.format(server.name, str(amount)))
    except:
        failed.append('could not estimate for {}'.format(server.name))

    result.extend(failed)

    return format_embed('prune estimates', result)



async def estimate_all_prune(days: int):
    result = []
    failed = []
    for server in client.servers:
        try:
            amount = await client.estimate_pruned_members(server = server, days = days)
            result.append('server: {} | estimate pruned: {}'.format(server.name, str(amount)))
        except:
            failed.append('could not estimate for {}'.format(server.name))

    result.append('')
    result.extend(failed)

    return format_embed('prune estimates', result)




def ping_time(message):
    start = message.timestamp
    print(start)
    return str(time.time() - start)




def check_message(content):
    if len(content) > 1000:
        return '#CONTENT TOO LONG# - BOT'
    return content


def serving():
    count = 0
    for member in client.get_all_members():
        count += 1
    return str(count)




async def delete_invte(invite_id: str):
    invite = await client.get_invite(invite_id)
    await client.delete_invite(invite)


async def invite_info(invite_id: str):
    Invite = None
    result_dict = dict()
    for server in client.servers:
        try:
            invites = await client.invites_from(server)

            for invite in invites:
                if str(invite.id) == invite_id:
                    Invite = invite
                    result_dict = {'uses': Invite.uses, 'max_uses': Invite.max_uses,
                    'inviter': Invite.inviter.name, 'server': Invite.server.name}
                    break

        except:
            pass


    if Invite == None:
        try:
            invite = await client.get_invite(invite_id)
            result_dict = {'inviter': Invite.inviter.name, 'server': Invite.server.name}
        except:
            return format_embed('Invite Info', ['No match or bot lacks permissions'])

    result = []

    for key,value in result_dict.items():
        result.append('{} | {}'.format(str(key), str(value)))

    return format_embed('Invite info', result)



async def server_invites(server_id: str):

    server = client.get_server(server_id)
    invites = await client.invites_from(server)

    result = []

    for invite in invites:
        result.append('{} | {} | Uses: {}'.format(str(invite.inviter.name), str(invite.code), str(invite.uses)))

    return format_embed('Invites from' + server.name, result)




def check_attatchments(attachments):
    '''Checks for attachments'''
    try:
        # print(attachments)
        return attachments[0]['url']
    except:
        return ''


async def report_message(message, state = 'Something happened'):
    info_dict = {'Author_id': message.author.id, 'server': message.server.name, 'server_id': message.server.id,
                'channel': message.channel.name}

    if message.content != '':
        info_dict.update({'content': message.content})

    if check_attatchments(message.attachments) != '':
        attachment_url = check_attatchments(message.attachments)
        info_dict.update({'attachments': attachment_url})


    if message.embeds != None and message.embeds != '' and message.embeds != []:
        info_dict.update({'embed': message.embeds})

    result = list(sorted('{}: {}'.format(key, value) for key, value in info_dict.items()))

    if state == 'deleted':
        result.append('recovered attachment: ' + retrieve_message_image(message))

    embed = format_embed('Message {}:'.format(state), result, author = message.author)


    return embed


########## classes ################

class Stalk_server:
    def __init__(self, server_id):
        self.server = client.get_server(server_id)

    def objects_to_names(self, obj_list):
        result = []
        for item in obj_list:
            result.append(item.name)

        if len(result) > 50:
            result = result[:50]


        return result

    def stalking(self):
        channels = self.server.channels
        roles = self.server.role_hierarchy

        roles = self.objects_to_names(roles)
        channels = self.objects_to_names(channels)

        result = [('Created', str(self.server.created_at)),
                ('Owner', str(self.server.owner)),
                ('Members', str(self.server.member_count)),
                ('Channels', str(channels)),
                ('Roles', str(roles))
                ]

        return format_embed(str(self.server.id), result, fields = True, author =  self.server)





class Dumping:
    def __init__(self, channelid, dumpid):
        global IGNORE_CHANNELS
        '''I use this so that when a bot command was used in another server
        and said by the bot during a channel dump or server duplication, it will ignore
        all commands said in that channel... remove this if you don't have the
        rest of my script'''
        self.channelid = channelid
        self.dumpid = dumpid

        IGNORE_CHANNELS.append(dumpid)




    def check_attatchments(self, attachments):
        '''Checks for attachments'''
        try:
            # print(attachments)
            return attachments[0]['proxy_url']
        except:
            return ''


    async def get_messages(self):
        self.messages = []
        channel = client.get_channel(self.channelid)
        self.channel_messages = []
        print('-----------------', channel.name, '-----------------')
        print(channel.id)



        try:
            async for message in client.logs_from(channel, limit=1000):


                info_dict = dict()
                if message.content != '':
                    info_dict.update({'content': message.content})

                if self.check_attatchments(message.attachments) != '':
                    info_dict.update({'attachments': self.check_attatchments(message.attachments)})

                if message.embeds != None and message.embeds != '' and message.embeds != []:
                    info_dict.update({'embed': message.embeds})

                if len(info_dict) != 0:
                    info_dict.update({'author': '__**Author: {}**__'.format(message.author)})

                self.channel_messages.append(info_dict)


        except:
            print('insufficient perms')

        self.messages.extend(self.channel_messages[::-1])



        print('\n\n')
        return self.messages


    async def dump_messages(self):


        messages = await self.get_messages()
        previous_author = ''

        for message in messages:
            attributes = ['content', 'attachments', 'embed']




            if len(message) > 1:
                if message['author'] != previous_author:
                    previous_author = message['author']
                    attributes = ['author','content', 'attachments', 'embed']

                    await client.send_message(client.get_channel(self.dumpid), '–––––––––––––––––––––––––––––')
                for attribute in attributes:
                    try:
                        try:
                            if attribute == 'embed':
                                for embed in message[attribute]:
                                    # embed_kargs = ""
                                    #
                                    # for key, value in embed.items():
                                    #     embed_kargs += ("{} = '{}',").format(key, value)

                                    #embed_kargs = embed_kargs[:-1]
                                    await client.send_message(client.get_channel(self.dumpid), str(embed))

                            else:
                                await client.send_message(client.get_channel(self.dumpid), message[attribute])

                        except KeyError:
                            pass
                    except:
                        print('failed', message[attribute])



class Backup:
    def __init__(self, origin: 'serverid', target: 'serverid'):
        self.origin = client.get_server(origin)
        self.target = client.get_server(target)


    def name_check(self, name):
        Flag = True
        while Flag:
            Flag = False
            for channel in self.target.channels:
                if name == channel.name:
                    name = '_' + name
                    Flag = True

        return name



    async def backing_up(self):
        for channel in self.origin.channels:
            name = self.name_check(channel.name)
            target_channel = await client.create_channel(self.target, name)

            to_dump = Dumping(channel.id, target_channel.id)

            await to_dump.dump_messages()



class Watching:
    def __init__(self, message):
        ''' watches servers, reports to specific channel '''

        global WHITE_LIST

        global DESTINATIONS

        global BAD_MOJO
        global BAD_MOJO_START
        global BAD_MOJOS

        self.bad_mojo = BAD_MOJO
        self.bad_mojo_start = BAD_MOJO_START
        self.bad_mojos = BAD_MOJOS

        self.message = message

        self.watch_dict = {'xtheo': '425771582879957013', 'arz': '424918128850370560',
                            'comms': '431655161119768576', 'xiris': '452319062391783425'} #server ids, consider moving this to global

        self.destination_dict = DESTINATIONS #channel ids
        self.white_list = WHITE_LIST

        self.message_info = {'author_name': message.author.name, 'author_id': message.author.id,
                        'channel_name': message.channel.name, 'channel_id': message.channel.id,
                        'server_name': message.server.name, 'server_id': message.server.id,
                        'attachments': message.attachments, 'embeds': message.embeds}


        if message.attachments == []:
            del self.message_info['attachments']

        if message.embeds == []:
            del self.message_info['embeds']


    def compile_message_info(self):
        '''returns list of message info/content to be sent'''

        result = ['']

        for key, value in self.message_info.items():
            result.append(str(key) + ':    ' + str(value))

        return list(sorted(result))


    def print_message(self):
        format_message_log(self.message.content, self.compile_message_info())

    async def send_watch(self):
        if self.message.server.id in self.watch_dict.values():
            await client.send_message(client.get_channel(self.destination_dict['dump']),
                    embed = format_embed(check_message(self.message.content), self.compile_message_info()))

        elif self.message.server.id == '451424263845445643':  # brett
            await client.send_message(client.get_channel(self.destination_dict['dump']),
                    embed = format_embed(check_message(self.message.content), self.compile_message_info()))

    async def spam_counter(self):
        '''Reports spam if reaches thresholds'''
        global USER_SPAM_COUNT
        global SERVER_SPAM_COUNT
        global START_TIME

        time_period = 60
        small_threshold = 60
        big_threshold = 120

        destination = self.destination_dict['secure alert']


        #if self.message.server.id in self.watch_dict.values():
        if str(self.message.author.id) not in self.white_list:
            USER_SPAM_COUNT[self.message.author.id] += 1
            SERVER_SPAM_COUNT[self.message.server.id] += 1

        print(SERVER_SPAM_COUNT)
        print(time.time() - START_TIME)

        if time_period <= time.time() - START_TIME:


            START_TIME = time.time()

            report = False
            defcon1 = False
            for server,count in SERVER_SPAM_COUNT.items():
                if count > big_threshold:
                    report = True
                    defcon1 = True
                    await client.send_message(client.get_channel(destination), 'spam detected (extremely likely raid) in ' + \
                                str(client.get_server(server).name))
                    break

                elif count > small_threshold:
                    report = True
                    await client.send_message(client.get_channel(destination), 'spam detected (likely raid) in ' + \
                                str(client.get_server(server).name))
                    break

            if report:
                '''report user who is spamming'''
                top_users = list(sorted(((user, count) for user, count in USER_SPAM_COUNT.items()), key = (lambda tup: tup[0]), reverse = True))
                print(top_users)
                await client.send_message(client.get_channel(destination), 'user spamming the most is this boi: ' + str(top_users[0]))

                embed = await Stalking(top_users[0][0]).embed_user_info()
                await client.send_message(client.get_channel(destination), embed = embed)


            SERVER_SPAM_COUNT = defaultdict(int)
            USER_SPAM_COUNT = defaultdict(int)

            if defcon1:
                await Raidmode(server, defcon = 'defcon1').defcons()
                defcon1 = False

    async def bad_mojo_track(member, mojo: 'key'):
        time_period = 60

        threshold = 20

        mojos = defaultdict(int)



        self.bad_mojos[member.server.id] = mojos
        self.bad_mojo += 1








class Stalking:
    def __init__(self, userid, useroverride = None, serveroverride = None):
        '''I include override options so I can target specific servers or
        user objects. It helps with audit logs.
        '''
        self.userid = userid #now can also be name
        self.useroverride = useroverride
        self.serveroverride = serveroverride #MUST BE LIST!!!!!


    async def embed_matched_names(self):
        '''For $stalkname, searches users given
        a string'''
        matches = set()
        for member in client.get_all_members():
            if self.userid.lower() in member.name.lower():
                matches.add(str(member.name + ' | ' + str(member.id)))
        if len(str(matches)) > 1600:
            matches = ['Too many results, please be more specific']

        elif len(matches) == 0:
            matches = ['No Matches']

        embed = format_embed('Results for ' + self.userid + ', format = name | id', list(matches))

        return embed



    async def aggregate_information(self):
        '''Collects user information'''
        result = []
        check_servers = client.servers

        if self.useroverride == None:
            self.user = await client.get_user_info(self.userid)
        else:
            self.user = self.useroverride

        if self.serveroverride != None:
            check_servers = self.serveroverride


        self.user_info = {'id': self.user.id, 'date_created': self.user.created_at}
        result.append(self.user_info)

        for server in check_servers:
            try:
                if len(check_servers) == 1 and self.useroverride != None:
                    ''' Assumes this is an audit log thingy, i need to do this,
                    whatever, too long to explain
                    '''
                    member = self.user
                else:
                    member  = server.get_member(self.userid)

                role_names =  list(role.name for role in member.roles)
                if '@everyone' in role_names:
                    role_names.remove('@everyone')

                server_info = {'server_name': server.name, 'id': server.id,
                                'joined': str(member.joined_at), 'roles': str(role_names),
                                'nickname': str(member.nick)}

                if server_info['nickname'] == 'None':
                    del server_info['nickname']

                if server_info['roles'] == '[]':
                    del server_info['roles']


                #if 'server roles': str(role_names) <--- wot????

                result.append(server_info)
                # 'roles': str(member.roles)
            except: # i think this is to avoid error when member = None
                pass

        return result

    async def compile_user_info(self):
        '''Compiles user info into list, set for extraction'''
        final_formatted = ['']
        info = await self.aggregate_information()
        print(info)

        if len(info) == 0:
            return ['ERROR (may have no results or invalid input)']

        for info_dict in info:
            server_formatted = []
            server = 'null'
            if 'server_name' not in info_dict.keys():
                for key in info_dict.keys():
                    final_formatted.append(str(key) + ': ' + str(info_dict[key]))
            else:
                for key in info_dict.keys():

                    if key == 'server_name':
                        server = info_dict[key]
                    else:
                        server_formatted.append(str(key) + ':  ' + str(info_dict[key]))



            #final_formatted.extend(list(sorted(server_formatted)))
                final_formatted.append((server, server_formatted))

        return final_formatted


    async def embed_user_info(self, title = None):
        global DESTINATIONS
        compiled = await self.compile_user_info()
        print(compiled)
        if title == None:
            title = 'Information on user:'
        embed = format_embed(title, compiled, author = self.user, display_pfp = True, fields = True)
        #print(compiled)

        return embed




class Raidmode:
    def __init__(self, server, defcon = 'defcon3'):

        global DESTINATIONS
        global CREATOR
        global WATCH
        global ALERTS
        global BLACK_LIST
        global SUSPICIOUS

        WATCH = True

        self.destination = DESTINATIONS['secure alert']
        self.creator = CREATOR
        self.alerts = test_alerts
        self.black_list = BLACK_LIST


        self.server = client.get_server(server)

        if defcon == 'defcon1':
            self.defcon = 1
        elif defcon == 'defcon2':
            self.defcon = 2
        else:
            self.defcon = 3

        self.alert = '$mute - muting bot for raid | Raidmode defcon {} activated {}, target server = {}'.format(self.defcon, self.creator, self.server.name)


    async def defcon_1(self):
        try:
            alert = 'RAID IN PROGRESS IN {}. Owners, administrators, please take precautions'.format(self.server.name)

            try:
                await clean_house(self.black_list, announce = False)
                await client.send_message(client.get_channel(self.destination), 'blacklisted users banned on all servers') #deactivate bot
            except:
                await client.send_message(client.get_channel(self.destination), 'failed to ban blacklisted users') #deactivate bot


            await client.send_message(client.get_channel(self.destination), '$activate - deactivating bot to focus on raid') #deactivate bot
            await client.change_presence(game= None, status= discord.Status.invisible, afk=False) #incognitoooo

            for server in self.alerts.values():
                try:
                    await client.send_message(client.get_channel(server), alert) #announce raid to other servers
                except:
                    print('alert failed in server channel', server)
        except:
            print('Defcon 1 activation failed')


    async def defcon_2(self):
        pass

    async def defcon_3(self):
        pass


    async def defcons(self):
        await client.send_message(client.get_channel(self.destination), self.alert)
        if self.defcon <= 1:
            await self.defcon_1()
        elif self.defcon == 2:
            await self.defcon_2()
        else:
            await self.defcon_3()






#client.run('piewalker442@gmail.com', 'taco442')
client.run('NDI4NTkxMTk0MTg1MTM4MTc4.DZ1ULw.13-6vutJY1w0dmvnWeXDI7cStNQ')


'''




16 Jue 2018, Saturday
[20:15]
Here above the clouds
So much done yet so little.
Maybe I'll talk about it more later.
I'll never get tired of flying






'''
