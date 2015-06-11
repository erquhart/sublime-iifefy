import sublime, sublime_plugin

class IifefyCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.somethingIsSelected():
      self.wrapSelections(edit)
    else:
      self.wrapAllContent(edit)

  def wrapSelections(self, edit):
    selections = self.view.sel()
    for selection in selections:
      if not selection.empty():
        self.generateIife(edit, selection)

  def wrapAllContent(self, edit):
    content = sublime.Region(0, self.view.size())
    self.generateIife(edit, content)

  def generateIife(self, edit, region):
    iifeContent = self.getIifeContent(region)
    iife = self.wrapIife(iifeContent, region)
    self.view.replace(edit, region, iife)

  def getIifeContent(self, region):
    iifeContent = ""
    lines = self.view.lines(region)
    precedingLinesEmpty = True
    for line in lines:
      precedingLinesEmpty = self.emptyLinesCheck(precedingLinesEmpty, line)

      if not precedingLinesEmpty:
        line = self.view.substr(line)
        line = self.wrapIifeLine(line)
        iifeContent = iifeContent + line

    return iifeContent

  def wrapIifeLine(self, line):
    return '\t' + line + '\n'

  def wrapIife(self, content, region):
    return self.wrapStart + content + self.wrapEnd

  def somethingIsSelected(self):
    nonEmptySelectionFound = False
    selections = self.view.sel()
    for selection in selections:
      if not selection.empty():
        nonEmptySelectionFound = True

    return nonEmptySelectionFound

  def emptyLinesCheck(self, flag, line):
    if (flag and line.empty()):
      pass
    elif not line.empty():
      flag = False

    return flag

  wrapStart = '(function() {\n  \'use strict\';\n\n'
  wrapEnd = '})();\n'

class IifefySkipInitialCommentsCommand(IifefyCommand):
  def wrapIife(self, content, region):
    comments = ""
    iifeContent = ""
    lines = self.view.lines(region)
    precedingLinesEmpty = True
    precedingLinesComments = True
    for line in lines:
      precedingLinesEmpty = self.emptyLinesCheck(precedingLinesEmpty, line)

      if not precedingLinesEmpty:
        line = self.view.substr(line)

        if precedingLinesComments:
          if (self.isComment(line) or line == ''):
            comments = comments + line + '\n'
          else:
            precedingLinesComments = False
            continue

        if not precedingLinesComments:
          line = self.wrapIifeLine(line)
          iifeContent = iifeContent + line

    iife = self.wrapStart + iifeContent + self.wrapEnd
    content = comments + '\n' + iife
    return content

  def isComment(self, line):
    commentPrefixes = ('/*', '//', '*' )
    return line.lstrip().startswith(commentPrefixes)
