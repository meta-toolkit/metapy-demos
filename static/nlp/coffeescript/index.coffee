$ ->
  Handlebars.registerPartial 'observation', $('#observation').html()
  Handlebars.registerPartial 'treenode', $('#treenode').html()

  $("#analyzerOutput").hide()
  $("#analyzeButton").click ->
    input = $("#inputText").val()
    if input.length == 0
      input = "Here is a sentence to analyze."
    if input.length > (512 * 1024) # about 512 KB
      input = "Try using a smaller amount of text."
    $("#analyzerOutput").show()
    $.ajax "/nlp-api",
      type: "POST"
      contentType: "application/json; charset=utf-8"
      dataType: "json"
      data: JSON.stringify {"text": input}
      success: (data, stat, xhr) -> printSentences data
      failure: (axhr, stat, err) -> console.log "Failed!"

tagToLabel = (tag) ->
  "label_#{tag.replace("$", "DOLLAR").replace(/[.:,]/, "PUNCT")}"

addLabels = (tree) ->
  tree.label = tagToLabel tree.tag
  if tree.children
    tree.children = tree.children.map addLabels
  tree

parseTree = (tree) ->
  template = Handlebars.compile $('#parse-tree').html()

  tree = addLabels tree
  template tree

taggedText = (observations) ->
  template = Handlebars.compile $('#tagged-text').html()

  observations = observations.map (elem) ->
    elem['label'] = tagToLabel(elem['tag'])
    return elem

  template {'observations': observations}

printSentences = (result) ->
  window.DT.destroy() if window.DT isnt undefined # clear old data
  $("#sentenceList tbody").html('') # clear old data
  totalSentences = 0
  for elem in result.sentences
    ++totalSentences
    html = "<tr><td>#{totalSentences}</td>"
    html += "<td><p>#{elem.tokenized}</p>"
    html += "<p>#{taggedText(elem.tagged)}</p>"
    html += "<p>#{parseTree(elem['json-tree'])}</p></td></tr>"
    $("#sentenceList tbody").append(html)
  window.DT = $("#sentenceList").DataTable({"bPaginate": false, "bInfo": false})
