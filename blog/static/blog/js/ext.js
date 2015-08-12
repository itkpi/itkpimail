var HighlighterButton = MediumEditor.extensions.button.extend({
  name: 'highlighter',
  tagNames: ['pre'],
  contentDefault: '<b>H</b>',
  contentFA: '<i class="fa fa-terminal"></i>',
  aria: 'Hightlight',
  action: 'highlight',

  init: function () {
    MediumEditor.extensions.button.prototype.init.call(this);

    this.classApplier = rangy.createCssClassApplier('highlight', {
        elementTagName: 'pre',
        normalize: true
    });
  },

  handleClick: function (event) {
    var range = rangy.getSelection().getRangeAt(0);
    if (range.text()) {
        if (MediumEditor.selection.getSelectionStart(document).tagName.toLowerCase() != 'pre') {
            range.pasteHtml('<pre class="prettyprint">' + range.toHtml().replace(/(<\/p>)/ig, "\n").replace(/(<([^>]+)>)/ig,"") + '</pre>');
        } else {
            MediumEditor.selection.getSelectionStart(document).classList.remove('prettyprint');
            MediumEditor.util.execFormatBlock(document, 'pre');
        }
    }
  },

  isAlreadyApplied: function (node) {
    return node.nodeName.toLowerCase() === 'pre';
  }
});



var SpoilerButton = MediumEditor.extensions.button.extend({
  name: 'spoiler',
  tagNames: ['pre'],
  contentDefault: '<b>H</b>',
  contentFA: '<i class="fa fa-plus-square-o"></i>',
  aria: 'Spoiler',
  action: 'spoiler',

  init: function () {
    MediumEditor.extensions.button.prototype.init.call(this);

    this.classApplier = rangy.createCssClassApplier('highlight', {
        elementTagName: 'pre',
        normalize: true
    });
  },

  handleClick: function (event) {
    var range = rangy.getSelection().getRangeAt(0);
    console.log(range.toHtml());
    range.pasteHtml('<div class="spoiler_links spoiler_links_opened">Toggle spoiler</div><div class="spoiler_body">' + range.toHtml() + '</div>');
  },
});
