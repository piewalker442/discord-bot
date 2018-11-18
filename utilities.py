import discord
import random
import process_json
import time
import datetime
import requests
import read_write
import asyncio
import traceback


BOT_ID = '428591194185138178'

WATCH_THESE_SERVERS = {}


#### utility classes ####

class TestError(Exception):
    pass

class Command:
    def __init__(self, prefix, content, embed):
        self.prefix = 'r$' + prefix
        pass




class Custom_search:
    def __init__(self, message):
        self.message = message
        self.server_id = message.server.id
        self.file = read_write.Interact_json('info_json.txt')



    def check_engine_exist(self, engine_name):
        try:
            self.engine_id = self.file.return_search_engines()[str(self.server_id)][engine_name]
            return True
        except KeyError:
            return False


    def return_engine_id(self, engine_name):
        return self.file.return_search_engines()[str(self.server_id)][engine_name]


    def check_engine_valid(self, engine_id):
        try:
            specific_search(engine_id, 'test')
            return True
        except:
            return False


    def get_engines(self):
        try:
            result = ["Name ID"]
            engines = self.file.return_search_engines()[str(self.server_id)]
            for engine_name in engines:
                result.append("{} {}".format(engine_name, engines[engine_name]))

            return format_embed("Engines in {}".format(self.message.server.name), result)

        except KeyError:
            return format_embed("No search engines in this server!", ['Use "r$engine help" to find out how to add a search engine'])



    def execute_search(self, command):
        try:
            engine_name = command.split()[0]
            query = clean_command(command)

            if self.check_engine_exist(engine_name):
                return specific_search(self.engine_id, query, name = engine_name)

            else:
                return format_embed('Engine {} does not exist'.format(engine_name), ['Use "r$engine help" to find out how to set engines or view existing engines'])

        except:
            traceback.print_exc()
            return format_embed('Oof', ['Sorry boss, an error occured... Maybe the search engine ID is invalid?'])


    def add_engine(self, command):
        try:
            engine_name = command.split()[0]
            engine_id = command.split()[1]

            if self.check_engine_valid(engine_id):
                self.file.mutate_search_engines('edit', self.server_id, engine_name, engine_id = engine_id)
                self.file.save()
                return format_embed('Success!', ['{} was added as a search engine. use "r$search {}" to use it'.format(command, engine_name)])

            else:
                return format_embed('Failed', ['{} is an invalid Search Engine ID. Use "r$engine help" for more info'.format(engine_id)])

        except IndexError:
            return format_embed("You're missing something...", ['Be sure that you included engine name AND engine ID'])

        except:
            traceback.print_exc()
            return format_embed('OOF', ['An error occured while adding the engine, pls try again'])


    def delete_engine(self, engine_name):
        try:
            self.file.mutate_search_engines('delete', self.server_id, engine_name)
            self.file.save()
            return format_embed('Custom Search Engine deleted!', ['{} was successfully deleted'.format(engine_name)])

        except read_write.ServerNotFound:
            return format_embed('No Custom Search Engines in your server!', ['Find out how to add some by using "r$engine help"'])

        except read_write.ItemNotFound:
            return format_embed('{} Search Engine not found'.format(engine_name), ['use "r$engines" to see the Custom Search Engines in your server'])

        except:
            traceback.print_exc()
            return format_embed('OOF', ['An error occured, nothing was deleted'])




class Tag:
    def __init__(self, name = None, content = None, attachments = []):
        self.name = name
        self.content = content
        if content == '':
            self.content = None

        self.attachments = attachments

        if type(content) is dict:
            self.name = content['name']
            self.content = content['content']
            self.attachments = content['attachments']


        if (self.content == None and self.attachments == []) or self.name == None:
            raise ValueError

    def preview(self):
        result = ''
        if self.content != None:
            if len(self.content) > 25:
                result += self.content[:25] + '...'
            else:
                result += self.content

        elif len(self.attachments) > 0:
            result += ' Has an attachment'

        return result


    def to_dict(self):
        '''To be recorded as JSON'''
        result = {
        'name': self.name,
        'content': self.content,
        'attachments': self.attachments
        }
        return result




class Tags:
    def __init__(self, message):
        self.message = message
        self.server_id = message.server.id
        self.file = read_write.Interact_json('info_json.txt')



    def check_tag_exist(self, tag_name):
        if tag_name in self.file.return_tags()[str(self.server_id)].keys():
            self.tag_dict = self.file.return_tags()[str(self.server_id)][tag_name]
            self.tag = Tag(content = self.tag_dict)
            return True

        else:
            for name in self.file.return_tags()[str(self.server_id)].keys():
                if name.lower() in tag_name.lower():
                    self.tag_dict = self.file.return_tags()[str(self.server_id)][name]
                    self.tag = Tag(content = self.tag_dict)
                    return True

            if len(tag_name) < 3:
                return False

            for name in self.file.return_tags()[str(self.server_id)].keys():
                if tag_name.lower() in name.lower():
                    self.tag_dict = self.file.return_tags()[str(self.server_id)][name]
                    self.tag = Tag(content = self.tag_dict)
                    return True

            return False



    def return_tag(self, tag_name):
        return self.file.return_tags()[str(self.server_id)][tag_name]



    def get_tags(self):
        try:
            result = []
            tags = self.file.return_tags()[str(self.server_id)]
            for tag_name in tags:
                result.append("{} - {}".format(tag_name, Tag(content=tags[tag_name]).preview()))

            return format_embed("Tags in in {}".format(self.message.server.name), result)

        except KeyError:
            return format_embed("No search tags in this server!", ['Use "r$tag help" to find out how to add a tag'])



    def get_tag(self, tag_name):
        try:

            if self.check_tag_exist(tag_name):
                return self.tag
            else:
                return format_embed('Tag {} does not exist'.format(tag_name), ['Use "r$tag help" to find out how to create tags or view existing tags'])

        except:
            traceback.print_exc()
            return format_embed('Oof', ['Sorry boss, an error occured...'])


    def add_tag(self, command):
        try:
            tag_name = command.split()[0]
            content = clean_command(command)

            file_urls = []
            for attachment in self.message.attachments:
                file_urls.append(attachment['url'])

            tag = Tag(name = tag_name, content = content, attachments = file_urls)

            self.file.mutate_tags('edit', self.server_id, tag_name, value = tag.to_dict())
            self.file.save()

            return format_embed('Success!', ['{} tag was added. use "r$tag {}" to use it'.format(tag_name, tag_name)])


        except ValueError:
            return format_embed("You're missing something...", ['Be sure that you included some text (link, words, whatever), or an attachment. If both are missing then, why add the tag lol...'])

        except:
            traceback.print_exc()
            return format_embed('OOpsie - An error occured', ['Maybe your tag was too long or something was funky. Maybe change something and try again? Use "r$tag help" for more info'])


    def delete_tag(self, tag_name):
        try:
            self.file.mutate_tags('delete', self.server_id, tag_name)
            self.file.save()
            return format_embed('Tag deleted!', ['{} was successfully deleted'.format(tag_name)])

        except read_write.ServerNotFound:
            return format_embed('No tags in your server!', ['Find out how to add some by using "r$tag help"'])

        except read_write.ItemNotFound:
            return format_embed('{} tag not found'.format(tag_name), ['use "r$all tags" to see the tags in your server'])

        except:
            traceback.print_exc()
            return format_embed('OOF', ['An error occured, nothing was deleted'])










####### utility functions ######

def clean_command(content:str, words = 1):
    content = content.rstrip().strip().split()[words:]
    result = ''
    for word in content:
        result += word + ' '

    return result.strip()



async def log_message_image(message):
    pass

def retrieve_message_image(message):
    return "no attachments"




def check_attatchments(attachments):
    '''Checks for attachments'''
    try:
        return attachments[0]['url']
    except:
        return ''



def server_report_message(message):
    info_dict = {'Author_id': message.author.id,
                'Channel ': message.channel.mention}



    if check_attatchments(message.attachments) != '':
        attachment_url = check_attatchments(message.attachments)
        info_dict.update({'attachment': attachment_url})

    if message.embeds != None and message.embeds != '' and message.embeds != []:
        info_dict.update({'embed': message.embeds})

    result = list(sorted('{}: {}'.format(key, value) for key, value in info_dict.items()))

    return result



async def server_deleted_message(message):
    info = server_report_message(message)


    if message.content != '':
        info.append(('content', message.content))
    recover = retrieve_message_image(message)
    if recover.lower() != 'no attachments':
        info.append('recovered attachment: ' + recover)

    return format_embed('Deleted message', info, author = message.author,
            color = message.author.color, fields = True)


async def server_edited_message(before, after):
    result = server_report_message(before)

    if before.content != '':
        result.append(('Before', before.content))

    if after.content != '':
        result.append(('After', after.content))

    return format_embed('Edited Message', result, author = after.author,
                color = after.author.color, fields = True)



async def server_member_update(member_before, member_after, action ='Something Changed'):
    before = user_info(member_before)
    after = user_info(member_after)

    result = [('Before', before), ('After', after)]

    embed = format_embed(action, result, fields = True, author = member_after, display_pfp = True)

    embed.set_thumbnail(url = member_before.avatar_url)

    return embed


async def whois(member_name, message):
    if len(message.mentions) > 0:
        member = message.mentions[0]
    else:
        member = message.server.get_member_named(member_name)
    if member == None:
        embed = format_embed('OOf', ['Member not found'])
    else:
        info = user_info(member, fields = True)
        footer = 'Worried about security? DM creator <@353603600443768835> for more info. '
        embed = format_embed('User info', info, fields =  True, footer = footer,
                author = member, display_pfp = True)
    return embed

async def avatar_big(member_name, message):
    if len(message.mentions) > 0:
        member = message.mentions[0]
    else:
        member = message.server.get_member_named(member_name)
    member = message.server.get_member_named(member_name)
    if member == None:
        embed = format_embed('OOf', ['Member not found'])
    else:
        embed = format_embed('Avatar', ['guapo ikaw~'], author = member,
                        display_pfp = True)

    return embed






def user_info(member, fields = False):
    result = []
    role_names =  list(role.name for role in member.roles)
    if '@everyone' in role_names:
        role_names.remove('@everyone')

    if len(role_names) > 30:
        role_names = role_names[:30]
        role_names.append('Too many roles, {} left out of {}'.format(str(len(roles)-30), str(len(roles))))


    if fields:
        result.append(('ID', str(member.id)))
        result.append(("User Created", member.created_at.ctime()))
        result.append(("Joined", member.joined_at.ctime()))
        result.append(('Status', member.status))
        if len(role_names) > 0:
            result.append(('Roles', role_names)) # <-- may have to change to str()

        if member.nick != None:
            result.append(('Nickname', member.nick))

    else:
        result.append('ID:' +str(member.id))
        result.append("User Created: " + member.created_at.ctime())
        result.append("Joined: " + member.joined_at.ctime())
        if len(role_names) > 0:
            result.append('Roles: ' + str(role_names))

        if member.nick != None:
            result.append('Nickname: ' + member.nick)

    return result



async def welcome(member):
    greets = ["I've heard lots about you... welcome", "Late to the party as usual",
    "...oh you survived. Welcome to the server.", "Welcome " + member.name,
    "The coolest kid on the block has joined us", "Hi", "hi", "Bonjour",
    "Hallo. Ich verstehe nur Bahnhof.",
    "Hallo. Mein Englisch ist unter aller Sau.", "Hallo. " + member.name + " ist mir Wurst.",
    "hey"]

    greet = random.choice(greets)
    info = ("User Created at " + member.created_at.ctime())
    joined = ("Joined " + member.joined_at.ctime())

    embed = format_embed(greet, [(joined, info)], author = member,
                    fields = True, color = member.color)

    return embed



async def bye(member, Banned = False):
    if Banned:
        greet = str(member) + ' Banned'
    else:
        greets = ["Bye " + member.name + ". Alles hat ein Ende, nur die Wurst hat zwei.",
        "buh-bye", "See you later alligator", "Afterwhile crocodile", "Bye. Auf Wiedersehen",
        "Peace out", "Peace out girl scout", "Bye", "I won't miss you~", "Bye~", "bye :(",
        "Deceased.", "A moment of silence", "bye", "F", "f", "Sad", "sad day", "sad boi",
        "F"]

        greet = random.choice(greets)
    info = ("User Created at " + member.created_at.ctime())
    left = "Left " + datetime.datetime.utcfromtimestamp(time.time()).ctime()

    footer = 'ID: {} |'.format(str(member.id))

    embed = format_embed(greet, [(left, info)], author = member,
                    fields = True, footer = footer, color = member.color)

    return embed




def specific_search(s_id: str, query:str, name = ''):
    processed = process_json.Specific_search(s_id, query)


    title = '{} {} results for {}{}'.format(name, processed.total,
                query[:19], processed.corrected)

    embed = format_embed(title, processed.format_results(),
                        fields = True)

    return embed



async def contextual_search(query:str):
    processed = process_json.Contextual_search(query)

    title = '{} results for {}{}'.format(processed.total,
                query, processed.corrected)

    embed = format_embed(title, processed.format_results()[:15],
                        fields = True, footer = 'via Contextual Search | ')

    return embed


def all_users(client):
    count = 0
    for server in client.servers:
        count += int(server.member_count)
    return str(count)


async def random_presence(client, words = ''):
    people =[
    'People', 'users', 'ducks', 'potatos', 'tomatos', '...?', ' wat?',
    'Yeets', 'haters', 'lovers', 'dogs', 'cats', 'kids', 'children',
    'trolls', 'whales', 'narwhals', 'goats', 'GOATS', 'poops', 'youngsters',
    'whipper snappers', 'reasons to live', 'reasons to die', 'deaths', 'births',
    'dollars', 'bots', 'who love me', 'who vote for me', 'games', 'nates']

    s = '{} {}'.format(words, random.choice(people))
    await client.change_presence(game= discord.Game(name = s, type = 3))


def hastebin(content, message):
    for file in message.attachments:
        content += ' ' + file['url']
    return process_json.Hastebin(content)



def format_embed(message_title, formatted_message: list, color = None, author = None, display_pfp = False,
                    fields = False, footer = '', inline = True, thumbnail = False):
    '''From a list of formatted messages, return embed'''

    a_message = ''

    formatted_message = list_len_check(formatted_message)


    thumbnail = None

    if color == None:
        #color = 0x000000 # to default
        color = random_color()


    if fields:
        '''expects list of tuples'''
        amount = 0
        chars = 0
        desc = 0



        maybe_description = ''
        description = None
        fields = []
        for line in formatted_message:

            if amount < 25 and chars < 5000 and desc < 2000:
                amount += 1
                if type(line) is tuple:
                    if type(line[1]) is list:
                        text = ''
                        for item in line[1]:
                            text += item +'\n'
                            chars += 7 + len(item)
                        fields.append((line[0], text, inline))
                    else:
                        fields.append((line[0], line[1], inline))
                else:
                    desc += len(line)
                    chars += len(line) + 2
                    maybe_description += line +'\n'

            else:
                maybe_description += process_json.Hastebin(str(formatted_message))
                break

        if maybe_description != '':
            description = maybe_description

        embed = discord.Embed(title = message_title, description = description, color=color)

        for item in fields:
            embed.add_field(name = item[0], value = item[1], inline = item[2])


    else:
        for line in formatted_message:
            a_message += line + '\n'
        embed = discord.Embed(title= message_title, description= a_message, color=color)
    #embed.set_thumbnail(url=url)

    if author != None:
        try:
            if author.avatar_url != None:
                try:
                    embed.set_author(name = str(author), url = author.url, icon_url = author.avatar_url)
                except:
                    embed.set_author(name = str(author), icon_url = author.avatar_url)

            elif author.url != None:
                embed.set_author(name = str(author), url = author.url)


            if display_pfp:
                try:
                    embed.set_image(url = author.avatar_url)
                except:
                    print('failed to set image')

        except:
            embed.set_author(name = str(author))

    footer += '{} © nananananate'.format(datetime.datetime.utcfromtimestamp(time.time()).ctime())

    embed.set_footer(text=footer)

    return embed


def format_message_log(message_title: str, formatted_message: list):
    print('------------')
    print('Content: ' + message_title)

    for line in (formatted_message):
        print(line)

    print('\n')


def list_len_check(content: list):
    '''Ensures that a given list is safely below the 2000
    char limit '''

    result = []

    total = 0
    threshold = 1900
    ommitted = 0
    for line in content:
        total += len(line)
        if total < threshold:
            result.append(line)
        else:
            ommitted += 1

    if ommitted > 0:
        result.append('__**embed over char limit, {} lines ommitted**__'.format(ommitted))

    return result


def return_None():
    return


def random_color():
    color = "%06x" % random.randint(0, 0xFFFFFF)
    return int(color, 16)



def emoticon(do_it=True):
    '''lol'''
    if do_it:
        emoticons = ['( ͡° ͜ʖ ͡°)', '（‐＾▽＾‐）', 'ヾ(＾∇＾)',
                    '≧(´▽｀)≦','°˖✧◝(⁰▿⁰)◜✧˖°', '☜(˚▽˚)☞',
                    'ヽ(･∀･)ﾉ', 'ヾ(｡･ω･｡)', '(.=^・ェ・^=)']


        return random.choice(emoticons)
    return ''


##### test functions #####


async def test_edit_message():
    message = await client.get_message(client.get_channel('425701700775706628'),'463940717010616346')
    edit = Editing_message(message)
    await edit.coloring()


def test_image():
    obj = Image_archive('https://cdn.discordapp.com/attachments/454246614144385035/471115425812447242/unknown.png')
    obj.upload()
