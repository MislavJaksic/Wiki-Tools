import {WikiActionPayload, WikiAction} from "./action.mjs";
import {curlyStringToValues, whitespaceToPlus, whitespaceToUnderscore} from "./helper.mjs";
import {curlyOptions, movePagesUrl, curlyMovePagesReferer, curlyMovePagesBody} from "./secrets.mjs";

let namespaceCode = "3000"; /* Archive: is 3000 */

let pages = [];

let reason = "";

let leaveRedirect = "1"; /* 0, 1*/

for (let page of pages) {
    let movePayload = new WikiActionPayload(movePagesUrl, curlyOptions);
    movePayload.setReferer(curlyStringToValues(curlyMovePagesReferer, [whitespaceToUnderscore(page)]));
    movePayload.setBody(whitespaceToPlus(curlyStringToValues(curlyMovePagesBody, [namespaceCode, page, reason, leaveRedirect, page])));

    let movePage = new WikiAction(movePayload);
    movePage.do();
}
