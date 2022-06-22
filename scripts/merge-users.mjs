import {execute} from "./helper.mjs";
import {mergeUsersUrl} from "./secrets.mjs";

let options = {} 

let body = 'wpolduser={}&wpnewuser={}&wpdelete=1&...'

const lowercaseNames = [] /* Generate a list of usernames that have only the starting letter capitalized */

for (let lowercaseName of lowercaseNames) {
  let uppercaseName = lowercaseName.replace(/\b\w/g, l => l.toUpperCase());
  console.log(lowercaseName);
  options["body"] = body.format(lowercaseName.replace(" ", "+"), uppercaseName).replace(" ", "+")
  /*execute(mergeUsersUrl, options)*/
}

