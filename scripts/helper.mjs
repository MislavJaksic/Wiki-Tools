import fetch from "node-fetch";

String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
      return typeof args[i] != 'undefined' ? args[i++] : '';
    });
  };

export function pageNameToReferer(pageName, referer) {
    return curlyStringToValues(referer, [whitespaceToUnderscore(pageName)]);
}

export function curlyStringToValues(string, values) {
    let newString = string;
    for (let value of values) {
        newString = newString.replace("{}", value.toString())
    }
    return newString;
}

export function whitespaceToPlus(string) {
    return string.replace(/ /g, "+");
}

function whitespaceToUnderscore(string) {
    return string.replace(/ /g, "_");
}

export async function execute(url, options) {
    const reponse = await fetch(url, options);
    console.log(reponse.ok);
    console.log(reponse.redirected);
    console.log(reponse.status);
    console.log(reponse.type);
    console.log(reponse.url);
  }
  