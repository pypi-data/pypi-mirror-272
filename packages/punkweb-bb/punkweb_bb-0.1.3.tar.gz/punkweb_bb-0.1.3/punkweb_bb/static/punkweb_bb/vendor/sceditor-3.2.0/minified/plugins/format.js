/* SCEditor v3.2.0 | (C) 2017, Sam Clarke | sceditor.com/license */
!function(i){"use strict";i.plugins.format=function(){var n,a,c={p:"Paragraph",h1:"Heading 1",h2:"Heading 2",h3:"Heading 3",h4:"Heading 4",h5:"Heading 5",h6:"Heading 6",address:"Address",pre:"Preformatted Text"};this.init=function(){var e=this.opts,t=e.paragraphformat;e.format&&"bbcode"===e.format||(t&&(t.tags&&(c=t.tags),t.excludeTags&&t.excludeTags.forEach(function(e){delete c[e]})),this.commands.format||(this.commands.format={exec:a,txtExec:a,tooltip:"Format Paragraph"}),e.toolbar===i.defaultOptions.toolbar&&(e.toolbar=e.toolbar.replace(",color,",",color,format,")))},n=function(e,t){e.sourceMode()?e.insert("<"+t+">","</"+t+">"):e.execCommand("formatblock","<"+t+">")},a=function(e){var o=this,r=document.createElement("div");i.utils.each(c,function(t,a){var e=document.createElement("a");e.className="sceditor-option",e.textContent=a.name||a,e.addEventListener("click",function(e){o.closeDropDown(!0),a.exec?a.exec(o):n(o,t),e.preventDefault()}),r.appendChild(e)}),o.createDropDown(e,"format",r)}}}(sceditor);