export function correctPhoneWithMask(phone) {
  return !(phone.trim() === "" || phone.trim().includes("_"));
}
