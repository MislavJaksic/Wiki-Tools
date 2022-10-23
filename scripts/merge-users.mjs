import {WikiActionPayload, WikiAction} from "./action.mjs";
import {curlyStringToValues, whitespaceToPlus} from "./helper.mjs";
import {curlyOptions, mergeUsersUrl, curlyMergeUsersReferer, curlyMergeUsersBody} from "./secrets.mjs";

class NewOldUserPair {
  constructor(newName, oldName) {
    this.newName = newName;
    this.oldName = oldName;
  }
}

const newOldNamePairs = []

for (let newOldNamePair of newOldNamePairs) {
  let movePayload = new WikiActionPayload(mergeUsersUrl, curlyOptions);
  movePayload.setReferer(curlyStringToValues(curlyMergeUsersReferer, []));
  movePayload.setBody(whitespaceToPlus(curlyStringToValues(curlyMergeUsersBody, [newOldNamePair.oldName, newOldNamePair.newName])));

  let mergeUser = new WikiAction(movePayload);
  mergeUser.do();
}