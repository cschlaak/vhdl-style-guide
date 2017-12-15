import re


def variable_assignment(dVars, oLine):

    if re.match('^\s*.*\s*:=', oLine.line) and not oLine.isComment and not oLine.insideIf and not oLine.isElseKeyword and not oLine.isVariable and not oLine.isSignal:
        oLine.isVariableAssignment = True
        oLine.insideVariableAssignment = True
        oLine.indentLevel = dVars['iCurrentIndentLevel']
        oLine.variableAssignmentAlignmentColumn = oLine.line.find(':=')
    if oLine.insideVariableAssignment:
        if ';' in oLine.line:
            oLine.isVariableAssignmentEnd = True
