export function phoneToNumbers(phoneString) {
  return (
    "8" +
    phoneString
      .slice(2)
      .split("")
      .filter((el) => {
        if (!isNaN(+el)) return true;
      })
      .join("")
  );
}
