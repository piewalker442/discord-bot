import read_write
import random


class TestError(Exception):
    pass

class TodoError(Exception):
    pass

class To_do_list:
    def __init__(self, file_name, id):
        self.file_interact = read_write.Interact(file_name)

        self.file_name = file_name
        self.id = id

    def __len__(self):
        total = 0
        for item in self.return_to_do():
            total += len(item)
        return total


    def check_empty(self, content):
        '''filler for when a to do item
        is just blank'''


        # phrases = ['Wow you are lazy', "I'm lazy",
        # "Try editing this, cuz it's empty rn",
        # 'Maybe you want to delete this?', "literally nothing",
        # "Consider being productive", ""
        # ]
        #
        # if content.rstrip().strip() == '':
        #     return random.choice(phrases)

        return content


    def return_to_do(self, Formatted = False):

        try:
            my_to_do = self.file_interact.read_to_do_list()[self.id]
            if Formatted:
                return list(sorted((('{}. {}'.format(key,self.check_empty(my_to_do[key])) for key in my_to_do.keys())), key = (lambda x: int(x.split('.')[0]))))

            return my_to_do
        except KeyError:
            raise TodoError

    def find_to_do(self, query, Deep = True):
        my_to_do = self.return_to_do()
        keys = my_to_do.keys()
        for key in keys:
            if query == my_to_do[key]:
                return key

        for key in keys:
            if query == key:
                return key

        if query.rstrip().strip() == '':
            ''' prevents identifying any item when query empty
            or given an empty space'''
            raise TodoError

        if Deep:

            for key in keys:
                if query.lower() in my_to_do[key].lower():
                    return key

            for key in keys:
                if key in query:
                    return key

        raise TodoError


    def delete_to_do(self, item):
        key = self.find_to_do(item)
        self.file_interact.mutating('to_do_list', 'delete', self.id, another_id = key)

    def edit_to_do(self, edit):

        if edit.rstrip().strip() == '':
            raise TodoError

        key = '999' #to be sure it's at the end. lol
        try:
            key = self.find_to_do(edit.strip().split()[0].replace('.', ''), Deep=False)
            edit = edit.replace(edit.strip().split()[0], '').strip()
        except TodoError:
            '''if it does not exist, add it as a new item / id '''
            pass
        except IndexError:
            raise TodoError

        #print(len(self))

        # if (len(edit) + len(self)) > 1800:
        #     raise TodoError

        self.file_interact.mutating('to_do_list', 'edit', self.id, another_id = key, content = edit)


    def save_to_do(self):
        self.file_interact.save()
        self.file_interact = read_write.Interact(self.file_name)




### tests ###

def test1():
    test = To_do_list('hello.txt', 'yehet')
    print(test.return_to_do(Formatted = True))

    content = input('Wat:')
    test.edit_to_do(content)
    test.save_to_do()
    print(test.return_to_do(Formatted = True))



if __name__ == '__main__':
    test1()
