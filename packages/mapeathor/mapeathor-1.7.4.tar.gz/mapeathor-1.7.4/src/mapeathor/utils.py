import json
import re

from . import global_config


def replaceVars(element, type_, termtype_):
    """
    Writes the objects 'element' correctly according to their type 'type_' and termtype 'termtype_', returns the
    corrected object
    """
    config = json.loads(open(global_config.templatesDir + 'config.json').read())
    # Add "" to the constant literal objects in YARRRML
    if(global_config.language == 'yarrrml' and type_ == 'constant'):
        result = str(config['variable'][type_]['before']) + element + str(config['variable'][type_]['after'])

    # Replace '{' and '}' in all but constant objects according to the config.json file of each language
    elif(type_ != 'constant' and str(config['variable'][type_]['before']) != '{' and str(config['variable'][type_]['after']) != '}'):
        result = element.replace("{", str(config['variable'][type_]['before'])).replace("}", config['variable'][type_]['after'])

    elif(((termtype_ != 'IRI' and type_ == 'constant') or type_ == 'template' or (termtype_ == 'IRI' and element[0:4] == 'http')) and (global_config.language != 'yarrrml')):
        result = "\"" + element + "\""

    else:
        result = element
    return result


def replaceTermMap(type_):
    config = json.loads(open(global_config.templatesDir + 'config.json').read())
    result = config['variable'][type_]['termMap']
    return result


def dataTypeIdentifier(element):
    """
    Identifies the datatype of the object 'element' and returns it
    """
    # Load the json with some xsd datatypes predefined

    try:
        data = open(global_config.dataTypesFile).read()
        dataTypes = json.loads()
    except:
        dataTypes = global_config.defaultDataTypes

    for key in dataTypes.keys():
        if element.lower().strip() in dataTypes[key]:
            return key

    print('WARNING: datatype not recognized (' + element + '), check XSD datatypes')
    return element


def termTypeIdentifier(element, dataType):
    """
    Identifies the termtype of the object 'element' based on itself and its datatype 'dataType' and returns it
    """
    if(len(str(element).split(":")) == 2 or "http" in str(element) or dataType == "anyURI"):
        return 'IRI', '~iri'
    elif dataType == "BlankNode":
        return 'BlankNode', '~iri'
    else:
        return 'Literal', ''

def subjectTermTypeIdentifier(element):
    """
    Identifies the termtype of the subject 'element' based on if it is formatted as an IRI or not
    """
    if(len(str(element).split(":")) == 2 or "http" in str(element)):
        return 'IRI'
    elif element == 'nan':
        return 'BlankNode'
    else:
        return 'BlankNode'


def predicateTypeIdentifier(element):
    """
    Identifies the type of the predicate, distinguishing between constant, reference and template, and returns it
    """
    # For reference
    if(str(element)[:1] == '{' and str(element)[-1:] == '}' and len(str(element).split(" "))  == 1):
        return 'reference'
    # For template
    elif(bool(re.search("{.+}.+", str(element))) or bool(re.search(".+{.+}", str(element)))):
        return 'template'
    # For star maps
    #elif(bool(re.search("^<<.+>>$", str(element)))):
    #    print("\n\n\n")
    #    return 'starmap'
    # For constant
    elif(len(str(element).split(":")) == 2 and "{" not in str(element) and "}" not in str(element)):
        return 'constant'
    # Constant when not recognized
    else:
        #print("WARNING: type not identified for predicate '" + element + "', 'constant' assigned")
        return 'constant'


def cleanDir(path):
    """
    Cleans the results directory
    """
    dir = os.listdir(path)
    for f in dir:
        os.remove(path + f)
