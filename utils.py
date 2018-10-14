
import re

def validateText(text):
    text = text[67:-56:1] # Removes XML tags that surround the text block
    text = validateQuote(text)
    text = validateFormatting(text)
    text = validateImg(text)
    text = validateUrl(text)

    return text

# Fixes quote tags
def validateQuote(text):
    text = re.sub(r'<div class=\"bbCodeBlock bbCodeQuote\" data-author=\"(.+?)\">\n<aside>\n<div class=\"attribution type\">', "[quote=\"author:", text)
    text = text.replace("<div class=\"bbCodeBlock bbCodeQuote\">\n<aside>\n<blockquote class=\"quoteContainer\"><div class=\"quote\">", "[quote]")
    text = text.replace(" said:\n<a href=\"goto/post?id=", ", post:")
    text = text.replace(" said:\n\n<a href=\"goto/post?id=", ", post:")
    text = re.sub(r' onclick=\"return scrollToId\(\'\#post-(.+?)\'\)\">↑</a>\n</div>\n<blockquote class=\"quoteContainer\"><div class=\"quote\">', "]", text)
    text = re.sub(r'#post-[0-9]+\"\]', "\"]", text)
    text = text.replace("</div><div class=\"quoteExpand\">Click to expand...</div></blockquote>\n</aside>\n</div>\n<script>\nfunction scrollToId(selector, offset = 60) {\n  window.scroll(0, document.querySelector(selector).offsetTop - offset);\n  return false\n}\n</script>\n", "[/quote]\n")

    return text

# Fixes img tags
def validateImg(text):
    text = text.replace("<img alt=\"[​IMG]\" class=\"bbCodeImage LbImage\" data-url=", "[img]")
    text = text.replace("/>", "[/img]")

    url = re.search(r' src=\"(.+?)\"\[/img\]', text)
    if url:
        text = re.sub(r' src=\"(.+?)\"\[/img\]', "[/img]", text)

    text = text.replace("[img]\"", "[img]")
    text = text.replace("\"[/img]", "[/img]")

    return text

# Fixes url tags
def validateUrl(text):

    text = text.replace("<a class=\"externalLink\" href=\"", "[url='")
    text = text.replace("<a class=\"internalLink\" href=\"", "[url='")

    # User mentioning
    url = re.search(r'<a class=\"username\" data-user=\"(.+?)\" href=\"', text)
    if url:
        text = re.sub(r'<a class=\"username\" data-user=\"(.+?)\" href=\"', "[url='", text)

    # Media tags
    text = text.replace("<iframe allowfullscreen=\"\" data-s9e-livepreview-ignore-attrs=\"style\" data-s9e-mediaembed=\"twitter\" onload=\"var a=Math.random();window.addEventListener('message',function(b){if(b.data.id==a)style.height=b.data.height+'px'});contentWindow.postMessage('s9e:'+a,'https://s9e.github.io')\" scrolling=\"no\" src=\"", "[url]")
    text = text.replace("\" style=\"background:url(https://abs.twimg.com/favicons/favicon.ico) no-repeat 50% 50%;border:0;height:186px;max-width:500px;width:100%\"></iframe>", "[/url]")

    text = text.replace("\" rel=\"nofollow\" target=\"_blank\">", "']")
    text = text.replace("\">", "']")
    text = text.replace("</a>", "[/url]")

    return text

# Fixes formatting tags
def validateFormatting(text):
    text = text.replace("<br/>", "")

    text = text.replace("<i>", "[i]")
    text = text.replace("</i>", "[/i]")

    text = text.replace("<b>", "[b]")
    text = text.replace("</b>", "[/b]")

    text = text.replace("<span style=\"text-decoration: line-through\">", "[s]")
    strikeCount = text.count("[s]")
    regex = re.compile(r'\[s\]((.|\n)+?)</span>', re.M)
    strike = regex.search(text)
    while strike and (strikeCount > 0):
        text = regex.sub("[s]" + strike.group(1) + "[/s]", text)
        strikeCount -= 1
        strike = regex.search(text)

    text = text.replace("<span style=\"text-decoration: underline\">", "[u]")
    underlineCount = text.count("[u]")
    regex = re.compile(r'\[u\]((.|\n)+?)</span>', re.M)
    underline = regex.search(text)
    while underline and (underlineCount > 0):
        text = regex.sub("[u]" + underline.group(1) + "[/u]", text)
        underlineCount -= 1
        underline = regex.search(text)

    text = text.replace("<span style=\"font-size: ", "[size]")
    sizeCount = text.count("[size]")
    regex = re.compile(r'\[size\](.+?)px\">((.|\n)+?)</span>', re.M)
    size = regex.search(text)
    while size and (sizeCount > 0):
        text = re.sub(r'\[size\](.+?)px\">', "[size=" + size.group(1) + "px]", text)
        text = re.sub(r'px\]((.|\n)+?)</span>', "px]" + size.group(2) + "[/size]", text)
        sizeCount -= 1
        size = regex.search(text)

    #text = text.replace("<span class=\"bbHighlight", "[highlight]")
    '''highlightCount = text.count("[highlight]")
    regex = re.compile(r'\[highlight\]((.|\n)+?)</span>', re.M)
    highlight = regex.search(text)
    while highlight and (highlightCount > 0):
        text = regex.sub("[highlight]" + underline.group(1) + "[/highlight]", text)
        highlightCount -= 1
        highlight = regex.search(text)'''

    return text
