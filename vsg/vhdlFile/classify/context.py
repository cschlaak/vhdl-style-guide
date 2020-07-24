
from vsg import parser


def context(self, dVars, lTokens, lObjects, oLine):
    '''
    Classifies context declarations.

    context identifier is
        [ library ;]
    end [context] [identifier] ;

    Sets the following line attributes:

      * insideContext

    Modifies the following variables:

      * bInsideContext
      * bContextEndFound
      * bContextIsFound
      * iCurrentIndentLevel
    '''
    for iToken, sToken in enumerate(lTokens):
        if dVars['bInsideContext']:

            classify_context_identifier(sToken, iToken, lObjects, dVars)

            classify_context_is_keyword(sToken, iToken, lObjects, dVars)

            if dVars['bContextEndFound']:

               classify_context_end_context_keyword(sToken, iToken, lObjects)

               classify_context_end_identifier(sToken, iToken, lObjects)

               classify_semicolon(sToken, iToken, lObjects, dVars)

            classify_context_end_keyword(sToken, iToken, lObjects, dVars, oLine)
 
        else:
            classify_context_keyword(sToken, iToken, lObjects, dVars, oLine)


def classify_semicolon(sToken, iToken, lObjects, dVars):
    if sToken == ';':
        lObjects[iToken] = parser.context_semicolon()
        dVars['bInsideContext'] = False
        dVars['bContextIsFound'] = False
        dVars['bContextEndFound'] = False


def classify_context_end_identifier(sToken, iToken, lObjects):
    if sToken.lower() != 'context' and sToken != ';' and not isinstance(lObjects[iToken], parser.whitespace) and not isinstance(lObjects[iToken], parser.comment):
        lObjects[iToken] = parser.context_end_identifier(sToken)


def classify_context_end_context_keyword(sToken, iToken, lObjects):
    if sToken.lower() == 'context':  
        lObjects[iToken] = parser.context_end_context_keyword(sToken)


def classify_context_end_keyword(sToken, iToken, lObjects, dVars, oLine):
    if sToken.lower() == 'end':
        lObjects[iToken] = parser.context_end_keyword(sToken)
        dVars['bContextEndFound'] = True
        if iToken < 2:
            oLine.indentLevel = 0
            dVars['iCurrentIndentLevel'] = 0


def classify_context_is_keyword(sToken, iToken, lObjects, dVars):
    if sToken.lower() == 'is':
        lObjects[iToken] = parser.context_is_keyword(sToken)
        dVars['bContextIsFound'] = True


def classify_context_identifier(sToken, iToken, lObjects, dVars):
    if not dVars['bContextIsFound'] and not isinstance(lObjects[iToken], parser.whitespace) and not isinstance(lObjects[iToken], parser.comment):
        lObjects[iToken] = parser.context_identifier(sToken)


def classify_context_keyword(sToken, iToken, lObjects, dVars, oLine):
    if sToken.lower() == 'context':
        lObjects[iToken] = parser.context_keyword(sToken)
        dVars['bInsideContext'] = True
        dVars['iCurrentIndentLevel'] += 1
        if iToken < 2:
            oLine.indentLevel = 0
