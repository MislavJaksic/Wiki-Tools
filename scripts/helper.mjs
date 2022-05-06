String.prototype.format = function () {
    var i = 0, args = arguments;
    return this.replace(/{}/g, function () {
      return typeof args[i] != 'undefined' ? args[i++] : '';
    });
  };

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

export function whitespaceToUnderscore(string) {
    return string.replace(/ /g, "_");
}
