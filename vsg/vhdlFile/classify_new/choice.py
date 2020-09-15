
from vsg import parser

from vsg.vhdlFile import utils

from vsg.vhdlFile.classify_new import choice


def classify_until(lUntils, iToken, lObjects):
    '''
    choice ::=
        simple_expression
      | discrete_range
      | *element*_simple_name
      | others
    '''

    for iIndex in range(iToken, len(lObjects)):
        if not utils.is_item(lObjects, iIndex):
            continue
        if utils.is_next_token_in_list(lUntils, iIndex, lObjects):
            return iIndex
        else:
            if utils.is_next_token('others', iIndex, lObjects):
                utils.assign_next_token_required('others', token.others, iIndex, lObjects)
            else:
                utils.assign_next_token(parser.todo, iIndex, lObjects)

    return iToken
