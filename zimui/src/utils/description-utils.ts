import LinkifyIt from "linkify-it";

const linkify = new LinkifyIt();

export const formatVideoDescription = (text: string): Array<[string, string]> => {
    const desc: Array<[string, string]> = [];
  
    if (linkify.test(text)) {
      const matches = linkify.match(text) || [];
      let lastIndex = 0;
      for (const match of matches) {
        if (lastIndex < match.index) {
          desc.push([text.slice(lastIndex, match.index), "span"]);
        }
        desc.push([match.url, "a"]);
        lastIndex = match.lastIndex;
      }
      if (lastIndex < text.length) {
        desc.push([text.slice(lastIndex), "span"]);
      }
    } else {
      desc.push([text || "", text ? "span" : "br"]);
    }
  
    return desc;
};