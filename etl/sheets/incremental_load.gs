function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  var row = e.range.getRow();
  if (row == 1) return; // skip header row

  var sheetName = sheet.getName();
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

  // helper: find column index by header name
  function colIndex(name) {
    return headers.indexOf(name) + 1; // +1 because indexOf is 0-based
  }

  // -------------------
  // Case 1: Job Applicants Sheet
  // -------------------
  if (sheetName === "applications") {
    var idCol = colIndex("app_id");
    var createdAtCol = colIndex("created_at");
    var lastModifiedCol = colIndex("last_modified");

    // assign app_id if empty
    if (!sheet.getRange(row, idCol).getValue()) {
      var lastRow = sheet.getLastRow();
      var nextId = lastRow - 1; // exclude header
      sheet.getRange(row, idCol).setValue(nextId);

      // set created_at only if empty
      if (!sheet.getRange(row, createdAtCol).getValue()) {
        sheet.getRange(row, createdAtCol).setValue(new Date());
      }
    }

    // always update last_modified
    sheet.getRange(row, lastModifiedCol).setValue(new Date());
  }

  // -------------------
  // Case 2: Study Logs Sheet
  // -------------------
  if (sheetName === "study_logs") {
    var idCol = colIndex("study_id");
    var createdAtCol = colIndex("created_at");
    var lastModifiedCol = colIndex("last_modified");

    // assign study_id if empty
    if (!sheet.getRange(row, idCol).getValue()) {
      var lastRow = sheet.getLastRow();
      var nextId = lastRow - 1; // exclude header
      sheet.getRange(row, idCol).setValue(nextId);

      // set created_at only if empty
      if (!sheet.getRange(row, createdAtCol).getValue()) {
        sheet.getRange(row, createdAtCol).setValue(new Date());
      }
    }

    // always update last_modified
    sheet.getRange(row, lastModifiedCol).setValue(new Date());
  }
}
