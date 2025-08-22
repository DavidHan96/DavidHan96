function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  var row = e.range.getRow();
  if (row == 1) return; // skip header row

  var sheetName = sheet.getName();
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];

  function colIndex(name) {
    return headers.indexOf(name) + 1;
  }

  // date format function
  function formatDate(value) {
    if (!value) return "";
    var dateObj = (typeof value === "object") ? value : new Date(value);
    return Utilities.formatDate(dateObj, Session.getScriptTimeZone(), "yyyy-MM-dd HH:mm:ss");
  }

  function fixRowDates(createdAtCol, lastModifiedCol) {
    var createdVal = sheet.getRange(row, createdAtCol).getValue();
    var lastModifiedVal = sheet.getRange(row, lastModifiedCol).getValue();

    if (createdVal) {
      sheet.getRange(row, createdAtCol).setValue(formatDate(createdVal));
    }
    sheet.getRange(row, lastModifiedCol).setValue(formatDate(new Date()));
  }

  // -------------------
  // applications sheet
  // -------------------
  if (sheetName === "applications") {
    var idCol = colIndex("app_id");
    var createdAtCol = colIndex("created_at");
    var lastModifiedCol = colIndex("last_modified");

    if (!sheet.getRange(row, idCol).getValue()) {
      var lastRow = sheet.getLastRow();
      var nextId = lastRow - 1;
      sheet.getRange(row, idCol).setValue(nextId);

      if (!sheet.getRange(row, createdAtCol).getValue()) {
        sheet.getRange(row, createdAtCol).setValue(formatDate(new Date()));
      }
    }

    fixRowDates(createdAtCol, lastModifiedCol);
  }

  // -------------------
  // study_logs sheet
  // -------------------
  if (sheetName === "study_logs") {
    var idCol = colIndex("study_id");
    var createdAtCol = colIndex("created_at");
    var lastModifiedCol = colIndex("last_modified");

    if (!sheet.getRange(row, idCol).getValue()) {
      var lastRow = sheet.getLastRow();
      var nextId = lastRow - 1;
      sheet.getRange(row, idCol).setValue(nextId);

      if (!sheet.getRange(row, createdAtCol).getValue()) {
        sheet.getRange(row, createdAtCol).setValue(formatDate(new Date()));
      }
    }

    fixRowDates(createdAtCol, lastModifiedCol);
  }
}
