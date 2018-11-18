from collections import defaultdict
import json


class TestError(Exception):
    pass

class ServerNotFound(Exception):
    pass

class ItemNotFound(Exception):
    pass




class Read:
    def __init__(self, file_name):
        file = open(file_name, 'r')
        self.result = defaultdict(list)
        current_type = ''

        for line in file:
            line = line.rstrip()
            if line.startswith('#') or len(line) < 1:
                pass
            elif line.startswith('type'):
                current_type = line.replace('type','').strip()
            else:
                self.result[current_type].append(line)

        file.close()
        self.result = dict(self.result)

    def image_archive(self):
        info = self.result['image_archive']
        processed = dict()
        for line in info:
            deetz = line.rstrip().split()
            name = deetz[0] # which will commonly be a attachment id
            link = deetz[1]
            processed.update({name: link})

        return processed



    def to_do_list(self):
        '''reads information dictionary and
        prepares it for the to_do_list
        '''
        info = self.result['to_do_list']
        current_id = 'Undefined'
        processed = defaultdict(dict)

        for line in info:
            dp(line)
            if line.startswith('id'):
                current_id= line.replace('id', '').strip()
            else:
                to_do = ' '
                if len(line) > 2:
                    to_do = line.replace(line.split()[0], '').strip()
                processed[current_id][line.split()[0]] = to_do

        processed = dict(processed)

        for key in processed.keys():
            processed[key] = self.check_enumeration(processed[key])

        return processed


    def check_enumeration(self, d: dict):
        '''used mainly for the to-do list, to check
        that everything is numbered correctly and that
        no numbers are skipped in a numbered dict'''
        result = dict()
        for number,line in enumerate(list(sorted(((key,d[key]) for key in d.keys()), key = (lambda x: int(x[0]))))):
            result.update({str(number + 1): line[1]}) #have to do line[1] bc line is a tuple, and I only really want the value, which i put in line[1]
        return result


    def discord_event(self):
        info = self.result['discord_event']
        current_event = 'Undefined'
        processed = defaultdict(dict)

        for line in info:
            if line.startswith('event'):
                current_event = line.replace('event', '').strip()
            elif line.startswith('destination'):
                destination = line.replace('destination', '').strip().split()
                processed[current_event].update({destination[0]: destination[1]})
                # destination[0] is server, destination[1] is channel

        return dict(processed)





    def discord_update(self):
        '''reads information disctionary and
        prepares it for the functions in
        discord_interact
        '''
        info = self.result['discord_update']
        current_medium = 'Undefined'
        current_id = 'Undefined'
        processed = defaultdict(dict)
        dp("CHECKING")

        for line in info:
            dp(line)
            if line.startswith('medium'):
                current_medium = line.replace('medium', '').strip()
            elif line.startswith('id'):
                current_id = line.replace('id','').strip()
                if current_id not in processed[current_medium].keys():
                    processed[current_medium].update({current_id: []})
            elif line.startswith('channel'):
                processed[current_medium][current_id].append(line.replace('channel', '').strip())

        processed = dict(processed)

        return processed


class Interact:
    def __init__(self, file_name):
        self.file_name = file_name
        self.processed = Read(file_name)
        self.to_mutate_to_do_list = self.processed.to_do_list()
        self.to_mutate_discord_update = self.processed.discord_update()
        self.to_mutate_image_archive = self.processed.image_archive()
        self.to_mutate_discord_event = self.processed.discord_event()


    def read_discord_update(self):
        return self.processed.discord_update()

    def read_to_do_list(self):
        return self.processed.to_do_list()

    def read_image_archive(self):
        return self.processed.image_archive()

    def read_discord_event(self):
        return self.processed.discord_event()


    def mutate_discord_event(self,action,event,server,channel):
        '''server and channel are both str(id)
        '''
        result = []
        if action == 'delete':
            del self.to_mutate_discord_event[event][server]
        elif action == 'edit':
            try:
                self.to_mutate_discord_event[event][server] == channel
            except KeyError:
                self.to_mutate_discord_event[event].update({server:channel})


        for event in self.to_mutate_discord_event.keys():
            result.append('event ' + event)

            for server in self.to_mutate_discord_event[event].keys():
                result.append('destination {} {}'.format(server,
                        self.to_mutate_discord_event[event][server]))

        self.processed.result['discord_event'] = result



    def rewrite_twitter_id(self, old_id, new_id):
        result = []
        to_move_channels = self.to_mutate_discord_update['twitter'][old_id]

        if new_id in self.to_mutate_discord_update['twitter'].keys():
            self.to_mutate_discord_update['twitter'][new_id].extend(to_move_channels)

        else:
            self.to_mutate_discord_update['twitter'].update({new_id: to_move_channels})

        del self.to_mutate_discord_update['twitter'][old_id]


        for medium in self.to_mutate_discord_update.keys():
            result.append('medium ' + medium)
            for id in self.to_mutate_discord_update[medium].keys():
                result.append('id ' + id)

                for channel in set(self.to_mutate_discord_update[medium][id]): # changed to set to remove duplicates
                    if channel != None:
                        result.append('channel ' + channel)

        self.processed.result['discord_update'] = result




    def mutate_discord_update(self, action, id , medium, channel):
        result = []
        if action == 'delete':
            self.to_mutate_discord_update[medium][id].remove(channel)
        elif action == 'edit':
            if id not in self.to_mutate_discord_update[medium].keys():
                self.to_mutate_discord_update[medium].update({id: [channel]})
            else:
                self.to_mutate_discord_update[medium][id].append(channel)

        for medium in self.to_mutate_discord_update.keys():
            result.append('medium ' + medium)
            for id in self.to_mutate_discord_update[medium].keys():
                result.append('id ' + id)

                for channel in set(self.to_mutate_discord_update[medium][id]): # changed to set to remove duplicates
                    if channel != None:
                        result.append('channel ' + channel)

        self.processed.result['discord_update'] = result


    def mutate_to_do_list(self,id,number,action,content):
        result = []
        if action == 'delete':
            del self.to_mutate_to_do_list[id][number]
        elif action == 'edit':
            if id not in self.to_mutate_to_do_list.keys():
                self.to_mutate_to_do_list.update({id: {'1': content}})
            else:
                self.to_mutate_to_do_list[id][number] = content
            self.to_mutate_to_do_list[id] = (self.to_mutate_to_do_list[id])

        for key in self.to_mutate_to_do_list.keys():
            result.append('id ' + key)
            for item_number in self.to_mutate_to_do_list[key].keys():
                result.append(item_number + ' ' + self.to_mutate_to_do_list[key][item_number])

        self.processed.result['to_do_list'] = result


    def mutate_image_archive(self, name, link):
        result = []
        self.to_mutate_image_archive.update({name: link})

        for key in self.to_mutate_image_archive:
            result.append(key + ' ' + self.to_mutate_image_archive[key])

        self.processed.result['image_archive'] = result



    def mutating(self, kind: 'basically type', action, id, another_id = None, content=None, medium = None, channel = None):
        '''Honestly, I wasn't thinking when I made this.
        Some function i've forgotten about is probably using this, so I'll
        keep it here, but it's no longer being applied to newer functions.
        '''
        if kind == 'to_do_list':
            self.mutate_to_do_list(id, another_id, action, content)
        elif kind == 'discord_update':
            self.mutate_discord_update(id, action, medium, channel)


    def save(self):
        file = open(self.file_name, 'w')
        for key in self.processed.result.keys():
            file.write('type ' + key + '\n')
            for value in self.processed.result[key]:
                file.write(value + '\n')

            file.write('\n') # just for readability

        file.close()



class Interact_json:
    def __init__(self, file_name: str):
        self.file_name = file_name
        with open(file_name) as json_file:
            self.jason = json.load(json_file)

    def return_tags(self):
        return self.jason['tags']

    def return_search_engines(self):
        return self.jason['search_engines']




    def return_replies(self):
        if 'replies' not in self.jason.keys():
            self.jason.update({'replies': {'server_id': {'trigger': ['replies']}}})

        return self.jason['replies']





    def mutate_tags(self, action, server_id: str, name: str, value = None):
        tags = self.return_tags()
        if action == 'edit':
            if server_id not in tags.keys():
                tags.update({server_id: {name: value}})
            else:
                tags[server_id].update({name:value})

        elif action == 'delete':
            try:
                del tags[server_id][name]
            except KeyError:
                if server_id not in tags.keys():
                    raise ServerNotFound
                else:
                    raise ItemNotFound



    def mutate_search_engines(self, action, server_id: str, name: str, engine_id = None):
        engines = self.return_search_engines()
        if action == 'edit':
            if server_id not in engines.keys():
                engines.update({server_id: {name: engine_id}})
            else:
                engines[server_id].update({name: engine_id})

        elif action == 'delete':
            try:
                del engines[server_id][name]

            except KeyError:
                if server_id not in engines.keys():
                    raise ServerNotFound
                else:
                    raise ItemNotFound


    def mutate_replies(self, action, server_id: str, trigger: str, reply): # reply can be list (to add, for convenience of multiple at once) or string (to delete)
        replies = self.return_replies()
        if action == 'edit':
            if server_id not in replies.keys():
                replies.update({server_id: {trigger: reply}})
            elif trigger not in replies[server_id]:
                replies[server_id].update({trigger: reply})
            else:
                replies[server_id][trigger].extend(reply)

        elif action == 'delete':
            try:
                if reply == '' or reply == None:
                    del replies[server_id][trigger]
                else:
                    replies[server_id][trigger].remove(reply)
            except ValueError:
                raise ItemNotFound



    def save(self):
        with open(self.file_name, 'w+') as outfile:
            json.dump(self.jason, outfile)







#### tests ####

def dp(content):
    if False:
        print(content)

def test1():
    ha = Mutate('hello.txt')
    ha.mutating('to_do_list', 'yehet', 'edit', another_id = '7', content = 'so cool')
    ha.mutating('discord_update', 'yehet', 'edit', medium = 'google_plus', channel = 'poo')

    ha.mutating('to_do_list', 'yehet', 'edit', another_id = '6', content = 'so cool')
    ha.save()

    print(Read('hello.txt').to_do_list())

def test2():
    print('testing...')
    ho = Interact_json('info_json.txt')
    #ho.mutate_tags('delete', 'yehet', 'name', value = 'value')
    ho.mutate_search_engines('edit', 'another_yehet', 'name', engine_id = 'id')
    ho.save()




if __name__ == '__main__':
    #test2()
    pass
