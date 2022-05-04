import {pageNameToReferer, curlyStringToValues, whitespaceToPlus, execute} from "./helper.mjs";
import {movePagesUrl, movePagesReferer, movePagesBody, movePagesOptions} from "./secrets.mjs";

let namespaceCode = "3000"; /* Archive: is 3000 */

let pages = [];

let reason = "";

let leaveRedirect = "1"; /* 0, 1*/

let url = movePagesUrl;
let blankReferer = movePagesReferer;
let blankBody = movePagesBody;
let blankOptions = movePagesOptions;

for (let page of pages) {
    let referer = pageNameToReferer(page, blankReferer);
    blankOptions.headers.Referer = referer;
    let body = curlyStringToValues(blankBody, [namespaceCode, whitespaceToPlus(page), whitespaceToPlus(reason), leaveRedirect, whitespaceToPlus(page)]);
    blankOptions.body = body;
    execute(url, blankOptions);
}
