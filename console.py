#!/usr/bin/python3
"""A program containing the entry point
of the command interpreter
"""
import models
from models import storage
import cmd
import re
import os


def parse(line):
    """Convert a series of zero or more numbers to an argument tuple"""
    return tuple(map(str, line.split()))


class HBNBCommand(cmd.Cmd):
    """Represents a Console Program
    """
    prompt = "(hbnb) "

    def default(self, line):
        """Default behaviour when argument format is not recognised by cmd
        """
        classname = ''
        method = ''
        uid = ''
        attr_and_value = ''

        incomplete_classname = True
        incomplete_method = True
        incomplete_uid = True
        for i in line:
            if incomplete_classname is True:
                if i == '.':
                    incomplete_classname = False
                else:
                    classname += i
            elif incomplete_method is True:
                if i == '(':
                    incomplete_method = False
                else:
                    method += i
            elif incomplete_uid is True:
                if i in [')', ',']:
                    incomplete_uid = False
                elif i not in ['"', "'"]:
                    uid += i
            else:
                if i not in [',', "'", ')']:
                    attr_and_value += i

        group_args = classname + ' ' + uid + ' ' + attr_and_value
        if method == 'all':
            self.do_all(group_args)
        elif method == 'show':
            self.do_show(group_args)
        elif method == 'destroy':
            self.do_show(group_args)
        elif method == 'update':
            self.do_update(group_args)
        elif method == 'count':
            count = {k: v for k, v in storage.all().items()
                     if type(v).__name__ == classname}
            print(len(count.keys()))

    @staticmethod
    def determine_type(line):
        """Determine the type of the attribute_value to update
        """
        if line[0] in ['"', "'"]:
            return 'str'
        for character in line:
            if (ord(character) != ord('.') and
                    (ord(character) < ord('0') or ord(character) > ord('9'))):
                return 'str'
        if '.' in list(line):
            return 'float'
        return 'int'

    @staticmethod
    def string_input(raw_list):
        """Create the final string input for setattr in do_update"""
        raw = raw_list[3]
        final = ''
        raw_len = len(raw)
        len_list = len(raw_list)
        for i in range(raw_len):
            if ((i != 0 or raw[i] not in ['"', "'"]) and
                    (i != raw_len - 1 or raw[i] not in ['"', "'"])):
                if raw[i] == "'":
                    final += '\''
                else:
                    final += raw[i]
        if raw[0] == '"' and raw[-1] != '"' and len_list > 4:
            for raw_str in raw_list[4:]:
                final += ' '
                for i in raw_str:
                    if i != '"':
                        final += i
        return final

    @staticmethod
    def remove_double_quotes(raw_str):
        final = ''
        for i in raw_str:
            if i not in ['"', "'"]:
                final += i
        return final

    def do_EOF(self, line):
        """Handles End Of File character.
        """
        print("")
        return True

    def emptyline(self):
        """Doesn't do anything on ENTER.
        """
        pass

    def do_quit(self, line):
        """Exits the program.
        """
        return True

    def do_create(self, line):
        """Creates an instance.
        """
        line = parse(line)
        if len(line) == 0:
            print("** class name missing **")
        elif line[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            cls = storage.classes()[line[0]]()
            cls.save()
            print(cls.id)

    def do_show(self, line):
        """Prints the string representation of an instance.
        """
        wrds = parse(line)
        if len(wrds) == 0:
            print("** class name missing **")
        elif wrds[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(wrds) == 1:
            print("** instance id missing **")
        else:
            obj_id = "{}.{}".format(wrds[0], wrds[1])
            if obj_id in storage.all():
                print(storage.all()[obj_id])
            else:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id.
        """
        wrds = parse(line)
        if len(wrds) == 0:
            print("** class name missing **")
        elif wrds[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(wrds) == 1:
            print("** instance id missing **")
        else:
            obj_id = "{}.{}".format(wrds[0], wrds[1])
            if obj_id not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[obj_id]
                storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances.
        """
        if len(line) == 0:
            full_list = [str(obj) for key, obj in storage.all().items()]
            print(full_list)
        if len(line) >= 1:
            wrds = line.split(' ')
            if wrds[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                instance_list = [str(obj) for key, obj in storage.all().items()
                                 if type(obj).__name__ == wrds[0]]
                print(instance_list)

    def do_update(self, line):
        """Updates an instance by adding or updating attribute.
        """
        wrds = parse(line)

        if len(wrds) == 0:
            print("** class name missing **")
        elif wrds[0] not in storage.classes():
            print("** class doesn't exist **")
        elif len(wrds) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(wrds[0], wrds[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                if len(wrds) == 2:
                    print("** attribute name missing **")
                elif len(wrds) == 3:
                    print("** value missing **")
                else:
                    if key in storage.all():
                        value_type = self.determine_type(wrds[3])
                        final_attribute = self.remove_double_quotes(wrds[2])
                        if value_type == 'str':
                            final_value = self.string_input(wrds)
                            setattr(storage.all()[key],
                                    final_attribute, final_value)
                        elif value_type == 'int':
                            setattr(storage.all()[key],
                                    final_attribute, int(wrds[3]))
                        elif value_type == 'float':
                            setattr(storage.all()[key],
                                    final_attribute, float(wrds[3]))
                        storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
