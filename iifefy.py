import sublime, sublime_plugin

# TODO: Consider adding one or more classes outside of the Command
# classes for better code modularization. Suboptimal parts of this
# code may be due to our use of class inheritance.
class IifefyCommand(sublime_plugin.TextCommand):
  settings = sublime.load_settings("Iifefy.sublime-settings")

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

    wrapStart = self.settings.get('wrapStart')
    wrapEnd = self.settings.get('wrapEnd')
    trailingNewline = '\n' if self.settings.get('trailingNewline') else ''
    iife = wrapStart + content + wrapEnd + trailingNewline
    content = comments + '\n' + iife
    return content

  def isComment(self, line):
    commentPrefixes = ('/*', '//', '*' )
    return line.lstrip().startswith(commentPrefixes)
