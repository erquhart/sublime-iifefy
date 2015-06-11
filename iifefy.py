import sublime, sublime_plugin

# TODO: Consider adding one or more classes outside of the Command
# classes for better code modularization. Suboptimal parts of this
# code may be due to our use of class inheritance.
class IifefyCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    self.settings = sublime.load_settings("Iifefy.sublime-settings")

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
    if not (line.isspace() or line == ''):
      line = '\t' + line
    return line + '\n'

  # This is overriden by the IifefySkipCommentsCommand class.
  # IifefyCommand class passes String "content", while
  # IifefySkipCommentsCommand passes Region "region".
  # TODO: both types of data should be accepted through a single param.
  def wrapIife(self, content, region):
    wrapStart = self.settings.get('wrapStart')
    wrapEnd = self.settings.get('wrapEnd')
    trailingNewline = '\n' if self.settings.get('trailingNewline') else ''
    return wrapStart + content + wrapEnd + trailingNewline

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

class IifefySkipInitialCommentsCommand(IifefyCommand):
  def wrapIife(self, content, region):
    comments = ''
    iifeContent = ''
    emptyLines = ''
    lines = self.view.lines(region)
    precedingLinesEmpty = True
    precedingLinesComments = True
    for line in lines:
      precedingLinesEmpty = self.emptyLinesCheck(precedingLinesEmpty, line)

      if not precedingLinesEmpty:
        line = self.view.substr(line)

        if precedingLinesComments:
          if line == '':
            emptyLines = emptyLines + '\n'
          elif (self.isComment(line) and emptyLines):
            comments = comments + emptyLines + line + '\n'
            emptyLines = ''
          elif self.isComment(line):
            comments = comments + line + '\n'
          else:
            comments = comments + '\n'
            precedingLinesComments = False

        if not precedingLinesComments:
          line = self.wrapIifeLine(line)
          iifeContent = iifeContent + line

    # TODO: Dry this up, it's duplicate code from the overriden
    # wrapIife method
    wrapStart = self.settings.get('wrapStart')
    wrapEnd = self.settings.get('wrapEnd')
    trailingNewline = '\n' if self.settings.get('trailingNewline') else ''
    iife = wrapStart + iifeContent + wrapEnd + trailingNewline
    content = comments + iife
    return content

  def isComment(self, line):
    commentPrefixes = ('/*', '//', '*' )
    return line.lstrip().startswith(commentPrefixes)
