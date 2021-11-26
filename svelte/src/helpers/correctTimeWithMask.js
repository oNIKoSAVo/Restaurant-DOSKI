export function correctTimeWithMask(time) {
  const [hours, minutes] = time.split(":");
  if (hours === '20' && minutes === '00') return true
  return !(
    time.trim() === "" ||
    time.trim().includes("_") ||
    hours > 19 || hours < 12 ||
    minutes > 59
  );
}
