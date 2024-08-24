#!/usr/bin/env python3
"""consle.py
----to start the file : ./console.py"""
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.amenity import Amenity
import cmd
import models
import shlex


class HBNBCommand(cmd.Cmd):
    """HBNBCommand"""
    prompt = "(hbnb)"
    classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }

    def do_create(self, args):
        """command to create a new instance of BaseModel
        usage: create <class_name>"""

        if not args:
            print("** class name missing **")
            return
        arg, *params = args.split(' ')
        new_obj = {}
        for param in params:
            try:
                key, value = param.split('=')
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1].replace('_', ' ')
                elif '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                new_obj[key] = value  # Update the new_obj dictionary
            except Exception:
                continue
        if arg in globals():
            model = HBNBCommand.classes[arg](**new_obj)
            model.save()
            print(model.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        """string representation based on the class name and id"""
        arg = shlex.split(args)
        if len(arg) == 0:
            print("** class name missing **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif arg[0] not in models.classes:
            print("** class doesn't exist **")
        else:
            dic = models.storage.all()
            keyU = arg[0] + '.' + str(arg[1])
            if keyU in dic:
                print(dic[keyU])
            else:
                print("** no instance found **")
        return

    def do_destroy(self, args):
        """Destroy an instance"""
        arg = shlex.split(args)
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        elif arg[0] not in models.classes:
            print("** class doesn't exist **")
            return
        else:
            dic = models.storage.all()
            keyU = arg[0] + '.' + str(arg[1])
            if keyU in dic:
                del dic[keyU]
                models.storage.save()
            else:
                print("** no instance found **")
        return

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        """show all instance"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            print('i am in the args')
            for k, v in storage.all(args).items():
                print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                # i removed the "args" from this line
                print_list.append(str(v))
        print(print_list)

    def do_update(self, args):
        """Updates an instance based on the class name and id """
        arg = shlex.split(args)
        if len(arg) == 0:
            print("** class name missing **")
            return
        elif len(arg) == 1:
            print("** instance id missing **")
            return
        elif len(arg) == 2:
            print("** attribute name missing **")
            return
        elif len(arg) == 3:
            print("** value missing **")
            return
        elif arg[0] not in models.classes:
            print("** class doesn't exist **")
            return
        key = arg[0] + '.' + arg[1]
        dic = models.storage.all()
        try:
            obj = dic[key]
        except KeyError:
            print("** no instance found **")
            return
        try:
            ins_one = type(getattr(obj, arg[2]))
            arg[3] == ins_one(arg[3])
        except AttributeError:
            pass
        setattr(obj, arg[2], arg[3])
        models.storage.save()
        return

    def do_quit(self, arg):
        """quit"""
        return True

    def do_EOF(self, args):
        """handel EOF"""
        return True

    def emptyline(self):
        """No action"""
        pass


if __name__ == '__main__':
    """HBNBCommand()"""
    HBNBCommand().cmdloop()
