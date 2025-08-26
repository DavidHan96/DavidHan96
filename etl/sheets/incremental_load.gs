/**
 * onEdit for "applications" and "study_logs".
 * - Stamps created_at once and last_modified on every edit.
 * - Uses UTC ISO8601 with milliseconds (TIMESTAMP_NTZ(3)-friendly).
 * - Prevents recursion when editing timestamp fields.
 * - Fills app_id / study_id with (max existing id + 1) when empty.
 */
function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const row = e.range.getRow();
  if (row === 1) return; // header

  const name = sheet.getName();
  if (name !== "applications" && name !== "study_logs") return;

  const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  const colIndex = (h) => headers.indexOf(h) + 1;

  // Avoid recursion on timestamp edits
  const editedHeader = headers[e.range.getColumn() - 1];
  if (editedHeader === "created_at" || editedHeader === "last_modified") return;

  // UTC ISO with milliseconds
  const nowIsoMs = Utilities.formatDate(new Date(), "Etc/UTC", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");

  function ensureId(idCol) {
    const cur = sheet.getRange(row, idCol).getValue();
    if (cur) return;
    const last = sheet.getLastRow();
    if (last < 2) {
      sheet.getRange(row, idCol).setValue(1);
      return;
    }
    const vals = sheet.getRange(2, idCol, Math.max(last - 1, 0), 1)
      .getValues().flat()
      .filter(v => v !== "" && !isNaN(v)).map(Number);
    const maxId = vals.length ? Math.max.apply(null, vals) : 0;
    sheet.getRange(row, idCol).setValue(maxId + 1);
  }

  function stamp(createdCol, modifiedCol) {
    const created = sheet.getRange(row, createdCol).getValue();
    if (!created) {
      sheet.getRange(row, createdCol).setValue(nowIsoMs);
    } else if (Object.prototype.toString.call(created) === "[object Date]") {
      const createdIso = Utilities.formatDate(created, "Etc/UTC", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
      sheet.getRange(row, createdCol).setValue(createdIso);
    }
    sheet.getRange(row, modifiedCol).setValue(nowIsoMs);
  }

  if (name === "applications") {
    const id = colIndex("app_id");
    const c  = colIndex("created_at");
    const m  = colIndex("last_modified");
    ensureId(id);
    stamp(c, m);
  } else if (name === "study_logs") {
    const id = colIndex("study_id");
    const c  = colIndex("created_at");
    const m  = colIndex("last_modified");
    ensureId(id);
    stamp(c, m);
  }
}
