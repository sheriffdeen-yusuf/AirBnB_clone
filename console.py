#!/usr/bin/python3
"""A program containing the entry point
of the command interpreter
"""
import models
from models import storage
import cmd


class HBNBCommand(cmd.Cmd):
    """Represents a Console Program"""
    prompt = '(hbnb) '

    def do_EOF(self, line):
        """Exit at End of File"""
        return True

    def emptyline(self):
        """When empty line + ENTER nothing
        executed"""
        pass

    def do_quit(self, line):
        """Exit the program"""
        return True

    def do_create(self, line):
        """Creates a new instance of BaseModel saves
        it to JSON & prints the id"""
        if len(line) == 0:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            cls = storage.classes()[line]()
            cls.save()
            print(cls.id)

    def do_show(self, line):
        """Prints the string representation of an instance based on the
        class name and id Ex $ show BaseModel 1234-1234-1234"""
        if len(line) == 0:
            print("** class name missing **")
        else:
            wrds = line.split(' ')
            if wrds[0] in storage.classes():
                key = "{}.{}".format(wrds[0], wrds[1])
                if key in storage.all():
                    print(storage.all()[key])
                else:
                    print("** no instance found **")
            elif len(wrds) < 2:
                print("** instance id missing **")
            else:
                print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
