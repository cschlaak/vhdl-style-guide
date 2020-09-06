
from vsg.vhdlFile.classify_new import expression
from vsg.vhdlFile.classify_new import identifier_list
from vsg.vhdlFile.classify_new import mode
from vsg.vhdlFile.classify_new import subtype_indication


from vsg.token import interface_variable_declaration as token

from vsg.vhdlFile import utils

'''
    interface_variable_declaration ::=
    [ variable ] identifier_list : [ mode ] subtype_indication [ := static_expression ]
'''

def detect(iToken, lObjects):
    if utils.is_next_token('variable', iToken, lObjects):
        return classify(iToken, lObjects)
    return iToken

def classify(iToken, lObjects):
    iCurrent = utils.assign_next_token_required('variable', token.variable_keyword, iToken, lObjects)
    iCurrent = identifier_list.classify(iCurrent, lObjects)
    iCurrent = utils.assign_next_token_required(':', token.colon, iCurrent, lObjects)
    iCurrent = mode.classify(iCurrent, lObjects)
    sEnd = utils.find_earliest_occurance([')', ';'], iCurrent, lObjects)
    if utils.find_in_range(':=', iCurrent, sEnd, lObjects):
        iCurrent = utils.classify_subelement_until(':=', subtype_indication, iCurrent, lObjects)
        iCurrent = utils.assign_next_token_required(':=', token.assignment, iCurrent, lObjects)
        iCurrent = utils.classify_subelement_until(sEnd, expression, iCurrent, lObjects)
    else:
        iCurrent = utils.classify_subelement_until(sEnd, subtype_indication, iCurrent, lObjects)

    return iCurrent
