import os
import argparse
import pystache
import logging
import io

def addSep(separator, data):
    for row in data[:-1]:
        row["sep"] = separator
    return data

def setup():
    parser = argparse.ArgumentParser(description="Generate code")
    parser.add_argument("className", help="name of the class to generate")
    parser.add_argument("members", help="members contained in the class in the format name1:type1,name2:type2")
    parser.add_argument("language", help="language to use", default="cs", nargs="?")
    args = parser.parse_args()
    return args

def parseMembers(serializedMembers):
    members = []
    for token in serializedMembers.split(","):
        name, type = token.split(":")
        members.append({"name" : name, "type" : type})
    return members

def getTemplate(language):
    templatePath = os.path.join("templates", language + "Class.mustache")
    with open(templatePath) as fp:
        return fp.read()

if __name__ == "__main__":
    args = setup()
    template = getTemplate(args.language)
    model = {
        "className" : args.className,
        "members" : addSep(", ", parseMembers(args.members))
        }
    print pystache.render(template, model)
